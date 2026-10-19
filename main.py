# -*- coding: utf-8 -*-
import io
import sys
from pathlib import Path
# Fix Windows console encoding for Arabic paths (cp1252 -> utf-8)
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import data_loader as L
from src import data_cleaning as C
from src import analysis as A
from src import visualization as V
from src import report as R
from src import rfm as F
from src import forecast as O
from src import profit as P
from src import basket as B
from src import cohort as H
from src import anomaly as N
from src import restock as Q
from src import store_db as D
from src import pdf_report as PR
from src import assistant as SA
from src import recommender as RC
from src import sentiment as SE
from src import deep_insights as DI
from config import settings as S
def main(tag='manual'):
    print('== E-commerce analysis ==')
    raw = L.load_all()
    orders = C.clean_orders(raw['orders'])
    products = C.clean_products(raw['products'])
    customers = C.clean_customers(raw['customers']) if 'customers' in raw else None
    S.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    orders.to_csv(S.PROCESSED_ORDERS_FILE, index=False, encoding=S.CSV_ENCODING)
    kpis = A.basic_kpis(orders)
    repeat = A.repeat_customers(orders)
    kpis = dict(kpis, **repeat)
    monthly = A.monthly_sales(orders)
    top = A.top_products(orders, products, S.TOP_N_PRODUCTS)
    cat = A.sales_by_category(orders, products)
    city = A.sales_by_city(orders)
    pay = A.payment_mix(orders)
    status = A.status_mix(orders)
    print('KPIs:', kpis)
    rfm = F.compute_rfm(orders)
    seg = F.segment_summary(rfm)
    print('SEGMENTS:')
    print(seg.to_string(index=False))
    rfm.to_csv(S.DATA_PROCESSED_DIR / 'rfm.csv', index=False, encoding=S.CSV_ENCODING)
    series = O.monthly_series(orders)
    combined, info = O.linear_forecast(series, 3)
    print('FORECAST:', info)
    enr = P.enrich(orders, products)
    pk = P.kpis(enr)
    print('PROFIT:', pk)
    pp = P.by_product(enr, products)
    pc = P.by_category(enr)
    print(pp[['product_name', 'revenue', 'profit', 'margin_pct']].head(5).to_string(index=False))
    pairs = B.cooccurrence(orders)
    print('BASKET pairs:', len(pairs))
    ret = H.retention(orders)
    print(ret.tail(3).to_string())
    cmp = H.compare_periods(orders, ('2025-01-01', '2025-06-30'), ('2025-07-01', '2025-12-31'))
    print('H1 vs H2:', cmp)
    daily = N.daily_series(orders)
    flagged = N.zscore_flags(daily)
    alerts = flagged[flagged['flag'] != 'ok']
    print('ALERTS:', len(alerts))
    print(alerts[['day', 'revenue', 'z', 'flag']].tail(5).to_string(index=False))
    cancels = N.cancel_alerts(orders)
    print('CANCEL-ALERT days:', len(cancels))
    dem = Q.demand(orders, products)
    print(dem.head(5).to_string(index=False))
    # sentiment from sample_reviews.csv if present
    senti = None
    senti_health = None
    try:
        rev_path = S.DATA_RAW_DIR / 'sample_reviews.csv'
        if rev_path.exists():
            import pandas as pd
            rdf = pd.read_csv(rev_path, encoding=S.CSV_ENCODING)
            senti = SE.analyze(rdf)
            senti_health = SE.overall_health(senti['summary'])
            print('SENTIMENT:', senti_health)
    except Exception as e:
        print('SENTIMENT skip:', e)
    recs = RC.recommend(orders, products, monthly, alerts,
                        sentiment_out=senti, restock_df=dem)
    print('RECOMMENDATIONS:', len(recs))
    print(recs.to_string(index=False))
    # DEEP INSIGHTS (data-analyst skill methodology)
    qa = DI.audit_quality(orders, products, customers)
    print('QUALITY:'); print(qa.to_string(index=False))
    churn, churn_sum = DI.loyalty_deep(orders)
    print('CHURN:'); print(churn_sum.to_string(index=False))
    tiers, tier_corr = DI.price_sensitivity(orders, products)
    print('PRICE-TIERS:'); print(tiers.to_string(index=False))
    gaps, recoverable, upsell = DI.growth_opportunities(orders, products, seg)
    print('GROWTH-GAPS:', len(gaps) if gaps is not None else 0)
    print('RECOVERABLE:'); print(recoverable.to_string(index=False) if recoverable is not None else 'none')
    print('UPSELL:', upsell)
    demo_q = ['profit in riyadh', 'ما الربح في الرياض؟', 'top products', 'أفضل المنتجات؟',
              'cancel rate', 'نسبة الإلغاء؟', 'monthly trend', 'توقع المبيعات؟', 'شرائح العملاء؟']
    print('ASSISTANT demo:')
    [print(' -', q, '->', SA.answer(q, orders, products)[0]) for q in demo_q]
    dbp = D.save_run(orders, products, kpis, tag=tag, rfm=rfm, profit=pk, recs=recs)
    print('DB:', dbp)
    charts = [V.plot_monthly(monthly), V.plot_top_products(top),
              V.plot_category_pie(cat), V.plot_city_bar(city),
              V.plot_payment_pie(pay), V.plot_price_hist(orders),
              V.plot_price_rating(products, orders),
              V.plot_rfm_segments(seg), V.plot_rfm_revenue(seg),
              V.plot_forecast(combined),
              V.plot_profit_products(pp), V.plot_margin_products(pp),
              V.plot_cohort_heat(ret), V.plot_anomaly(flagged),
              V.plot_daily_orders(flagged), V.plot_margin_vs_revenue(pp),
              V.plot_restock(dem)]
    if senti is not None:
        charts.append(V.plot_sentiment(senti['summary']))
    charts.append(V.plot_churn_risk(churn_sum))
    charts.append(V.plot_price_tiers(tiers))
    pdfp = PR.build(kpis, pk, [charts[0], charts[10], charts[9], charts[13], charts[-3]],
                    recs=recs, sentiment_health=senti_health)
    print('PDF:', pdfp)
    xlsx = R.export_excel(kpis, monthly, top, cat, city, pay, status, profit=pk, pprod=pp, pcat=pc,
                          basket=pairs, cohort=ret, forecast_info=info, forecast_series=combined,
                          rfm=rfm, seg=seg, restock=dem, alerts=alerts, recs=recs, repeat=repeat,
                          sentiment_summary=(senti['summary'] if senti else None),
                          sentiment_byprod=(senti.get('by_product') if senti else None),
                          quality=qa, churn=churn, churn_summary=churn_sum, tiers=tiers,
                          tier_corr=tier_corr, gaps=gaps, recoverable=recoverable, upsell=upsell)
    print('CHARTS:')
    [print(' -', c) for c in charts]
    print('EXCEL:', xlsx)
    print('DONE')
if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='manual')
    main(tag=ap.parse_args().tag)
