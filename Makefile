APP_NAME=su-api
SRC=cmd
BUILD_DIR=../build

.PHONY: all clean linux windows

all: clean linux windows

linux:
	@echo "Building for Linux AMD64..."
	@cd api && GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/linux/$(APP_NAME)
	@mkdir -p $(BUILD_DIR)/linux/{scripts,models,web,desktop}
	@cp -r api/scripts $(BUILD_DIR)/linux/
	@cp -r models $(BUILD_DIR)/linux/
	@cp -r web $(BUILD_DIR)/linux/
	@cp -r desktop $(BUILD_DIR)/linux/
	@cd $(BUILD_DIR)/linux && zip -r ../$(APP_NAME)_linux.zip .

windows:
	@echo "Building for Windows AMD64..."
	@cd api && GOOS=windows GOARCH=amd64 go build -o $(BUILD_DIR)/windows/$(APP_NAME).exe
	@mkdir -p $(BUILD_DIR)/windows/{scripts,models,web,desktop}
	@cp -r api/scripts $(BUILD_DIR)/windows/
	@cp -r models $(BUILD_DIR)/windows/
	@cp -r web $(BUILD_DIR)/windows/
	@cp -r desktop $(BUILD_DIR)/windows/
	@cd $(BUILD_DIR)/windows && zip -r ../$(APP_NAME)_windows.zip .

clean:
	@echo "Cleaning up..."
	@rm -rf $(BUILD_DIR)
