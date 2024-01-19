## Added nvidia cuda support
FROM nvidia/cuda:11.4.2-devel-ubuntu18.04
FROM python:3.10.4
# Install some basic utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    libopencv-dev \
    python3-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# Install necessary python packages you need
RUN python -m pip install --upgrade pip

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "python3 webcamtransformation.py && python3 yolo_transformed.py"]