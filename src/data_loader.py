# -*- coding: utf-8 -*-
# Helpers to load raw CSV files.
import pandas as pd
from config import settings as S

def load_csv(path, **kwargs):
    opts = {'encoding': S.CSV_ENCODING}
    opts.update(kwargs)
    return pd.read_csv(path, **opts)

def load_orders(path=None):
    return load_csv(path or S.ORDERS_FILE, parse_dates=['order_date'])

def load_products(path=None):
    return load_csv(path or S.PRODUCTS_FILE)

def load_customers(path=None):
    return load_csv(path or S.CUSTOMERS_FILE, parse_dates=['signup_date'])

def load_all():
    return {
        'orders': load_orders(),
        'products': load_products(),
        'customers': load_customers(),
    }
