FROM nvidia/cuda:12.9.1-cudnn-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN useradd -m -s /bin/bash zen
USER zen
WORKDIR /home/zen

COPY requirements.txt .
RUN pip install -r requirements.txt
