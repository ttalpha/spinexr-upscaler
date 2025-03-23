import os
import cv2
import concurrent.futures
import random
import numpy as np
import argparse

# Argument parser
parser = argparse.ArgumentParser(description='Degrade PNG images.')
parser.add_argument('-s', '--scale', type=int, default=4, help='Downscale factor')
args = parser.parse_args()

# Downscale factor
downscale_factor = args.scale

_set = 'train'

# Input and output directories
input_dir = f'datasets/{_set}_png'
output_dir = f'datasets/{_set}_png_x{downscale_factor}/v2'

noise_types = ['gaussian', 'sap', 'poisson']
os.makedirs(output_dir, exist_ok=True)

def add_gaussian_noise(image):
    mean = 0
    stddev = random.uniform(5, 15) * 256
    noise = np.random.normal(mean, stddev, image.shape).astype(np.uint16)
    return cv2.addWeighted(image, 0.8, noise, 0.2, 0.0)

def add_poisson_noise(image):
    noise_scale = random.uniform(70, 100)
    image = np.random.poisson(image / 65535.0 * noise_scale) / noise_scale * 65535
    image = np.clip(image, 0, 65535).astype(np.uint16)
    return image

def add_salt_and_pepper_noise(image, prob=0.03):
    noisy_image = image.copy()
    num_salt = int(prob * image.size * 0.5)
    num_pepper = int(prob * image.size * 0.5)

    # Create random coordinates for salt & pepper noise
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]

    # Handle grayscale and color images correctly
    if len(image.shape) == 3:  # RGB Image
        noisy_image[coords[0], coords[1], :] = 65535  # White pixels
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 0  # Black pixels
    else:  # Grayscale Image
        noisy_image[coords[0], coords[1]] = 65535
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1]] = 0

    return noisy_image

def degrade_image(filename):
    if filename.endswith('.png'):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED).astype(np.uint16)
        if img is None:
            print(f"Failed to load image {img_path}")
            return

        new_size = (img.shape[1] // downscale_factor, img.shape[0] // downscale_factor)
        img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA).astype(np.uint16)

        if random.random() < 0.6:
            noise_type = random.choice(noise_types)
            if noise_type == 'gaussian':
                img_resized = add_gaussian_noise(img_resized)
            elif noise_type == 'poisson':
                img_resized = add_poisson_noise(img_resized)
            else:
                img_resized = add_salt_and_pepper_noise(img_resized)
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img_resized, [cv2.IMWRITE_JPEG_QUALITY, random.randint(80, 95)])

input_files = os.listdir(input_dir)[:1]

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(degrade_image, input_files)