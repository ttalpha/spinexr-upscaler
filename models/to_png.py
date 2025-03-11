import os
import pydicom
import numpy as np
import warnings
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from pydicom.pixel_data_handlers.util import apply_voi_lut

warnings.filterwarnings('ignore')

def read_xray(path, voi_lut = True, fix_monochrome = True):
    dicom = pydicom.dcmread(path)
    dicom.decompress()
    # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array

    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data

    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 65535).astype(np.uint16)

    return data

# Function to convert DICOM to PNG
def dicom_to_png(dicom_path, png_path):
    img = read_xray(dicom_path, voi_lut=False)
    img = Image.fromarray(img)
    img.save(png_path, format="PNG")
    print(f"Converted: {dicom_path} -> {png_path}")

def process_directory_parallel(input_dir, output_dir, num_workers=8):
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
    input_files = set([f.split('.')[0] for f in os.listdir(input_dir)])
    output_files = set([f.split('.')[0] for f in os.listdir(output_dir)])
    not_output_files = list(input_files.difference(output_files))

    dicom_files = [
        (os.path.join(input_dir, f'{f}.dicom'), os.path.join(output_dir, f'{f}.jpg'))
        for f in not_output_files[:10]
    ]

    # Use ProcessPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(lambda args: dicom_to_png(*args), dicom_files)

# Directories
train_dicom_dir = "../ai/dataset/train_images"
# test_dicom_dir = "dataset/test_images"
train_png_dir = "datasets/train_png"
# test_png_dir = "dataset/test_png"

# Process train and test directories in parallel
process_directory_parallel(train_dicom_dir, train_png_dir, num_workers=4)
# process_directory_parallel(test_dicom_dir, test_png_dir, num_workers=4)

print("Parallel conversion complete!")
