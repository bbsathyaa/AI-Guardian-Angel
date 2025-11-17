import os
from google.cloud import secretmanager


# Configuration loader that prefers environment variables, falls back to Secret Manager


def get_secret(name: str) -> str | None:
# try env first
v = os.getenv(name)
if v:
return v
# try secret manager (only works if running on GCP with permissions)
try:
client = secretmanager.SecretManagerServiceClient()
project = os.getenv("GCP_PROJECT")
if not project:
return None
name_full = f"projects/{project}/secrets/{name}/versions/latest"
response = client.access_secret_version(request={"name": name_full})
return response.payload.data.decode("UTF-8")
except Exception:
return None


# Keys / config names (set these in Secret Manager or ENV)
VERTEX_PROJECT = os.getenv("VERTEX_PROJECT")
GCP_PROJECT = os.getenv("GCP_PROJECT")
MAPS_API_KEY = get_secret("MAPS_API_KEY")
TWILIO_SID = get_secret("TWILIO_SID")
TWILIO_TOKEN = get_secret("TWILIO_TOKEN")
TWILIO_FROM = get_secret("TWILIO_FROM")
FIREBASE_CREDENTIALS = get_secret("FIREBASE_CREDENTIALS_JSON")
VERTEX_MODEL = os.getenv("VERTEX_MODEL") # e.g. projects/.../locations/.../models/...
