import torch
import torchvision.transforms.v2 as transforms
from torchvision.transforms import InterpolationMode

from constants import PATCH_SIZE

hr_transform = transforms.Compose([
  transforms.ToImage(),
  transforms.ToDtype(dtype=torch.float32, scale=True),
  transforms.Resize((PATCH_SIZE, PATCH_SIZE), interpolation=InterpolationMode.BICUBIC)
])

lr_transform = transforms.Compose([
  transforms.Resize((PATCH_SIZE // 2, PATCH_SIZE // 2), interpolation=InterpolationMode.BICUBIC),
])
