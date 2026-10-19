# -*- coding: utf-8 -*-
import pandas as pd
from src import assistant as S
from src import recommender as R
from src import sentiment as T
def _data():
    o=pd.DataFrame({'order_id':['O1','O2'],'customer_id':['C1','C2'],'product_id':['P1','P2'],'quantity':[1,1],'price':[100.0,200.0],'total':[100.0,200.0],'status':['completed','completed'],'order_date':pd.to_datetime(['2025-01-05','2025-02-05']),'payment_method':['mada','visa'],'city':['Riyadh','Jeddah'],'month':['2025-01','2025-02']})
    pr=pd.DataFrame({'product_id':['P1','P2'],'product_name':['A','B'],'category':['c1','c2'],'price':[100.0,200.0],'cost':[95.0,50.0],'rating':[4.0,4.5]})
    return o,pr
def test_assistant():
    o,pr=_data()
    k,_,t=S.answer('profit in riyadh',o,pr)
    assert k=='profit'
    k2,_,t2=S.answer('top products',o,pr)
    assert k2=='table'
def test_recommender():
    o,pr=_data()
    r=R.recommend(o,pr)
    assert len(r)>=1 and 'text' in r.columns
def test_sentiment():
    df=pd.DataFrame({'product_id':['P1','P1','P2'],'review':['great love it 5 stars','terrible broken refund','ok fine']})
    out=T.analyze(df)
    assert len(out['summary'])>=2
    assert 'neg_rate' in out['by_product'].columns
