from enum import Enum
from aenum import MultiValueEnum
from torch import optim


class OptimizerClass(MultiValueEnum):
    SGD = optim.SGD, 1
    Adam = optim.Adam, 2
    AdamW = optim.AdamW, 3
    RMSprop = optim.RMSprop, 4
    Adadelta = optim.Adadelta, 5


class SchedulerClass(MultiValueEnum):
    StepLR = optim.lr_scheduler.StepLR, 1
    LinearLR = optim.lr_scheduler.LinearLR, 2
    CosineAnnealingLR = optim.lr_scheduler.CosineAnnealingLR, 3
    ReduceLROnPlateau = optim.lr_scheduler.ReduceLROnPlateau, 4


class TunningStrategy(Enum):
    RANDOM = 1
    GRID = 2
    BAYESIAN = 3


class JobType(Enum):
    TRAIN = 0
    TUNE = 1


class Status(Enum):
    BACKLOG = 0
    QUEUE = 1
    RUNNING = 2
    FINISHED = 3
    CANCELLED = 4
    ERROR = 5
    PAUSED = 6
