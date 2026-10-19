# -*- coding: utf-8 -*-
import pandas as pd
def retention(orders, periods=6):
    d=orders[orders['status']=='completed'].copy()
    d['order_date']=pd.to_datetime(d['order_date'])
    d['om']=d['order_date'].dt.to_period('M')
    first=d.groupby('customer_id')['om'].min().rename('cohort')
    d=d.merge(first,on='customer_id')
    d['age']=(d['om']-d['cohort']).apply(lambda x:x.n)
    d=d[d['age']<periods]
    piv=d.pivot_table(index='cohort',columns='age',values='customer_id',aggfunc=pd.Series.nunique)
    base=piv.iloc[:,0]
    return (piv.divide(base,axis=0)*100).round(1)
def compare_periods(orders, p1, p2):
    d=orders[orders['status']=='completed'].copy()
    d['order_date']=pd.to_datetime(d['order_date'])
    s1=pd.to_datetime(p1[0]); e1=pd.to_datetime(p1[1])
    s2=pd.to_datetime(p2[0]); e2=pd.to_datetime(p2[1])
    a=d[(d['order_date']>=s1)&(d['order_date']<=e1)]
    b=d[(d['order_date']>=s2)&(d['order_date']<=e2)]
    def k(x):
        return {'revenue':round(float(x['total'].sum()),2),'orders':int(len(x)),'customers':int(x['customer_id'].nunique()),'aov':round(float(x['total'].sum())/len(x),2) if len(x) else 0.0}
    r1=k(a); r2=k(b)
    out={}
    for kk in r1:
        dlt=round(r2[kk]-r1[kk],2)
        pct=round(dlt/r1[kk]*100,2) if r1[kk] else 0.0
        out[kk]={'p1':r1[kk],'p2':r2[kk],'delta':dlt,'pct':pct}
    return out
