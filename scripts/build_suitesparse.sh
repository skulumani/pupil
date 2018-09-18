#!/bin/bash

SUITESPARSE_VERSION=5.2.0
TEMP_DIR="$(mktemp -d)"
INSTALL_DIR="/usr/local"

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

cd $TEMP_DIR
mkdir suitesparse
cd suitesparse
git clone https://github.com/jluttine/suitesparse.git .
make config




