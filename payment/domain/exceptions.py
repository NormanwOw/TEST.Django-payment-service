
class DomainException(Exception):
    pass


class PaymentAlreadyExist(DomainException):
    pass


class OrganizationDoesNotExist(DomainException):
    pass
