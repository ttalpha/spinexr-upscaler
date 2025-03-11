import cv2
import pandas as pd
import matplotlib.pyplot as plt

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
    image_path = f"datasets/test_jpeg/{image_id}.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image {image_path} not found.")
        return

    # Convert image to RGB (OpenCV loads images in BGR format)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Plot image
    plt.figure(figsize=(10, 10))
    plt.imshow(image)

    # Plot bounding boxes
    for _, row in image_df.iterrows():
        xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        plt.gca().add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                          edgecolor='red', linewidth=2, fill=False))
        plt.text(xmin, ymin - 5, row['lesion_type'], color='red', fontsize=12, weight='bold')

    plt.axis('off')
    plt.show()

# Example usage
image_id = '08414859451eaae51432ba37ca34ae3f'  # Replace with actual ID
plot_bounding_boxes(image_id)
