import argparse
import json
import pydicom
import numpy as np
from PIL import Image
import os

def read_xray(path, voi_lut=True, fix_monochrome=True):
    dicom = pydicom.dcmread(path)
    dicom.decompress()

    if voi_lut:
        from pydicom.pixel_data_handlers.util import apply_voi_lut
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array

    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data

    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 65535).astype(np.uint16)

    return data, dicom

def dicom_to_png(dicom_path, png_path, metadata_path):
    pixel_data, dicom = read_xray(dicom_path, voi_lut=False)

    # Lưu ảnh PNG
    Image.fromarray(pixel_data).save(png_path, format="PNG")

    # Lưu metadata thành JSON
    metadata = {tag.keyword: dicom.get(tag.keyword, "") for tag in dicom.keys()}
    with open(metadata_path, "w") as json_file:
        json.dump(metadata, json_file, indent=4)

    print(f"✅ Đã chuyển đổi: {dicom_path} -> {png_path} | Metadata: {metadata_path}")

# Setup tham số dòng lệnh
parser = argparse.ArgumentParser(description="Chuyển đổi DICOM sang PNG và lưu metadata JSON")
parser.add_argument("-i", "--input", required=True, help="Đường dẫn file DICOM")
parser.add_argument("-o", "--output", required=True, help="Đường dẫn file PNG đầu ra")
parser.add_argument("-m", "--metadata", required=True, help="Đường dẫn file metadata JSON")

args = parser.parse_args()
dicom_to_png(args.input, args.output, args.metadata)
