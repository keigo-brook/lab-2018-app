echo '0 start yolo and camara'
kubectl apply -f ./darknet-no-display-deployment.yaml
sleep 3
kubectl apply -f ./yolo-load-balancer-deployment.yaml
sleep 60

echo '60: start garbage'
kubectl apply -f ./garbage-detect-listener.yaml
sleep 3
kubectl apply -f ./garbage-load-balancer-deployment.yaml
sleep 60

echo '120: start road'
kubectl apply -f ./road-detect-listener.yaml
sleep 3
kubectl apply -f ./road-load-balancer-deployment.yaml
sleep 60
echo '180: finish'
kubectl delete -f ./darknet-no-display-deployment.yaml
kubectl delete -f ./yolo-load-balancer-deployment.yaml
kubectl delete -f ./garbage-detect-listener.yaml
kubectl delete -f ./garbage-load-balancer-deployment.yaml
kubectl delete -f ./road-detect-listener.yaml
kubectl delete -f ./road-load-balancer-deployment.yaml
