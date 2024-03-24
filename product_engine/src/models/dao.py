from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship

from common.base_orm_model import BaseOrmModel
from product_engine.src.models.dto import ProductDto, AgreementDto


class ProductDao(BaseOrmModel):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    code = Column(String(100), index=True, nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    version = Column(Integer, nullable=False)
    min_load_term = Column(Integer, nullable=False)
    max_load_term = Column(Integer, nullable=False)
    min_principal_amount = Column(Numeric, nullable=False)
    max_principal_amount = Column(Numeric, nullable=False)
    min_interest = Column(Numeric, nullable=False)
    max_interest = Column(Numeric, nullable=False)
    min_origination_amount = Column(Numeric, nullable=False)
    max_origination_amount = Column(Numeric, nullable=False)
    agreement = relationship('AgreementDao', back_populates='product')

    def convert_to_dto(self) -> ProductDto:
        return ProductDto(
            product_id=self.product_id,
            code=self.code,
            title=self.title,
            version=self.version,
            min_load_term=self.min_load_term,
            max_load_term=self.max_load_term,
            min_principal_amount=self.min_principal_amount,
            max_principal_amount=self.max_principal_amount,
            min_interest=self.min_interest,
            max_interest=self.max_interest,
            min_origination_amount=self.min_origination_amount,
            max_origination_amount=self.max_origination_amount)


class PersonDao(BaseOrmModel):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_nm = Column(String(30), nullable=False)
    last_nm = Column(String(30), nullable=False)
    middle_nm = Column(String(30), nullable=True)
    birth_dt = Column(Date, nullable=False)
    passport_no = Column(String(30), index=True, nullable=False)
    email = Column(String(30), nullable=False)
    mobile_phone_no = Column(String(12), nullable=False)
    monthly_income_amt = Column(Integer, nullable=False)
    agreement = relationship('AgreementDao', back_populates='person')


class AgreementDao(BaseOrmModel):
    __tablename__ = 'agreement'
    agreement_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_code = Column(String(100), ForeignKey('product.code'), index=True, nullable=False)
    person_id = Column(Integer, ForeignKey('person.person_id'), index=True, nullable=False)
    load_term = Column(Integer, nullable=False)
    principal_amount = Column(Numeric, nullable=False)
    interest = Column(Numeric, nullable=False)
    origination_amount = Column(Numeric, nullable=False)
    agreement_dttm = Column(DateTime, nullable=False)
    status = Column(String(30), nullable=False)
    schedule_payment = relationship('PaymentDao', back_populates='agreement')
    product = relationship('ProductDao', back_populates='agreement')
    person = relationship('PersonDao', back_populates='agreement')

    def convert_to_dto(self) -> AgreementDto:
        return AgreementDto(
            agreement_id=self.agreement_id,
            product_code=self.product_code,
            person_id=self.person_id,
            load_term=self.load_term,
            principal_amount=self.principal_amount,
            interest=self.interest,
            origination_amount=self.origination_amount,
            agreement_dttm=self.agreement_dttm,
            status=self.status)


class PaymentDao(BaseOrmModel):
    __tablename__ = 'schedule_payment'
    payment_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    agreement_id = Column(Integer, ForeignKey('agreement.agreement_id'), index=True, nullable=False)
    payment_dt = Column(Date, nullable=False)
    payment_period_start = Column(Date, nullable=False)
    payment_period_end = Column(Date, nullable=False)
    payment_amt_debt = Column(Numeric, nullable=False)
    payment_amt_proc = Column(Numeric, nullable=False)
    serial_nmb_payment = Column(Integer, nullable=False)
    status = Column(String(30), nullable=False)
    agreement = relationship('AgreementDao', back_populates='schedule_payment')
