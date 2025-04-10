# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o su-api .

# Stage 2: Run
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04
WORKDIR /app
EXPOSE 80
EXPOSE 8080
COPY --from=builder /app/su-api ./su-api
COPY --from=builder /app/scripts ./scripts
RUN chmod +x ./su-api

CMD ["./su-api"]
