from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import os
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server
from loguru import logger
from time import time
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# Load the YOLO model
model = YOLO('/home/donny/pothole_project/best.pt')

# Define the directory containing images
image_dir = ''

# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")

# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "pothole-detection-service"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("pothole-detection", "1.0.0")

# Create your first counter
counter = meter.create_counter(
    name="Service_request_counter", description="Number of service requests"
)

histogram = meter.create_histogram(
    name="Service_response_histogram",
    description="Service response histogram",
    unit="seconds",
)


#check health
@app.get("/")
def check_health():
    return {"status":"ok"}
# Create an endpoint for image prediction    
@app.post("/img_object_detection_to_img")
def img_object_detection_to_img(file: bytes = File(...)):
    """
    Object Detection from an image plot bbox on image

    Args:
        file (bytes): The image file in bytes format.
    Returns:
        Image: Image in bytes with bbox annotations.
    """
    starting_time = time()
    # get image from bytes
    input_image = get_image_from_bytes(file)

    # model predict
    predict = detect_sample_model(input_image)

    # add bbox on image
    final_image = add_bboxs_on_img(image = input_image, predict = predict)

    # return image in bytes format
    return StreamingResponse(content=get_bytes_from_image(final_image), media_type="image/jpeg")
    # Count the number of requests
    label = {"api": "/predict"}

     # Increase the counter
    counter.add(1, label)

    # Mark the end of the response
    ending_time = time()
   
    elapsed_time = ending_time - starting_time
    
    # Add histogram
    logger.info("elapsed time: ", elapsed_time)
    logger.info(elapsed_time)
    histogram.record(elapsed_time, label)

    return results_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
