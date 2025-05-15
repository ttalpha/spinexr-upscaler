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

        dicom = pydicom.dcmread(dicom_path, force=True)
        dicom.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

        png_image = cv2.imread(png_path, cv2.IMREAD_UNCHANGED).astype(np.uint16)
        print(png_image.max())

        if 'PixelData' in dicom and hasattr(dicom, "NumberOfFrames") and dicom.NumberOfFrames > 1:
            del dicom.PixelData

        if dicom.PhotometricInterpretation == 'MONOCHROME1':
          png_image = np.invert(png_image)

        dicom.PixelData = png_image.tobytes()
        dicom.Rows, dicom.Columns = png_image.shape
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

        output_dicom_path = os.path.join(output_folder, f"{file_id}.dicom")
        dicom.save_as(output_dicom_path)
        print(f"Modified DICOM saved: {output_dicom_path}")


process_dicom_with_png(
    test_png_folder="datasets/test_png_x4/",
    test_dicom_folder="datasets/test_dicom/",
    output_folder="datasets/output_dicom/"
)
