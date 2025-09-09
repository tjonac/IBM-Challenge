import uuid
from app.schemas import (
    CreateReportRequest, 
    CreateReportResponse, 
    GetReportResponse,
    GetUserInfoResponse,
    GetCallTrancsriptionResponse,
    CreateCallRequest,
    CreateCallResponse
)
from google import genai
from google.genai import types

client = genai.Client()

METADATA_PROMPT = """You are an expert at extracting structured data from unstructured text.

Your task:  
- Input: a call transcript.  
- Output: a single JSON object with exactly two keys:  
  - "sentiment": overall sentiment of the call, as one of ["positive", "neutral", "negative"].  
  - "call_target": the main subject or entity the caller is contacting (e.g., "billing", "technical support", "cancellation").  

Requirements:  
- Output **only** the JSON object, no extra text or explanation.  
- If the value cannot be determined, set it to null.

# Transcript
{transcript}

# Output

"""

print(response.text)

def handle_get_user_information(client_id: str)->GetUserInfoResponse:
    return 0

def handle_get_report(client_id: str, report_id: str)->GetReportResponse:
    return 0

def handle_get_call_transcript(client_id: str, call_id: str)->GetCallTrancsriptionResponse:
    return 0

def handle_create_report(request: CreateReportRequest) -> CreateReportResponse:
    return 0

def handle_create_call(request: CreateCallRequest) -> CreateCallResponse:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=METADATA_PROMPT.format(transcript = request.transcript),
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    


    return 0