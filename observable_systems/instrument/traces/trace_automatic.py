# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import os
import uvicorn
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "predict-pothole-service"}))
)
tracer = get_tracer_provider().get_tracer("mypredict", "1.0.0")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)

app = FastAPI()

# Load the YOLO model
model = YOLO('/home/donny/pothole_project/best.pt')

# Define the directory containing images
image_dir = ''

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


if __name__ == "__main__":
    FastAPIInstrumentor.instrument_app(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)




