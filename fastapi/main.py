from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import os
# Initialize the FastAPI app
app = FastAPI()

# Load the YOLO model
model = YOLO('./best.pt')

# Define the directory containing images
# image_dir = '/home/donny/pothole_project/pothole_dataset_v8/train/images'

# Create an endpoint for image prediction
@app.post("/predict/")
async def predict_images(files: List[UploadFile]):
    results_list = []

    for file in files:
        # Save the uploaded image temporarily
        file_path = os.path.join(image_dir, file.filename)
        with open(file_path, "wb") as image_file:
            image_file.write(file.file.read())

        # Perform inference on the uploaded image
        results = model(file_path)
        
        # Initialize a list to store bounding boxes for each image
        image_boxes = []
        results_list.append(image_boxes)

        # Remove the temporary image file
        os.remove(file_path)

    return results_list
