#!/usr/bin/env bash
set -euo pipefail

# Simple helper script to:
# 1) Start Minikube
# 2) Deploy v1 Deployment + Service
# 3) Show info about Deployment and Service
# 4) Optionally deploy v2 and switch traffic (blue/green)

APP_NAME="myapp"
NAMESPACE="default"

start_minikube() {
  echo "Starting Minikube (if not already running)..."
  minikube start --driver=docker
}

deploy_v1() {
  echo "Applying Deployment v1..."
  kubectl apply -f k8s/deployment-v1.yaml

  echo "Applying Service v1..."
  kubectl apply -f k8s/service-v1.yaml

  echo "Applying common Service (myapp-service, points to v1)..."
  kubectl apply -f k8s/myapp-service.yaml

  echo
  echo "Deployment info:"
  kubectl get deployment "${APP_NAME}-v1" -n "${NAMESPACE}"
  kubectl get pods -l app="${APP_NAME}",version=v1 -n "${NAMESPACE}"

  echo
  echo "Service info:"
  kubectl get service "${APP_NAME}-v1-service" -n "${NAMESPACE}" || true
  kubectl get service "${APP_NAME}-service" -n "${NAMESPACE}"
}

deploy_v2() {
  echo "Applying Deployment v2..."
  kubectl apply -f k8s/deployment-v2.yaml

  echo "Applying Service v2 (for testing)..."
  kubectl apply -f k8s/service-v2.yaml

  echo
  echo "Deployment v2 info:"
  kubectl get deployment "${APP_NAME}-v2" -n "${NAMESPACE}"
  kubectl get pods -l app="${APP_NAME}",version=v2 -n "${NAMESPACE}"

  echo
  echo "Service v2 info:"
  kubectl get service "${APP_NAME}-v2-service" -n "${NAMESPACE}"
}

switch_blue_to_green() {
  echo "Patching myapp-service selector to point to version v2 (blue -> green)..."
  kubectl patch service "${APP_NAME}-service" -n "${NAMESPACE}" -p '{
    "spec": {
      "selector": {
        "app": "'"${APP_NAME}"'",
        "version": "v2"
      }
    }
  }'

  echo
  echo "Endpoints for myapp-service after switch:"
  kubectl get endpoints "${APP_NAME}-service" -n "${NAMESPACE}"
}

open_dashboard() {
  echo "Opening Minikube dashboard..."
  minikube dashboard --url
}

usage() {
  cat <<EOF
Usage: $0 [command]

Commands:
  start           Start Minikube cluster
  deploy-v1       Deploy version v1 (Deployment + Services) and show info
  deploy-v2       Deploy version v2 (Deployment + Service) and show info
  switch          Switch traffic in myapp-service from v1 to v2 (blue/green)
  dashboard       Open Minikube dashboard URL

Examples:
  $0 start
  $0 deploy-v1
  $0 deploy-v2
  $0 switch
  $0 dashboard
EOF
}

cmd="${1:-}"
case "${cmd}" in
  start)
    start_minikube
    ;;
  deploy-v1)
    deploy_v1
    ;;
  deploy-v2)
    deploy_v2
    ;;
  switch)
    switch_blue_to_green
    ;;
  dashboard)
    open_dashboard
    ;;
  *)
    usage
    ;;
esac

