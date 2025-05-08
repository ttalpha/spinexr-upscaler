import pydicom
import numpy as np
import os
import cv2
from glob import glob

def process_dicom_with_jpg(test_jpg_folder, test_dicom_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    jpg_files = glob(os.path.join(test_jpg_folder, "*.jpeg"))

    for jpg_path in jpg_files:
        file_id = os.path.basename(jpg_path).replace(".jpeg", "")
        dicom_path = os.path.join(test_dicom_folder, f"{file_id}.dicom")

        if not os.path.exists(dicom_path):
            print(f"Skipping {file_id}: No corresponding DICOM found.")
            continue

        ds = pydicom.dcmread(dicom_path, force=True)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

        jpg_image = cv2.imread(jpg_path, cv2.IMREAD_GRAYSCALE)

        jpg_image = (jpg_image / 255.0) * 65535
        jpg_image = jpg_image.astype(np.uint16)

        if 'PixelData' in ds and hasattr(ds, "NumberOfFrames") and ds.NumberOfFrames > 1:
            del ds.PixelData

        if ds.PhotometricInterpretation == 'MONOCHROME1':
          jpg_image = np.invert(jpg_image)

        ds.PixelData = jpg_image.tobytes()
        ds.Rows, ds.Columns = jpg_image.shape
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0

        output_dicom_path = os.path.join(output_folder, f"{file_id}.dicom")
        print(f"Modified DICOM saved: {output_dicom_path}")


process_dicom_with_jpg(
    test_jpg_folder="datasets/test_jpg_x4/",
    test_dicom_folder="datasets/test_images/",
    output_folder="datasets/output_dicom/"
)
