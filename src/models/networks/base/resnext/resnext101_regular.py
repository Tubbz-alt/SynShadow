from pathlib import Path

import torch
from torch import nn

from . import resnext_101_32x4d_


class ResNeXt101(nn.Module):
    # The model is downloaded from:
    # https://drive.google.com/file/d/1EDUcaGNiakWO9Xvk9kWgkkcnTYZ6VQoT/view
    def __init__(self):
        backbone_path = str(Path(__file__).parent / 'resnext_101_32x4d.pth')
        super(ResNeXt101, self).__init__()
        net = resnext_101_32x4d_.resnext_101_32x4d
        if backbone_path is not None:
            weights = torch.load(backbone_path)
            # del weights['0.weight']
            net.load_state_dict(weights, strict=True)
            print("Load ResNeXt Weights Succeed!")

        net = list(net.children())
        self.layer0 = nn.Sequential(*net[:3])
        self.layer1 = nn.Sequential(*net[3: 5])
        self.layer2 = net[5]
        self.layer3 = net[6]
        self.layer4 = net[7]

    def forward(self, x):
        layer0 = self.layer0(x)
        layer1 = self.layer1(layer0)
        layer2 = self.layer2(layer1)
        layer3 = self.layer3(layer2)
        layer4 = self.layer4(layer3)
        return layer4
