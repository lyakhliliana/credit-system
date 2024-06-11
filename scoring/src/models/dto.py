from pydantic import BaseModel


class AgreementDto(BaseModel):
    person_id: int
    agreement_id: int
    status: str
