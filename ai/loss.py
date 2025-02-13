import torch
import torch.nn as nn
import constants as c
from models import VGGFeatureExtractor

class SNSRGANLoss(nn.Module):
  def __init__(self, vgg, device='cpu', alpha=1, beta=1e-3, _lambda=1e-6, eta=0.1, n=10):
    super(SNSRGANLoss, self).__init__()
    self.device = device
    self.alpha = alpha
    self.beta = beta
    self._lambda = _lambda
    self.eta = eta
    self.n = n

    self.vgg = VGGFeatureExtractor(vgg).vgg
    self.mse = nn.MSELoss()
    self.bce = nn.BCELoss()

  def conditional_adversarial_loss(self, d_fake):
    return torch.mean(torch.log(d_fake + 1e-8))

  def pixelwise_mse(self, sr, hr):
    return self.mse(hr, sr)

  def perceptual_loss(self, sr, hr):
    sr_image_features = self.vgg(sr)
    hr_image_features = self.vgg(hr)
    return self.mse(sr_image_features, hr_image_features)

  def total_variation_loss(self, sr):
    diff_h = torch.abs(sr[:, :, 1:, :] - sr[:, :, :-1, :])
    diff_v = torch.abs(sr[:, :, :, 1:] - sr[:, :, :, :-1])
    tv_loss = torch.sum(diff_h**2) + torch.sum(diff_v**2)
    return tv_loss

  def __distance_transform(self, mask):
    mask = (mask > 0).float()
    zero_pixels = (mask == 0).nonzero(as_tuple=False).float()
    h, w = mask.shape
    y_coords, x_coords = torch.meshgrid(torch.arange(h), torch.arange(w))
    coords = torch.stack([y_coords.flatten(), x_coords.flatten()], dim=1).float()

    distances = torch.cdist(coords.to(self.device), zero_pixels, p=2)  # p=2 for Euclidean distance
    min_distances = distances.min(dim=1)[0]  # Find the minimum distance for each pixel

    distance_transform = min_distances.reshape(h, w)
    return distance_transform

  def transform_loss(self, sr, hr):
    mask = torch.randint(0, 2, (c.PATCH_SIZE, c.PATCH_SIZE), device=self.device).float()
    dist_transform = self.__distance_transform(mask)
    dist_transform = dist_transform

    # Raise the distance transform to the power of n
    d_con_n = dist_transform ** self.n
    d_con_n = d_con_n.unsqueeze(0).unsqueeze(0)  # Add batch and channel dimensions
    loss = 0.5 * torch.mean((sr * d_con_n - hr * d_con_n) ** 2)
    return loss

  def forward(self, sr, hr, d_fake):
    return (
      self.conditional_adversarial_loss(d_fake) + \
      self.alpha * self.pixelwise_mse(sr, hr) + \
      self.beta * self.perceptual_loss(sr, hr) + \
      self._lambda * self.total_variation_loss(sr) + \
      self.eta * self.transform_loss(sr, hr)
    )