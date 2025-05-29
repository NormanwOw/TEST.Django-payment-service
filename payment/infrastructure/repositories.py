from typing import Optional
from uuid import UUID

from payment.domain.aggregates import Payment
from payment.domain.entities import Organization, Document
from payment.infrastructure.interfaces import (IOrganizationRepository, IDocumentRepository,
                                               IPaymentRepository)
from payment.models import OrganizationModel, DocumentModel, PaymentModel


class OrganizationRepository(IOrganizationRepository):
    model = OrganizationModel

    @classmethod
    def add(cls, organization: Organization) -> Organization:
        organization_model = cls.model.from_domain(organization)
        organization_model.save()
        organization.id = organization_model.id
        return organization

    @classmethod
    def get(cls, inn: int) -> Optional[Organization]:
        organization_model = cls.model.objects.filter(inn=inn).first()
        return organization_model.to_domain() if organization_model else None

    @classmethod
    def update(cls, organization: Organization) -> Organization:
        cls.model.objects.filter(inn=organization.inn).update(balance=organization.balance)
        return organization

    @classmethod
    def delete(cls, organization: Organization):
        cls.model.objects.filter(name=organization.name).delete()


class PaymentRepository(IPaymentRepository):
    model = PaymentModel

    @classmethod
    def add(cls, payment: Payment) -> Payment:
        payment_model = cls.model.from_domain(payment)
        payment_model.save()
        payment.id = payment_model.id
        return payment

    @classmethod
    def get(cls, payment_id: UUID) -> Optional[Payment]:
        payment_model = cls.model.objects.filter(id=payment_id).first()
        return payment_model.to_domain() if payment_model else None

    @classmethod
    def update(cls, payment: Payment) -> Payment:
        cls.model.objects.filter(id=payment.id).update(amount=payment.amount)
        return payment

    @classmethod
    def delete(cls, payment: Payment):
        cls.model.objects.filter(id=payment.id).delete()


class DocumentRepository(IDocumentRepository):
    model = DocumentModel

    @classmethod
    def add(cls, document: Document) -> Document:
        document_model = cls.model.from_domain(document)
        document_model.save()
        document.id = document_model.id
        return document

    @classmethod
    def get(cls, name: str) -> Optional[Document]:
        document_model = cls.model.objects.filter(name=name).first()
        return document_model.to_domain() if document_model else None

    @classmethod
    def update(cls, document: Document) -> Document:
        cls.model.objects.filter(id=document.id).update(
            number=document.number,
            date=document.date
        )
        return document

    @classmethod
    def delete(cls, document: Document):
        cls.model.objects.filter(number=document.number).delete()
