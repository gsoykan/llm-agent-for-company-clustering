import json
import os
from typing import List
from celery.utils.log import get_task_logger
from celery import Celery, group, chord, chain
from pydantic.json import pydantic_encoder

from analyzer import analyse_corporates
from data import Corporate
from glassdollar_repo import get_company_ids, get_company_by_id

# TODO: @gsoykan - make this depend on env
app = Celery('tasks',
             # broker='pyamqp://guest@localhost//',
             # backend='redis://localhost:6379/0'
             broker="amqp://user:password@rabbitmq:5672//",
             backend='redis://redis/0',
             )

app.conf.update(result_extended=True)

num_companies = 848

logger = get_task_logger(__name__)


@app.task
def flatten_and_combine(results: List[List]):
    # This function combines the results from each chain into a single list
    # logger.info('\n------------START RESULTS-----------------\n')
    # logger.debug(results[0])
    # logger.info(f"Combined Flattened results: {results}")
    # logger.info('\n-------------END RESULTS-------------\n')
    # flat_list = []
    # for sub_list in results:
    #     flat_list.extend(sub_list)  # Extend the main list with elements from sub-lists
    flat_list = []

    def flatten(items):
        for item in items:
            if isinstance(item, list):
                flatten(item)
            else:
                flat_list.append(item)

    flatten(results)

    # logger.info('\n------------START FLAT-----------------\n')
    # logger.info(f"Combined Flattened results: {flat_list}")
    # logger.info('\n-------------END FLAT-------------\n')
    return flat_list


# this works
@app.task
def fetch_company_by_id(id: str):
    try:
        corp = get_company_by_id(id).model_dump_json()
        logger.info(f"Fetched company data for ID {id}: {corp[:5]}")
        return corp
    except Exception as e:
        logger.error(f"Error fetching company data for ID {id}: {e}")
        return {"error": "Data fetch failed", "company_id": id}


@app.task
def fetch_company_by_ids(ids: List[str]):
    logger.info(f"\nProcessing company IDs:\n {ids}")
    group_result = chord([fetch_company_by_id.s(id) for id in ids], body=analysis.s())
    return group_result()


@app.task
def fetch_company_ids(page: int):
    ids = get_company_ids(page)['ids']
    return ids


@app.task
def task_result(*args, **kwargs):
    logger.info(f"\nOK TASK\n")
    return args


@app.task(name='tasks.analysis')
def analysis(*args, **kwargs):
    logger.info(f"\nIn the analysis\n")
    logger.info(len(args[0]))
    valid_items = []
    for item in args[0]:
        is_valid = not (not isinstance(item, str) and item.get('error') is not None)
        if is_valid:
            valid_items.append(item)
    logger.info('num valid items: ' + str(len(valid_items)))
    all_corporates = list(map(lambda x: Corporate(**json.loads(x)), valid_items))
    # TODO: @gsoykan - for debugging purposes
    proj_folder = '/home/gsoykan/Desktop/dev/entrapeer-agent'
    all_companies_path = os.path.join(proj_folder, 'all_companies.json')
    if not os.path.exists(all_companies_path):
        with open('all_companies.json', 'w', encoding='utf-8') as f:
            json.dump(all_corporates,
                      f,
                      ensure_ascii=False,
                      indent=4,
                      default=pydantic_encoder)

    summaries = analyse_corporates(all_corporates)
    return summaries


@app.task
def complete_tasks(*args, **kwargs):
    logger.info(f"\nCOMPLETED TASK\n")
    return args


@app.task
def collect_companies():
    num_pages = (num_companies + 32) // 32  # Calculate number of pages needed

    tasks = []
    for page in range(1, num_pages + 1):
        # Creating a chain for each page: fetch ids and then process them
        task = fetch_company_ids.s(page)
        tasks.append(task)

    group_result = chain(chord(tasks, body=task_result.s(), ),
                         flatten_and_combine.s(),
                         # try splitting it to chunks then apply chord?
                         # fetch_company_by_ids.s(),
                         # flatten_and_combine.s(),
                         # complete_tasks.s()
                         )

    return group_result()


@app.task
def collect_companies_alternative():
    num_pages = (num_companies + 32) // 32
    tasks = []

    for page in range(1, num_pages + 1):
        task = fetch_company_ids.s(page)
        tasks.append(task)

    group_result = group(tasks) | flatten_and_combine.s() | fetch_company_by_ids.s()
    return group_result()
