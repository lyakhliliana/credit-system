from pydantic import BaseModel


class AgreementDto(BaseModel):
    agreement_id: int
    person_id: int
    status: str


class AgreementCreateDto(BaseModel):
    person_id: int
    agreement_id: int
