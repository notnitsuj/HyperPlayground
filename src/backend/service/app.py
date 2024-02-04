from typing import List

from fastapi import FastAPI, Depends
from sqlmodel import Session, select

from ..database.db import instantiate_db, get_session
from ..database.models import *

app = FastAPI()


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
