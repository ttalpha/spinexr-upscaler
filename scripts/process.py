import sys
from PIL import Image

def process_dicom(input_path, output_path):
    # Giả lập việc xử lý DICOM và lưu dưới dạng PNG
    image = Image.new('RGB', (256, 256), (0, 0, 0))  # Tạo ảnh đen
    image.save(output_path)
    print(f"Processed {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: process.py <input.dcm> <output.png>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_dicom(input_file, output_file)
