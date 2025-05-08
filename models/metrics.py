import os
import torch
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr

# Define paths
test_png_dir = 'datasets/test_png/'
result_dir = 'results/ftx4_v3/'

# Get list of image IDs
image_ids = [f.split('.')[0] for f in os.listdir(test_png_dir) if f.endswith('.png')]

# Initialize dictionaries to store SSIM and PSNR values for each result directory
ssim_results = []
psnr_results = []

# Loop through each image ID
for image_id in image_ids:
    # Load the original image
    original_image_path = os.path.join(test_png_dir, f'{image_id}.png')
    original_image = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)

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

    # Compute SSIM and PSNR
    ssim_value = ssim(resized_original, processed_image, data_range=1.0)
    psnr_value = psnr(resized_original, processed_image, data_range=1.0)

    ssim_results.append(ssim_value)
    psnr_results.append(psnr_value)

    print(f"ID: {image_id}: SSIM = {ssim_value:.4f}, PSNR = {psnr_value:.4f}")

average_ssim = sum(ssim_results) / len(ssim_results)
average_psnr = sum(psnr_results) / len(psnr_results)

# Write the results to metrics.txt
with open('metrics.txt', 'w') as f:
    for image_id, ssim_value, psnr_value in zip(image_ids, ssim_results, psnr_results):
        f.write(f'ID: {image_id}: SSIM = {ssim_value:.4f}, PSNR = {psnr_value:.4f}\n')
    f.write('\n')
    f.write(f'Average SSIM: {average_ssim:.4f}\n')
    f.write(f'Average PSNR: {average_psnr:.4f}\n')
    f.write('\n')

print("SSIM and PSNR results written to metrics.txt")