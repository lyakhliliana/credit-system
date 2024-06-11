import datetime

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.payment_math import calc_periods


def test_first_parameters():
    answer = {
        1: {'payment_amt_debt': -37073.47, 'payment_amt_proc': -10000.0, 'payment_dt': datetime.date(2024, 5, 27)},
        2: {'payment_amt_debt': -37444.21, 'payment_amt_proc': -9629.27, 'payment_dt': datetime.date(2024, 6, 26)},
        3: {'payment_amt_debt': -37818.65, 'payment_amt_proc': -9254.82, 'payment_dt': datetime.date(2024, 7, 26)},
        4: {'payment_amt_debt': -38196.84, 'payment_amt_proc': -8876.64, 'payment_dt': datetime.date(2024, 8, 25)},
        5: {'payment_amt_debt': -38578.8, 'payment_amt_proc': -8494.67, 'payment_dt': datetime.date(2024, 9, 24)},
        6: {'payment_amt_debt': -38964.59, 'payment_amt_proc': -8108.88, 'payment_dt': datetime.date(2024, 10, 24)},
        7: {'payment_amt_debt': -39354.24, 'payment_amt_proc': -7719.23, 'payment_dt': datetime.date(2024, 11, 23)},
        8: {'payment_amt_debt': -39747.78, 'payment_amt_proc': -7325.69, 'payment_dt': datetime.date(2024, 12, 23)},
        9: {'payment_amt_debt': -40145.26, 'payment_amt_proc': -6928.21, 'payment_dt': datetime.date(2025, 1, 22)},
        10: {'payment_amt_debt': -40546.71, 'payment_amt_proc': -6526.76, 'payment_dt': datetime.date(2025, 2, 21)},
        11: {'payment_amt_debt': -40952.18, 'payment_amt_proc': -6121.29, 'payment_dt': datetime.date(2025, 3, 23)},
        12: {'payment_amt_debt': -41361.7, 'payment_amt_proc': -5711.77, 'payment_dt': datetime.date(2025, 4, 22)},
        13: {'payment_amt_debt': -41775.32, 'payment_amt_proc': -5298.16, 'payment_dt': datetime.date(2025, 5, 22)},
        14: {'payment_amt_debt': -42193.07, 'payment_amt_proc': -4880.4, 'payment_dt': datetime.date(2025, 6, 21)},
        15: {'payment_amt_debt': -42615.0, 'payment_amt_proc': -4458.47, 'payment_dt': datetime.date(2025, 7, 21)},
        16: {'payment_amt_debt': -43041.15, 'payment_amt_proc': -4032.32, 'payment_dt': datetime.date(2025, 8, 20)},
        17: {'payment_amt_debt': -43471.56, 'payment_amt_proc': -3601.91, 'payment_dt': datetime.date(2025, 9, 19)},
        18: {'payment_amt_debt': -43906.28, 'payment_amt_proc': -3167.19, 'payment_dt': datetime.date(2025, 10, 19)},
        19: {'payment_amt_debt': -44345.34, 'payment_amt_proc': -2728.13, 'payment_dt': datetime.date(2025, 11, 18)},
        20: {'payment_amt_debt': -44788.79, 'payment_amt_proc': -2284.68, 'payment_dt': datetime.date(2025, 12, 18)},
        21: {'payment_amt_debt': -45236.68, 'payment_amt_proc': -1836.79, 'payment_dt': datetime.date(2026, 1, 17)},
        22: {'payment_amt_debt': -45689.05, 'payment_amt_proc': -1384.42, 'payment_dt': datetime.date(2026, 2, 16)},
        23: {'payment_amt_debt': -46145.94, 'payment_amt_proc': -927.53, 'payment_dt': datetime.date(2026, 3, 18)},
        24: {'payment_amt_debt': -46607.4, 'payment_amt_proc': -466.07, 'payment_dt': datetime.date(2026, 4, 17)}}

    periods = calc_periods(0.12, 24, 1000000, datetime.date(2024, 4, 27))

    for i, values in answer.items():
        assert values["payment_amt_debt"] == periods[i]["payment_amt_debt"]
        assert values["payment_amt_proc"] == periods[i]["payment_amt_proc"]
        assert values["payment_dt"] == periods[i]["payment_dt"]


