from abc import abstractmethod, ABC

from payment.domain.aggregates import Payment


class IProcessPaymentService(ABC):

    @abstractmethod
    def process(self, payment: Payment) -> Payment:
        raise NotImplementedError
