import time

import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import Adadelta
from torch.optim.lr_scheduler import StepLR
from torchvision.datasets.vision import VisionDataset

from .args import TrainerArguments
from ..enums import OptimizerClass, SchedulerClass


class Trainer:
    def __init__(self,
                 model: nn.Module,
                 train_set: VisionDataset,
                 test_set: VisionDataset,
                 trainer_args: TrainerArguments,
                 logger):

        self.model = model
        self.train_set = train_set
        self.test_set = test_set
        self.trainer_args = trainer_args
        self.logger = logger

        self.train_args = {"batch_size": self.trainer_args.train_batch_size}
        self.test_args = {"batch_size": self.trainer_args.test_batch_size}

        if self.trainer_args.use_gpu and torch.cuda.is_available():
            self.device = torch.device("cuda")

            cuda_args = {"num_workers": 1,
                         "pin_memory": True,
                         "shuffle": True}
            self.train_args.update(cuda_args)
            self.test_args.update(cuda_args)
        else:
            self.device = torch.device("cpu")

        self.model.to(self.device)

        self.train_loader = torch.utils.data.DataLoader(
            self.train_set, **self.train_args)
        self.test_loader = torch.utils.data.DataLoader(
            self.test_set, **self.test_args)

        self.__register_optimizer(self.trainer_args.optimizer)
        self.__register_scheduler(self.trainer_args.scheduler)

    def train(self):

        self.start_time = time.time()

        for epoch in range(1, self.trainer_args.epoch + 1):
            self.__train(epoch)
            self.__test(epoch)
            self.scheduler.step()

        torch.save(self.model.state_dict(), self.logger.checkpoint_path)

    def __train(self, epoch):

        self.model.train()

        for (data, target) in self.train_loader:
            data, target = data.to(self.device), target.to(self.device)
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            self.optimizer.step()

            current_time = int(time.time() - self.start_time)
            self.logger.log_train(
                epoch=epoch, loss=loss.item(), time=current_time)

    def __test(self, epoch):

        self.model.eval()

        test_loss = 0
        correct = 0

        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = F.nll_loss(output, target, reduction='sum').item()
                test_loss += loss
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()

                current_time = int(time.time() - self.start_time)
                self.logger.log_test(epoch=epoch, loss=loss, time=current_time)

        test_loss /= len(self.test_loader.dataset)
        accuracy = correct / len(self.test_loader.dataset)

        current_time = int(time.time() - self.start_time)
        self.logger.log_accuracy(
            epoch=epoch, accuracy=accuracy, time=current_time)

    def __register_optimizer(self, optim):
        if not optim:
            self.optimizer = Adadelta(self.model.parameters(),
                                      lr=self.trainer_args.lr)

        optimizer_class = OptimizerClass(optim).value
        self.optimizer = optimizer_class(
            self.model.parameters(), lr=self.trainer_args.lr)

    def __register_scheduler(self, scheduler):
        if not scheduler:
            self.scheduler = StepLR(self.optimizer, step_size=1, gamma=0.7)

        scheduler_id, scheduler_args = scheduler
        scheduler_class = SchedulerClass(scheduler_id).value
        self.scheduler = scheduler_class(self.optimizer, **scheduler_args)
