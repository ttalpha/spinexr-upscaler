import math
import torch
from torch import nn
import torch.nn.functional as F

leak = 0.2

class Model(nn.Module):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load_weights(self, weights_path: str):
		self.load_state_dict(torch.load(weights_path, weights_only=True))


class Generator(Model):
    def __init__(self, scale_factor):
        upsample_block_num = int(math.log(scale_factor, 2))

        super(Generator, self).__init__()
        self.block1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=9, padding=4),
            nn.PReLU()
        )
        self.residual_blocks = nn.Sequential(*[ResidualBlock(64) for _ in range(5)])
        self.conv_block = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.PReLU()
        )
        upsampler_blocks = [UpsampleBLock(64, 2) for _ in range(upsample_block_num)]
        upsampler_blocks.append(nn.Conv2d(64, 3, kernel_size=9, padding=4))
        self.upsampler = nn.Sequential(*upsampler_blocks)

    def forward(self, x):
      x = self.block1(x)
      res = self.residual_blocks(x)
      res = self.conv_block(res)
      x = self.upsampler(x + res)

      return (torch.tanh(x) + 1) / 2

class Discriminator(Model):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.LeakyReLU(0.2),

            nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1),
            nn.SyncBatchNorm(64),
            nn.LeakyReLU(0.2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.SyncBatchNorm(128),
            nn.LeakyReLU(0.2),

            nn.Conv2d(128, 128, kernel_size=3, stride=2, padding=1),
            nn.SyncBatchNorm(128),
            nn.LeakyReLU(0.2),

            # nn.Conv2d(128, 256, kernel_size=3, padding=1),
            # nn.SyncBatchNorm(256),
            # nn.LeakyReLU(0.2),

            # nn.Conv2d(256, 256, kernel_size=3, stride=2, padding=1),
            # nn.SyncBatchNorm(256),
            # nn.LeakyReLU(0.2),

            # nn.Conv2d(256, 512, kernel_size=3, padding=1),
            # nn.SyncBatchNorm(512),
            # nn.LeakyReLU(0.2),

            # nn.Conv2d(512, 512, kernel_size=3, stride=2, padding=1),
            # nn.SyncBatchNorm(512),
            # nn.LeakyReLU(0.2),

            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(128, 256, kernel_size=1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(256, 1, kernel_size=1)
        )

    def forward(self, x):
        batch_size = x.size(0)
        return F.sigmoid(self.net(x).view(batch_size, 1))


class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.SyncBatchNorm(channels)
        self.prelu = nn.PReLU()
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.SyncBatchNorm(channels)

    def forward(self, x):
        residual = self.conv1(x)
        residual = self.bn1(residual)
        residual = self.prelu(residual)
        residual = self.conv2(residual)
        residual = self.bn2(residual)

        return x + residual

class UpsampleBLock(nn.Module):
    def __init__(self, in_channels, up_scale):
        super(UpsampleBLock, self).__init__()
        self.conv = nn.Conv2d(in_channels, in_channels * up_scale ** 2, kernel_size=3, padding=1)
        self.pixel_shuffle = nn.PixelShuffle(up_scale)
        self.prelu = nn.PReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.pixel_shuffle(x)
        x = self.prelu(x)
        return x

class VGGFeatureExtractor(nn.Module):
    def __init__(self, vgg: nn.Module):
        super(VGGFeatureExtractor, self).__init__()
        self.vgg = vgg
        self.vgg.eval()
        for param in vgg.parameters():
            param.requires_grad = False
        self.vgg = vgg

    def forward(self, x):
        return self.vgg(x)
