# -*- coding: utf-8 -*-
import pandas as pd
from src import analysis as A
def test_basic_kpis():
    df = pd.DataFrame({
        'order_id': ['O1', 'O2', 'O3'],
        'customer_id': ['C1', 'C1', 'C2'],
        'product_id': ['P1', 'P2', 'P1'],
        'quantity': [1, 2, 1],
        'price': [100.0, 50.0, 100.0],
        'total': [100.0, 100.0, 100.0],
        'status': ['completed', 'completed', 'cancelled'],
    })
    k = A.basic_kpis(df)
    assert k['total_revenue'] == 200.0
    assert k['completed_orders'] == 2
    assert k['aov'] == 100.0
