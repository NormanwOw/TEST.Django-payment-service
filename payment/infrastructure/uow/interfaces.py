from abc import ABC, abstractmethod

from payment.infrastructure.interfaces import IOrganizationRepository, IDocumentRepository, IPaymentRepository


class IUnitOfWork(ABC):

    organizations: IOrganizationRepository
    documents: IDocumentRepository
    payments: IPaymentRepository

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
