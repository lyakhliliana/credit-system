from enum import Enum


class AgreementStatus(Enum):
    NEW = 'NEW'
    SCORING = 'SCORING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'


class PaymentStatus(Enum):
    FUTURE = 'FUTURE'
    PAID = 'PAID'
    OVERDUE = 'OVERDUE'