def test_second_parameters():
    answer = {1: {'payment_amt_debt': -957.27, 'payment_amt_proc': -750.0, 'payment_dt': datetime.date(2024, 5, 27)},
              2: {'payment_amt_debt': -1029.07, 'payment_amt_proc': -678.2, 'payment_dt': datetime.date(2024, 6, 26)},
              3: {'payment_amt_debt': -1106.25, 'payment_amt_proc': -601.02, 'payment_dt': datetime.date(2024, 7, 26)},
              4: {'payment_amt_debt': -1189.21, 'payment_amt_proc': -518.06, 'payment_dt': datetime.date(2024, 8, 25)},
              5: {'payment_amt_debt': -1278.4, 'payment_amt_proc': -428.87, 'payment_dt': datetime.date(2024, 9, 24)},
              6: {'payment_amt_debt': -1374.29, 'payment_amt_proc': -332.99, 'payment_dt': datetime.date(2024, 10, 24)},
              7: {'payment_amt_debt': -1477.36, 'payment_amt_proc': -229.91, 'payment_dt': datetime.date(2024, 11, 23)},
              8: {'payment_amt_debt': -1588.16, 'payment_amt_proc': -119.11, 'payment_dt': datetime.date(2024, 12, 23)}}

    periods = calc_periods(0.9, 8, 10000, datetime.date(2024, 4, 27))

    for i, values in answer.items():
        assert values["payment_amt_debt"] == periods[i]["payment_amt_debt"]
        assert values["payment_amt_proc"] == periods[i]["payment_amt_proc"]
        assert values["payment_dt"] == periods[i]["payment_dt"]


