import torch
import torch.optim as optim
import torch.nn as nn
import scipy.ndimage as ndi
import cv2

class DistanceTransformLoss(nn.Module):
    def __init__(self, device="cuda", n=2):
        """
        Initializes the class with device and power for distance transformation.
        """
        super(DistanceTransformLoss, self).__init__()
        self.device = device
        self.n = n

    def tensor_to_grayscale(self, image: torch.Tensor):
        """
        Converts a batched tensor image (standardized in [-1,1]) to grayscale in range [0, 255].
        Assumes input shape: (B, C, H, W), where C=3 (RGB).
        """
        image = (image * 255).clamp(0, 255)

        # Convert RGB to grayscale using luminance formula
        grayscale = (0.299 * image[:, 0, :, :] + 0.587 * image[:, 1, :, :] + 0.114 * image[:, 2, :, :])

        return grayscale.unsqueeze(1)  # Shape: (B, 1, H, W)

    def distance_transform(self, image):
        """
        Computes the distance transform for an input image batch.
        - Background (non-object) areas will be positive
        - Foreground (object) areas will be negative

        Args:
            image (torch.Tensor): Input image batch (B, C, H, W) in range [-1,1].

        Returns:
            torch.Tensor: Distance transform of shape (B, 1, H, W).
        """
        B, _, H, W = image.shape
        image_gray = self.tensor_to_grayscale(image).byte()  # Convert to grayscale
        image_np = image_gray.cpu().numpy()

        dist_bg_list = []

        for b in range(B):
            binary_mask = cv2.adaptiveThreshold(
                image_np[b, 0], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 21, 2
            )
            binary_mask = binary_mask.astype(bool)

            # Compute distance transforms
            dist_bg = ndi.distance_transform_edt(~binary_mask)  # Background (positive)
            dist_fg = ndi.distance_transform_edt(binary_mask)   # Foreground (negative)
            # Combine background and foreground distance maps
            dist_template = dist_bg - dist_fg

            # Convert back to PyTorch tensor
            dist_template = torch.tensor(dist_template, dtype=torch.float32, device=self.device)
            dist_bg_list.append(dist_template.unsqueeze(0))  # Shape: (1, H, W)

        # Stack to form batch tensor
        dist_template = torch.stack(dist_bg_list) ** self.n   # Apply power transformation
        dist_template = torch.clamp(dist_template, max=2**30)

        return dist_template

    def forward(self, sr, hr):
        """
        Computes the transformation loss using distance-aware weighting.

        Args:
            sr (torch.Tensor): Super-resolved image (B, C, H, W).
            hr (torch.Tensor): High-resolution ground truth image (B, C, H, W).

        Returns:
            torch.Tensor: Computed transformation loss.
        """
        # Compute distance transform for super-resolved images
        dist_template = self.distance_transform(sr)

        # Compute pixel-wise loss using weighted distance transform
        loss = 0.5 * torch.mean((sr * dist_template - hr * dist_template) ** 2)

        return loss