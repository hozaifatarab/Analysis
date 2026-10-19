# -*- coding: utf-8 -*-
import re
import pandas as pd
POS = ['good','great','excellent','love','fast','nice','perfect','recommended','happy','thanks','amazing','best','5','exceeded','awesome','wonderful','satisfied','ممتاز','رائع','جميل','ممتازة','سريع','شكرا','احببته','مفيد','جيد','مريح','اصلي']
NEG = ['bad','poor','slow','late','broken','wrong','refund','complaint','disappointed','worst','terrible','damaged','missing','1','awful','horrible','useless','defect','سيء','سئ','رديء','تالف','مكسور','متأخر','بطيء','خسارة','استرداد','شكوى','مخيب','سيئه','غلط','ناقص']
def score_text(t):
    s = str(t)
    sl = s.lower()
    words = re.findall(r'[a-z\u0600-\u06ff]+', sl)
    p = sum(1 for x in words if x in POS)
    n = sum(1 for x in words if x in NEG)
    m = re.search(r'([1-5])(?:/5| stars?)?', sl)
    if m:
        v = int(m.group(1))
        if v >= 4:
            p += 2
        elif v <= 2:
            n += 2
    if p > n:
        return 'positive'
    if n > p:
        return 'negative'
    return 'neutral'
def analyze(df, text_col='review'):
    d = df.copy()
    if text_col not in d.columns:
        # fallback: last text column
        text_col = d.columns[-1]
    d['sentiment'] = d[text_col].apply(score_text)
    s = d.groupby('sentiment').size().reset_index(name='n')
    out = {'summary': s, 'detail': d}
    if 'product_id' in d.columns:
        g = d.groupby(['product_id', 'sentiment']).size().unstack(fill_value=0)
        for c in ['positive', 'negative', 'neutral']:
            if c not in g.columns:
                g[c] = 0
        g['total'] = g['positive'] + g['negative'] + g['neutral']
        g['neg_rate'] = (g['negative'] / g['total'].replace(0, 1) * 100).round(1)
        g['pos_rate'] = (g['positive'] / g['total'].replace(0, 1) * 100).round(1)
        out['by_product'] = g.reset_index().sort_values('neg_rate', ascending=False)
    return out
def overall_health(summary):
    # summary: DataFrame with sentiment/n
    tot = int(summary['n'].sum()) if len(summary) else 0
    if not tot:
        return {'total': 0, 'pos_pct': 0.0, 'neg_pct': 0.0, 'verdict': 'no_reviews'}
    pos = int(summary.loc[summary['sentiment'] == 'positive', 'n'].sum()) if 'positive' in summary['sentiment'].values else 0
    neg = int(summary.loc[summary['sentiment'] == 'negative', 'n'].sum()) if 'negative' in summary['sentiment'].values else 0
    pp = round(pos / tot * 100, 1)
    np_ = round(neg / tot * 100, 1)
    verdict = 'healthy' if np_ < 20 else ('watch' if np_ < 40 else 'critical')
    return {'total': tot, 'pos_pct': pp, 'neg_pct': np_, 'verdict': verdict}

