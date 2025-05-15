import pydicom
import numpy as np
import warnings
import logging
from pathlib import Path
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
from pydicom.pixel_data_handlers.util import apply_voi_lut


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

def read_xray(path, voi_lut=True, fix_monochrome=True):
    dicom = pydicom.dcmread(path)

    data = apply_voi_lut(dicom.pixel_array, dicom) if voi_lut else dicom.pixel_array

    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.invert(data)

    data = (data - data.min()) / (np.ptp(data) + 1e-7)
    return (data * 255).astype(np.uint8)

def dicom_to_jpeg(dicom_path, jpeg_path):
    try:
        img = read_xray(dicom_path, voi_lut=False)
        Image.fromarray(img).save(jpeg_path, format="JPEG")
        logger.info(f"Converted: {dicom_path} -> {jpeg_path}")
    except Exception as e:
        logger.error(f"Error processing {dicom_path}: {e}")

def process_directory_parallel(input_dir, output_dir, num_workers=8):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_files = {f.stem for f in input_dir.glob("*.dicom")}
    output_files = {f.stem for f in output_dir.glob("*.jpeg")}

    dicom_files = [(input_dir / f"{f}.dicom", output_dir / f"{f}.jpeg") for f in (input_files - output_files)][:30]

    logger.info(f"Processing {len(dicom_files)} files in parallel with {num_workers} workers.")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_file = {executor.submit(dicom_to_jpeg, dicom, jpeg): dicom for dicom, jpeg in dicom_files}

        for future in as_completed(future_to_file):
            future.result()

    logger.info("Parallel conversion complete!")

# Modify the path
test_dicom_dir = "datasets/test"
test_jpeg_dir = "datasets/test_jpeg"

process_directory_parallel(test_dicom_dir, test_jpeg_dir, num_workers=4)