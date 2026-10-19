# -*- coding: utf-8 -*-
from itertools import combinations
import pandas as pd
def cooccurrence(orders, min_support=3):
    d=orders[orders['status']=='completed']
    cust=d.groupby('customer_id')['product_id'].apply(lambda s:sorted(set(s)))
    pair={}; single={}
    for items in cust:
        for i in items:
            single[i]=single.get(i,0)+1
        for a,b in combinations(items,2):
            pair[(a,b)]=pair.get((a,b),0)+1
    rows=[]
    for (a,b),n in pair.items():
        if n>=min_support:
            rows.append({'A':a,'B':b,'together':n,'conf_A_B':round(n/single[a],3),'conf_B_A':round(n/single[b],3)})
    out=pd.DataFrame(rows)
    if len(out):
        out=out.sort_values('together',ascending=False)
    return out.reset_index(drop=True)
