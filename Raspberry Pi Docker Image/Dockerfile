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
    libglib2.0-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Build OpenCV from source with GStreamer compatabilitiy on
RUN mkdir ~/opencv_build && cd ~/opencv_build
RUN git clone --branch 4.x https://github.com/opencv/opencv.git
RUN git clone --branch 4.x https://github.com/opencv/opencv_contrib.git

RUN cd ~/opencv_build/opencv
RUN mkdir build && cd build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D WITH_GSTREAMER=ON \
    -D WITH_V4L=ON \
    -D WITH_QT=OFF \
    -D WITH_OPENGL=ON \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_opencv_python3=ON \
    -D PYTHON_EXECUTABLE=$(which python3) ..

RUN make -j$(nproc)
RUN make install
RUN ldconfig

# Copy code from working directory unless specified to pull from the github repository
ARG USE_GIT=false
ARG REPO=https://github.com/the-project-type-shi

RUN if [ "$USE_GIT" = "true" ]; then \
        git clone --branch main $REPO /app; \
    fi

COPY . /app

# Default command
CMD ["python3", "main.py"]