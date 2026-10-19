# -*- coding: utf-8 -*-
# Data cleaning: missing values, duplicates, types, derived columns.
import pandas as pd

def clean_orders(df):
    df = df.copy()
    df = df.drop_duplicates(subset=['order_id'])
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date', 'customer_id', 'product_id'])
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1)
    df = df[df['quantity'] > 0]
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    df['payment_method'] = df['payment_method'].fillna('unknown')
    df['status'] = df['status'].fillna('unknown')
    df['city'] = df['city'].fillna('unknown')
    df['total'] = (df['quantity'] * df['price']).round(2)
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    return df.reset_index(drop=True)

def clean_products(df):
    df = df.copy().drop_duplicates(subset=['product_id'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').clip(1, 5)
    df['category'] = df['category'].fillna('unknown')
    return df.reset_index(drop=True)

def clean_customers(df):
    df = df.copy().drop_duplicates(subset=['customer_id'])
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['gender'] = df['gender'].fillna('unknown')
    df['city'] = df['city'].fillna('unknown')
    return df.reset_index(drop=True)
