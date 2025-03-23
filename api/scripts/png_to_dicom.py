import argparse
import json
import pydicom
import numpy as np
from PIL import Image

def png_to_dicom(png_path, json_path, dicom_path):
    # Đọc ảnh PNG
    img = Image.open(png_path).convert("L")  # Chuyển về ảnh xám
    pixel_array = np.array(img).astype(np.uint16)

    # Đọc metadata từ file JSON
    with open(json_path, "r") as json_file:
        metadata = json.load(json_file)

    # Tạo file DICOM mới
    dicom = pydicom.Dataset()
    dicom.file_meta = pydicom.dataset.FileMetaDataset()
    dicom.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    # Gán lại metadata
    for key, value in metadata.items():
        setattr(dicom, key, value)

    # Gán pixel data
    dicom.PixelData = pixel_array.tobytes()
    dicom.Rows, dicom.Columns = pixel_array.shape
    dicom.BitsAllocated = 16
    dicom.BitsStored = 16
    dicom.HighBit = 15
    dicom.SamplesPerPixel = 1
    dicom.PhotometricInterpretation = "MONOCHROME2"

    # Lưu DICOM
    dicom.save_as(dicom_path)
    print(f"✅ Đã chuyển đổi: {png_path} -> {dicom_path}")

# Setup tham số dòng lệnh
parser = argparse.ArgumentParser(description="Chuyển đổi PNG về DICOM từ metadata JSON")
parser.add_argument("-i", "--input", required=True, help="Đường dẫn file PNG")
parser.add_argument("-o", "--output", required=True, help="Đường dẫn file DICOM đầu ra")
parser.add_argument("-m", "--metadata", required=True, help="Đường dẫn file metadata JSON")

args = parser.parse_args()
png_to_dicom(args.input, args.metadata, args.output)
