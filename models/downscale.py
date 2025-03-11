import os
import cv2
import concurrent.futures
import random

downscale_factor = 2

input_dir = 'datasets/test_jpeg'
output_dir = f'datasets/test_jpeg_x{downscale_factor}'

def add_gaussian_blur(image):
    kernel_size = random.randrange(3, 8, 2)
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)  # Reduced kernel size for more subtle blur

os.makedirs(output_dir, exist_ok=True)
def downscale_image(filename):
    print('Filename:', filename)
    if filename.endswith('.jpg'):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)
        new_size = (img.shape[1] // downscale_factor, img.shape[0] // downscale_factor)
        img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

        if random.random() < 0.8:
            img_resized = add_gaussian_blur(img_resized)

        # Save with JPEG compression
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img_resized, [int(cv2.IMWRITE_JPEG_QUALITY), random.randint(75, 100)])

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(downscale_image, os.listdir(input_dir))

print("Downscaling completed.")