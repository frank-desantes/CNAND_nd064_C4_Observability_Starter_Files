#!/bin/bash
docker build -t python-trace .
docker tag python-trace frankdesantes/python-trace:latest
docker push frankdesantes/python-trace:latest
#kubectl delete -f ../../deployment/udaconnect-api.yaml
#kubectl apply -f ../../deployment/udaconnect-api.yaml
#kubectl get pods
