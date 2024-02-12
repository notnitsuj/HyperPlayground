import os

from sqlmodel import SQLModel, create_engine, Session

from . import models


sqlite_dir_name = os.path.dirname(os.path.abspath(__file__))
sqlite_file_name = os.path.join(sqlite_dir_name, "hp_database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def instantiate_db():
    if not os.path.exists(sqlite_file_name):
        SQLModel.metadata.create_all(engine)

        from .models import Job, Task

        with Session(engine) as session:
            job1 = Job(type=0, strategy=0, backlog_order=1)
            job2 = Job(type=1, strategy=1, backlog_order=2)
            job3 = Job(type=1, strategy=2, backlog_order=3)
            job4 = Job(type=0, strategy=0, status=1, queue_order=1)
            job5 = Job(type=1, strategy=1, status=1, queue_order=2)

            session.add(job1)
            session.add(job2)
            session.add(job3)
            session.add(job4)
            session.add(job5)
            session.commit()
            session.refresh(job1)
            session.refresh(job2)
            session.refresh(job3)

            task1 = Task(job_id=job1.id, train_batch_size=1024,
                         test_batch_size=512, use_gpu=True)
            task2 = Task(job_id=job2.id, lr=1e-4, epoch=100,
                         accuracy=0.7, avg_precision=0.8, avg_recall=0.9, runtime=2323)
            task3 = Task(job_id=job2.id, lr=1e-5, epoch=200,
                         accuracy=0.4, avg_precision=0.6, avg_recall=0.7, runtime=23231)
            task4 = Task(job_id=job3.id, lr=1e-2, epoch=20,
                         accuracy=0.9, avg_precision=0.6, avg_recall=0.72, runtime=20232)
            task5 = Task(job_id=job3.id, lr=3e-4,
                         epoch=150, train_batch_size=256, accuracy=0.85, avg_precision=0.43, avg_recall=0.5, runtime=23235)
            task6 = Task(job_id=job3.id, lr=1e-2,
                         epoch=90, train_batch_size=15, accuracy=0.34, avg_precision=0.62, avg_recall=0.53, runtime=20012)
            task7 = Task(job_id=job3.id, lr=5e-3, epoch=300, use_gpu=True,
                         accuracy=0.93, avg_precision=0.2, avg_recall=0.45, runtime=232392)
            task8 = Task(job_id=job3.id, lr=1e-2, epoch=100, use_gpu=True,
                         accuracy=0.26, avg_precision=0.28, avg_recall=0.64, runtime=12432)

            session.add_all((task1, task2, task3, task4,
                            task5, task6, task7, task8))
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session
