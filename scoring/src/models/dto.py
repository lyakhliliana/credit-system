from pydantic import BaseModel


class AgreementDto(BaseModel):
    agreement_id: int
    status: str
