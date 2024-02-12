import os
import json
from typing import Iterable

from sqlmodel import Session, select

from .models import Job, Task
from enums import JobType, Status


class Logger:
    def __init__(self):
        self.__session = None
        self.__db_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.__db_dir, "data/")
        self.checkpoint_dir = os.path.join(self.__db_dir, "checkpoints/")
        self.log_dir = os.path.join(self.__db_dir, "logs/")

        self.checkpoint_path = None
        self.log_path = None

        self.task = Task()

        self.train_logs = []
        self.test_logs = []
        self.runtime = None

    def register_session(self, session: Session):
        self.__session = session

    def register_task(self, task: Task):
        self.task = task

        self.checkpoint_path = self.checkpoint_dir + \
            f"Job{self.task.job_id}_Task{self.task.id}.pt"
        self.task.checkpoint = self.checkpoint_path

        self.log_path = self.log_dir + \
            f"Job{self.task.job_id}_Task{self.task.id}.json"
        self.task.logs = self.log_path

        self.task.status = Status.RUNNING.value

        self.update_db()

    def finish(self, runtime: float):
        self.task.runtime = runtime
        self.update_db()

        self.save_logs()

        self.checkpoint_path = None
        self.log_path = None

        self.task = Task()

        self.train_logs = []
        self.val_logs = []
        self.runtime = None

    def log_train(self, epoch: int, step: int,  loss: float, time: float):
        self.train_logs.append({
            "epoch": epoch,
            "step": step,
            "loss": loss,
            "time": time
        })

    def log_test(self, epoch: int, step: int,  loss: float, time: float):
        self.test_logs.append({
            "epoch": epoch,
            "step": step,
            "loss": loss,
            "time": time
        })

    def update_db(self):
        self.__session.add(self.task)
        self.__session.commit()
        self.__session.refresh(self.task)

    def save_logs(self):
        logs = {
            "train": self.train_logs,
            "test": self.test_logs
        }

        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)


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
