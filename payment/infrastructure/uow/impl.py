from django.db import transaction

from payment.infrastructure.interfaces import (IOrganizationRepository, IDocumentRepository,
                                               IPaymentRepository)
from payment.infrastructure.repositories import (OrganizationRepository, DocumentRepository,
                                                 PaymentRepository)
from payment.infrastructure.uow.interfaces import IUnitOfWork


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.ctx = None
        self.sid = None
        self.organizations: IOrganizationRepository = OrganizationRepository()
        self.documents: IDocumentRepository = DocumentRepository()
        self.payments: IPaymentRepository = PaymentRepository()

    def __enter__(self):
        self.ctx = transaction.atomic()
        self.ctx.__enter__()
        self.sid = transaction.savepoint()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            self.commit()
        self.ctx.__exit__(exc_type, exc_value, traceback)
        return False

    def commit(self):
        if self.sid is not None:
            transaction.savepoint_commit(self.sid)
            self.sid = None

    def rollback(self):
        if self.sid is not None:
            transaction.savepoint_rollback(self.sid)
            self.sid = None
