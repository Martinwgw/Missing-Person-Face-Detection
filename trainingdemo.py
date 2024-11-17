import cv2
import numpy as np
from PIL import Image
import os

# Initialize the recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Path to the dataset and log file
dataset_path = "datasets"
log_file = "processed_files.log"

# Supported image formats
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png")

def get_unprocessed_files(path, log_file):
    """Get the list of unprocessed image files."""
    if not os.path.exists(log_file):
        open(log_file, 'w').close()  # Create an empty log file if it doesn't exist

    with open(log_file, 'r') as file:
        processed_files = file.read().splitlines()  # Read all processed file names

    all_files = [
        os.path.join(path, f) 
        for f in os.listdir(path) 
        if f.lower().endswith(SUPPORTED_FORMATS)  # Check for supported formats
    ]
    unprocessed_files = [file for file in all_files if file not in processed_files]

    return unprocessed_files

def log_processed_files(files, log_file):
    """Append the processed files to the log."""
    with open(log_file, 'a') as file:
        for file_name in files:
            file.write(file_name + '\n')

def get_image_id(file_paths):
    """Extract faces and IDs from the provided file paths."""
    faces = []
    ids = []
    for image_path in file_paths:
        face_image = Image.open(image_path).convert('L')  # Convert to grayscale
        face_np = np.array(face_image, 'uint8')  # Convert to NumPy array
        id_ = int(os.path.split(image_path)[-1].split(".")[1])  # Extract ID from file name
        faces.append(face_np)
        ids.append(id_)
        cv2.imshow("Training", face_np)
        cv2.waitKey(10)
    return ids, faces

# Fetch unprocessed files
unprocessed_files = get_unprocessed_files(dataset_path, log_file)

if unprocessed_files:
    print(f"Found {len(unprocessed_files)} new files for training.")
    
    # Extract faces and IDs
    IDs, face_data = get_image_id(unprocessed_files)

    # Train the recognizer
    recognizer.train(face_data, np.array(IDs))

    # Save the trained model
    recognizer.write("Trainer.yml")
    print("Training completed and model updated.")

    # Log the processed files
    log_processed_files(unprocessed_files, log_file)
else:
    print("No new files to process.")

cv2.destroyAllWindows()
