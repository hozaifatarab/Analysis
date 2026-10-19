# -*- coding: utf-8 -*-
# Central project settings.
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / 'data' / 'raw'
DATA_PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
DATA_REPORTS_DIR = BASE_DIR / 'data' / 'reports'

ORDERS_FILE = DATA_RAW_DIR / 'orders.csv'
PRODUCTS_FILE = DATA_RAW_DIR / 'products.csv'
CUSTOMERS_FILE = DATA_RAW_DIR / 'customers.csv'

PROCESSED_ORDERS_FILE = DATA_PROCESSED_DIR / 'orders_clean.csv'
EXCEL_REPORT_FILE = DATA_REPORTS_DIR / 'ecommerce_report.xlsx'

CSV_ENCODING = 'utf-8-sig'
RANDOM_SEED = 42
CHART_DPI = 130
TOP_N_PRODUCTS = 10
CURRENCY = 'r.s'
