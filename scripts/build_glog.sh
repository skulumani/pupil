#!/bin/bash

# download and build glog from source
GLOG_VERSION=0.3.5

TEMP_DIR="$(mktemp -d)"
INSTALL_DIR="/usr/local/"

GFLAGS_VERSION="2.2.1"
GFLAGS_URL="https://github.com/gflags/gflags/archive/v${GFLAGS_VERSION}.tar.gz"

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

echo "This will download and build Glog from source"
read -p "Press Enter to continue"

if [ -d "${TEMP_DIR}/glog" ]; then
    echo "Glog source already exists"
    cd "${TEMP_DIR}/glog"
    git checkout master
else
    mkdir -p "${TEMP_DIR}/glog"
    cd "${TEMP_DIR}/glog"
    git clone https://github.com/google/glog.git .
    git checkout master
fi

read -p "Download and install gflags"
cd ${TEMP_DIR}
mkdir gflags
wget ${GFLAGS_URL} -O ${TEMP_DIR}/gflags.tar.gz
tar -xzvf gflags.tar.gz -C ./gflags --strip-components=1
cd gflags
mkdir build && cd build
cmake \
    -D BUILD_SHARED_LIBS=ON \
    -D INSTALL_HEADERS=ON \
    ..
make
sudo checkinstall make install

read -p "Press Enter to build and install glog"

cd "${TEMP_DIR}/glog"
./autogen.sh
./configure
make
sudo checkinstall make install

