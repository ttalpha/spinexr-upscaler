import os
import torch
import cv2
import numpy as np
from torchmetrics.image import MultiScaleStructuralSimilarityIndexMeasure
torch.set_default_device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Define paths
test_png_dir = 'datasets/test_png/'
result_dir = 'results/ftx4_v3/'

# Get list of image IDs
image_ids = [f.split('.')[0] for f in os.listdir(test_png_dir) if f.endswith('.png')]

ms_ssim = MultiScaleStructuralSimilarityIndexMeasure(data_range=1.0)
# Initialize dictionaries to store SSIM and PSNR values for each result directory
ms_ssim_results = []

# Loop through each image ID
for image_id in image_ids:
    # Load the original image
    original_image_path = os.path.join(test_png_dir, f'{image_id}.png')
    original_image = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)
    print(original_image.dtype)
    break
    original_image = original_image.astype(np.float64) / 65535.0
    if original_image is None:
        print(f"Warning: {original_image_path} could not be loaded. Skipping.")
        continue
    processed_image_path = os.path.join(result_dir, f'{image_id}_out.png')
    if not os.path.exists(processed_image_path):
        print(f"Warning: {processed_image_path} does not exist. Skipping.")
        continue

    processed_image = cv2.imread(processed_image_path, cv2.IMREAD_UNCHANGED)
    processed_image = processed_image.astype(np.float64) / 65535.0
    if processed_image is None:
        print(f"Warning: {processed_image_path} could not be loaded. Skipping.")
        continue

    resized_original = cv2.resize(original_image, (processed_image.shape[1], processed_image.shape[0]))
    resized_original = torch.tensor(resized_original).unsqueeze(0).unsqueeze(0)
    processed_image = torch.tensor(processed_image).unsqueeze(0).unsqueeze(0)
    ms_ssim_value = ms_ssim(resized_original, processed_image)
    ms_ssim_results.append(ms_ssim_value)

    print(f"ID: {image_id}: MS_SSIM = {ms_ssim_value:.4f}")

average_ms_ssim = sum(ms_ssim_results) / len(ms_ssim_results)

# Write the results to ssim.txt
with open('metrics.txt', 'w') as f:
    for image_id, ms_ssim_value in zip(image_ids, ms_ssim_results):
        f.write(f'ID: {image_id}: MS_SSIM = {ms_ssim_value:.4f}\n')
    f.write('\n')
    f.write(f'Average MS_SSIM: {average_ms_ssim:.4f}\n')
    f.write('\n')

print("SSIM and PSNR results written to metrics.txt")