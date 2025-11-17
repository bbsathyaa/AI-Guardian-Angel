from fastapi import FastAPI
from routes import emergency, health


app = FastAPI(title="SOS AI Agent")
app.include_router(health.router, prefix="/health")
app.include_router(emergency.router, prefix="/api")


@app.get("/")
async def root():
return {"service":"sos-ai-agent","status":"ok"}
