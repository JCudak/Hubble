#!/bin/bash

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

minikube start --force

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

# Add Helm repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add cowboysysop https://cowboysysop.github.io/charts/
helm repo update # pull the data from newly added repositories

helm install mongo bitnami/mongodb -f helm/mongo_values.yaml
helm install mongo-express cowboysysop/mongo-express -f helm/mongo_express_values.yaml

# Build and push Docker images
# cd ../services/service1
# docker build -t zpaks/service1:latest .
# docker push zpaks/service1:latest
# cd ../service2
# docker build -t zpaks/service2:latest .
# docker push zpaks/service2:latest
# cd ../service3
# docker build -t zpaks/service3:latest .
# docker push zpaks/service3:latest

cd helm

./kubectl apply -f ../deployments/service1-deployment.yaml
./kubectl apply -f ../deployments/service2-deployment.yaml
./kubectl apply -f ../deployments/service3-deployment.yaml

./kubectl rollout restart deployment/service1
./kubectl rollout restart deployment/service2
./kubectl rollout restart deployment/service3
