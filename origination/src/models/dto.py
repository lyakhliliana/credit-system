from pydantic import BaseModel


class AgreementDto(BaseModel):
    id: int
    status: str  # {NEW, REJECT, APPROVED} пока не добавилось взаимодействие со Scoring


class AgreementCreateDto(BaseModel):
    id: int
