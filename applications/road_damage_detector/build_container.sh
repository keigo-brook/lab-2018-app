cp ../lab_2018_app/env.sh .
cp ../lab_2018_app/applications/road_damage_detector/Dockerfile .
docker build -t localhost:5000/k_ogawa/road-damage-listener:v1 .
