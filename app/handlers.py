from fastapi import HTTPException
from app.table_config import SessionDep
from sqlmodel import select, desc, delete
import os
from app.schemas import (
    CreateReportRequest, 
    CreateReportResponse, 
    GetReportResponse,
    GetUserInfoResponse,
    GetCallTrancsriptionResponse
)
from app.models import Call, Report


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