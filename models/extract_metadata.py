import pydicom
import json

def extract_dicom_metadata(dicom_path, json_path):
    # Load DICOM file without pixel data
    dicom_data = pydicom.dcmread(dicom_path, stop_before_pixels=True)

    # Convert all metadata (excluding pixel data) to a dictionary
    metadata = {}
    for elem in dicom_data.iterall():
        metadata[elem.name] = str(elem.value)

    # Save metadata as JSON
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(metadata, json_file, indent=4)

    print(f"Metadata saved to {json_path}")


# Example usage
extract_dicom_metadata("datasets/output_dicom/3cc0a50c9c6f8d47a27ecbcc522c431d.dicom", "output.json")
