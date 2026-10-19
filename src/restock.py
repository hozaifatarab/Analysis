# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
def demand(orders, products, lead_days=7, safety_days=7):
    d=orders[orders['status']=='completed'].copy()
    d['order_date']=pd.to_datetime(d['order_date'])
    span=(d['order_date'].max()-d['order_date'].min()).days or 1
    q=d.groupby('product_id')['quantity'].sum().reset_index()
    q=q.merge(products[['product_id','product_name']],on='product_id',how='left')
    q['daily']=q['quantity']/span
    q['reorder_point']=(q['daily']*(lead_days+safety_days)).round(1)
    q['order_qty']=(q['daily']*30).round(0)
    return q.sort_values('daily',ascending=False)
