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
	@mkdir -p $(BUILD_DIR)/linux/{scripts,models,web,desktop}
	@cp -r $(PWD)/api/scripts $(BUILD_DIR)/linux/
	@cp -r $(PWD)/models $(BUILD_DIR)/linux/
	@cp -r $(PWD)/web $(BUILD_DIR)/linux/
	@cp -r $(PWD)/desktop $(BUILD_DIR)/linux/
	@cd $(BUILD_DIR)/linux && zip -r $(BUILD_DIR)/$(FULL_NAME)-linux.zip .

windows:
	@echo "Building for Windows AMD64..."
	@cd api && GOOS=windows GOARCH=amd64 go build -o $(BUILD_DIR)/windows/$(APP_NAME).exe
	@mkdir -p $(BUILD_DIR)/windows/{scripts,models,web,desktop}
	@cp -r $(PWD)/api/scripts $(BUILD_DIR)/windows/
	@cp -r $(PWD)/models $(BUILD_DIR)/windows/
	@cp -r $(PWD)/web $(BUILD_DIR)/windows/
	@cp -r $(PWD)/desktop $(BUILD_DIR)/windows/
	@cd $(BUILD_DIR)/windows && zip -r $(BUILD_DIR)/$(FULL_NAME)-windows.zip .

clean:
	@echo "Cleaning up..."
	@rm -rf $(BUILD_DIR)
