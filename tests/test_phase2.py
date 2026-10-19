# -*- coding: utf-8 -*-
import pandas as pd
from src import anomaly as N
from src import restock as Q
def _o():
    return pd.DataFrame({'order_id':[f'O{i}' for i in range(20)],'customer_id':['C1']*20,'product_id':['P1']*20,'quantity':[1]*20,'price':[100.0]*20,'total':[100.0]*19+[900.0],'status':['completed']*20,'order_date':pd.to_datetime([f'2025-01-{d:02d}' for d in range(1,21)]),'payment_method':['mada']*20,'city':['Riyadh']*20,'month':['2025-01']*20})
def test_flags():
    s=N.zscore_flags(N.daily_series(_o()))
    assert 'flag' in s.columns
    assert (s['flag']!='ok').any()
def test_demand():
    pr=pd.DataFrame({'product_id':['P1'],'product_name':['A']})
    d=Q.demand(_o(),pr)
    assert 'reorder_point' in d.columns
