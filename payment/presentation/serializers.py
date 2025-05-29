from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from payment.domain.aggregates import Payment
from payment.domain.entities import Organization, Document
from payment.models import OrganizationModel


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name='OK',
            value={'status': 'OK'},
            response_only=True
        )
    ]
)
class StatusOKSerializer(serializers.Serializer):
    status = serializers.CharField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name='Success',
            value={'status': 'success'},
            response_only=True
        )
    ]
)
class StatusSuccessSerializer(serializers.Serializer):
    status = serializers.CharField()


class OrganizationBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationModel
        fields = ['inn', 'balance']


class BankWebhookSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    payer_inn = serializers.CharField()
    document_number = serializers.CharField()
    document_date = serializers.DateTimeField()

    def to_domain(self) -> Payment:
        data = self.validated_data
        return Payment(
            id=data['operation_id'],
            amount=data['amount'],
            payer=Organization(
                inn=data['payer_inn'],
                balance=None,
            ),
            document=Document(
                number=data['document_number'],
                date=data['document_date'],
            )
        )
