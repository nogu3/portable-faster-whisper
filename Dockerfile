FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN useradd -m -s /bin/bash zen
USER zen
WORKDIR /home/zen

RUN pip install faster-whisper
