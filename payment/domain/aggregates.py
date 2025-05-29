from typing import Optional

from payment.domain.entities import Organization, Document, BaseID


class Payment(BaseID):
    amount: int
    payer: Optional[Organization] = None
    document: Optional[Document] = None
