from ultralytics import YOLO
import os
import cv2
# Load a model
model = YOLO('/home/donny/pothole_project/runs/detect/yolov8n_custom3/weights/best.pt')  # pretrained YOLOv8n model

# Define the directory containing images
image_dir = '/home/donny/pothole_project/pothole_dataset_v8/img_test'

# Get a list of image file names in the directory
image_files = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('.jpg', '.png', '.jpeg'))]

# Run inference on each image in the directory
results = model(image_files)  # Perform detection on all images in the list

# Process the results as needed
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
# for image_path, result in zip(image_files, results):
#     # Load the original image
#     image = cv2.imread(image_path)
    
#     # Get the bounding box coordinates from result.boxes
#     boxes = result.boxes.xyxy
    
#     # Draw bounding boxes on the image
#     for box in boxes:
#         x_min, y_min, x_max, y_max = map(int, box)
#         cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Draw a green rectangle
    
#     # Show the image
#     cv2.imshow('Image with Detection', image)
    
#     # Wait for a key press and close the window when a key is pressed
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()