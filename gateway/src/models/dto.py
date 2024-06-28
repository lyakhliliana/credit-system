from datetime import datetime, date

from pydantic import BaseModel


class ProductDto(BaseModel):
    product_id: int
    code: str
    title: str
    version: int
    min_load_term: int
    max_load_term: int
    min_principal_amount: float
    max_principal_amount: float
    min_interest: float
    max_interest: float
    min_origination_amount: float
    max_origination_amount: float


class ApplicationCreateDto(BaseModel):
    product_code: str
    first_name: str
    second_name: str
    third_name: str
    birthday: str
    passport_number: str
    email: str
    phone: str
    salary: float
    term: int
    interest: float
    disbursement_amount: float


class AgreementDto(BaseModel):
    agreement_id: int
    product_code: str
    person_id: int
    load_term: int
    principal_amount: float
    interest: float
    origination_amount: float
    agreement_dttm: datetime
    status: str


class PaymentDto(BaseModel):
    payment_id: int
    agreement_id: int
    payment_dt: date
    payment_amt_debt: float
    payment_amt_proc: float
    serial_nmb_payment: int
    status: str


class PersonPaymentDto(BaseModel):
    date: str
    agreement_id: int
    payment: float
