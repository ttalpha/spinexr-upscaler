import torch
import torchvision.transforms.v2 as transforms
from torchvision.transforms import InterpolationMode

from constants import PATCH_SIZE, SCALE_FACTOR

hr_transform = transforms.Compose([
  transforms.ToImage(),
  transforms.ToDtype(dtype=torch.float32, scale=True),
  transforms.Resize((PATCH_SIZE * 4, PATCH_SIZE * 4), interpolation=InterpolationMode.BICUBIC),
])

lr_transform = transforms.Compose([
  transforms.Resize((PATCH_SIZE // SCALE_FACTOR, PATCH_SIZE // SCALE_FACTOR), interpolation=InterpolationMode.BICUBIC),
])
