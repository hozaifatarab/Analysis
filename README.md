# E-commerce Data Analysis (Python + Matplotlib + Streamlit)

## Idea
Pipeline that loads store data, cleans it, computes KPIs, draws Arabic charts, and exports Excel/PDF reports + interactive Arabic dashboard.

## Structure
```
main.py
config/settings.py
src/data_loader.py
src/data_cleaning.py
src/analysis.py
src/visualization.py
src/report.py
src/rfm.py
src/forecast.py
src/profit.py
src/basket.py
src/cohort.py
src/anomaly.py
src/restock.py
src/store_db.py
src/pdf_report.py
src/assistant.py
src/recommender.py
src/sentiment.py
dashboard.py
scripts/generate_sample_data.py
data/raw/  data/processed/  data/reports/
tests/
DATA_GUIDE.md
```

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python scripts/generate_sample_data.py
python main.py --tag manual
python -m pytest tests/ -q
streamlit run dashboard.py
```

## Outputs
- 18 PNG charts in data/reports (Arabic labels): monthly, top products, category, city, payment, price hist, price-rating, RFM x2, forecast, profit x2, cohort, anomaly, daily orders, margin-vs-revenue, restock, sentiment
- ecommerce_report.xlsx with 21 styled sheets (KPIs, Monthly, TopProducts, Categories, Cities, Payments, Status, Profit, ProfitProducts, ProfitCats, Basket, Cohort, Forecast, ForecastSeries, RFM, RFM_Segments, Restock, Sentiment, SentimentByProd, Alerts, Recommend, Repeat)
- weekly_report.pdf (KPI cover + top actions + key charts)
- store.db (SQLite: orders/products/runs/rfm/profit/recommendations + run history)
- orders_clean.csv + rfm.csv in data/processed

## KPIs
- Total revenue, completed orders, AOV, cancel rate, repeat customers
- Monthly sales, top products, categories, cities
- Payment mix, order status, repeat customers
- RFM segments (champions/loyal/potential/at-risk/lost) + 3-month sales forecast
- Profit (net/margin/cost/returns) + basket pairs + cohort retention + period compare
- Daily anomaly alerts + cancel-day alerts + restock plan + SQLite history + weekly PDF
- AI: Arabic Q&A assistant (AR+EN, 15 intents incl. forecast/RFM/restock/alerts/cohort) + 10-rule auto recommendations + AR/EN review sentiment
