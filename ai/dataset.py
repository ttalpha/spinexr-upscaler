import cv2
import torch
from torchvision.transforms import transforms
from torch.utils.data import Dataset

class XrayDataset(Dataset):
  def __init__(self, images_path, hr_patch_size, hr_transform, lr_transform):
    self.images_path = images_path
    self.hr_transform = hr_transform
    self.hr_patch_size = hr_patch_size
    self.lr_transform = lr_transform
    self.normalizer = transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))

  def __len__(self):
    return len(self.images_path)

  def __getitem__(self, index):
    image_path = self.images_path[index]
    hr_image = cv2.imread(image_path, flags=cv2.IMREAD_COLOR_RGB)
    hr_image = torch.tensor(hr_image).permute(2, 0, 1)
    hr_image = self.hr_transform(hr_image)
    lr_image = self.lr_transform(hr_image)
    hr_image = self.normalizer(hr_image)
    lr_image = self.normalizer(lr_image)
    return lr_image, hr_image