def test_third_parameters():
    ans = {1: {'payment_amt_debt': -9928.56, 'payment_amt_proc': -9166.67, 'payment_dt': datetime.date(2024, 5, 27)},
           2: {'payment_amt_debt': -10110.58, 'payment_amt_proc': -8984.64, 'payment_dt': datetime.date(2024, 6, 26)},
           3: {'payment_amt_debt': -10295.94, 'payment_amt_proc': -8799.28, 'payment_dt': datetime.date(2024, 7, 26)},
           4: {'payment_amt_debt': -10484.7, 'payment_amt_proc': -8610.52, 'payment_dt': datetime.date(2024, 8, 25)},
           5: {'payment_amt_debt': -10676.92, 'payment_amt_proc': -8418.3, 'payment_dt': datetime.date(2024, 9, 24)},
           6: {'payment_amt_debt': -10872.67, 'payment_amt_proc': -8222.56, 'payment_dt': datetime.date(2024, 10, 24)},
           7: {'payment_amt_debt': -11072.0, 'payment_amt_proc': -8023.23, 'payment_dt': datetime.date(2024, 11, 23)},
           8: {'payment_amt_debt': -11274.99, 'payment_amt_proc': -7820.24, 'payment_dt': datetime.date(2024, 12, 23)},
           9: {'payment_amt_debt': -11481.69, 'payment_amt_proc': -7613.53, 'payment_dt': datetime.date(2025, 1, 22)},
           10: {'payment_amt_debt': -11692.19, 'payment_amt_proc': -7403.04, 'payment_dt': datetime.date(2025, 2, 21)},
           11: {'payment_amt_debt': -11906.55, 'payment_amt_proc': -7188.68, 'payment_dt': datetime.date(2025, 3, 23)},
           12: {'payment_amt_debt': -12124.83, 'payment_amt_proc': -6970.39, 'payment_dt': datetime.date(2025, 4, 22)},
           13: {'payment_amt_debt': -12347.12, 'payment_amt_proc': -6748.1, 'payment_dt': datetime.date(2025, 5, 22)},
           14: {'payment_amt_debt': -12573.49, 'payment_amt_proc': -6521.74, 'payment_dt': datetime.date(2025, 6, 21)},
           15: {'payment_amt_debt': -12804.0, 'payment_amt_proc': -6291.23, 'payment_dt': datetime.date(2025, 7, 21)},
           16: {'payment_amt_debt': -13038.74, 'payment_amt_proc': -6056.49, 'payment_dt': datetime.date(2025, 8, 20)},
           17: {'payment_amt_debt': -13277.78, 'payment_amt_proc': -5817.44, 'payment_dt': datetime.date(2025, 9, 19)},
           18: {'payment_amt_debt': -13521.21, 'payment_amt_proc': -5574.02, 'payment_dt': datetime.date(2025, 10, 19)},
           19: {'payment_amt_debt': -13769.1, 'payment_amt_proc': -5326.13, 'payment_dt': datetime.date(2025, 11, 18)},
           20: {'payment_amt_debt': -14021.53, 'payment_amt_proc': -5073.69, 'payment_dt': datetime.date(2025, 12, 18)},
           21: {'payment_amt_debt': -14278.59, 'payment_amt_proc': -4816.63, 'payment_dt': datetime.date(2026, 1, 17)},
           22: {'payment_amt_debt': -14540.37, 'payment_amt_proc': -4554.86, 'payment_dt': datetime.date(2026, 2, 16)},
           23: {'payment_amt_debt': -14806.94, 'payment_amt_proc': -4288.28, 'payment_dt': datetime.date(2026, 3, 18)},
           24: {'payment_amt_debt': -15078.4, 'payment_amt_proc': -4016.82, 'payment_dt': datetime.date(2026, 4, 17)},
           25: {'payment_amt_debt': -15354.84, 'payment_amt_proc': -3740.39, 'payment_dt': datetime.date(2026, 5, 17)},
           26: {'payment_amt_debt': -15636.35, 'payment_amt_proc': -3458.88, 'payment_dt': datetime.date(2026, 6, 16)},
           27: {'payment_amt_debt': -15923.01, 'payment_amt_proc': -3172.21, 'payment_dt': datetime.date(2026, 7, 16)},
           28: {'payment_amt_debt': -16214.93, 'payment_amt_proc': -2880.29, 'payment_dt': datetime.date(2026, 8, 15)},
           29: {'payment_amt_debt': -16512.21, 'payment_amt_proc': -2583.02, 'payment_dt': datetime.date(2026, 9, 14)},
           30: {'payment_amt_debt': -16814.93, 'payment_amt_proc': -2280.3, 'payment_dt': datetime.date(2026, 10, 14)},
           31: {'payment_amt_debt': -17123.21, 'payment_amt_proc': -1972.02, 'payment_dt': datetime.date(2026, 11, 13)},
           32: {'payment_amt_debt': -17437.13, 'payment_amt_proc': -1658.1, 'payment_dt': datetime.date(2026, 12, 13)},
           33: {'payment_amt_debt': -17756.81, 'payment_amt_proc': -1338.42, 'payment_dt': datetime.date(2027, 1, 12)},
           34: {'payment_amt_debt': -18082.35, 'payment_amt_proc': -1012.87, 'payment_dt': datetime.date(2027, 2, 11)},
           35: {'payment_amt_debt': -18413.86, 'payment_amt_proc': -681.36, 'payment_dt': datetime.date(2027, 3, 13)},
           36: {'payment_amt_debt': -18751.45, 'payment_amt_proc': -343.78, 'payment_dt': datetime.date(2027, 4, 12)}}

    periods = calc_periods(0.22, 36, 500000, datetime.date(2024, 4, 27))

    for i, values in ans.items():
        assert values["payment_amt_debt"] == periods[i]["payment_amt_debt"]
        assert values["payment_amt_proc"] == periods[i]["payment_amt_proc"]
        assert values["payment_dt"] == periods[i]["payment_dt"]
