#!/bin/bash
docker build -t trial .
docker tag trial frankdesantes/trial:latest
docker push frankdesantes/trial:latest
kubectl delete -f ../../manifests/app/trial.yaml
kubectl apply -f ../../manifests/app/trial.yaml

kubectl get pods
