# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
from config import settings as S
DB = S.BASE_DIR / 'data' / 'processed' / 'store.db'
def _ensure_runs_table(con):
    try:
        cols = [r[1] for r in con.execute('PRAGMA table_info(runs)').fetchall()]
        for c in ['repeat_customers', 'one_time']:
            if c not in cols:
                con.execute(f'ALTER TABLE runs ADD COLUMN {c} REAL')
        con.commit()
    except Exception:
        pass
def save_run(orders, products, kpis, tag='manual', rfm=None, profit=None, recs=None):
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    _ensure_runs_table(con)
    orders.to_sql('orders', con, if_exists='replace', index=False)
    products.to_sql('products', con, if_exists='replace', index=False)
    try:
        pd.DataFrame([dict(kpis, tag=tag)]).to_sql('runs', con, if_exists='append', index=False)
    except Exception:
        # schema drift (old DB): rebuild runs table then append
        con.execute('DROP TABLE IF EXISTS runs')
        pd.DataFrame([dict(kpis, tag=tag)]).to_sql('runs', con, if_exists='append', index=False)
    if rfm is not None and len(rfm):
        rfm.to_sql('rfm', con, if_exists='replace', index=False)
    if profit is not None:
        pd.DataFrame([profit]).to_sql('profit', con, if_exists='replace', index=False)
    if recs is not None and len(recs):
        recs.to_sql('recommendations', con, if_exists='replace', index=False)
    con.close()
    return str(DB)
def run_history(limit=50):
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    try:
        df = pd.read_sql(f'select * from runs order by rowid desc limit {int(limit)}', con)
    except Exception:
        df = pd.DataFrame()
    con.close()
    return df
def kpi_trend(metric='total_revenue'):
    h = run_history(100)
    if len(h) and metric in h.columns:
        return h[['tag', metric]].reset_index(drop=True)
    return pd.DataFrame()

