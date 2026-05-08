#!/usr/bin/env bash
set -euo pipefail

echo "==> Validating dependencies"

for cmd in docker terraform kubectl helm; do
  if ! command -v "$cmd" &> /dev/null; then
    echo "❌ $cmd is not installed. Please install it first."
    exit 1
  fi
done

echo "==> Validating Kubernetes context"

CURRENT_CONTEXT=$(kubectl config current-context)

if [ "$CURRENT_CONTEXT" != "docker-desktop" ]; then
  echo "⚠️  Switching context to docker-desktop"
  kubectl config use-context docker-desktop
fi

echo "==> Checking cluster connectivity"
kubectl get nodes >/dev/null

echo "==> Building Docker image"
docker build -t skybyte/app:latest .

echo "==> Applying Terraform"
pushd terraform >/dev/null
terraform init -input=false
terraform apply -auto-approve -input=false
popd >/dev/null

echo "==> Installing Helm chart"
helm upgrade --install skybyte-app helm/skybyte-app \
  --namespace devops-challenge \
  --create-namespace

echo "==> Verifying deployment"
kubectl rollout status deployment/skybyte-app -n devops-challenge --timeout=60s

echo "==> Setup complete ✅"