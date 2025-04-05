from math import isnan
import os
import cv2
import pandas as pd

GENERATED_DIR = 'results/ftx4_v3'
GT_DIR = 'datasets/test_png'

def plot_bounding_boxes(image_id):
  # Load bounding box data
  csv_path = 'datasets/annotations/test.csv'
  df = pd.read_csv(csv_path)

  # Filter rows for the given image_id
  image_df = df[df['image_id'] == image_id]

  if image_df.empty:
    print(f"No bounding boxes found for {image_id}.jpg")
    return

  # Load image
  image_path = f"{GENERATED_DIR}/{image_id}_out.png"
  image = cv2.imread(image_path)
  if image is None:
    print(f"Image {image_path} not found.")
    return

  # Convert image to RGB (OpenCV loads images in BGR format)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  # Define colors for different lesion types
  colors = {
      'Disc_space_narrowing': (0, 0, 255),
      'Foraminal_stenosis': (255, 0, 0),
      'Osteophytes': (0, 255, 0),
      'Spondylolysthesis': (255, 0, 255),
      'Surgical_implant': (0, 165, 255),
      'Vertebral_collapse': (255, 192, 203),
      'Other_lesions': (0, 255, 255),
  }

  # Draw bounding boxes on the image
  for _, row in image_df.iterrows():
    xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']

    if isnan(xmin):
      continue
    xmin, ymin, xmax, ymax = int(row['xmin']), int(
      row['ymin']), int(row['xmax']), int(row['ymax'])
    lesion_type = row['lesion_type']
    # Default to red if type not found
    color = colors.get(lesion_type, (255, 0, 0))
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=color, thickness=2)
    cv2.putText(image, lesion_type, (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)

  # Save the image with bounding boxes to the plots/ directory
  output_dir = 'plots'
  os.makedirs(output_dir, exist_ok=True)
  output_path = os.path.join(output_dir, f"{image_id}_bbox.jpg")
  cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))


# Example usage
image_file_paths = [os.path.join(GENERATED_DIR, f.split('.')[0])
                    for f in os.listdir(GENERATED_DIR)]
for image_file_path in image_file_paths:
  image_id = image_file_path.split('/')[-1].split('_')[0]
  print(image_id)
  plot_bounding_boxes(image_id)
