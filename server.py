from fastapi import FastAPI

from tasks import collect_companies_alternative
from test import check_job_progress

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "GlassDollar Company Analysis"}


@app.post("/start_job/")
async def start_job():
    collect_and_analyse_task = collect_companies_alternative()
    main_job_id = collect_and_analyse_task.id
    return {"task_id": main_job_id}


@app.get("/results/{task_id}")
async def get_results(task_id: str):
    progress_result = check_job_progress(task_id)
    return progress_result
