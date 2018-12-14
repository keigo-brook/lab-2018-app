kubectl apply -f ./darknet-no-display-deployment.yaml
kubectl apply -f ./yolo-load-balancer-deployment.yaml
kubectl apply -f ./road-detect-listener.yaml
kubectl apply -f ./road-load-balancer-deployment.yaml
kubectl apply -f ./garbage-detect-listener.yaml
kubectl apply -f ./garbage-load-balancer-deployment.yaml
