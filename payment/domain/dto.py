from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BankWebhookRequest(BaseModel):
    operation_id: UUID
    amount: int
    payer_inn: str
    document_number: str
    document_date: datetime
