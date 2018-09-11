#!/bin/bash -e

# TEMP_DIR="$(mktemp -d)"
TEMP_DIR="/tmp/pupil_dep"
WORK_DIR="$(pwd)"

read -p "Press Enter to Install APT"
echo "Installing APT packages"
sudo apt-get install -y pkg-config git cmake build-essential nasm wget libusb-1.0-0-dev libglew-dev libglfw3-dev libtbb-dev libboost-dev libgoogle-glog-dev libatlas-base-dev 

read - p "Press Enter to Install TurboJPEG"
echo "Install TurboJPEG"
cd $TEMP_DIR
wget -O $TEMP_DIR/libjpeg-turbo.tar.gz https://sourceforge.net/projects/libjpeg-turbo/files/1.5.1/libjpeg-turbo-1.5.1.tar.gz/download
mkdir -p $TEMP_DIR/libjpeg
tar -xvzf libjpeg-turbo.tar.gz -C $TEMP_DIR/libjpeg --strip-components=1
cd $TEMP_DIR/libjpeg
./configure --enable-static=no --prefix=/usr/local
sudo checkinstall
sudo ldconfig

read -p "Press Enter to Install LibUVC"
echo "Install LibUVC"
cd $TEMP_DIR
git clone https://github.com/pupil-labs/libuvc
cd libuvc
mkdir build
cd build
cmake ..
make && sudo checkinstall
sudo ldconfig

echo 'SUBSYSTEM=="usb",  ENV{DEVTYPE}=="usb_device", GROUP="plugdev", MODE="0664"' | sudo tee /etc/udev/rules.d/10-libuvc.rules > /dev/null
sudo udevadm trigger

echo "Activate the Eyetracking enviornment"
read -p "Press Enter to continue"
cd $WORK_DIR
conda env update -f ./scripts/eyetracking.yml -n eyetracking

# setup opencv at the end
