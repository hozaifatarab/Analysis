# -*- coding: utf-8 -*-
# KPIs and exploratory aggregations for the e-commerce dataset.
import pandas as pd

def basic_kpis(orders):
    done = orders[orders['status'] == 'completed'] if 'status' in orders.columns else orders
    total_revenue = float(done['total'].sum())
    n_orders = int(len(done))
    aov = round(total_revenue / n_orders, 2) if n_orders else 0.0
    cancel_rate = 0.0
    if 'status' in orders.columns and len(orders):
        cancelled = (orders['status'] == 'cancelled').sum()
        cancel_rate = round(cancelled / len(orders) * 100, 2)
    return {
        'total_revenue': round(total_revenue, 2),
        'completed_orders': n_orders,
        'total_orders': int(len(orders)),
        'aov': aov,
        'cancel_rate_pct': cancel_rate,
        'unique_customers': int(orders['customer_id'].nunique()),
        'unique_products': int(orders['product_id'].nunique()),
    }

def monthly_sales(orders):
    done = orders[orders['status'] == 'completed']
    g = done.groupby('month').agg(revenue=('total', 'sum'), orders=('order_id', 'count'))
    return g.reset_index().sort_values('month')

def top_products(orders, products, n=10):
    done = orders[orders['status'] == 'completed']
    g = done.groupby('product_id').agg(qty=('quantity', 'sum'), revenue=('total', 'sum'),
                                       orders=('order_id', 'count'))
    g = g.reset_index().merge(products[['product_id', 'product_name', 'category']],
                              on='product_id', how='left')
    return g.sort_values('revenue', ascending=False).head(n)

def sales_by_category(orders, products):
    done = orders[orders['status'] == 'completed']
    m = done.merge(products[['product_id', 'category']], on='product_id', how='left')
    g = m.groupby('category').agg(revenue=('total', 'sum'), orders=('order_id', 'count'))
    return g.reset_index().sort_values('revenue', ascending=False)

def sales_by_city(orders):
    done = orders[orders['status'] == 'completed']
    g = done.groupby('city').agg(revenue=('total', 'sum'), orders=('order_id', 'count'),
                                 customers=('customer_id', 'nunique'))
    return g.reset_index().sort_values('revenue', ascending=False)

def payment_mix(orders):
    g = orders.groupby('payment_method').agg(orders=('order_id', 'count'),
                                             revenue=('total', 'sum'))
    return g.reset_index().sort_values('orders', ascending=False)

def status_mix(orders):
    g = orders.groupby('status').agg(orders=('order_id', 'count'), revenue=('total', 'sum'))
    return g.reset_index().sort_values('orders', ascending=False)

def repeat_customers(orders):
    done = orders[orders['status'] == 'completed']
    c = done.groupby('customer_id').size()
    return {'repeat_customers': int((c > 1).sum()), 'one_time': int((c == 1).sum())}
