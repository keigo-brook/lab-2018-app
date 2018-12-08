FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

# 自動アップグレード
ENV DEBIAN_FRONTEND "noninteractive"
RUN apt-get update -y
RUN apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" dist-upgrade

RUN apt-get install -y --no-install-recommends libopencv-dev build-essential cmake git libgtk2.0-dev pkg-config python-dev python-numpy libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff5-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libxine2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev libtbb-dev libqt4-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils unzip vim sudo python-pip

# キャッシュを消してイメージを小さくする
RUN apt-get clean -y
RUN apt-get autoremove -y
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get autoremove -y
RUN apt-get autoclean -y
RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# ユーザ設定
# ユーザ ID をパラメータにすることでホストボリュームに対する操作をユーザ権限で実行するようにしている。
# `--userns-remap` の設定が面倒なときに使う。
ARG user_name=ubuntu
ARG user_id=1942
ARG group_name=ubuntu
ARG group_id=1942

RUN groupadd -g ${group_id} ${group_name}
RUN useradd -u ${user_id} -g ${group_id} -d /home/${user_name} --create-home --shell /usr/bin/zsh ${user_name}
RUN echo "${user_name} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R ${user_name}:${group_name} /home/${user_name}

# ubuntu ユーザの設定
USER ubuntu
WORKDIR /home/ubuntu
ENV HOME /home/ubuntu

WORKDIR $HOME/

RUN mkdir ./darknet-no-display
COPY --chown=ubuntu:ubuntu ./ ./darknet-no-display/
RUN pip install kafka

## opencv_contrib
#RUN git clone https://github.com/opencv/opencv_contrib.git
#WORKDIR $HOME/opencv_contrib
#RUN git checkout 3.3.1 refs/tags/3.3.1
#
## opencv
#WORKDIR $HOME/
#RUN git clone https://github.com/opencv/opencv.git
#WORKDIR $HOME/opencv
#RUN git checkout 3.3.1 refs/tags/3.3.1
#RUN mkdir build
#
#RUN cd $HOME/opencv/build && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D WITH_CUDA=ON .. && make -j${num_proc} && sudo make install
#RUN sudo ldconfig
#
## darknet
#RUN git clone https://github.com/pjreddie/darknet
#WORKDIR $HOME/darknet/
#RUN sed -ie "s/GPU=0/GPU=1/" ./Makefile
#RUN sed -ie "s/OPENCV=0/OPENCV=1/" ./Makefile
#RUN sed -ie "s/CUDNN=0/CUDNN=1/" ./Makefile
#RUN sed -ie "s/OPENMP=0/OPENMP=1/" ./Makefile
#RUN make -j${num_proc}

# openpose
#WORKDIR $HOME/
#RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
#WORKDIR $HOME/openpose
#RUN sudo bash ./ubuntu/install_cmake.sh
#RUN mkdir ./build && cd ./build/ && cmake .. && make -j${num_proc} && sudo make install


