# -*- coding: utf-8 -*-
import pandas as pd
from src import deep_insights as DI
def _d():
    o = pd.DataFrame({'order_id': ['O1', 'O2', 'O3', 'O4'], 'customer_id': ['C1', 'C1', 'C2', 'C3'],
                      'product_id': ['P1', 'P2', 'P1', 'P1'], 'quantity': [1, 1, 1, 1],
                      'price': [100.0, 500.0, 100.0, 100.0], 'total': [100.0, 500.0, 100.0, 100.0],
                      'status': ['completed'] * 4, 'order_date': pd.to_datetime(['2025-01-05'] * 4),
                      'payment_method': ['mada'] * 4, 'city': ['Riyadh', 'Riyadh', 'Jeddah', 'Riyadh'],
                      'month': ['2025-01'] * 4})
    pr = pd.DataFrame({'product_id': ['P1', 'P2'], 'product_name': ['A', 'B'], 'category': ['c1', 'c2'],
                       'price': [100.0, 500.0], 'cost': [60.0, 300.0], 'rating': [4.0, 4.5]})
    cu = pd.DataFrame({'customer_id': ['C1', 'C2', 'C3'], 'name': ['a', 'b', 'c'],
                       'gender': ['male'] * 3, 'age': [30] * 3, 'city': ['Riyadh'] * 3,
                       'signup_date': pd.to_datetime(['2024-01-01'] * 3)})
    return o, pr, cu
def test_audit_quality():
    o, pr, cu = _d()
    q = DI.audit_quality(o, pr, cu)
    assert 'status' in q.columns and (q['status'] == 'pass').all()
def test_loyalty_deep():
    o, pr, cu = _d()
    rec, summ = DI.loyalty_deep(o)
    assert 'churn_risk' in rec.columns and len(summ) >= 1
def test_price_sensitivity():
    o, pr, cu = _d()
    tiers, corr = DI.price_sensitivity(o, pr)
    assert 'margin_pct' in tiers.columns and 'price_units_corr' in corr.columns
def test_growth_opps():
    o, pr, cu = _d()
    gaps, recv, ups = DI.growth_opportunities(o, pr)
    assert 'single_cat_buyers' in ups
