from datetime import datetime, date

from pydantic import BaseModel, field_validator


class ProductBaseDto(BaseModel):
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


class ProductCreateDto(ProductBaseDto):
    pass


class ProductDto(ProductBaseDto):
    product_id: int

    class Config:
        orm_mode = True


class PersonBaseDto(BaseModel):
    first_nm: str
    last_nm: str
    middle_nm: str
    birth_dt: date
    passport_no: str
    email: str
    mobile_phone_no: str
    monthly_income_amt: str


class PersonCreateDto(PersonBaseDto):
    pass


class PersonDto(PersonBaseDto):
    person_id: int

    class Config:
        orm_mode = True


class AgreementBaseDto(BaseModel):
    product_code: str
    person_id: int
    load_term: int
    principal_amount: float
    interest: float
    origination_amount: float
    agreement_dttm: datetime
    status: str


class AgreementDto(AgreementBaseDto):
    agreement_id: int

    class Config:
        orm_mode = True


class KafkaAgreementDto(BaseModel):
    person_id: int
    agreement_id: int
    status: str


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

    @field_validator('birthday')
    def parse_birthday(cls, value):
        try:
            parsed_date = datetime.strptime(value, '%d.%m.%Y')
            if not (18 <= datetime.now().year - parsed_date.year <= 70):
                raise ValueError()
        except ValueError:
            raise ValueError('Неправильно указан возраст, возраст 18-70 лет')
        return value

    @field_validator('email')
    def validate_email(cls, value: str):
        if '@' in value and len(value) >= 3:
            return value
        raise ValueError('Неправильно указана электронная почта')

    @field_validator('phone')
    def validate_phone(cls, value: str):
        if value.startswith('+7') and len(value) == 12:
            return value
        if value.startswith('8') and len(value) == 11:
            return value
        raise ValueError('Неправильно указана электронная почта')

    @field_validator('salary')
    def validate_salary(cls, value):
        return float(int(value))


class PaymentBaseDto(BaseModel):
    payment_id: int
    agreement_id: int
    payment_dt: date
    # payment_period_start: date  # should be str representing date
    # payment_period_end: date  # should be str representing date
    payment_amt_debt: float
    payment_amt_proc: float
    serial_nmb_payment: int
    status: str


class PaymentDto(PaymentBaseDto):
    payment_id: int
