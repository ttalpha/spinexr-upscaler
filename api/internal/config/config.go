package config

type Config struct {
	UploadFolder string
	MaxUploadFiles int
}

var Default = Config{
	UploadFolder: "your_folder",
	MaxUploadFiles: 3,
}
