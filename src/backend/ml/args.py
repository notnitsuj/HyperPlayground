from pydantic import BaseModel


class TrainerArguments(BaseModel):
    lr: int = 1e-3
    train_batch_size: int = 64
    test_batch_size: int = 128
    epoch: int = 50
    dropout_rate: float | None = None
    transform: list | None = None
    optimizer: int | None = None
    scheduler: tuple[int, dict[str, float]
                     ] | list[int, dict[str, float]] | None = None
    cleanlab: bool = False
    use_gpu: bool = False
