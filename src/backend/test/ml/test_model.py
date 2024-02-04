import unittest

import torch

from ...ml.model import SimpleModel


class TestSimpleModel(unittest.TestCase):
    def test_forward(self):
        model = SimpleModel()

        # MNIST dataset
        input_size = (16, 1, 28, 28)  # batch size x channel x height x width
        output_size = (16, 10)  # batch size x number of classes

        x = torch.testing.make_tensor(
            input_size, dtype=torch.float, device="cpu")
        y = model(x)

        self.assertIsInstance(y, torch.Tensor)
        self.assertEqual(y.shape[0], output_size[0])
        self.assertEqual(y.shape[1], output_size[1])
