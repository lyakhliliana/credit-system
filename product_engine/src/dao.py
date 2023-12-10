from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship

from product_engine.src.database import Base


class ProductDao(Base):
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


class PersonDao(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_nm = Column(String(30), nullable=False)
    last_nm = Column(String(30), nullable=False)
    middle_nm = Column(String(30), nullable=True)
    birth_dt = Column(Date, nullable=False)
    passport_no = Column(String(30), index=True, nullable=False)
    mobile_phone_no = Column(String(12), nullable=False)
    monthly_income_amt = Column(Integer, nullable=False)
    agreement = relationship('AgreementDao', back_populates='person')


class AgreementDao(Base):
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


class PaymentDao(Base):
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
