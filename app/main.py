from fastapi import FastAPI
from app.handlers import (
    handle_get_user_information, 
    handle_create_report,
    handle_get_report,
    handle_get_call_transcript,
    handle_create_call
)
from app.schemas import (
    CreateReportRequest,
    CreateCallRequest,
)

app = FastAPI()

@app.get("/user")
def get_user_information(client_id: str):
    return handle_get_user_information(client_id)

@app.get("/report")
def get_user_information(client_id: str, report_id: str):
    return handle_get_report(client_id, report_id)

@app.get("/call_transcript")
def get_call_transcript(client_id: str, call_id: str):
    return handle_get_call_transcript(client_id, call_id)

@app.post("/report")
def create_report(request: CreateReportRequest):
    return handle_create_report(request)

@app.post("/call")
def create_report(request: CreateCallRequest):
    return handle_create_call(request)
