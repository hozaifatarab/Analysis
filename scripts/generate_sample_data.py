# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pathlib import Path
SEED = 42
rng = np.random.default_rng(SEED)
RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
PRODUCTS = [
 ('P001','laptop Pro 15','electronics',4200.0,3100.0),
 ('P002','smart phone X','electronics',2600.0,1900.0),
 ('P003','wireless earbuds','electronics',350.0,210.0),
 ('P004','smart watch S','electronics',900.0,620.0),
 ('P005','running shoes','fashion',480.0,260.0),
 ('P006','cotton shirt','fashion',160.0,80.0),
 ('P007','leather wallet','fashion',220.0,110.0),
 ('P008','sunglasses classic','fashion',300.0,150.0),
 ('P009','arabic coffee set','home',260.0,150.0),
 ('P010','non-stick pot set','home',520.0,330.0),
 ('P011','table lamp LED','home',180.0,100.0),
 ('P012','bedding set','home',200.0,200.0),
 ('P013','vitamin C serum','beauty',140.0,70.0),
 ('P014','hair dryer Pro','beauty',320.0,190.0),
 ('P015','kids building blocks','toys',200.0,110.0),
 ('P016','board game family','toys',150.0,80.0),
]
products = pd.DataFrame(PRODUCTS, columns=['product_id','product_name','category','price','cost'])
products['rating'] = np.round(rng.uniform(3.4, 4.9, len(products)), 1)
CITIES = ['Riyadh','Jeddah','Dammam','Mecca','Medina','Abha']
CITY_W = [0.32,0.24,0.14,0.12,0.10,0.08]
N_CUSTOMERS, N_ORDERS = 600, 2500
cust_ids = [f'C{i:04d}' for i in range(1, N_CUSTOMERS+1)]
customers = pd.DataFrame({
 'customer_id': cust_ids,
 'name': [f'customer {i}' for i in range(1, N_CUSTOMERS+1)],
 'gender': rng.choice(['male','female'], N_CUSTOMERS, p=[0.52,0.48]),
 'age': rng.integers(18, 65, N_CUSTOMERS),
 'city': rng.choice(CITIES, N_CUSTOMERS, p=CITY_W),
 'signup_date': pd.to_datetime(rng.integers(1704067200, 1748736000, N_CUSTOMERS), unit='s').date,
})
price_map = dict(zip(products['product_id'], products['price']))
pop = np.array([14,13,11,10,8,7,6,5,6,5,3,3,4,3,3,3], dtype=float)
pop = pop / pop.sum()
orders = pd.DataFrame({
 'order_id': [f'O{i:05d}' for i in range(1, N_ORDERS+1)],
 'customer_id': rng.choice(cust_ids, N_ORDERS),
 'product_id': rng.choice(products['product_id'].tolist(), N_ORDERS, p=pop),
 'quantity': rng.choice([1,1,1,2,2,3], N_ORDERS),
 'order_date': pd.to_datetime(rng.integers(1735689600, 1767225600, N_ORDERS), unit='s'),
 'payment_method': rng.choice(['mada','visa','apple_pay','cod'], N_ORDERS, p=[0.42,0.34,0.14,0.10]),
 'status': rng.choice(['completed']*4 + ['cancelled','returned'], N_ORDERS),
})
orders['city'] = orders['customer_id'].map(dict(zip(customers['customer_id'], customers['city'])))
orders['price'] = orders['product_id'].map(price_map)
orders['order_date'] = pd.to_datetime(orders['order_date']).dt.strftime('%Y-%m-%d')
orders = orders[['order_id','customer_id','product_id','quantity','price','order_date','payment_method','status','city']]
print('WROTE', len(orders), len(products), len(customers))
orders.to_csv(RAW/'orders.csv', index=False, encoding='utf-8-sig')
products.to_csv(RAW/'products.csv', index=False, encoding='utf-8-sig')
customers.to_csv(RAW/'customers.csv', index=False, encoding='utf-8-sig')
print('DONE')
