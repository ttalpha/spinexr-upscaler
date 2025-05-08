# ===== Stage 1: Build the Go binary =====
FROM golang:1.24 AS builder

WORKDIR /app

# Copy Go API source
COPY api/ api/

# Copy models into api/models
COPY models/weights/g_x4_v3.pth api/models/weights/
COPY models/realesrgan/ api/models/realesrgan/
COPY models/inference_realesrgan.py api/models/
COPY models/degradations.py api/models/
COPY models/requirements.txt api/models/

# Build the Go app
RUN cd api && go build -o su-api .

# ===== Stage 2: Final image with PyTorch and the binary =====
FROM pytorch/pytorch:2.5.0-cuda12.1-cudnn9-runtime

WORKDIR /app

COPY --from=builder /app/api /app/api
COPY --from=builder /app/api/models /app/api/models
RUN apt-get update && apt-get install libgl1 libglib2.0-0 -y
RUN cd api/models && pip install --no-cache-dir -r requirements.txt
RUN cat api/models/degradations.py > /opt/conda/lib/python3.11/site-packages/basicsr/data/degradations.py
RUN chmod +x ./api/su-api

EXPOSE 8080

CMD ["./api/su-api"]
