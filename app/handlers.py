from fastapi import HTTPException
from app.table_config import SessionDep
from sqlmodel import select, desc, delete
import os
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
from app.models import Call, Report

client = genai.Client()

METADATA_PROMPT = """You are an expert at extracting structured data from unstructured text.

Your task:  
- Input: a call transcript.  
- Output: a single JSON object with exactly two keys:  
  - "sentiment": overall sentiment of the call, as one of ["positive", "neutral", "negative"].  
  - "call_target": the main subject or entity the caller is contacting (e.g., "billing", "technical support", "cancellation").  

Requirements:  
- Output *only* the JSON object, no extra text or explanation.  
- If the value cannot be determined, set it to null.

# Transcript
{transcript}

# Output

"""

print(response.text)


@staticmethod
async def handle_get_user_information(client_id: str, session: SessionDep) -> GetUserInfoResponse:
    statement = select(Call.id,Call.report_id, Call.sentiment, Call.timestamp).where(Call.client_id == client_id).order_by(desc(Call.timestamp))
    result =  session.exec(statement).all()

    calls = [str(row[0]) for row in result if row[0] is not None]
    reports = [str(row[1]) for row in result if row[1] is not None]
    last_call_sentiment = result[0][2] if result[0][2] is not None else "neutral"
    return GetUserInfoResponse(
        calls=calls,
        reports=reports,
        last_call_sentiment=last_call_sentiment
    )


def handle_get_report(client_id: str, report_id: str, session: SessionDep)->GetReportResponse:
    statement = select(Call.id,Call.report_id, Call.sentiment, Call.timestamp).where(Call.client_id == client_id).order_by(desc(Call.timestamp))
    result =  session.exec(statement).all()

    calls = [str(row[0]) for row in result if row[0] is not None]
    reports = [str(row[1]) for row in result if row[1] is not None]
    last_call_sentiment = result[0][2] if result[0][2] is not None else "neutral"
    return GetUserInfoResponse(
        calls=calls,
        reports=reports,
        last_call_sentiment=last_call_sentiment
    )

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