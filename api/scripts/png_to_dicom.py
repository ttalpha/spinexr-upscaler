import argparse
import numpy as np
from PIL import Image
import pydicom
from pydicom.datadict import tag_for_keyword, dictionary_VR
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import json

def parse_value(vr, value):
    """Cast string value back to proper DICOM VR type"""
    if isinstance(value, list):
        return [parse_value(vr, v) for v in value]

    try:
        if vr in ["IS", "US", "SS", "UL", "SL"]:
            return int(value)
        elif vr in ["DS", "FL", "FD"]:
            return float(value)
        elif vr in ["DA"]:  # Date
            return pydicom.valuerep.DA(value)
        elif vr in ["TM"]:  # Time
            return pydicom.valuerep.TM(value)
        elif vr in ["PN"]:  # Person Name
            return pydicom.valuerep.PersonName(value)
        elif vr in ["UI"]:  # UID
            return pydicom.uid.UID(value)
        else:
            return value
    except:
        return value

def png_to_dicom(png_path, json_path, dicom_path):
    # Load image
    img = Image.open(png_path).convert("I;16")  # 16-bit grayscale
    pixel_array = np.array(img)

    # Load metadata
    with open(json_path, "r") as f:
        metadata = json.load(f)

    dicom = pydicom.Dataset()
    dicom.file_meta = pydicom.dataset.FileMetaDataset()
    dicom.file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    dicom.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    dicom.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    dicom.file_meta.ImplementationClassUID = generate_uid()

    dicom.SOPClassUID = dicom.file_meta.MediaStorageSOPClassUID
    dicom.SOPInstanceUID = dicom.file_meta.MediaStorageSOPInstanceUID

    # Restore metadata
    for key, value in metadata.items():
        try:
            tag = tag_for_keyword(key)
            vr = dictionary_VR(tag)
            parsed = parse_value(vr, value)
            setattr(dicom, key, parsed)
        except Exception as e:
            print(f"[!] Skipping {key}: {e}")

    # Add pixel data
    dicom.PixelData = pixel_array.tobytes()
    dicom.Rows, dicom.Columns = pixel_array.shape
    dicom.BitsAllocated = 16
    dicom.BitsStored = 16
    dicom.HighBit = 15
    dicom.SamplesPerPixel = 1
    dicom.PhotometricInterpretation = "MONOCHROME2"
    dicom.PixelRepresentation = 0  # unsigned int

    dicom.save_as(dicom_path, enforce_file_format=True)
    print(f"✅ Converted to DICOM: {png_path} -> {dicom_path}")

parser = argparse.ArgumentParser(description="Convert PNG to DICOM")
parser.add_argument("-i", "--input", required=True, help="Input PNG file path")
parser.add_argument("-o", "--output", required=True, help="Output DICOM file path")
parser.add_argument("-m", "--metadata", required=True, help="Metadata JSON file path")

args = parser.parse_args()
png_to_dicom(args.input, args.metadata, args.output)
