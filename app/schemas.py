from pydantic import BaseModel
from typing import Literal, Optional, List

class GetReportResponse(BaseModel):
    status: Literal["closed", "in progress", "open"]
    summary: str
    count: int
    closed_date: Optional[int]

class GetCallTrancsriptionResponse(BaseModel):
    client_id: str
    call_id: str
    transcription: str

class GetUserInfoResponse(BaseModel):
    calls: List[str]
    reports: List[str]
    last_call_sentiment: Literal["positive", "neutral", "negative"]

class CreateReportRequest(BaseModel):
    client_id: str
    summary: str
    call_id: str

class CreateReportResponse(BaseModel):
    message: str
    report_id: str

