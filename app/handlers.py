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
import json
import re
import uuid

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

def extract_json(text: str):
    """
    Extract the first JSON object found in a string and return it as a Python dict.
    If no valid JSON is found, return None.
    """
    # Regex to capture {...} including nested braces
    match = re.search(r'\{(?:[^{}]|(?R))*\}', text, re.DOTALL)
    if not match:
        return None
    
    json_str = match.group(0)
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None



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
    statement = select(Call.report_id, Call.sentiment,Call.timestamp).where(Call.report_id == report_id).order_by(desc(Call.timestamp))
    statement_report = select(Report.id, Report.summary, Report.status, Report.timestamp).where(Report.id == report_id)
    result =  session.exec(statement).all()
    result_report =  session.exec(statement).all()

    status = result_report[0][2] if result_report[0][2] is not None else "open"
    summary = result_report[0][1] if result_report[0][1] is not None else ""
    closed_date = result_report[0][3].timestamp() if result_report[0][2]=="closed" else None

    return GetUserInfoResponse(
        status=status,
        summary=summary,
        closed_date=closed_date
    )

def handle_get_call_transcript(client_id: str, call_id: str, session: SessionDep)->GetCallTrancsriptionResponse:
    statement = select(Call.id, Call.transcript).where(Call.id == call_id).order_by(desc(Call.timestamp))
    result =  session.exec(statement).all()

    client_id = client_id
    call_id = call_id
    transcription = result[0][1] if result[0][1] is not None else ""

    return GetUserInfoResponse(
        client_id=client_id,
        call_id=call_id,
        transcription=transcription
    )

def handle_create_report(request: CreateReportRequest, session: SessionDep) -> CreateReportResponse:

    client_id = request.client_id
    summary = request.summary
    call_id = request.call_id

    report_id = str(uuid.uuid4())

    report_db = Report(
        id=report_id,
        call_id=call_id,
        topic="hello",
        summary=summary,
        client_id=client_id,
        priority=1
    )

    session.add(report_db)
    session.commit()
    session.refresh(report_db)

    return CreateReportResponse(
        message="Report created sucesfully!",
        report_id=report_id
    )

def handle_create_call(request: CreateCallRequest, session: SessionDep) -> CreateCallResponse:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=METADATA_PROMPT.format(transcript = request.transcript),
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )
    
    metadata = extract_json(response.text)

    call_id = str(uuid.uuid4())

    call_db = Call(
        id= call_id,
        operator= request.operator,
        client_id =request.client_id,
        transcript=request.transcript,
        sentiment=metadata.get("sentiment"),
        call_target=metadata.get("call_target")
    )

    session.add(call_db)
    session.commit()
    session.refresh(call_db)

    return CreateCallResponse(
        message="Call uploaded sucesfully!!!",
        call_id=call_id
    )
