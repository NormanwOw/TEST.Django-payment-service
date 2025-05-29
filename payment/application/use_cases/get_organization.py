from main.infrastructure.interfaces import ILogger
from payment.domain.entities import Organization
from payment.domain.exceptions import OrganizationDoesNotExist
from payment.infrastructure.uow.interfaces import IUnitOfWork


class GetOrganizationUseCase:

    def __init__(self, uow: IUnitOfWork, logger: ILogger):
        self.uow = uow
        self.logger = logger

    def __call__(self, inn: int) -> Organization:
        try:
            with self.uow:
                organization = self.uow.organizations.get(inn)
                if not organization:
                    raise OrganizationDoesNotExist()

                return organization
        except OrganizationDoesNotExist as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при получении организации {inn}', exc_info=True)
            raise ex
