# Use your real data

## 1. Replace files in data/raw/
- orders.csv columns: order_id, customer_id, product_id, quantity, price, order_date (YYYY-MM-DD), payment_method, status, city
- products.csv columns: product_id, product_name, category, price, cost, rating
- customers.csv columns: customer_id, name, gender, age, city, signup_date (YYYY-MM-DD)
- Save with UTF-8-SIG encoding (Excel Arabic safe).

## 2. Run
```bash
python main.py
```

## 3. Notes
- status values: completed / cancelled / returned
- Missing values are auto-filled by data_cleaning.py
- Extra columns are ignored safely
