from enum import Enum


class Status(Enum):
    NEW = 'NEW'
    SCORING = 'SCORING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CLOSED = 'CLOSED'
