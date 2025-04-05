yolo task=detect \
      mode=train \
      model=best.pt \
      data=data.yaml \
      epochs=200 \
      imgsz=640 \
      batch=48 \
      optimizer=Adam