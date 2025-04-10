# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o su-api .

# Stage 2: Run
FROM pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel
WORKDIR /app
EXPOSE 80
EXPOSE 8080
COPY --from=builder /app/su-api ./su-api
COPY --from=builder /app/scripts ./scripts
RUN chmod +x ./su-api

CMD ["./su-api"]
