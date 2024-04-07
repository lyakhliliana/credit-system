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
