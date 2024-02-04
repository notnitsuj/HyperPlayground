import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from ...service.app import app, get_session, Job, Task


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        job1 = Job(type=0, strategy=0)
        job2 = Job(type=1, strategy=1)
        job3 = Job(type=1, strategy=2)

        session.add(job1)
        session.add(job2)
        session.add(job3)
        session.commit()
        session.refresh(job1)
        session.refresh(job2)
        session.refresh(job3)

        task1 = Task(job_id=job1.id)
        task2 = Task(job_id=job2.id, lr=1e-4, epoch=100)
        task3 = Task(job_id=job2.id, lr=1e-5, epoch=200)
        task4 = Task(job_id=job3.id, lr=1e-2, epoch=20)
        task5 = Task(job_id=job3.id, lr=3e-4, epoch=150, train_batch_size=256)
        task6 = Task(job_id=job3.id, lr=1e-2, epoch=90, train_batch_size=15)
        task7 = Task(job_id=job3.id, lr=5e-3, epoch=300, use_gpu=True)
        task8 = Task(job_id=job3.id, lr=1e-2, epoch=100, use_gpu=True)

        session.add_all((task1, task2, task3, task4,
                        task5, task6, task7, task8))
        session.commit()

        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_all_jobs(client: TestClient):
    response = client.get("/jobs/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["id"] == 1
    assert data[1]["type"] == 1
    assert data[2]["strategy"] == 2


def test_get_all_tasks(client: TestClient):
    response = client.get("/tasks/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 8
    assert data[0]["job_id"] == 1
    assert data[2]["lr"] == 1e-5
    assert data[4]["train_batch_size"] == 256
    assert data[6]["use_gpu"] == True
    assert data[7]["dropout_rate"] == None
