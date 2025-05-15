# YOLO model

## Introduction
This is the source code for the YOLO model pretrained on spine X-ray images.

## Set up and installation
Install `ultralytics`
```bash
pip install ultralytics
```

Download `best.pt` model and put it in `weights/` folder.

### Inference
Run
```bash
python infer.py
```

### Continue training
Run
```bash
sh train.sh
```
