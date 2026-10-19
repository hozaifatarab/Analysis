# -*- coding: utf-8 -*-
import re
import pandas as pd
CITIES = {'riyadh': 'Riyadh', 'jeddah': 'Jeddah', 'dammam': 'Dammam', 'mecca': 'Mecca', 'medina': 'Medina', 'abha': 'Abha',
          'الرياض': 'Riyadh', 'جدة': 'Jeddah', 'الدمام': 'Dammam', 'مكة': 'Mecca', 'المدينة': 'Medina', 'أبها': 'Abha', 'ابها': 'Abha'}
def _find_city(q):
    ql = q.lower()
    for k, v in CITIES.items():
        if k.lower() in ql:
            return v
    return None
def _has(q, *words):
    return any(w in q for w in words)
def answer(q, orders, products):
    from src import analysis as A, profit as P
    ql = q.strip().lower()
    city = _find_city(ql)
    f = orders.copy()
    if city:
        f = f[f['city'] == city]
    k = A.basic_kpis(f)
    enr = P.enrich(f, products)
    pk = P.kpis(enr)
    if _has(ql, 'profit', 'margin', 'net', 'ربح', 'هامش', 'صافي', 'تكلفة'):
        return ('profit', {'net': pk['net_profit'], 'margin': pk['margin_pct'], 'cost': pk['cost'], 'revenue': pk['revenue']}, None)
    if _has(ql, 'cancel', 'إلغاء', 'الغاء', 'ملغي'):
        return ('cancel', {'rate': k['cancel_rate_pct'], 'total': k['total_orders']}, None)
    if _has(ql, 'return', 'مرتجع', 'مسترجع', 'استرجاع'):
        from src import analysis as _A
        st = _A.status_mix(f)
        return ('table', {'title': 'returns'}, st)
    if _has(ql, 'aov', 'average', 'basket', 'avg', 'متوسط', 'سلة'):
        return ('aov', {'aov': k['aov']}, None)
    if _has(ql, 'forecast', 'توقع', 'تنبؤ', 'المستقبل'):
        from src import forecast as O
        s = O.monthly_series(f)
        if len(s) >= 2:
            comb, info = O.linear_forecast(s, 3)
            return ('forecast', info, comb)
        return ('kpis', k, None)
    if _has(ql, 'rfm', 'segment', 'شريحة', 'شرائح', 'ولاء', 'عملاء'):
        from src import rfm as F
        rfm = F.compute_rfm(f)
        t = F.segment_summary(rfm)
        return ('table', {'title': 'rfm'}, t)
    if _has(ql, 'retention', 'cohort', 'احتفاظ', 'تماسك'):
        from src import cohort as H
        return ('table', {'title': 'cohort'}, H.retention(f))
    if _has(ql, 'anomaly', 'alert', 'شاذ', 'تنبيه', 'غير طبيعي'):
        from src import anomaly as N
        fl = N.zscore_flags(N.daily_series(f))
        return ('table', {'title': 'alerts'}, fl[fl['flag'] != 'ok'].tail(10))
    if _has(ql, 'restock', 'stock', 'مخزون', 'اعادة طلب', 'إعادة', 'نفد'):
        from src import restock as Q
        return ('table', {'title': 'restock'}, Q.demand(f, products).head(10))
    if _has(ql, 'sentiment', 'review', 'رأي', 'تقييمات', 'مشاعر', 'اراء'):
        return ('sentiment', {'hint': 'upload reviews file for sentiment'}, None)
    if _has(ql, 'category', 'categories', 'فئة', 'قسم', 'تصنيف'):
        t = A.sales_by_category(f, products)
        return ('table', {'title': 'by_category'}, t)
    if _has(ql, 'city', 'cities', 'مدينة', 'مدن'):
        t = A.sales_by_city(orders)
        return ('table', {'title': 'by_city'}, t)
    if _has(ql, 'top', 'best', 'product', 'الأفضل', 'افضل', 'منتج', 'الاعلى', 'الأعلى'):
        t = A.top_products(f, products, 5)
        return ('table', {'title': 'top5'}, t[['product_name', 'revenue']])
    if _has(ql, 'month', 'trend', 'sales', 'شهر', 'اتجاه', 'مبيعات'):
        t = A.monthly_sales(f)
        return ('chart', {'title': 'monthly'}, t.set_index('month')['revenue'])
    if _has(ql, 'payment', 'pay', 'دفع', 'مدى', 'فيزا'):
        t = A.payment_mix(f)
        return ('table', {'title': 'pay'}, t)
    if _has(ql, 'customer', 'عميل', 'زبون'):
        from src import rfm as F
        t = F.segment_summary(F.compute_rfm(f))
        return ('table', {'title': 'rfm'}, t)
    return ('kpis', k, None)
def suggest_questions():
    return ['ما الربح في الرياض؟', 'أفضل المنتجات؟', 'نسبة الإلغاء؟', 'اتجاه المبيعات الشهرية؟',
            'توقع المبيعات؟', 'شرائح العملاء؟', 'المنتجات تحتاج إعادة طلب؟', 'أيام الشذوذ؟']

