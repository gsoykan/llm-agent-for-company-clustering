from celery import Celery, group

from glassdollar_repo import get_company_ids, get_company_by_id

num_companies = 848
app = Celery('main',
             broker='pyamqp://guest@localhost//',
             backend='rpc://',
             )


@app.task
def fetch_company_by_id(id: str):
    # Fetch and possibly store the data, then return it
    return get_company_by_id(id)


@app.task
def fetch_company_ids(page: int):
    # This task now triggers fetching of individual company data in parallel
    ids = get_company_ids(page)['ids']
    # Create a group of tasks to fetch details for each ID
    task_group = group(fetch_company_by_id.s(id) for id in [ids[0]])
    result = task_group.apply_async()
    return result.get()  # Collect results from the group


@app.task
def collect_companies():
    # Calculate the number of pages needed based on the assumed number per page (adjust according to actual API pagination)
    # num_pages = (num_companies + 24) // 25  # Ensure rounding up
    num_pages = 1
    # Create a group of tasks for each page
    all_tasks = group(fetch_company_ids.s(page) for page in range(1, num_pages + 1))
    result_group = all_tasks.apply_async()
    results = result_group.get()  # Collect results from all groups
    # Process or store results here if needed
    return results


if __name__ == '__main__':
    company_res = fetch_company_by_id.delay("ab47d80c-7971-c8e6-b620-7483498d0c5b")
    print(company_res.get())
    # result = collect_companies.delay()
    # Since we are in asynchronous mode, result.get() is needed to wait for the result
    # final = result.get()  # Be careful with get() in production code as it can block the caller
    # print(final)
