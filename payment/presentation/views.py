
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from logger import Logger
from payment.application.use_cases.get_organization import GetOrganizationUseCase
from payment.application.use_cases.handle_payment import HandlePaymentUseCase
from payment.domain.exceptions import PaymentAlreadyExist, OrganizationDoesNotExist
from payment.domain.services.payment_service import ProcessPaymentService
from payment.infrastructure.uow.impl import UnitOfWork
from payment.presentation.serializers import (BankWebhookSerializer, OrganizationBalanceSerializer,
                                              StatusOKSerializer, StatusSuccessSerializer)


class BankWebhookView(APIView):
    serializer_class = BankWebhookSerializer
    uow = UnitOfWork()
    logger = Logger()
    payment_service = ProcessPaymentService(uow, logger)
    handle_payment_use_case = HandlePaymentUseCase(payment_service, uow, logger)

    @extend_schema(
        summary='Webhook от банка',
        description='Принимает уведомление об операции по счёту от банка.',
        responses={
            200: OpenApiResponse(response=StatusOKSerializer),
            201: OpenApiResponse(response=StatusSuccessSerializer)
        }
    )
    def post(self, request):
        serializer = BankWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.to_domain()
        try:
            self.handle_payment_use_case(payment)
        except PaymentAlreadyExist:
            return Response({'status': 'OK'})
        except Exception:
            return Response({'status': 'server error'}, status=500)

        return Response({'status': 'success'}, status=201)


class OrganizationBalanceView(APIView):
    serializer_class = OrganizationBalanceSerializer
    uow = UnitOfWork()
    logger = Logger()
    get_organization_use_case = GetOrganizationUseCase(uow, logger)

    def get(self, request, inn: int):
        try:
            organization = self.get_organization_use_case(inn=inn)
        except OrganizationDoesNotExist:
            return Response({'detail': 'Organization not found'}, status=404)
        except Exception:
            return Response({'status': 'server error'}, status=500)

        return Response(organization.model_dump(exclude={'id'}))
