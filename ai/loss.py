import torch
import torch.nn as nn
from distance_transform import DistanceTransformLoss
from models import VGGFeatureExtractor

class SNSRGANLoss(nn.Module):
    def __init__(self, vgg: VGGFeatureExtractor, dtl: DistanceTransformLoss, device='cpu', alpha=1, beta=1e-3, _lambda=1e-6, eta=0.1):
        super(SNSRGANLoss, self).__init__()
        self.device = device
        self.alpha = alpha
        self.beta = beta
        self._lambda = _lambda
        self.eta = eta
        self.dtl = dtl
        self.vgg = VGGFeatureExtractor(vgg).vgg
        self.mse = nn.MSELoss()

    def pixelwise_mse(self, sr, hr):
        return self.mse(sr, hr)

    def perceptual_loss(self, sr, hr):
        sr_image_features = self.vgg(sr)
        hr_image_features = self.vgg(hr)
        return self.mse(sr_image_features, hr_image_features)

    def total_variation_loss(self, sr):
        diff_h = torch.abs(sr[:, :, 1:, :] - sr[:, :, :-1, :])
        diff_v = torch.abs(sr[:, :, :, 1:] - sr[:, :, :, :-1])
        tv_loss = torch.sum(diff_h**2) + torch.sum(diff_v**2)
        return tv_loss

    def forward(self, sr, hr):
        return (
            self.alpha * self.pixelwise_mse(sr, hr) +
            self.beta * self.perceptual_loss(sr, hr) +
            self._lambda * self.total_variation_loss(sr) +
            self.eta * self.dtl(sr, hr)
        )