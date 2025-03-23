import cv2
import os
from pathlib import Path

import numpy as np

def resize_images_to_multiple_of_4(input_dir, output_dir):
    """
    Resizes all images in the input directory so that their dimensions are multiples of 4.
    Saves the resized images to the output directory.

    Args:
        input_dir (str): Path to the directory containing the input images.
        output_dir (str): Path to the directory where resized images will be saved.
    """
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filenames = os.listdir(input_dir)

    # Iterate through all files in the input directory
    for filename in filenames:
        # Construct the full file path
        file_path = os.path.join(input_dir, filename)

        # Check if the file is an image (supports JPEG, PNG, etc.)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Load the image
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED).astype(np.uint16)
            if len(image.shape) == 3:  # RGB image
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.uint16)
                print('Converting to Grayscale', filename)
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, image)
            continue

            if image is not None:
                # # Get the original dimensions
                # height, width = image.shape[:2]

                # # Calculate new dimensions that are multiples of 4
                # new_width = (width // 4) * 4
                # new_height = (height // 4) * 4

                # # Resize the image
                # resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA).astype(np.uint16)

                # # Save the resized image to the output directory
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, image)

                # print(f"Resized {filename} to {new_width}x{new_height}")
            else:
                print(f"Failed to load {filename}")
        else:
            print(f"Skipping non-image file: {filename}")

# Example usage
input_directory = 'datasets/train_png'
output_directory = 'datasets/train_png'

resize_images_to_multiple_of_4(input_directory, output_directory)