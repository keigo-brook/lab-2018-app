cp ../lab_2018_app/env.sh .
cp ../lab_2018_app/applications/garbage_detector/Dockerfile .
docker build -t localhost:5000/k_ogawa/garbage-detect-listener:v1 .
