FROM bvlc/caffe:gpu
RUN apt update && apt install -y vim-nox python-tk

COPY . /app
WORKDIR /app
RUN pip install pillow opencv-python numpy kafka
