import os
import random
import shutil

# Define paths
train_dir = "datasets/train_jpeg"
val_dir = "datasets/val"

# Create val directory if it doesn't exist
os.makedirs(val_dir, exist_ok=True)

# List all files in the train directory
files = [f for f in os.listdir(train_dir) if os.path.isfile(os.path.join(train_dir, f))]

# Determine the number of files to move (20%)
num_to_move = int(len(files) * 0.2)

# Randomly select files to move
files_to_move = random.sample(files, num_to_move)

# Move selected files
for file in files_to_move:
    shutil.move(os.path.join(train_dir, file), os.path.join(val_dir, file))

print(f"Moved {num_to_move} files from {train_dir} to {val_dir}")
