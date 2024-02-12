import time

from sqlmodel import Session, select

from ml.worker import Trainer
from database.models import Job
from database.io import Logger
from enums import Status


def start_training_thread(engine, logger: Logger, looper):
    with Session(engine) as session:
        while looper.is_loop:
            job = session.exec(select(Job).where(
                Job.status == Status.QUEUE.value).where(Job.queue_order == 1)).first()

            if not job:
                time.sleep(1)
                continue

            print(job)
            job.status = Status.RUNNING.value
            session.add(job)
            session.commit()

            for task in sorted(job.tasks, key=lambda x: x.execute_order):
                logger.register_task(task=task)
                trainer = Trainer(logger=logger)
                print(f"Start training task: {task}")
                trainer.train()
