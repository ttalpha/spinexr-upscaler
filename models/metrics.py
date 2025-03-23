import os
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

# Define paths
test_jpeg_dir = 'datasets/test_jpeg/'
results_dirs = {
    'base': 'results/base/',
    'ftx4': 'results/ftx4/',
    'ftx2': 'results/ftx2/',
}

# Get list of image IDs
image_ids = [f.split('.')[0] for f in os.listdir(test_jpeg_dir) if f.endswith('.jpg')]

# Initialize dictionaries to store SSIM and PSNR values for each result directory
ssim_results = {key: [] for key in results_dirs.keys()}
psnr_results = {key: [] for key in results_dirs.keys()}

# Loop through each image ID
for image_id in image_ids:
    # Load the original image
    original_image_path = os.path.join(test_jpeg_dir, f'{image_id}.jpg')
    original_image = cv2.imread(original_image_path)
    if original_image is None:
        print(f"Warning: {original_image_path} could not be loaded. Skipping.")
        continue

    print(f"ID: {image_id}")
    # Compare with images in each results directory
    for result_name, result_dir in results_dirs.items():
        # Load the processed image
        processed_image_path = os.path.join(result_dir, f'{image_id}_out.jpg')
        if not os.path.exists(processed_image_path):
            print(f"Warning: {processed_image_path} does not exist. Skipping.")
            continue

        processed_image = cv2.imread(processed_image_path)
        if processed_image is None:
            print(f"Warning: {processed_image_path} could not be loaded. Skipping.")
            continue

        # Resize the original image to match the dimensions of the processed image
        resized_original = cv2.resize(original_image, (processed_image.shape[1], processed_image.shape[0]))

        # Convert images to grayscale for SSIM (optional, but recommended for SSIM)
        resized_original_gray = cv2.cvtColor(resized_original, cv2.COLOR_BGR2GRAY)
        processed_gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)

        # Compute SSIM
        ssim_value = ssim(resized_original_gray, processed_gray, data_range=255)
        ssim_results[result_name].append(ssim_value)

        # Compute PSNR
        psnr_value = psnr(resized_original, processed_image, data_range=255)
        psnr_results[result_name].append(psnr_value)
        print(f"  {result_name}: SSIM = {ssim_value:.4f}, PSNR = {psnr_value:.4f}")
    print('-' * 40)
# Compute the average SSIM and PSNR for each results directory
average_ssim = {result_name: sum(values) / len(values) for result_name, values in ssim_results.items()}
average_psnr = {result_name: sum(values) / len(values) for result_name, values in psnr_results.items()}

# Write the results to ssim.txt
with open('metrics.txt', 'w') as f:
    for result_name in results_dirs.keys():
        f.write(f'Results for {result_name}:\n')
        f.write(f'  Average SSIM: {average_ssim[result_name]:.4f}\n')
        f.write(f'  Average PSNR: {average_psnr[result_name]:.4f}\n')
        f.write('\n')

print("SSIM and PSNR results written to metrics.txt")