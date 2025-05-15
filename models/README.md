# ESRGAN Model

## Prerequisites

- Python 3.12.x
- Conda (optional)

## Setup and Installation

Install all necessary packages
```bash
pip install -r requirements.txt
```

[Download the dataset here](https://physionet.org/content/vindr-spinexr/1.0.0/) and place `train/` and `test/` directories in `datasets/`

Download ESRGAN model `g_x4_v3.pth` and place it in `weights/` directory
Download YOLO model `best.pt` and place it in `yolo/weights/` directory

Change the `infer.sh` file to the corresponding input path, output path and model path.

Then, run the script
```bash
sh infer.sh
```

> If there are errors regarding the `degradations.py` from `basicsr` package, modify the package code with the `degradations.py` from the current directory.

## Training
Convert the DICOM files in `datasets/` directory to either PNG or JPEG with `to_png.py` or `to_jpeg.py`. Modify the specified path in the python scripts if needed. The output by default will be in either `*_png` or `*_jpeg` directory.

Run `resize.py` to resize the output images to multiples of 4 to avoid any errors when training.

Run `degrade_jpg.py` or `degrade_png.py` based on the output format above to generate low-res images. The output will be in `*_jpeg_x4` or `*_png_x4` directory.

[Follow the instruction](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/Training.md#use-your-own-paired-data) to continue.