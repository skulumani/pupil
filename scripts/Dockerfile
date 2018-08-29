# ubuntu paranet
FROM ubuntu:18.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# pre-install apt setup
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git software-properties-common

# apt dependencies
RUN apt-get install -y pkg-config cmake build-essential nasm libglew-dev \
    libglfw3-dev libtbb-dev libusb-1.0-0-dev \
	libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev \
	libavresample-dev ffmpeg x264 x265 libportaudio2 portaudio19-dev

# setup anaconda python and enviornment
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p ~/anaconda3 && \
    rm ~/miniconda.sh && \
    ~/anaconda3/bin/conda clean -tipsy && \
    ln -s ~/anaconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". ~/anaconda3/etc/profile.d/conda.sh" >> ~/.bashrc
    # echo "conda activate base" >> ~/.bashrc

# install python environment
ADD eyetracking.yml /tmp/eyetracking.yml
RUN conda env create -f /tmp/eyetracking.yml

# build opencv from source
ADD build_opencv.sh /tmp/build_opencv.sh
RUN /bin/bash /tmp/build_opencv.sh

# build eigen from source

ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

