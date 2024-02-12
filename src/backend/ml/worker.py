import time

import torch
from torch.nn import functional as F
from torch.optim import Adadelta
from torch.optim.lr_scheduler import StepLR
import torchvision

from enums import OptimizerClass, SchedulerClass
from .model import SimpleModel
from database.io import Logger


class Trainer:
    def __init__(self, logger: Logger):

        self.model = SimpleModel()

        self.train_set = torchvision.datasets.MNIST(
            root=logger.data_dir, train=True, download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    (0.1307,), (0.3081,))
            ]))
        self.test_set = torchvision.datasets.MNIST(
            root=logger.data_dir, train=False, download=True,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    (0.1307,), (0.3081,))
            ]))

        self.logger = logger

        self.train_args = {"batch_size": self.logger.task.train_batch_size}
        self.test_args = {"batch_size": self.logger.task.test_batch_size}

        if self.logger.task.use_gpu and torch.cuda.is_available():
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

        self.__register_optimizer(self.logger.task.optimizer)
        self.__register_scheduler(self.logger.task.scheduler)

        self.train_step = 1
        self.test_step = 1

    def train(self):

        self.start_time = time.time()

        for epoch in range(1, self.logger.task.epoch + 1):
            self.__train(epoch)
            self.__test(epoch)
            self.scheduler.step()

        torch.save(self.model.state_dict(), self.logger.checkpoint_path)

        self.logger.finish(runtime=time.time() - self.start_time)

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
                epoch=epoch, step=self.train_step, loss=loss.item(), time=current_time)
            self.train_step += 1

            print(f"Step {self.train_step}, loss {loss.item()}", flush=True)

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
                self.logger.log_test(
                    epoch=epoch, step=self.test_step, loss=loss, time=current_time)
                self.test_step += 1

                print(f"Step {self.test_step}, loss {loss}", flush=True)

        test_loss /= len(self.test_loader.dataset)
        accuracy = correct / len(self.test_loader.dataset)

        print(
            f"Epoch {epoch}, test loss: {test_loss}, accuracy {accuracy}", flush=True)

        current_time = int(time.time() - self.start_time)
        self.logger.log_accuracy(
            epoch=epoch, avg_loss=test_loss, accuracy=accuracy, avg_precision=accuracy, avg_recall=accuracy)  # TODO: Add precision and recall

    def __register_optimizer(self, optim):
        if not optim:
            self.optimizer = Adadelta(self.model.parameters(),
                                      lr=self.logger.task.lr)

        optimizer_class = OptimizerClass(optim).value
        self.optimizer = optimizer_class(
            self.model.parameters(), lr=self.logger.task.lr)

    def __register_scheduler(self, scheduler):
        if not scheduler:
            self.scheduler = StepLR(self.optimizer, step_size=1, gamma=0.7)

        scheduler_id, scheduler_args = scheduler
        scheduler_class = SchedulerClass(scheduler_id).value
        self.scheduler = scheduler_class(self.optimizer, **scheduler_args)
