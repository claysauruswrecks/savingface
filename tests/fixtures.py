"""Test fixtures."""

import torch
import torch.nn as nn
from huggingface_hub import PyTorchModelHubMixin


class SimpleFixtureModel(nn.Module, PyTorchModelHubMixin):
    """Simple NN model fixture to save and load."""

    def __init__(self, config: dict):
        super().__init__()
        self.param = nn.Parameter(
            torch.rand(config["num_channels"], config["hidden_size"])
        )
        self.linear = nn.Linear(config["hidden_size"], config["num_classes"])

    def forward(self, x):
        return self.linear(x + self.param)
