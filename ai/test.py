import torch
import torch.nn as nn
import torchvision.transforms as transforms
import glob
import random
from constants import SCALE_FACTOR
from PIL import Image
import concurrent.futures
import os
from torchmetrics.image.ssim import StructuralSimilarityIndexMeasure
from models import Generator

input_dir = "images/test_jpeg/"
output_dir = "images/upscaled/"
os.makedirs(output_dir, exist_ok=True)


# Load Generator Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the state_dict
state_dict = torch.load("models/generator.pt", map_location="cpu")

new_state_dict = {}
for key, value in state_dict.items():
    new_key = key.replace("module.", "")
    new_key = new_key.replace("upsampler.1.weight", "upsampler.1.conv.weight")  # Adjust based on the difference
    new_key = new_key.replace("upsampler.1.bias", "upsampler.1.conv.bias")
    new_state_dict[new_key] = value

# Load into model
generator = Generator(scale_factor=SCALE_FACTOR).to(device)  # Assuming Generator class is in models.py
generator.load_state_dict(new_state_dict)
generator.eval()  # Set to evaluation mode

# Select 10 random images
image_paths = glob.glob(f"{input_dir}/*.jpg")
selected_images = set(random.sample(image_paths, 10))

# Define transforms
to_tensor = transforms.ToTensor()
to_pil = transforms.ToPILImage()
# Initialize SSIM metric
ssim_metric = StructuralSimilarityIndexMeasure().to(device)

ssim_scores = []

def process_image(img_path):
    # Load image
    img = Image.open(img_path).convert("RGB")
    w, h = img.width, img.height
    w -= (w % SCALE_FACTOR)
    h -= (h % SCALE_FACTOR)

    # Downscale by factor of 4
    cropped = img.resize((w, h), Image.BICUBIC)
    downscaled = img.resize((w // SCALE_FACTOR, h // SCALE_FACTOR), Image.BICUBIC)

    # Convert to tensor and normalize
    lr_tensor = to_tensor(downscaled).unsqueeze(0).to(device)  # (1, C, H, W)

    # Super-resolve using the generator
    with torch.no_grad():
        sr_tensor = generator(lr_tensor).clamp(0, 1)  # Ensure values are valid

    # Convert back to PIL Image
    sr_image = to_pil(sr_tensor.squeeze(0).cpu())

    # Save upscaled image
    if img_path in selected_images:
        output_path = os.path.join(output_dir, os.path.basename(img_path))
        sr_image.save(output_path)

    # Compute SSIM
    hr_tensor = to_tensor(cropped).unsqueeze(0).to(device)  # Convert original to tensor
    ssim_score = ssim_metric(sr_tensor, hr_tensor).item()
    return ssim_score

# Use ThreadPoolExecutor to process images concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    ssim_scores = list(executor.map(process_image, image_paths))

# Compute average SSIM
avg_ssim = sum(ssim_scores) / len(ssim_scores)
print(f"Average SSIM: {avg_ssim:.4f}")
