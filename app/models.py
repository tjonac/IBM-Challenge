from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Calls(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    operator: str = Field(index=True)
    client_id: int | None = Field(index=True)
    transcript: str