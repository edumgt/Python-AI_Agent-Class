#!/usr/bin/env bash
set -euo pipefail

# Build local image and always sync to Docker Hub.
# Usage:
#   ./Agent/scripts/push_dockerhub.sh <tagname>
# Example:
#   ./Agent/scripts/push_dockerhub.sh v1.0.0

IMAGE_REPO="${IMAGE_REPO:-edumgt/ai-class}"
TAG="${1:-}"

if [[ -z "$TAG" ]]; then
  echo "Usage: $0 <tagname>"
  exit 1
fi

if [[ $# -gt 1 ]]; then
  echo "Usage: $0 <tagname>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

echo "[1/3] Building image: ${IMAGE_REPO}:${TAG}"
docker build -f Agent/Dockerfile -t "${IMAGE_REPO}:${TAG}" .

echo "[2/3] Pushing image: ${IMAGE_REPO}:${TAG}"
docker push "${IMAGE_REPO}:${TAG}"

echo "[3/3] Tagging and pushing latest"
docker tag "${IMAGE_REPO}:${TAG}" "${IMAGE_REPO}:latest"
docker push "${IMAGE_REPO}:latest"

echo "Done"
echo "Pushed: ${IMAGE_REPO}:${TAG}"
echo "Pushed: ${IMAGE_REPO}:latest"
