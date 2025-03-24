import pydicom
import numpy as np
import os
import cv2
from glob import glob

def process_dicom_with_png(test_png_folder, test_dicom_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    png_files = glob(os.path.join(test_png_folder, "*.png"))

    for png_path in png_files:
        file_id = os.path.basename(png_path).replace(".png", "")
        dicom_path = os.path.join(test_dicom_folder, f"{file_id}.dicom")

        if not os.path.exists(dicom_path):
            print(f"Skipping {file_id}: No corresponding DICOM found.")
            continue

        # Load the original DICOM file
        ds = pydicom.dcmread(dicom_path, force=True)  # Force read in case of compressed images

        # Ensure the file is uncompressed (reset transfer syntax)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

        # Read the PNG image and convert to grayscale
        png_image = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)

        # Convert 8-bit PNG to 16-bit grayscale (DICOM standard)
        png_image = (png_image / 255.0) * 65535
        png_image = png_image.astype(np.uint16)

        if 'PixelData' in ds and hasattr(ds, "NumberOfFrames") and ds.NumberOfFrames > 1:
            del ds.PixelData  # Remove any old compressed pixel data

        # Set pixel data
        if ds.PhotometricInterpretation == 'MONOCHROME1':
          png_image = np.invert(png_image)

        ds.PixelData = png_image.tobytes()
        ds.Rows, ds.Columns = png_image.shape
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0  # Unsigned integers

        # Save the modified DICOM file
        output_dicom_path = os.path.join(output_folder, f"{file_id}.dicom")
        ds.save_as(output_dicom_path)
        print(f"Modified DICOM saved: {output_dicom_path}")

# Example usage
process_dicom_with_png(
    test_png_folder="datasets/test_png_x4/",
    test_dicom_folder="datasets/test_images/",
    output_folder="datasets/output_dicom/"
)
