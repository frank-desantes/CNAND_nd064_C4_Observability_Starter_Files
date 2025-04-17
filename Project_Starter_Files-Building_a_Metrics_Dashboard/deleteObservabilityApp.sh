#!/bin/bash
kubectl delete -f ./manifests/app/frontend.yaml
kubectl delete -f ./manifests/app/backend.yaml
kubectl delete -f ./manifests/app/trial.yaml
