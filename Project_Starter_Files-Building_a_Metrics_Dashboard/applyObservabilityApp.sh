#!/bin/bash
kubectl apply -f ./manifests/app/frontend.yaml
kubectl apply -f ./manifests/app/backend.yaml
kubectl apply -f ./manifests/app/trial.yaml