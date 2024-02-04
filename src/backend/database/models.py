from typing import Optional, List
from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: int = Field(default=0, nullable=False)
    queue_order: Optional[int] = Field(default=None)
    backlog_order: Optional[int] = Field(default=None)
    type: int = Field(nullable=False)
    strategy: int = Field(nullable=False)
    created_at: Optional[datetime]

    tasks: List["Task"] = Relationship(back_populates="job")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: int = Field(default=0, nullable=False)
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

    job_id: int = Field(foreign_key="job.id")
    job: Job = Relationship(back_populates="tasks")
