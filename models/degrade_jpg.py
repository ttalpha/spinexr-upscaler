import os
import cv2
import concurrent.futures
import random
import numpy as np

# Downscale factor
downscale_factor = 4

_set = 'test'

# Input and output directories
input_dir = f'datasets/{_set}_jpeg'
output_dir = f'datasets/{_set}_jpeg_x{downscale_factor}'

noise_types = ['gaussian', 'sap', 'poisson']
# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store effects applied to each image
effects_dict = {}

def add_gaussian_noise(image):
    """Subtle Gaussian noise"""
    mean = 0
    stddev = random.uniform(5, 15)
    noise = np.random.normal(mean, stddev, image.shape).astype(np.uint8)
    return cv2.addWeighted(image, 0.9, noise, 0.1, 0.0)

def add_poisson_noise(image):
    """Add Poisson noise"""
    image = np.random.poisson(image / 255.0 * 100) / 100 * 255
    image = np.clip(image, 0, 255).astype(np.uint8)
    return image

def add_salt_and_pepper_noise(image, prob=0.03):
    noisy_image = image.copy()
    num_salt = int(prob * image.size * 0.5)
    num_pepper = int(prob * image.size * 0.5)

    # Create random coordinates for salt & pepper noise
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]

    # Handle grayscale and color images correctly
    if len(image.shape) == 3:  # RGB Image
        noisy_image[coords[0], coords[1], :] = 255  # White pixels
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 0  # Black pixels
    else:  # Grayscale Image
        noisy_image[coords[0], coords[1]] = 255
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
        noisy_image[coords[0], coords[1]] = 0

    return noisy_image


def add_motion_blur(image):
    size = random.randint(3, 8)
    angle = random.uniform(-360, 360)
    kernel = np.zeros((size, size))
    kernel[(size - 1) // 2, :] = np.ones(size)
    rotation_matrix = cv2.getRotationMatrix2D((size // 2, size // 2), angle, 1)
    kernel = cv2.warpAffine(kernel, rotation_matrix, (size, size))
    kernel /= np.sum(kernel)
    return cv2.filter2D(image, -1, kernel)

sap_count = 0
gaussian_count = 0
poisson_count = 0

def downscale_image(filename):
    global sap_count, gaussian_count, poisson_count
    print('Processing:', filename)
    if filename.endswith('.jpg'):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        new_size = (img.shape[1] // downscale_factor, img.shape[0] // downscale_factor)
        img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA).astype(np.uint8)

        if random.random() < 0.8:
            noise_type = random.choice(noise_types)
            print(noise_type, filename)

            if noise_type == 'gaussian':
                img_resized = add_gaussian_noise(img_resized)
                gaussian_count += 1
            elif noise_type == 'poisson':
                img_resized = add_poisson_noise(img_resized)
                poisson_count += 1
            else:
                img_resized = add_salt_and_pepper_noise(img_resized)
                sap_count += 1

        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img_resized, [cv2.IMWRITE_JPEG_QUALITY, random.randint(75, 100)])

input_files = os.listdir(input_dir)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(downscale_image, input_files)

print(f"Gaussian: {gaussian_count}, Poisson: {poisson_count}, SAP: {sap_count}")
