from ultralytics import YOLO

# Example usage
model = YOLO("best.pt")  # Load a YOLO model
metrics = model.val(data='data.yaml')
print(metrics.box.map)  # mAP@0.5