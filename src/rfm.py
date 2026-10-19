# -*- coding: utf-8 -*-
import pandas as pd
def compute_rfm(orders, ref_date=None):
    done = orders[orders['status'] == 'completed'].copy()
    ref = pd.to_datetime(ref_date) if ref_date else done['order_date'].max()
    g = done.groupby('customer_id').agg(last=('order_date', 'max'), freq=('order_id', 'count'), monetary=('total', 'sum'))
    g = g.reset_index()
    g['recency'] = (ref - g['last']).dt.days
    for col, asc, name in [('recency', False, 'R'), ('freq', True, 'F'), ('monetary', True, 'M')]:
        try:
            g[name] = pd.qcut(g[col], 5, labels=[1, 2, 3, 4, 5], duplicates='drop').astype(int)
        except Exception:
            g[name] = pd.cut(g[col].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        if not asc:
            g[name] = 6 - g[name]
    g['score'] = g['R'] + g['F'] + g['M']
    def seg(r):
        s = r['score']
        if s >= 13: return 'champions'
        if s >= 11: return 'loyal'
        if s >= 9: return 'potential'
        if s >= 6: return 'at_risk'
        return 'lost'
    g['segment'] = g.apply(seg, axis=1)
    return g
def segment_summary(rfm):
    g = rfm.groupby('segment').agg(customers=('customer_id', 'count'), revenue=('monetary', 'sum'), avg_recency=('recency', 'mean'))
    return g.reset_index().sort_values('revenue', ascending=False)
