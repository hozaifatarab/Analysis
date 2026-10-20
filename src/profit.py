# -*- coding: utf-8 -*-
import pandas as pd
def enrich(orders, products):
    prod_cols = ['product_id', 'category']
    if 'cost' in products.columns:
        prod_cols.insert(1, 'cost')
    m = orders.merge(products[prod_cols], on='product_id', how='left')
    m['cost'] = m['cost'].fillna(0) if 'cost' in m.columns else 0.0
    m['line_cost'] = (m['quantity'] * m['cost']).round(2)
    m['line_profit'] = (m['total'] - m['line_cost']).round(2)
    return m
def kpis(enr):
    d=enr[enr['status']=='completed']
    rev=float(d['total'].sum()); cost=float(d['line_cost'].sum())
    prof=round(rev-cost,2)
    mg=round(prof/rev*100,2) if rev else 0.0
    r=enr[enr['status']=='returned']
    rloss=round(float((r['line_cost']*0.15+r['total']*0.02).sum()),2)
    return {'revenue':round(rev,2),'cost':round(cost,2),'gross_profit':prof,'margin_pct':mg,'return_loss':rloss,'net_profit':round(prof-rloss,2)}
def by_product(enr,products):
    d=enr[enr['status']=='completed']
    g=d.groupby('product_id').agg(revenue=('total','sum'),cost=('line_cost','sum'),orders=('order_id','count'),qty=('quantity','sum'))
    g=g.reset_index()
    g['profit']=(g['revenue']-g['cost']).round(2)
    g['margin_pct']=(g['profit']/g['revenue']*100).round(2)
    g=g.merge(products[['product_id','product_name','category']],on='product_id',how='left')
    return g.sort_values('profit',ascending=False)
def by_category(enr):
    d=enr[enr['status']=='completed']
    g=d.groupby('category').agg(revenue=('total','sum'),cost=('line_cost','sum'),orders=('order_id','count'))
    g=g.reset_index()
    g['profit']=(g['revenue']-g['cost']).round(2)
    g['margin_pct']=(g['profit']/g['revenue']*100).round(2)
    return g.sort_values('profit',ascending=False)
