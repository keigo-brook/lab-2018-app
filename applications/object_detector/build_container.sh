cp ../lab_2018_app/env.sh .
cp ../lab_2018_app/applications/object_detector/Dockerfile .
docker build -t localhost:5000/k_ogawa/darknet_listener:v1 .
