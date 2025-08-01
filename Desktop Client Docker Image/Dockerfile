# Use the latest AMD64 base image of Ubuntu
FROM amd64/ubuntu:latest

# Metadata
LABEL maintainer="simon.boeckner@mail.utoronto.ca"
LABEL description="OpenCV, GStreamer and PyQt5 Docker image for AMD64 Ubuntu"

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
    build-essential \
    cmake \
    git \
    pkg-config \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    python3-numpy \
    python3-opencv \
    python3-pyqt5 \
    python3-gi \
    gir1.2-gst-plugins-base-1.0 \
    gir1.2-gstreamer-1.0 \
    libglib2.0-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy code from working directory unless specified to pull from the github repository
ARG USE_GIT=false
ARG REPO=https://github.com/the-project-type-shi

RUN if [ "$USE_GIT" = "true" ]; then \
        git clone --branch main $REPO /app; \
    fi

COPY . /app

#Default command
CMD ["python3", "main.py"]