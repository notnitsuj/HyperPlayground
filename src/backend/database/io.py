from typing import Iterable

from sqlmodel import Session, select

from .models import Job, Task
from enums import JobType, Status


class Logger:
    ...


def create_tasks(job: Job) -> Iterable[object]:
    if job.type == JobType.TRAIN:
        tasks = (Task(job_id=job.id))
    else:
        tasks = (Task(job_id=job.id, execute_order=i) for i in range(4))

    return tasks


def reorder_backlog_queue(reorder_data: dict, session: Session) -> None:
    job_id = int(reorder_data["job_id"].split("-")[-1])
    job = session.get(Job, job_id)

    old_status = "backlog" if job.status == 0 else "queue"
    new_status = reorder_data["new_status"].lower()

    old_status_order = old_status + "_order"
    new_status_order = new_status + "_order"

    old_order = getattr(job, old_status_order)
    new_order = reorder_data["new_order"]

    old_order = job.backlog_order if job.status == 0 else job.queue_order

    if new_status != old_status:
        old_jobs = session.exec(select(Job).where(Job.status == Status[old_status.upper()].value).where(
            getattr(Job, old_status_order) > old_order)).all()

        for old_job in old_jobs:
            order = getattr(old_job, old_status_order)
            setattr(old_job, old_status_order, order - 1)
            session.add(old_job)

        new_jobs = session.exec(select(Job).where(Job.status == Status[new_status.upper()].value).where(
            getattr(Job, new_status_order) >= new_order)).all()

        for new_job in new_jobs:
            order = getattr(new_job, new_status_order)
            setattr(new_job, new_status_order, order + 1)
            session.add(new_job)
    elif new_order > old_order:
        jobs = session.exec(select(Job).where(Job.status == Status[new_status.upper()].value).where(
            getattr(Job, new_status_order) <= new_order, getattr(
                Job, new_status_order) > old_order
        )).all()

        for new_job in jobs:
            order = getattr(new_job, new_status_order)
            setattr(new_job, new_status_order, order - 1)
            session.add(new_job)
    else:
        jobs = session.exec(select(Job).where(Job.status == Status[new_status.upper()].value).where(
            getattr(Job, new_status_order) >= new_order, getattr(
                Job, new_status_order) < old_order
        )).all()

        for new_job in jobs:
            order = getattr(new_job, new_status_order)
            setattr(new_job, new_status_order, order + 1)
            session.add(new_job)

    job.status = Status[new_status.upper()].value
    setattr(job, old_status_order, -1)
    setattr(job, new_status_order, new_order)

    session.add(job)
    session.commit()
