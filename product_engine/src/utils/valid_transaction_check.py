from product_engine.src.models.dao import ProductDao, AgreementDao


def check_valid_agreement_condition(product: ProductDao, agreement: AgreementDao) -> bool:
    if agreement.load_term < product.min_load_term or agreement.load_term > product.max_load_term:
        return False
    if agreement.interest < product.min_interest or agreement.load_term > product.max_interest:
        return False
    if (agreement.origination_amount < product.min_origination_amount or
            agreement.load_term > product.max_origination_amount):
        return False
    if agreement.principal_amount < product.min_principal_amount or agreement.load_term > product.max_principal_amount:
        return False
    return True
