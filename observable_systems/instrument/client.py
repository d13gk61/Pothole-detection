from time import sleep

import requests
from loguru import logger

def predict():
    logger.info("Sending POST requests!")
    
    headers = {
    'accept': 'application/json',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

    files = {
    'files': open('/home/donny/pothole_project/data_crawler/data/images/image_1.jpg', 'rb'),
}

    response = requests.post('http://0.0.0.0:8000/predict/', headers=headers, files=files)


if __name__ == "__main__":
    while True:
        predict()
        sleep(0.5)
