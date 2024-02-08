from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class JobBase(SQLModel):
    status: int = Field(default=0, nullable=False)
    queue_order: int = Field(default=-1, nullable=False)
    backlog_order: int = Field(default=-1, nullable=False)
    type: int = Field(nullable=False)
    strategy: int = Field(nullable=False)


class Job(JobBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="job")


class JobCreate(JobBase):
    ...


class JobRead(JobBase):
    id: int
    best: Optional[int]


class TaskBase(SQLModel):
    status: int = Field(default=0, nullable=False)
    job_id: int = Field(foreign_key="job.id")
    execute_order: Optional[int] = Field(default=0, nullable=False)
    checkpoint: Optional[str] = Field(default=None)
    logs: Optional[str] = Field(default=None)
    use_gpu: Optional[bool] = Field(default=False, nullable=False)
    lr: Optional[float] = Field(default=1e-3, nullable=False)
    train_batch_size: Optional[int] = Field(default=64, nullable=False)
    test_batch_size: Optional[int] = Field(default=128, nullable=False)
    epoch: Optional[int] = Field(default=50, nullable=False)
    dropout_rate: Optional[float] = Field(default=None)
    transform: Optional[str] = Field(default=None)
    optimizer: Optional[int] = Field(default=5, nullable=False)
    optimizer_args: Optional[str] = Field(default=None)
    scheduler: Optional[int] = Field(default=None)
    scheduler_args: Optional[str] = Field(default=None)
    cleanlab: Optional[bool] = Field(default=False)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    accuracy: Optional[float] = Field(default=None)
    avg_precision: Optional[float] = Field(default=None)
    avg_recall: Optional[float] = Field(default=None)

    job: Job = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    ...


class TaskRead(TaskBase):
    id: int
    accuracy: Optional[float]
    avg_precision: Optional[float]
    avg_recall: Optional[float]


class TaskReadWithJob(TaskRead):
    job: Optional[JobRead] = None


class JobReadWithTasks(JobRead):
    tasks: List[TaskRead] = []
