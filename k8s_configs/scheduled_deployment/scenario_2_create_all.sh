echo '0 start yolo and camara'
kubectl apply -f ./darknet-no-display-deployment-4.yaml
sleep 3
kubectl apply -f ./yolo-load-balancer-deployment.yaml

echo '60: start garbage'
kubectl apply -f ./garbage-detect-listener-1.yaml
sleep 3
kubectl apply -f ./garbage-load-balancer-deployment.yaml

echo '120: start road'
kubectl apply -f ./road-detect-listener-2.yaml
sleep 3
kubectl apply -f ./road-load-balancer-deployment.yaml
echo '180: finish'
