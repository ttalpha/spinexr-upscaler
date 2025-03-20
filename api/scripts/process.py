import sys
from PIL import Image

def process_dicom(input_path, output_path, upscale, bit):
    print(f"Processing {input_path} with upscale={upscale}, bit={bit}")

    # Giả lập xử lý DICOM
    image = Image.new('RGB', (256, 256), (0, 0, 0))  # Tạo ảnh đen

    # Giả lập upscale (không phải thật)
    if upscale == "x2":
        image = image.resize((512, 512))
    elif upscale == "x4":
        image = image.resize((1024, 1024))

    # Giả lập bit depth (chỉ để minh họa)
    if bit == "8":
        image = image.convert("L")  # 8-bit grayscale
    elif bit == "16":
        image = image.convert("I")  # 16-bit grayscale

    image.save(output_path)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: process.py <input.dcm> <output.png> <upscale> <bit>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    upscale = sys.argv[3]
    bit = sys.argv[4]
    
    process_dicom(input_file, output_file, upscale, bit)
