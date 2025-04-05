import argparse
import json
import pydicom
import numpy as np
from PIL import Image
import os

def read_xray(path, voi_lut=True, fix_monochrome=True):
    dicom = pydicom.dcmread(path)

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

    return data

def extract_dicom_metadata(dicom_path, json_path):
    dicom_data = pydicom.dcmread(dicom_path, stop_before_pixels=True)
    metadata = {}

    for elem in dicom_data.iterall():
        is_multivalue = isinstance(elem.value, pydicom.multival.MultiValue)
        value = elem.value if not is_multivalue else [str(v) for v in elem.value]

        if elem.keyword:
            metadata[elem.keyword] = value

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(metadata, json_file, indent=4, default=str)

    print(f"Metadata saved to {json_path}")


def dicom_to_png(dicom_path, png_path, metadata_path):
    pixel_data = read_xray(dicom_path, voi_lut=False)
    Image.fromarray(pixel_data).save(png_path, format="PNG")
    extract_dicom_metadata(dicom_path, metadata_path)
    print(f"✅ Converted: {dicom_path} -> {png_path} | Metadata: {metadata_path}")


parser = argparse.ArgumentParser(description="Convert DICOM to PNG and extract metadata")
parser.add_argument("-i", "--input", required=True, help="Path to DICOM file")
parser.add_argument("-o", "--output", required=True, help="Path to output PNG file")
parser.add_argument("-m", "--metadata", required=True, help="Path to output metadata JSON file")

args = parser.parse_args()
dicom_to_png(args.input, args.output, args.metadata)
