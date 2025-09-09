from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class Calls(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    operator: str = Field(index=True)
    client_id: int | None = Field(index=True)
    transcript: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    sentiment: str | None = None
    call_target: str | None = None

class Call(Calls):
    id: int | None = Field(primary_key=True)
    operator: str = Field(index=True)
    client_id: int | None = Field(index=True)
    transcript: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    sentiment: str | None = None
    call_target: str | None = None

class Reports(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    call_id: int | None = Field(index=True)
    client_id: int | None = Field(index=True)
    topic: str | None = None
    summary: str | None = None
    priority: int | None = None
    timestamp: datetime = Field(default_factory=datetime.now)

class Report(Reports, table=True):
    id: int | None = Field(primary_key=True)
    call_id: int | None = Field(index=True)
    client_id: int | None = Field(index=True)
    topic: str | None = None
    summary: str | None = None
    priority: int | None = None
    timestamp: datetime = Field(default_factory=datetime.now)