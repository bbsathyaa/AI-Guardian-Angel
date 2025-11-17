#!/usr/bin/env bash
set -euo pipefail


PROJECT=${GCP_PROJECT:-"your-gcp-project"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME=${SERVICE_NAME:-"sos-ai-agent"}
IMAGE_NAME=gcr.io/${PROJECT}/${SERVICE_NAME}:latest


# build
docker build -t ${IMAGE_NAME} .
# push (requires docker authenticated to gcloud)
docker push ${IMAGE_NAME}


# deploy to Cloud Run
gcloud run deploy ${SERVICE_NAME} \
--image ${IMAGE_NAME} \
--region ${REGION}
