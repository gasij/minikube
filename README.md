# Kubernetes / Minikube example

This project contains example manifests and a helper script to deploy a simple application to a local Minikube cluster.

## Structure

- `k8s/deployment-v1.yaml` – Deployment for version v1 (10 replicas, CPU/memory requests/limits).
- `k8s/service-v1.yaml` – Service exposing v1 Deployment (NodePort).
- `k8s/deployment-v2.yaml` – Deployment for version v2 (blue/green).
- `k8s/service-v2.yaml` – Service exposing v2 Deployment (for testing green).
- `k8s/myapp-service.yaml` – Common Service used for blue/green switch (initially points to v1).
- `scripts/minikube-deploy.sh` – Helper script for Minikube operations.

## Requirements

- macOS
- Homebrew
- Docker (for Minikube Docker driver)
- `kubectl`
- `minikube`

## Quick start

```bash
cd "$(dirname "$0")"

# 0. Install Minikube (once, via Homebrew)
brew install minikube

# 1. Start Minikube cluster (Docker driver)
minikube start --driver=docker

# 2. Check cluster and nodes
kubectl get nodes
kubectl get pods -A

# 3. Deploy application v1 (Deployment + Service + common Service)
./scripts/minikube-deploy.sh deploy-v1

# 4. Check v1 resources
kubectl get deployment myapp-v1
kubectl get pods -l app=myapp,version=v1
kubectl get service myapp-v1-service
kubectl get service myapp-service

# 5. Open v1 in browser (NodePort service)
minikube service myapp-v1-service --url

# 6. Deploy application v2 (green version)
./scripts/minikube-deploy.sh deploy-v2

# 7. Check v2 resources
kubectl get deployment myapp-v2
kubectl get pods -l app=myapp,version=v2
kubectl get service myapp-v2-service

# 8. Open v2 in browser (test green)
minikube service myapp-v2-service --url

# 9. Switch traffic from v1 (blue) to v2 (green) in common Service
./scripts/minikube-deploy.sh switch

# 10. Open common Service (now pointing to v2)
minikube service myapp-service --url

# 11. Open Minikube dashboard
./scripts/minikube-deploy.sh dashboard

# 12. (Optional) Clean up old blue version
kubectl delete deployment myapp-v1
kubectl delete service myapp-v1-service
```

