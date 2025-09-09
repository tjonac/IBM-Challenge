import uuid
from app.schemas import (
    CreateReportRequest, 
    CreateReportResponse, 
    GetReportResponse,
    GetUserInfoResponse,
    GetCallTrancsriptionResponse
)

def handle_get_user_information(client_id: str)->GetUserInfoResponse:
    return 0

def handle_get_report(client_id: str, report_id: str)->GetReportResponse:
    return 0

def handle_get_call_transcript(client_id: str, call_id: str)->GetCallTrancsriptionResponse:
    return 0

def handle_create_report(request: CreateReportRequest) -> CreateReportResponse:
    return 0