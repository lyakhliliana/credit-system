from datetime import timedelta, date

import numpy_financial as npf


def calc_periods(rate: float, n_per: int, present_value: float, activation_date: date) -> dict:
    """

    :param rate: процентная ставка [0, 1]
    :param n_per: количество периодов
    :param present_value: сумма кредита
    :param activation_date: дата активации договора
    :return: словарь с подсчитанными значениями
    """
    payments = {}
    cur_date = activation_date

    for i in range(1, n_per + 1):
        ppmt_sum = float(round(npf.ppmt(rate / 12, i, n_per, present_value), 2))
        ipmt_sum = float(round(npf.ipmt(rate / 12, i, n_per, present_value).sum(), 2))
        cur_date = cur_date + timedelta(days=30)
        cur_payment = {"payment_amt_debt": ppmt_sum, "payment_amt_proc": ipmt_sum, "payment_dt": cur_date}
        payments[i] = cur_payment

    return payments


# import datetime
# print(calc_periods(0.22, 36, 500000, datetime.date(2024, 4, 27)))
