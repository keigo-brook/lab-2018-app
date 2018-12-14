echo '0 start yolo and camara'
kubectl apply -f ./darknet-no-display-deployment-7.yaml
kubectl apply -f ./yolo-load-balancer-deployment.yaml
sleep 10

echo '60: start garbage'
kubectl delete -f ./darknet-no-display-deployment-7.yaml
kubectl apply -f ./darknet-no-display-deployment-6.yaml
sleep 2
kubectl delete -f ./yolo-load-balancer-deployment.yaml
kubectl apply -f ./yolo-load-balancer-deployment.yaml

kubectl apply -f ./garbage-detect-listener.yaml
kubectl apply -f ./garbage-load-balancer-deployment.yaml
sleep 10

echo '120: delete garbage, start road'
kubectl delete -f ./darknet-no-display-deployment-6.yaml
kubectl apply -f ./darknet-no-display-deployment-5.yaml
sleep 2
kubectl delete -f ./yolo-load-balancer-deployment.yaml
kubectl apply -f ./yolo-load-balancer-deployment.yaml

kubectl delete -f ./garbage-detect-listener.yaml
kubectl delete -f ./garbage-load-balancer-deployment.yaml
kubectl apply -f ./road-detect-listener.yaml
kubectl apply -f ./road-load-balancer-deployment.yaml
sleep 10

echo '180: start garbage'
kubectl delete -f ./darknet-no-display-deployment-5.yaml
kubectl apply -f ./darknet-no-display-deployment-4.yaml
sleep 2
kubectl delete -f ./yolo-load-balancer-deployment.yaml
kubectl apply -f ./yolo-load-balancer-deployment.yaml

kubectl apply -f ./garbage-detect-listener.yaml
kubectl apply -f ./garbage-load-balancer-deployment.yaml
sleep 10

echo '240: delete garbage, delete road'
kubectl delete -f ./garbage-detect-listener.yaml
kubectl delete -f ./garbage-load-balancer-deployment.yaml
kubectl delete -f ./road-detect-listener.yaml
kubectl delete -f ./road-load-balancer-deployment.yaml

kubectl delete -f ./darknet-no-display-deployment-4.yaml
kubectl apply -f ./darknet-no-display-deployment-7.yaml
sleep 2
kubectl delete -f ./yolo-load-balancer-deployment.yaml
kubectl apply -f ./yolo-load-balancer-deployment.yaml
sleep 10
echo '300: finish'
