from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class BaseID(BaseModel):
    id: Optional[UUID] = None


class Organization(BaseID):
    inn: int
    balance: Optional[int] = None


class Document(BaseID):
    number: str
    date: datetime
