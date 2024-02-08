from enums import Status
from database.io import create_tasks, Logger, reorder_backlog_queue
from database.models import *
from database.db import instantiate_db, get_session
from typing import List

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    instantiate_db()


@app.get("/jobs/", response_model=List[JobReadWithTasks])
def get_all_jobs(*, session: Session = Depends(get_session)):
    jobs = session.exec(select(Job)).all()

    return jobs


@app.get("/tasks/", response_model=List[TaskReadWithJob])
def get_all_tasks(*, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()

    return tasks


@app.post("/jobs/create", response_model=JobReadWithTasks)
def create_job(*, session: Session = Depends(get_session), job: JobCreate):
    db_job = Job.model_validate(job)

    backlog_jobs = session.exec(select(Job).where(
        Job.status == Status.STAGED.value)).all()
    db_job.backlog_order = len(backlog_jobs)

    session.add(db_job)
    session.commit()
    session.refresh(db_job)

    tasks = create_tasks(db_job)

    session.add_all(tasks)
    session.commit()
    session.refresh(db_job)

    return db_job


@app.patch("/jobs/reorder")
async def reorder_job(*, session: Session = Depends(get_session), request: Request):
    reorder_data = await request.json()

    reorder_backlog_queue(reorder_data=reorder_data, session=session)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_level="info")
