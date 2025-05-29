from django.db import IntegrityError

from main.infrastructure.interfaces import ILogger
from payment.domain.aggregates import Payment
from payment.domain.exceptions import PaymentAlreadyExist
from payment.domain.interfaces import IProcessPaymentService
from payment.infrastructure.uow.interfaces import IUnitOfWork


class HandlePaymentUseCase:

    def __init__(
        self,
        payment_service: IProcessPaymentService,
        uow: IUnitOfWork,
        logger: ILogger
    ):
        self.payment_service = payment_service
        self.uow = uow
        self.logger = logger

    def __call__(self, payment: Payment):
        try:
            with self.uow:
                processed_payment = self.payment_service.process(payment)
                self.uow.documents.add(processed_payment.document)
                try:
                    self.uow.payments.add(processed_payment)
                except IntegrityError:
                    raise PaymentAlreadyExist()
                self.logger.info(f'Изменён баланс организации '
                                 f'{payment.payer.inn}: '
                                 f'{processed_payment.payer.balance - payment.amount} -> '
                                 f'{processed_payment.payer.balance}')
        except PaymentAlreadyExist as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при обработке платежа {payment}', exc_info=True)
            raise ex
