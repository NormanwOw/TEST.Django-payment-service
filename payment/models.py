import uuid

from django.core.validators import MaxValueValidator
from django.db import models

from payment.domain.aggregates import Payment
from payment.domain.entities import Organization, Document


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        null=False,
        unique=True,
        blank=False
    )

    class Meta:
        abstract = True


class DocumentModel(BaseModel):
    number = models.CharField(
        blank=False,
        max_length=12,
        verbose_name='Номер документа',
        db_index=True,
    )
    date = models.DateField(blank=False, verbose_name='Дата')

    class Meta:
        db_table = 'documents'
        verbose_name = 'документ'
        verbose_name_plural = 'документы'

    def __str__(self):
        return self.number

    def to_domain(self) -> Document:
        return Document(
            id=self.id,
            number=self.number,
            date=self.date
        )

    @classmethod
    def from_domain(cls, document: Document) -> 'DocumentModel':
        return cls(
            id=document.id or uuid.uuid4(),
            number=document.number,
            date=document.date
        )


class OrganizationModel(BaseModel):
    inn = models.PositiveBigIntegerField(
        blank=False,
        unique=True,
        validators=[MaxValueValidator(10**13-1)],
        verbose_name='ИНН',
        db_index=True,
    )
    balance = models.PositiveBigIntegerField(
        null=False,
        blank=False,
        validators=[MaxValueValidator(10**15-1)],
        verbose_name='Баланс'
    )

    class Meta:
        db_table = 'organizations'
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        return f'{self.inn}'

    def to_domain(self) -> Organization:
        return Organization(
            id=self.id,
            inn=self.inn,
            balance=self.balance or 0
        )

    @classmethod
    def from_domain(cls, org: Organization) -> 'OrganizationModel':
        return cls(
            id=org.id or uuid.uuid4(),
            inn=org.inn,
            balance=org.balance or 0
        )


class PaymentModel(BaseModel):
    amount = models.PositiveBigIntegerField(null=False, blank=False)
    payer = models.ForeignKey(
        to=OrganizationModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Плательщик'
    )
    document = models.ForeignKey(
        to=DocumentModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Документ'
    )

    class Meta:
        db_table = 'payments'
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return str(self.id)

    def to_domain(self) -> Payment:
        return Payment(
            id=self.id,
            amount=self.amount,
            payer=self.payer.to_domain() if self.payer else None,
            document=self.document.to_domain() if self.document else None,
        )

    @classmethod
    def from_domain(cls, payment: Payment) -> 'PaymentModel':
        return cls(
            id=payment.id or uuid.uuid4(),
            amount=payment.amount,
            payer=OrganizationModel.from_domain(payment.payer) if payment.payer else None,
            document=DocumentModel.from_domain(payment.document) if payment.document else None
        )
