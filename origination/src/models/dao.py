from sqlalchemy import Column, Integer, String

from database.base_orm_model import BaseOrmModel


class AgreementDao(BaseOrmModel):
    __tablename__ = 'origination'
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(30), nullable=False)
