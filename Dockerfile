# Use latest ARM64 base image of Ubuntu
FROM arm64v8/ubuntu:latest

# Metadata
LABEL maintainer="simonboeckner@gmail.com"
LABEL description="OpenCV and GStreamer Docker image for Raspberry Pi 4B"

# Avoid timezone prompt and update packages
RUN apt-get update && apt-get install -y \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    git \
    libglib2.0-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCV using pip
RUN pip install opencv-python \
    opencv-contrib-python

# Copy code from working directory unless specified to pull from the github repository
ARG USE_GIT=false
ARG REPO=https://github.com/the-project-type-shi

RUN if [ "$USE_GIT" = "true" ]; then \
        git clone --branch main $REPO /app; \
    fi

COPY . /app

# Default command
CMD ["python3", "main.py"]