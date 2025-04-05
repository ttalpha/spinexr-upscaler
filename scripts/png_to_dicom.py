import argparse
from PIL import Image
import numpy as np
import pydicom

def png_to_dicom(png_path, dicom_path):
    # Load image
    img = Image.open(png_path).convert("I;16")  # 16-bit grayscale
    pixel_array = np.array(img)

    # Read existing DICOM file
    dicom = pydicom.dcmread(dicom_path)

    # Modify pixel data
    dicom.PixelData = pixel_array.tobytes()
    dicom.Rows, dicom.Columns = pixel_array.shape
    dicom.BitsAllocated = 16
    dicom.BitsStored = 16
    dicom.WindowCenter = 32768
    dicom.WindowWidth = 65536
    dicom.RescaleIntercept = 0
    dicom.RescaleSlope = 1

    dicom.HighBit = 15
    dicom.SamplesPerPixel = 1
    dicom.PhotometricInterpretation = "MONOCHROME2"
    dicom.PixelRepresentation = 0  # unsigned int

    # Save modified DICOM file
    dicom.save_as(dicom_path, enforce_file_format=True)
    print(f"✅ Modified DICOM: {png_path} -> {dicom_path}")

parser = argparse.ArgumentParser(description="Convert PNG to DICOM")
parser.add_argument("-i", "--input", required=True, help="Input PNG file path")
parser.add_argument("-o", "--output", required=True, help="Output DICOM file path")

args = parser.parse_args()
png_to_dicom(args.input, args.output)
