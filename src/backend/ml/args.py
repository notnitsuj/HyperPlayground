from pydantic import BaseModel


class TrainerArguments(BaseModel):
    lr: int = 6e-3
    train_batch_size: int = 512
    test_batch_size: int = 1024
    epoch: int = 50
    dropout_rate: float | None = None
    transform: list | None = None
    optimizer: int | None = None
    # scheduler: list[int, dict[str, float]] | None = None
    cleanlab: bool = False
    use_gpu: bool = True
