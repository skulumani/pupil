#!/bin/bash

CERES_VERSION="1.14.0"
CERES_URL="http://ceres-solver.org/ceres-solver-${CERES_VERSION}.tar.gz"
TEMP_DIR="$(mktemp -d)"

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

# build and install Ceres optimization solver

# Eigen, Cmake, glog, gflags, SuiteSparse, CXSparse, ATLAS (For BLAS AND LAPACK), TBB
echo "Get Ceres dependencies"
read -p "Press ENTER to install apt deps"
sudo apt-get install -y  libatlas-base-dev libtbb-dev  checkinstall
# sudo apt-get install -y libgoogle-glog-dev libsuitesparse-dev

# - However, if you want to build Ceres as a *shared* library, you must
# #   add the following PPA:
# sudo add-apt-repository ppa:bzindovic/suitesparse-bugfix-1319687
# sudo apt-get update
# sudo apt-get install libsuitesparse-dev

echo "Now going to download and build Ceres from source"
read -p "Press Enter to continue"
cd ${TEMP_DIR}
mkdir ceres
wget ${CERES_URL} -O ${TEMP_DIR}/${CERES_VER}.tar.gz
tar -xvzf ${CERES_VER}.tar.gz -C ./ceres --strip-components=1
cd ceres
mkdir build
cd build
cmake ..
make -j4
make test

read -p "Press Enter to install"
sudo checkinstall

