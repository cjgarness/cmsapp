#!/usr/bin/env bash
set -euo pipefail

# Build and push cmsapp, nginx, and postgres images to AWS ECR.
# Required env:
#   AWS_REGION, AWS_ACCOUNT_ID
#   ECR_REPO_WEB, ECR_REPO_NGINX, ECR_REPO_POSTGRES
# Optional env:
#   IMAGE_TAG (default: prod)
#   AWS_PROFILE

if [[ -f .env ]]; then
  echo "Loading .env"
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
else
  echo "Warning: .env not found; relying on current environment" >&2
fi

IMAGE_TAG=${IMAGE_TAG:-prod}
AWS_PROFILE_OPT=${AWS_PROFILE:+--profile "$AWS_PROFILE"}
echo "AWS_PROFILE_OPT: ${AWS_PROFILE_OPT:-<none>}"
echo "Using configuration:"
echo "  AWS_REGION=$AWS_REGION"
echo "  AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID"
echo "  ECR_REPO_WEB=$ECR_REPO_WEB"
echo "  ECR_REPO_NGINX=$ECR_REPO_NGINX"
echo "  ECR_REPO_POSTGRES=$ECR_REPO_POSTGRES"
echo "  IMAGE_TAG=$IMAGE_TAG"

for v in AWS_REGION AWS_ACCOUNT_ID ECR_REPO_WEB ECR_REPO_NGINX ECR_REPO_POSTGRES; do
  if [[ -z ${!v:-} ]]; then
    echo "Missing required env: $v" >&2
    exit 1
  fi
done

ECR_DOMAIN="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

function ensure_repo() {
  local name="$1"
  if ! aws $AWS_PROFILE_OPT --region "$AWS_REGION" ecr describe-repositories --repository-names "$name" >/dev/null 2>&1; then
    aws $AWS_PROFILE_OPT --region "$AWS_REGION" ecr create-repository --repository-name "$name" >/dev/null
    echo "Created ECR repo: $name"
  fi
}

echo "Ensuring ECR repositories exist..."
ensure_repo "$ECR_REPO_WEB"
ensure_repo "$ECR_REPO_NGINX"
ensure_repo "$ECR_REPO_POSTGRES"

echo "Logging into ECR..."
aws $AWS_PROFILE_OPT --region "$AWS_REGION" ecr get-login-password | docker login --username AWS --password-stdin "$ECR_DOMAIN"

function build_and_push() {
  local repo="$1"; local tag="$2"; local dockerfile="$3"; local context="$4"
  local image="$ECR_DOMAIN/$repo:$tag"
  echo "Building $image using $dockerfile"
  docker build -f "$dockerfile" -t "$image" "$context"
  docker push "$image"
}

build_and_push "$ECR_REPO_WEB" "$IMAGE_TAG" "Dockerfile" .
build_and_push "$ECR_REPO_NGINX" "$IMAGE_TAG" "Dockerfile.nginx" .
build_and_push "$ECR_REPO_POSTGRES" "$IMAGE_TAG" "Dockerfile.postgres" .

echo "All images pushed with tag: $IMAGE_TAG"
