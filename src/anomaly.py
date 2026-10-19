# -*- coding: utf-8 -*-
import pandas as pd
def daily_series(orders):
    d=orders[orders['status']=='completed'].copy()
    d['order_date']=pd.to_datetime(d['order_date'])
    g=d.groupby(d['order_date'].dt.date).agg(revenue=('total','sum'),orders=('order_id','count'),cancel_share=('status',lambda s:0.0))
    g=g.reset_index().rename(columns={'order_date':'day'})
    g['day']=pd.to_datetime(g['day'])
    return g.sort_values('day')
def zscore_flags(series, col='revenue', window=14, thresh=2.0):
    s=series.copy()
    m=s[col].rolling(window, min_periods=7).mean()
    sd=s[col].rolling(window, min_periods=7).std().fillna(0)
    s['z']=((s[col]-m)/sd.replace(0,1)).round(2)
    s['flag']='ok'
    s.loc[s['z']>=thresh,'flag']='spike'
    s.loc[s['z']<=-thresh,'flag']='drop'
    return s
def cancel_alerts(orders, thresh_pct=25.0):
    g=orders.groupby(orders['order_date'].astype(str)).agg(t=('order_id','count'),c=('status',lambda s:(s=='cancelled').sum()))
    g=g.reset_index().rename(columns={'order_date':'day'})
    g['cancel_pct']=(g['c']/g['t']*100).round(2)
    return g[g['cancel_pct']>=thresh_pct]
