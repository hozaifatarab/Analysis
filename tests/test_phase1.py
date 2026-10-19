# -*- coding: utf-8 -*-
import pandas as pd
from src import profit as P
from src import basket as B
from src import cohort as H
def _data():
    o=pd.DataFrame({'order_id':['O1','O2','O3'],'customer_id':['C1','C1','C2'],'product_id':['P1','P2','P1'],'quantity':[2,1,1],'price':[100.0,200.0,100.0],'total':[200.0,200.0,100.0],'status':['completed','completed','completed'],'order_date':pd.to_datetime(['2025-01-05','2025-02-05','2025-03-05']),'payment_method':['mada','visa','mada'],'city':['Riyadh','Riyadh','Jeddah'],'month':['2025-01','2025-02','2025-03']})
    pr=pd.DataFrame({'product_id':['P1','P2'],'product_name':['A','B'],'category':['c1','c2'],'price':[100.0,200.0],'cost':[60.0,150.0],'rating':[4.5,4.0]})
    return o,pr
def test_profit():
    o,pr=_data()
    enr=P.enrich(o,pr)
    assert 'line_profit' in enr.columns
    k=P.kpis(enr)
    assert k['gross_profit']==170.0
    assert k['margin_pct']==34.0
def test_basket():
    o,pr=_data()
    out=B.cooccurrence(o,min_support=1)
    assert len(out)>=1
def test_cohort():
    o,pr=_data()
    r=H.retention(o)
    assert len(r)>=1
