#!/bin/bash
docker build -t backend .
docker tag backend frankdesantes/backend:latest
docker push frankdesantes/backend:latest
kubectl delete -f ../../manifests/app/backend.yaml
kubectl apply -f ../../manifests/app/backend.yaml

kubectl get pods
