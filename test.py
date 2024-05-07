from typing import Dict

from celery.result import AsyncResult

from tasks import app, collect_companies_alternative


def print_job_state_result(job_id: str):
    # getting task result with id
    res = AsyncResult(job_id, app=app)
    state = res.state  # 'SUCCESS'
    result = res.get()  # 7
    return result, state


def get_task_name(job_id) -> str:
    result = AsyncResult(job_id)
    task_name = result.name if result.name else "Unknown Task"
    return task_name


def check_job_progress(job_id: str) -> Dict:
    task = AsyncResult(job_id)
    if not task.ready():
        return {'status': 'NOT_READY'}

    company_task_list = task.get(timeout=10)
    analysis_task_id = company_task_list[0][0]
    main_task_list = [analysis_task_id, company_task_list[0][1][0][0], ]
    subtask_ids = list(map(lambda x: x[0][0], company_task_list[0][1][1]))
    subtask_ids = main_task_list + subtask_ids
    is_analysis_completed = None
    all_states = []
    for subtask_id in subtask_ids:
        subtask_res = AsyncResult(subtask_id, app=app)
        subtask_state = subtask_res.state
        all_states.append(subtask_state)
        subtask_name = get_task_name(subtask_id)
        # print(subtask_name, subtask_state)
        if subtask_state == 'SUCCESS' and subtask_id == analysis_task_id:
            is_analysis_completed = True
            # print('ANALYSIS COMPLETED')
    # print(all_states)
    if is_analysis_completed:
        analysis_results = AsyncResult(analysis_task_id, app=app).get(timeout=10)
        return {'status': 'SUCCESS', 'analysis': analysis_results}
    else:
        if any(map(lambda x: x not in ["SUCCESS", "PENDING"], all_states)):
            return {'status': 'FAILURE', 'all_states': all_states}
        elif any(map(lambda x: x == 'SUCCESS', all_states)):
            return {'status': 'IN_PROGRESS'}
        else:
            return {'status': 'PENDING'}


def test_functions():
    # this works :)
    # company_res = fetch_company_by_id.delay("ab47d80c-7971-c8e6-b620-7483498d0c5b")
    # print(company_res.get())

    # this works :)
    # page_res = fetch_company_ids.delay(1)
    # print(page_res.get())
    ids = ['ab47d80c-7971-c8e6-b620-7483498d0c5b', 'b462608d-8bf4-93f1-4f68-e41ee10f0df2',
           'ba08a876-9044-e504-c63e-a18974a8f942', '0d2b82ad-bd6f-9f54-c76a-448a455af317',
           'a90a2792-7fc3-c23e-836b-7b6271ec772d', 'eec354de-1ed2-254d-647b-f218643791d9',
           '7e65d993-40b9-c150-2594-cadeb1fc67c1', '8ee63939-bd06-6699-f575-dffcecb71daf',
           '8b4b73f6-f945-4d33-994d-ce87bc56365d', 'd2fc97d5-40e1-cc87-6032-f5cb41c3dc57',
           '23538a32-6087-12fb-dcd9-9b93abfa84fc', '3a863d01-4f3e-4c07-b033-c643bd666084',
           '811d5a4c-25ff-5428-c4ed-26a7d1cbb60b', '31fc3998-a1f1-2e5b-6358-f8d068fa9f71',
           '9bf11476-f2da-39a4-b8d0-e4ff450ad46a', 'ace7c133-b21c-9aa8-a8a5-c06d7d6f9232',
           '03099c0f-ed6a-d0ea-bf12-1347b36ed611', '591df276-a9a0-21b3-6cf6-36fa4afe036d',
           'a1d935af-1d49-55ef-2bf6-cbd1bf82af6d', 'dbab88e1-0c7d-7983-f881-c63f5caab83a',
           'e1a29c26-a6c2-b208-6ee4-165cf83b1656', 'b4041d82-527a-589b-0538-797a43b2b4ee',
           '85fdcfb6-0bab-ad9b-6a4a-2702a152232e', '34079d8d-e15b-3a6e-00cf-26db1b890ea8',
           '53ac35bb-6b2c-fc90-2223-de1cb4d72e9a', 'fe088d9d-3892-e0d5-9c27-cb0e0fdce561',
           'f695d0c6-9dea-237d-111d-fa9b35a19904', 'af3dc6a0-01d7-b61f-e94a-c79953160de3',
           '93853d8a-48b8-f3f1-c162-7c1d3b856082', 'b8f83b16-a892-8c02-4221-dcb7862b6e2c',
           '55c2d41d-9ddc-b9ab-978e-d86cca6f0c47', '0adf30e1-1947-4a16-4903-3a3568e02b12']
    # this works :)
    # task_group = fetch_company_by_ids(ids)
    # result = task_group # .apply_async()
    # print(result.get())

    # collect_group = collect_companies()
    # collect_result = collect_group.apply_async()
    # print(collect_result.get())

    # result = collect_companies.apply_async()
    # company_list = result.get()
    # print(company_list)

    # main issue
    # result = collect_companies()
    # print(result.ready())
    # print(result)
    # company_list = result.get()  # This blocks until the result is ready, consider handling this asynchronously if possible
    # print(result.ready())
    # print(company_list)

    # result = list(collect_companies.delay().collect())
    # print(result)
    # company_list = result.get()  # This blocks until the result is ready, consider handling this asynchronously if possible
    # print(company_list)

    #
    # # get() is used for getting results
    #
    # result.get(propagate=False)
    #
    # # In case the task raised an exception, get() will re-raise the exception, but you can override this by specifying the propagate argument


if __name__ == '__main__':
    result = collect_companies_alternative()
    main_job_id = result.id
    job_progress = check_job_progress(main_job_id)
    print(job_progress)
