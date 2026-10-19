# -*- coding: utf-8 -*-
import pandas as pd
from src import rfm as F
from src import forecast as O
def _orders():
    return pd.DataFrame({
        'order_id': [f'O{i}' for i in range(12)],
        'customer_id': ['C1'] * 6 + ['C2'] * 6,
        'product_id': ['P1'] * 12,
        'quantity': [1] * 12,
        'price': [100.0] * 12,
        'total': [100.0] * 12,
        'status': ['completed'] * 12,
        'order_date': pd.to_datetime([f'2025-{m:02d}-05' for m in range(1, 7)] * 2),
    })
def test_rfm_segments():
    r = F.compute_rfm(_orders())
    assert set(['R', 'F', 'M', 'segment']) <= set(r.columns)
    assert len(r) == 2
def test_forecast():
    s = O.monthly_series(_orders())
    comb, info = O.linear_forecast(s, 2)
    assert len(comb) == len(s) + 2
    assert 'mae' in info
