from sqlalchemy import Column, Integer, String

from common.base_orm_model import BaseOrmModel
from origination.src.models.dto import AgreementDto


class AgreementDao(BaseOrmModel):
    __tablename__ = 'origination'
    agreement_id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(30), nullable=False)

    def convert_to_dto(self) -> AgreementDto:
        return AgreementDto(
            agreement_id=self.agreement_id,
            status=self.status
        )
