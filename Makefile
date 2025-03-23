APP_NAME=su-api
FULL_NAME=Spinexr-Upscaler
SRC=cmd
BUILD_DIR=$(PWD)/build
PWD=$(shell pwd)

.PHONY: all clean linux windows

all: clean linux windows

linux:
	@echo "Building for Linux AMD64..."
	@cd api && GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/linux/$(APP_NAME)
	@mkdir -p $(BUILD_DIR)/linux/{scripts,models}
	@cp -r $(PWD)/api/scripts $(BUILD_DIR)/linux/
	@mkdir -p $(BUILD_DIR)/linux/models
	@cp -r $(PWD)/models/realesrgan $(BUILD_DIR)/linux/models/
	@cp -r $(PWD)/models/inference_realesrgan.py $(BUILD_DIR)/linux/models/
	@cd $(BUILD_DIR)/linux && zip -r $(BUILD_DIR)/$(FULL_NAME)-linux.zip .

windows:
	@echo "Building for Windows AMD64..."
	@cd api && GOOS=windows GOARCH=amd64 go build -o $(BUILD_DIR)/windows/$(APP_NAME).exe
	@mkdir -p $(BUILD_DIR)/windows/{scripts,models}
	@cp -r $(PWD)/api/scripts $(BUILD_DIR)/windows/
	@mkdir -p $(BUILD_DIR)/windows/models
        @cp -r $(PWD)/models/realesrgan $(BUILD_DIR)/windows/models/
        @cp -r $(PWD)/models/inference_realesrgan.py $(BUILD_DIR)/windows/models/
	@cd $(BUILD_DIR)/windows && zip -r $(BUILD_DIR)/$(FULL_NAME)-windows.zip .

clean:
	@echo "Cleaning up..."
	@rm -rf $(BUILD_DIR)
