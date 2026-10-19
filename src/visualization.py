# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import settings as S
def AR(s):
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(s)))
    except Exception:
        return s
plt.rcParams['font.family'] = ['Tahoma', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
REPORT_DIR = S.DATA_REPORTS_DIR
REPORT_DIR.mkdir(parents=True, exist_ok=True)
_PALETTE = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
_AR_CAT = {'electronics': 'إلكترونيات', 'fashion': 'أزياء', 'home': 'المنزل', 'beauty': 'تجميل', 'toys': 'ألعاب'}
_AR_CITY = {'Riyadh': 'الرياض', 'Jeddah': 'جدة', 'Dammam': 'الدمام', 'Mecca': 'مكة', 'Medina': 'المدينة', 'Abha': 'أبها'}
_AR_PAY = {'mada': 'مدى', 'visa': 'فيزا', 'apple_pay': 'آبل باي', 'cod': 'عند الاستلام'}
_AR_SEG = {'champions': 'النخبة', 'loyal': 'أوفياء', 'potential': 'واعدون', 'at_risk': 'معرضون للخطر', 'lost': 'خاملون'}
def _t(m, v):
    return AR(m.get(v, v))
def _save(fig, name):
    out = REPORT_DIR / name
    fig.tight_layout()
    fig.savefig(out, dpi=S.CHART_DPI)
    plt.close(fig)
    return str(out)
def plot_monthly(monthly):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly['month'], monthly['revenue'], marker='o', linewidth=2.2)
    ax.set_title(AR('إيرادات الشهر'))
    ax.set_xlabel(AR('الشهر')); ax.set_ylabel(AR('الإيراد'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(alpha=0.3)
    return _save(fig, 'monthly_revenue.png')
def plot_top_products(top):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top['product_name'][::-1], top['revenue'][::-1], color=_PALETTE[0])
    ax.set_title(AR('المنتجات الأعلى إيرادا'))
    ax.set_xlabel(AR('الإيراد'))
    return _save(fig, 'top_products.png')
def plot_category_pie(cat):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(cat['revenue'], labels=[_t(_AR_CAT, c) for c in cat['category']], autopct='%1.1f%%', colors=_PALETTE)
    ax.set_title(AR('الإيراد حسب الفئة'))
    return _save(fig, 'category_pie.png')
def plot_city_bar(city):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([_t(_AR_CITY, c) for c in city['city']], city['revenue'], color=_PALETTE[2])
    ax.set_title(AR('الإيراد حسب المدينة'))
    ax.set_ylabel(AR('الإيراد'))
    return _save(fig, 'city_revenue.png')
def plot_payment_pie(pay):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(pay['orders'], labels=[_t(_AR_PAY, c) for c in pay['payment_method']], autopct='%1.1f%%', colors=_PALETTE)
    ax.set_title(AR('الطلبات حسب الدفع'))
    return _save(fig, 'payment_mix.png')
def plot_price_hist(orders):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(orders['total'], bins=30, color=_PALETTE[1], edgecolor='white')
    ax.set_title(AR('توزيع قيمة الطلب'))
    ax.set_xlabel(AR('القيمة'))
    return _save(fig, 'price_hist.png')
def plot_price_rating(products, orders):
    rev = orders.groupby('product_id')['total'].sum().reset_index()
    m = products.merge(rev, on='product_id', how='left').fillna({'total': 0})
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(m['price'], m['rating'], s=m['total']/400+20, alpha=0.7, color=_PALETTE[4])
    ax.set_title(AR('السعر مقابل التقييم'))
    ax.set_xlabel(AR('السعر')); ax.set_ylabel(AR('التقييم'))
    ax.grid(alpha=0.3)
    return _save(fig, 'price_rating.png')
def plot_rfm_segments(seg):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([_t(_AR_SEG, c) for c in seg['segment']], seg['customers'], color=_PALETTE[5])
    ax.set_title(AR('العملاء حسب الشريحة'))
    return _save(fig, 'rfm_segments.png')
def plot_rfm_revenue(seg):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(seg['revenue'], labels=[_t(_AR_SEG, c) for c in seg['segment']], autopct='%1.1f%%', colors=_PALETTE)
    ax.set_title(AR('الإيراد حسب الشريحة'))
    return _save(fig, 'rfm_revenue.png')
def plot_forecast(combined):
    act = combined[combined['kind'] == 'actual']
    fc = combined[combined['kind'] == 'forecast']
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(act['ds'], act['y'], marker='o', label=AR('فعلي'))
    ax.plot(fc['ds'], fc['y'], marker='s', linestyle='--', color=_PALETTE[3], label=AR('متوقع'))
    ax.set_title(AR('توقع المبيعات'))
    ax.legend()
    ax.grid(alpha=0.3)
    return _save(fig, 'forecast.png')
def plot_profit_products(pp):
    t=pp.head(10).iloc[::-1]
    fig,ax=plt.subplots(figsize=(10,6))
    ax.barh(t['product_name'],t['profit'],color=_PALETTE[2])
    ax.set_title(AR('الأعلى ربحا'))
    return _save(fig,'profit_products.png')
def plot_margin_products(pp):
    t=pp.sort_values('margin_pct',ascending=False).head(10).iloc[::-1]
    fig,ax=plt.subplots(figsize=(10,6))
    ax.barh(t['product_name'],t['margin_pct'],color=_PALETTE[4])
    ax.set_title(AR('الأعلى هامش ربح'))
    return _save(fig,'margin_products.png')
def plot_cohort_heat(ret):
    fig,ax=plt.subplots(figsize=(9,6))
    im=ax.imshow(ret.values,cmap='Greens',vmin=0,vmax=100)
    ax.set_xticks(range(len(ret.columns)))
    ax.set_xticklabels([str(c) for c in ret.columns])
    ax.set_yticks(range(len(ret.index)))
    ax.set_yticklabels([str(c) for c in ret.index])
    ax.set_title(AR('الاحتفاظ بالعملاء'))
    fig.colorbar(im,ax=ax)
    return _save(fig,'cohort_retention.png')
def plot_anomaly(flagged):
    fig,ax=plt.subplots(figsize=(11,5))
    ax.plot(flagged['day'],flagged['revenue'],linewidth=1.5)
    sp=flagged[flagged['flag']=='spike']
    dr=flagged[flagged['flag']=='drop']
    ax.scatter(sp['day'],sp['revenue'],color='green',s=40)
    ax.scatter(dr['day'],dr['revenue'],color='red',s=40)
    ax.set_title(AR('التنبيهات اليومية'))
    ax.grid(alpha=0.3)
    return _save(fig,'anomaly.png')
def plot_sentiment(summary):
    mp = {'positive': AR('إيجابي'), 'negative': AR('سلبي'), 'neutral': AR('محايد')}
    labels = [mp.get(s, s) for s in summary['sentiment']]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(summary['n'], labels=labels, autopct='%1.1f%%', colors=['#22c55e', '#ef4444', '#94a3b8'])
    ax.set_title(AR('تحليل آراء العملاء'))
    return _save(fig, 'sentiment.png')
def plot_restock(dem):
    t = dem.head(10).iloc[::-1]
    names = t['product_name'] if 'product_name' in t.columns else t['product_id']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(names, t['reorder_point'], color=_PALETTE[1])
    ax.set_title(AR('نقاط إعادة الطلب'))
    ax.set_xlabel(AR('الكمية'))
    return _save(fig, 'restock.png')
def plot_margin_vs_revenue(pp):
    t = pp.head(12)
    fig, ax = plt.subplots(figsize=(10, 6))
    sc = ax.scatter(t['revenue'], t['margin_pct'], s=t['qty'] * 2 + 20 if 'qty' in t.columns else 60,
                    c=t['profit'], cmap='RdYlGn', alpha=0.8, edgecolors='black', linewidths=0.5)
    for _, r in t.iterrows():
        ax.annotate(str(r['product_id']), (r['revenue'], r['margin_pct']), fontsize=8, ha='center')
    ax.set_title(AR('الإيراد مقابل الهامش (الحجم = الكمية، اللون = الربح)'))
    ax.set_xlabel(AR('الإيراد'))
    ax.set_ylabel(AR('هامش الربح %'))
    fig.colorbar(sc, ax=ax)
    ax.grid(alpha=0.3)
    return _save(fig, 'margin_vs_revenue.png')
def plot_daily_orders(flagged):
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.bar(flagged['day'], flagged['orders'] if 'orders' in flagged.columns else flagged['revenue'],
           color=_PALETTE[0], alpha=0.8, width=1.0)
    ax.set_title(AR('الطلبات اليومية'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(alpha=0.3, axis='y')
    return _save(fig, 'daily_orders.png')
def plot_churn_risk(summary):
    mp = {'high': AR('خطر مرتفع'), 'medium': AR('متوسط'), 'low': AR('منخفض')}
    labels = [mp.get(s, s) for s in summary['churn_risk']]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, summary['customers'], color=['#ef4444', '#f59e0b', '#22c55e'])
    ax.set_title(AR('العملاء حسب خطر التوقف'))
    ax.set_ylabel(AR('عدد العملاء'))
    return _save(fig, 'churn_risk.png')
def plot_price_tiers(tiers):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = list(tiers['price_tier'].astype(str))
    ax.bar(x, tiers['revenue'], color=_PALETTE[:len(x)])
    ax.set_title(AR('الإيراد حسب الشريحة السعرية'))
    ax.set_ylabel(AR('الإيراد'))
    for i, v in enumerate(tiers['margin_pct']):
        ax.text(i, tiers['revenue'].iloc[i], f"{v}%", ha='center', va='bottom', fontsize=9)
    return _save(fig, 'price_tiers.png')
