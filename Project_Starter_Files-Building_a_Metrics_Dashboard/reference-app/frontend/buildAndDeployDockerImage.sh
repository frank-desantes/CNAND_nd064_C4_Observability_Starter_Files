#!/bin/bash
docker build -t frontend .
docker tag frontend frankdesantes/frontend:latest
docker push frankdesantes/frontend:latest
kubectl delete -f ../../manifests/app/frontend.yaml
kubectl apply -f ../../manifests/app/frontend.yaml

kubectl get pods
