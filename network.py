import torch
import torch.nn as nn
import torch.nn.functional as F


class DeepQNetwork(nn.Module):
    def __init__(self, input, output):
        super(DeepQNetwork, self).__init__()
        self.conv2d_1 = nn.Conv2d(input, 32, kernel_size=4, stride=4)
        self.max_pool2d = nn.MaxPool2d((2, 2))
        self.conv2d_2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv2d_3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.linear = nn.Linear((256), 512, bias=True)
        self.output = nn.Linear(512, output, bias=True)

    def forward(self, x):
        x = F.relu(self.conv2d_1(x))
        x = self.max_pool2d(x)
        x = F.relu(self.conv2d_2(x))
        x = F.relu(self.conv2d_3(x))
        x = x.view(-1, 256)
        outputs = torch.empty((x.size(0), 2))
        for i in range(0, x.size(0)):
            y = F.relu(self.linear(x[i]))
            outputs[i] = self.output(y)
        return outputs
