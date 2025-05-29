from abc import ABC, abstractmethod
from uuid import UUID

from payment.domain.aggregates import Payment
from payment.domain.entities import Organization, Document


class IOrganizationRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    def add(cls, organization: Organization) -> Organization:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(cls, inn: int) -> Organization:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, organization: Organization) -> Organization:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, organization: Organization):
        raise NotImplementedError


class IDocumentRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    def add(cls, document: Document) -> Document:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(cls, name: str) -> Document:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, document: Document) -> Document:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, document: Document):
        raise NotImplementedError


class IPaymentRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    def add(cls, payment: Payment) -> Payment:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(cls, payment_id: UUID) -> Payment:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, payment: Payment) -> Payment:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, payment: Payment):
        raise NotImplementedError
