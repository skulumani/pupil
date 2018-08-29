#!/bin/bash

# this will download and build opencv and install it into a Python environment
# Make sure you create the asteroid conda enviornment first before running this script

OPENCV_VERSION=3.4.2
TEMP_DIR="$(mktemp -d)"
INSTALL_DIR="/usr/local/"

# check if the temp dir was created
if [[ ! "$TEMP_DIR" || ! -d "$TEMP_DIR" ]]; then
    echo "Could not create temp dir"
    exit 1
fi

# delete the temp directory on cleanup
function cleanup {
    rm -rf "$TEMP_DIR"
    echo "Deleted temp working directory $TEMP_DIR"
}

trap cleanup EXIT

echo "This will download and build OpenCV"
read -p "Press ENTER to continue"

if [ -d "${TEMP_DIR}/opencv" ]; then
    echo "OpenCV source already exists"
    cd "${TEMP_DIR}/opencv"
    git checkout $OPENCV_VERSION
else
    mkdir -p "${TEMP_DIR}/opencv"
    cd "${TEMP_DIR}/opencv"
    git clone https://github.com/opencv/opencv.git .
    git checkout $OPENCV_VERSION
fi

if [ -d "${TEMP_DIR}/opencv_contrib" ]; then
    echo "OpenCV Contrib source already exists"
    cd "${TEMP_DIR}/opencv_contrib"
    git checkout $OPENCV_VERSION
else
    mkdir -p "${TEMP_DIR}/opencv_contrib"
    cd "${TEMP_DIR}/opencv_contrib"
    git clone https://github.com/opencv/opencv_contrib.git .
    git checkout $OPENCV_VERSION
fi

# update build requirements
sudo apt-get -y update
sudo apt-get -y upgrade

sudo apt-get -y install \
    build-essential \
    cmake \
    pkg-config \
    libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev \
    python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev  libdc1394-22-dev

# sudo apt-get -y install  libjasper-dev

# now build opencv
cd "${TEMP_DIR}/opencv"
mkdir build
cd build

read -p "Press enter to continue"

# call cmake
cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
    -D OPENCV_EXTRA_MODULES_PATH=$TEMP_DIR/opencv_contrib/modules \
    -D PYTHON_EXECUTABLE=$HOME/anaconda3/envs/eyetracking/bin/python \
    -D PYTHON3_EXECUTABLE=$HOME/anaconda3/envs/eyetracking/bin/python \
    ..

echo "Make sure Python paths are correct"
read -p "Press Enter to continue make install"

make -j4
sudo make install
# sudo checkinstall install

echo "Now symlinking OpenCV to anaconda path"
read -p "Press Enter to continue"
ln -s /usr/local/lib/python3.7/site-packages/cv2.cpython-37m-x86_64-linux-gnu.so $HOME/anaconda3/envs/eyetracking/lib/python3.7/site-packages/cv2.so
