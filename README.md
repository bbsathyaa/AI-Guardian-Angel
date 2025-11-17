# SOS AI — Emergency Alert Agent


This project implements a FastAPI backend that accepts emergency triggers (text + location), classifies intent & severity with Vertex AI, finds nearest services using Google Maps (client code provided), notifies emergency contacts (Twilio/FCM hooks), and logs incidents to Firestore.


## Quick start (manual)


1. Create a GCP project and enable APIs: Cloud Run, Firestore, Secret Manager, Vertex AI, Cloud Build, IAM, Maps.
2. Create Firestore (Native mode) and a Service Account with the roles described in infra/terraform.
3. Store credentials and API_KEYS in Secret Manager (see config.py).
4. Build & push Docker image, then deploy to Cloud Run: `scripts/deploy.sh`.


For automation, use the `.github/workflows/ci-cd.yml` GitHub Action or the Terraform in `infra/terraform`.
