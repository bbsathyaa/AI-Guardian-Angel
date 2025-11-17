from fastapi import APIRouter, HTTPException
"user_id": payload.user_id,
"timestamp": ts,
"location": {"lat": payload.lat, "lng": payload.lng},
"raw_text": payload.text,
"status": "received"
}
db.collection("incidents").document(doc_id).set(doc)


# classify text (if present)
classification = None
if payload.text:
try:
classification = classify_text(payload.text)
except Exception as e:
classification = {"error": str(e)}


# reverse geocode address
addr = reverse_geocode(payload.lat, payload.lng)


# decision logic (very simple)
severity = None
if classification and isinstance(classification, dict):
severity = classification.get("severity")


# compose notification
address = addr.get("address")
message = f"SOS: {classification.get('intent') if classification else 'emergency'} at {address or f'{payload.lat},{payload.lng}'} - user:{payload.user_id}"


sent = None
if payload.contacts:
sent = notify_contacts_sms(payload.contacts, message)


# update doc
db.collection("incidents").document(doc_id).update({
"classification": classification,
"address": address,
"notified_contacts": sent,
"status": "notified"
})


return {"incident_id": doc_id, "classification": classification, "address": address, "notified": sent}


@router.post("/cancel/{incident_id}")
async def cancel_incident(incident_id: str):
db = firestore.Client()
doc_ref = db.collection("incidents").document(incident_id)
if not doc_ref.get().exists:
raise HTTPException(status_code=404, detail="incident not found")
doc_ref.update({"status": "cancelled", "cancelled_at": datetime.utcnow().isoformat() + "Z"})
return {"incident_id": incident_id, "status": "cancelled"}
