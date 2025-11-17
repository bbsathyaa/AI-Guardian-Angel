# Sample Vertex AI classification helper using google-cloud-aiplatform
confidence must be a number between 0 and 1.


Examples:
"I slipped and my leg is broken" => {"intent":"medical","severity":"high","confidence":0.95}
"There's a fight on the street" => {"intent":"crime","severity":"high","confidence":0.9}
"I see smoke from a building" => {"intent":"fire","severity":"high","confidence":0.92}


Input: "{text}"
Output:
'''




def classify_text(text: str) -> dict:
if not MODEL_RESOURCE:
# Fallback: very naive rule-based classifier
t = text.lower()
if any(x in t for x in ["bleed","hurt","injur","broken","pain","unconscious"]):
return {"intent": "medical", "severity": "high", "confidence": 0.8}
if any(x in t for x in ["stabb","attack","robber","gun","fight","assault"]):
return {"intent": "crime", "severity": "high", "confidence": 0.85}
if any(x in t for x in ["fire","smoke","burning"]):
return {"intent": "fire", "severity": "high", "confidence": 0.9}
return {"intent": "other", "severity": "low", "confidence": 0.5}


# Call Vertex AI Text Generation/Classification - using prediction endpoint
aiplatform.init(project=PROJECT, location=LOCATION)
# For Vertex text generation, use the parameters appropriate for your model
prediction_client = aiplatform.gapic.PredictionServiceClient()
endpoint = MODEL_RESOURCE # if you stored an endpoint resource
prompt = PROMPT_TEMPLATE.replace('{text}', text)
instance = {"content": prompt}
response = prediction_client.predict(endpoint=endpoint, instances=[instance], parameters={})
# Parse response according to model output - this is model dependent
# Here we naively parse the first generated text as JSON
try:
generated = response.predictions[0].get('content', '')
import json
# Attempt to find JSON object in generated text
start = generated.find('{')
end = generated.rfind('}')
if start != -1 and end != -1:
obj = json.loads(generated[start:end+1])
return obj
except Exception:
pass
# fallback
return {"intent": "other", "severity": "low", "confidence": 0.5}
