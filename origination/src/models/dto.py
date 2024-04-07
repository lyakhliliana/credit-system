from pydantic import BaseModel


class AgreementDto(BaseModel):
    agreement_id: int
    status: str


class AgreementCreateDto(BaseModel):
    agreement_id: int
