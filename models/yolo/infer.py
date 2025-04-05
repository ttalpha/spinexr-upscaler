from ultralytics import YOLO

class CustomYOLO(YOLO):
    @property
    def names(self):
        return self.model.names  # Access the original names

    @names.setter
    def names(self, new_names):
        if isinstance(new_names, dict):
            self.model.names = new_names  # Assign new dictionary
        else:
            raise TypeError("names must be a dictionary")

# Example usage
model = CustomYOLO("runs/detect/train4/weights/best.pt")  # Load a YOLO model
model.names = {
    0: "Disc_space_narrowing",
    1: "Foraminal_stenosis",
    2: "Osteophytes",
    3: "Other_lesions",
    4: "Spondylolysthesis",
    5: "Surgical_implant",
    6: "Vertebral_collapse"
}
results = model.predict(source = '../datasets/test_png', show=False, save=True)