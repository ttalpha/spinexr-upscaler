import argparse
import pydicom
import numpy as np
from PIL import Image

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


def dicom_to_png(dicom_path, png_path):
    pixel_data = read_xray(dicom_path, voi_lut=False)
    Image.fromarray(pixel_data).save(png_path, format="PNG")
    print(f"✅ Converted: {dicom_path} -> {png_path}")


parser = argparse.ArgumentParser(description="Convert DICOM to PNG and extract metadata")
parser.add_argument("-i", "--input", required=True, help="Path to DICOM file")
parser.add_argument("-o", "--output", required=True, help="Path to output PNG file")

args = parser.parse_args()
dicom_to_png(args.input, args.output)
