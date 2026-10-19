# -*- coding: utf-8 -*-
"""Deep insights: loyalty, price sensitivity, growth gaps, data quality.
Methodology: Intent -> definitions -> bounded analysis -> findings.
"""
import pandas as pd
import numpy as np


def audit_quality(orders, products, customers=None):
    rows = []

    def add(check, scope, issues, detail):
        rows.append({'check': check, 'scope': scope, 'issues': int(issues), 'detail': detail})
    add('duplicate order_id', 'orders', orders.duplicated('order_id').sum(), 'double-count risk')
    add('missing customer/product', 'orders',
        int(orders['customer_id'].isna().sum() + orders['product_id'].isna().sum()), 'unjoinable rows')
    add('bad quantity', 'orders', int(((orders['quantity'] <= 0) | orders['quantity'].isna()).sum()), 'invalid sizes')
    add('bad price', 'orders', int((orders['price'].isna() | (orders['price'] <= 0)).sum()), 'breaks revenue')
    add('bad order_date', 'orders', int(pd.to_datetime(orders['order_date'], errors='coerce').isna().sum()), 'breaks series')
    add('unknown product_id', 'orders-vs-products', int((~orders['product_id'].isin(products['product_id'])).sum()), 'no cost/cat')
    neg = int((products['cost'] > products['price']).sum()) if 'cost' in products.columns else 0
    add('cost > price', 'products', neg, 'loss makers')
    if customers is not None:
        add('unknown customer_id', 'orders-vs-customers', int((~orders['customer_id'].isin(customers['customer_id'])).sum()), 'breaks RFM')
        add('duplicate customer_id', 'customers', customers.duplicated('customer_id').sum(), 'identity collision')
    out = pd.DataFrame(rows)
    out['status'] = np.where(out['issues'] == 0, 'pass', 'needs_fix')
    return out


def loyalty_deep(orders):
    done = orders[orders['status'] == 'completed'].copy()
    done['order_date'] = pd.to_datetime(done['order_date'])
    g = done.sort_values(['customer_id', 'order_date']).groupby('customer_id')
    rec = g.agg(orders=('order_id', 'count'), revenue=('total', 'sum'),
                first=('order_date', 'min'), last=('order_date', 'max')).reset_index()

    def _gap(dates):
        d = pd.to_datetime(dates).sort_values()
        if len(d) < 2:
            return np.nan
        return d.diff().dt.days.dropna().mean()
    gaps = done.groupby('customer_id')['order_date'].apply(_gap).rename('avg_gap_days')
    rec = rec.merge(gaps, on='customer_id', how='left')
    ref = done['order_date'].max()
    rec['days_since_last'] = (ref - rec['last']).dt.days
    rec['churn_risk'] = np.where(
        ((rec['orders'] == 1) & (rec['days_since_last'] > 90)) |
        ((rec['orders'] > 1) & (rec['days_since_last'] > rec['avg_gap_days'] * 3)),
        'high', np.where(rec['days_since_last'] > 60, 'medium', 'low'))
    summary = rec.groupby('churn_risk').agg(customers=('customer_id', 'count'),
                                            revenue=('revenue', 'sum')).reset_index()
    return rec, summary


def price_sensitivity(orders, products):
    enr = orders[orders['status'] == 'completed'].merge(
        products[['product_id', 'product_name', 'category', 'cost']], on='product_id', how='left')
    enr['line_profit'] = enr['total'] - enr['quantity'] * enr['cost'].fillna(0)
    try:
        enr['price_tier'] = pd.qcut(enr['price'], 4, labels=['budget', 'mid', 'premium', 'luxury'],
                                    duplicates='drop')
    except Exception:
        enr['price_tier'] = pd.cut(enr['price'].rank(method='first'), 4,
                                   labels=['budget', 'mid', 'premium', 'luxury'])
    t = enr.groupby('price_tier', observed=True).agg(orders=('order_id', 'count'),
                                                      revenue=('total', 'sum'),
                                                      profit=('line_profit', 'sum'),
                                                      avg_price=('price', 'mean')).reset_index()
    t['margin_pct'] = (t['profit'] / t['revenue'].replace(0, np.nan) * 100).round(1)
    t['share_orders'] = (t['orders'] / t['orders'].sum() * 100).round(1)
    cat = products.merge(orders[orders['status'] == 'completed'].groupby('product_id')['quantity']
                         .sum().rename('units'), on='product_id', how='left').fillna({'units': 0})
    corr = cat.groupby('category')[['price', 'units']].apply(
        lambda d: round(d['price'].corr(d['units']), 2) if len(d) > 2 else np.nan).reset_index()
    corr.columns = ['category', 'price_units_corr']
    return t.sort_values('revenue', ascending=False), corr


def growth_opportunities(orders, products, rfm_seg=None):
    done = orders[orders['status'] == 'completed']
    mix = done.merge(products[['product_id', 'category']], on='product_id', how='left')
    pivot = mix.pivot_table(index='city', columns='category', values='total', aggfunc='sum', fill_value=0)
    gaps = []
    for city in pivot.index:
        for cat in pivot.columns:
            if pivot.loc[city, cat] == 0 and pivot[cat].sum() > 0:
                gaps.append({'city': city, 'missing_category': cat,
                             'cat_revenue_elsewhere': round(float(pivot[cat].sum()), 2)})
    gaps = pd.DataFrame(gaps)
    if len(gaps):
        gaps = gaps.sort_values('cat_revenue_elsewhere', ascending=False)
    recoverable = None
    if rfm_seg is not None and len(rfm_seg):
        recoverable = rfm_seg[rfm_seg['segment'].isin(['at_risk', 'lost'])][['segment', 'customers', 'revenue']]
    cust_cats = mix.groupby('customer_id')['category'].nunique().rename('n_cats')
    single = int((cust_cats == 1).sum())
    multi = int((cust_cats > 1).sum())
    return gaps.head(10), recoverable, {'single_cat_buyers': single, 'multi_cat_buyers': multi}
