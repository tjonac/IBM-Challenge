from fastapi import FastAPI
from app.handlers import (
    handle_get_user_information, 
    handle_create_report,
    handle_get_report,
    handle_get_call_transcript,
    handle_create_call
)
from app.schemas import CreateReportRequest, CreateCallRequest
from app.table_config import SessionDep, create_db_and_tables
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/user")
def get_user_information(client_id: str, session: SessionDep):
    return handle_get_user_information(client_id, session)

@app.get("/report")
def get_user_information(client_id: str, report_id: str, session: SessionDep):
    return handle_get_report(client_id, report_id, session)

@app.get("/call_transcript")
def get_call_transcript(client_id: str, call_id: str, session: SessionDep):
    return handle_get_call_transcript(client_id, call_id, session)

@app.post("/report")
def create_report(request: CreateReportRequest, session: SessionDep):
    return handle_create_report(request, session)

@app.post("/call")
def create_call(request: CreateCallRequest, session: SessionDep):
    return handle_create_call(request, session)
