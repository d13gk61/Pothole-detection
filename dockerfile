# Python 3.8
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container and install dependencies
COPY ./requirements.txt /app
COPY ./best.pt /app/best.pt
COPY ./fastpi/main.py /app  
RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN mkdir /app/images

# Copy all the files from the current directory to the container

# Expose port 8000
EXPOSE 8000

# Start FastAPI when the container runs
CMD ["uvicorn", "main:  ", "--host", "0.0.0.0", "--port", "8000"]
