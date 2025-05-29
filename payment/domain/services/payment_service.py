from main.infrastructure.interfaces import ILogger
from payment.domain.aggregates import Payment
from payment.domain.interfaces import IProcessPaymentService
from payment.infrastructure.uow.interfaces import IUnitOfWork


class ProcessPaymentService(IProcessPaymentService):

    def __init__(self, uow: IUnitOfWork, logger: ILogger):
        self.uow = uow
        self.logger = logger

    def process(self, payment: Payment) -> Payment:
        existing_org = self.uow.organizations.get(payment.payer.inn)

        if existing_org:
            existing_org.balance += payment.amount
            payment.payer = existing_org
            self.uow.organizations.update(existing_org)
        else:
            payment.payer.balance = payment.amount
            self.uow.organizations.add(payment.payer)

        return payment
