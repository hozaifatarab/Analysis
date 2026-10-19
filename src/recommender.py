# -*- coding: utf-8 -*-
import pandas as pd
def _pct(a, b):
    return round((a - b) / b * 100, 1) if b else 0.0
def recommend(orders, products, monthly=None, alerts=None, sentiment_out=None, restock_df=None):
    from src import profit as P, analysis as A
    recs = []

    def add(area, level, text, value=None):
        recs.append({'area': area, 'level': level, 'text': text, 'value': value})
    enr = P.enrich(orders, products)
    pp = P.by_product(enr, products)
    pc = P.by_category(enr)
    # 1) low margin products
    for _, r in pp[pp['margin_pct'] < 10].head(5).iterrows():
        add('pricing', 'warn', f"Low margin {r['margin_pct']}% on {r['product_name']} (profit {r['profit']:,.0f}) - review price or cost", r['margin_pct'])
    # 1b) loss-making
    loss = pp[pp['profit'] <= 0]
    for _, r in loss.head(3).iterrows():
        add('pricing', 'bad', f"LOSS on {r['product_name']}: revenue {r['revenue']:,.0f} < cost {r['cost']:,.0f} - stop discount immediately", r['profit'])
    # 2) promote high margin
    hi = pp.sort_values('margin_pct', ascending=False).head(3)
    for _, r in hi.iterrows():
        add('promote', 'good', f"Push {r['product_name']} (margin {r['margin_pct']}%) in campaigns", r['margin_pct'])
    # 3) weak category
    if len(pc) >= 2:
        worst = pc.iloc[-1]
        best = pc.iloc[0]
        if best['revenue'] and worst['revenue'] / best['revenue'] < 0.15:
            add('promote', 'warn', f"Weak category '{worst['category']}': only {worst['revenue']:,.0f} vs {best['category']} {best['revenue']:,.0f} - bundle or discount it", worst['revenue'])
    # 4) cancel / return rates
    st = A.status_mix(orders)
    tot = float(st['orders'].sum()) if len(st) else 0
    c = float(st.loc[st['status'] == 'cancelled', 'orders'].sum()) / tot * 100 if tot else 0
    if c > 15:
        add('ops', 'warn', f'Cancel rate {c:.1f}% is high - audit payment failures and stock', round(c, 1))
    r_ = float(st.loc[st['status'] == 'returned', 'orders'].sum()) / tot * 100 if tot else 0
    if r_ > 10:
        add('ops', 'warn', f'Return rate {r_:.1f}% is high - check sizing/descriptions/QC', round(r_, 1))
    # 5) concentration risk: top product share
    if len(pp) and pp['revenue'].sum():
        share = pp.iloc[0]['revenue'] / pp['revenue'].sum() * 100
        if share > 40:
            add('ops', 'warn', f"Concentration risk: {pp.iloc[0]['product_name']} = {share:.1f}% of revenue - diversify", round(share, 1))
    # 6) repeat purchase
    rep = A.repeat_customers(orders)
    tot_c = rep['repeat_customers'] + rep['one_time']
    if tot_c:
        rp = rep['repeat_customers'] / tot_c * 100
        if rp < 25:
            add('growth', 'warn', f'Low repeat rate {rp:.1f}% ({rep["repeat_customers"]}/{tot_c}) - launch loyalty program', round(rp, 1))
        elif rp > 45:
            add('growth', 'good', f'Strong loyalty {rp:.1f}% repeat customers - upsell bundles', round(rp, 1))
    # 7) monthly momentum
    if monthly is not None and len(monthly) >= 2:
        last = float(monthly['revenue'].iloc[-1])
        prev = float(monthly['revenue'].iloc[-2])
        ch = _pct(last, prev)
        if ch < -10:
            add('growth', 'warn', f'Monthly revenue down {ch:.1f}% - launch retention offer', ch)
        elif ch > 10:
            add('growth', 'good', f'Monthly revenue up {ch:.1f}% - scale winning channel', ch)
    # 8) anomaly days
    if alerts is not None and len(alerts):
        add('alerts', 'warn', f'{len(alerts)} anomaly days detected - review causes', len(alerts))
    # 9) sentiment-driven
    if sentiment_out and 'by_product' in sentiment_out:
        bp = sentiment_out['by_product']
        bad = bp[bp['neg_rate'] >= 40].head(3) if len(bp) else bp.head(0)
        for _, r in bad.iterrows():
            add('quality', 'bad', f"Negative reviews {r['neg_rate']}% on {r['product_id']} - inspect quality & listing", r['neg_rate'])
    # 10) restock urgency
    if restock_df is not None and len(restock_df):
        top_r = restock_df.head(3)
        for _, r in top_r.iterrows():
            add('stock', 'warn', f"Restock {r.get('product_name', r['product_id'])}: daily {float(r['daily']):.2f}, reorder point {float(r['reorder_point']):.1f}", float(r['daily']))
    if not recs:
        return pd.DataFrame([{'area': 'ok', 'level': 'good', 'text': 'No issues - store is healthy', 'value': None}])
    order = {'bad': 0, 'warn': 1, 'good': 2}
    out = pd.DataFrame(recs)
    out['rank'] = out['level'].map(order)
    return out.sort_values('rank').drop(columns='rank').reset_index(drop=True)

