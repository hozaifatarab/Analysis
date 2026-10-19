# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src import data_loader as L
from src import data_cleaning as C
from src import analysis as A
from src import rfm as F
from src import forecast as O
from src import anomaly as N
from src import restock as Q
from src import store_db as D
from src import profit as P
from src import basket as B
from src import cohort as H
from src import assistant as SA
from src import recommender as RC
from src import sentiment as SE
from src import deep_insights as DI
U = lambda *cs: ''.join(chr(c) for c in cs)
T_TITLE=U(1604,1608,1581,1577,32,1575,1604,1605,1578,1580,1585)
T_B1=U(1575,1604,1576,1610,1575,1606,1575,1578,32,1575,1604,1580,1575,1607,1586,1577)
T_B2=U(1585,1601,1593,32,1605,1604,1601)
T_CITY=U(1575,1604,1605,1583,1610,1606,1577)
T_CAT=U(1575,1604,1601,1574,1577)
T_REV=U(1575,1604,1575,1610,1585,1575,1583)
T_ORD=U(1575,1604,1591,1604,1576,1575,1578)
T_AOV=U(1605,1578,1608,1587,1591,32,1575,1604,1591,1604,1576)
T_CN=U(1606,1587,1576,1577,32,1575,1604,1575,1604,1594,1575,1569)
T_MON=U(1575,1604,1575,1610,1585,1575,1583,32,1575,1604,1588,1607,1585,1610)
T_TOP=U(1575,1601,1590,1604,32,1575,1604,1605,1606,1578,1580,1575,1578)
T_RFM=U(1588,1585,1575,1574,1581,32,1575,1604,1593,1605,1604,1575,1569)
T_FC=U(1578,1608,1602,1593,32,1575,1604,1605,1576,1610,1593,1575,1578)
T_DL=U(1578,1581,1605,1610,1604,32,1575,1604,1578,1602,1585,1610,1585)
T_UP1=U(1605,1604,1601,32,1575,1604,1591,1604,1576,1575,1578)
T_UP2=U(1605,1604,1601,32,1575,1604,1605,1606,1578,1580,1575,1578)
T_HINT=U(1575,1585,1601,1593,32,1605,1604,1601,1575,1611)
T_OK=U(1578,1605,32,1575,1604,1578,1606,1592,1610,1601)
T_ALL=U(1575,1604,1603,1604)
T_EMPTY=U(1604,1575,32,1578,1608,1580,1583,32,1576,1610,1575,1606,1575,1578)
T_MISS=U(1575,1593,1605,1583,1577,32,1606,1575,1602,1589,1577)
T_TPP=U(1575,1604,1575,1593,1604,1609,32,1585,1576,1581,1575)
T_SEN=U(1575,1604,1578,1602,1610,1610,1605,1575,1578)
T_BSK=U(1587,1604,1577,32,1575,1604,1605,1588,1578,1585,1610,1575,1578)
T_RET=U(1575,1604,1575,1581,1578,1601,1575,1592)
T_CMP=U(1605,1602,1575,1585,1606,1577)
T_AN=U(1575,1604,1578,1606,1576,1610,1607,1575,1578)
T_RS=U(1575,1593,1575,1583,1577,32,1575,1604,1591,1604,1576)
T_HS=U(1587,1580,1604)
T_ASK=U(1575,1587,1575,1604)
T_REC=U(1578,1608,1589,1610,1575,1578)
st.set_page_config(page_title=T_TITLE, layout='wide', initial_sidebar_state='expanded')
st.markdown("<link href='https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap' rel='stylesheet'>", unsafe_allow_html=True)
st.markdown("<style>:root{--bg:#0d1117;--card:#161b22;--gold:#e8b64c;--teal:#2dd4bf;--rose:#fb7185;--ink:#f0f3f6;--mut:#8b949e}html,body,[data-testid='stAppViewContainer']{background:var(--bg);color:var(--ink);font-family:'Tajawal',sans-serif}div[data-testid='stAppViewContainer']{direction:rtl;text-align:right;background:radial-gradient(1000px 400px at 80% -10%,rgba(232,182,76,.12),transparent),var(--bg)}section[data-testid='stSidebar']{background:#0a0d12;border-left:1px solid #222}section[data-testid='stSidebar'] *{color:var(--ink)!important}h1,h2,h3{font-family:'Tajawal',sans-serif!important;font-weight:800}.kpi{background:linear-gradient(135deg,#1a2230,#10151f);border:1px solid #2a3342;border-radius:16px;padding:18px 16px;text-align:center;box-shadow:0 6px 24px rgba(0,0,0,.35)}.kpi .v{font-size:30px;font-weight:800;color:var(--gold)}.kpi .l{font-size:14px;color:var(--mut);margin-top:4px}.kpi.teal .v{color:var(--teal)}.kpi.rose .v{color:var(--rose)}.kpi.sky .v{color:#7dd3fc}.stTabs [data-baseweb='tab']{font-family:'Tajawal';font-weight:700}.stDataFrame{border-radius:12px;overflow:hidden}</style>", unsafe_allow_html=True)
st.title(T_TITLE)
AR_CITY={'Riyadh':U(1575,1604,1585,1610,1575,1590),'Jeddah':U(1580,1583,1577),'Dammam':U(1575,1604,1583,1605,1575,1605),'Mecca':U(1605,1603,1577),'Medina':U(1575,1604,1605,1583,1610,1606,1577),'Abha':U(1571,1576,1607,1575)}
AR_CAT={'electronics':U(1575,1604,1603,1578,1585,1608,1606,1610,1575,1578),'fashion':U(1571,1586,1610,1575,1569),'home':U(1575,1604,1605,1606,1586,1604),'beauty':U(1578,1580,1605,1610,1604),'toys':U(1575,1604,1593,1575,1576)}
AR_SEG={'champions':U(1575,1604,1606,1582,1576,1577),'loyal':U(1575,1608,1601,1610,1575,1569),'potential':U(1608,1575,1593,1583,1608,1606),'at_risk':U(1605,1593,1585,1590,1608,1606),'lost':U(1582,1575,1605,1604,1608,1606)}
AR_PAY={'mada':U(1605,1583,1609),'visa':U(1601,1610,1586,1575),'apple_pay':U(1575,1576,1604,32,1576,1575,1610),'cod':U(1593,1606,1583,32,1575,1604,1575,1587,1578,1604,1575,1605)}
COLUMN_MAP={'order_id':'order_id','id':'order_id','customer_id':'customer_id','customer':'customer_id','product_id':'product_id','product':'product_id','quantity':'quantity','qty':'quantity','price':'price','order_date':'order_date','date':'order_date','payment_method':'payment_method','payment':'payment_method','status':'status','city':'city'}
def norm_col(c):
    c=str(c).strip().lower().replace(' ','_')
    return COLUMN_MAP.get(c,c)
PXP={'template':'plotly_dark','paper_bgcolor':'rgba(0,0,0,0)','plot_bgcolor':'rgba(0,0,0,0)','font':{'family':'Tajawal','color':'#f0f3f6'}}
def kpi_card(col,label,value,cls=''):
    col.markdown(f"<div class='kpi {cls}'><div class='v'>{value}</div><div class='l'>{label}</div></div>",unsafe_allow_html=True)
def fig_line(df,x,y,title,color='#e8b64c'):
    fg=px.line(df,x=x,y=y,title=title,color_discrete_sequence=[color])
    fg.update_layout(**PXP)
    return fg
def sec(num,title):
    st.markdown(f"<div style='display:flex;align-items:center;gap:10px;margin:26px 0 8px'><span style='background:linear-gradient(135deg,#e8b64c,#b97f1f);color:#111;font-weight:800;border-radius:10px;min-width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center'>{num}</span><span style='font-size:22px;font-weight:800'>{title}</span><span style='flex:1;height:2px;background:linear-gradient(-90deg,#e8b64c55,transparent)'></span></div>",unsafe_allow_html=True)
def fig_bar(df,x,y,title,color='#2dd4bf',h=False):
    fg=px.bar(df,x=x,y=y,title=title,color_discrete_sequence=[color],orientation='h' if h else 'v')
    fg.update_layout(**PXP,height=420)
    return fg
def render_dashboard(orders, products):
    st.sidebar.header(T_TITLE)
    city_keys=['all']+sorted(orders['city'].dropna().unique().tolist())
    cat_keys=['all']+sorted(products['category'].dropna().unique().tolist())
    city=st.sidebar.selectbox(T_CITY,city_keys,format_func=lambda v:T_ALL if v=='all' else AR_CITY.get(v,v))
    cat=st.sidebar.selectbox(T_CAT,cat_keys,format_func=lambda v:T_ALL if v=='all' else AR_CAT.get(v,v))
    f=orders.copy()
    if city != 'all':
        f=f[f['city']==city]
    if cat != 'all':
        ids=products[products['category']==cat]['product_id']
        f=f[f['product_id'].isin(ids)]
    if len(f)==0:
        st.warning(T_EMPTY)
        return
    k=A.basic_kpis(f)
    m1,m2,m3,m4=st.columns(4)
    kpi_card(m1,T_REV,f"{k['total_revenue']:,.0f}",'')
    kpi_card(m2,T_ORD,k['completed_orders'],'teal')
    kpi_card(m3,T_AOV,f"{k['aov']:,.0f}",'sky')
    kpi_card(m4,T_CN,k['cancel_rate_pct'],'rose')
    sec('1',T_MON)
    mon=A.monthly_sales(f)
    st.plotly_chart(fig_line(mon,'month','revenue',T_MON),width='stretch')
    sec('2',T_TOP)
    st.plotly_chart(fig_bar(A.top_products(f,products,10),'revenue','product_name',T_TOP,h=True),width='stretch')
    sec('3',T_RFM)
    rfm=F.compute_rfm(f)
    seg=F.segment_summary(rfm).copy()
    seg['segment']=seg['segment'].map(lambda s:AR_SEG.get(s,s))
    st.dataframe(seg,width='stretch')
    st.plotly_chart(px.pie(seg,names='segment',values='revenue',title=T_RFM,template='plotly_dark',height=420),width='stretch')
    sec('4',T_FC)
    comb,info=O.linear_forecast(O.monthly_series(f),3)
    fg=go.Figure()
    a2=comb[comb['kind']=='actual']; b2=comb[comb['kind']=='forecast']
    fg.add_trace(go.Scatter(x=a2['ds'],y=a2['y'],mode='lines+markers',name='actual'))
    fg.add_trace(go.Scatter(x=b2['ds'],y=b2['y'],mode='lines+markers',name='forecast',line={'dash':'dash'}))
    fg.update_layout(**PXP,title=T_FC,height=420)
    st.plotly_chart(fg,width='stretch')
    sec('5',U(1575,1604,1578,1606,1576,1610,1607,1575,1578))
    daily=N.daily_series(f)
    flag=N.zscore_flags(daily)
    al=flag[flag['flag']!='ok']
    st.write(len(al))
    st.dataframe(al.tail(10),width='stretch')
    st.plotly_chart(fig_line(flag,'day','revenue',T_MON,color='#fb7185'),width='stretch')
    sec('6',U(1575,1593,1575,1583,1577,32,1575,1604,1591,1604,1576))
    st.dataframe(Q.demand(f,products).head(10),width='stretch')
    sec('7',U(1587,1580,1604,32,1575,1604,1578,1588,1594,1610,1604,1575,1578))
    st.dataframe(D.run_history().tail(10),width='stretch')
    sec('8',U(1575,1587,1571,1604,32,1575,1604,1576,1610,1575,1606,1575,1578))
    sug = SA.suggest_questions()
    pick = st.selectbox('أسئلة مقترحة', [''] + sug)
    q = st.text_input(U(1575,1587,1571,1604,32,1605,1579,1575,1604), pick if pick else U(1605,1575,32,1575,1604,1585,1576,1581,32,1601,1610,32,1575,1604,1585,1610,1575,1590,1567))
    kind, meta, tbl = SA.answer(q if q else 'summary', f, products)
    st.write(kind)
    st.write(meta)
    st.dataframe(tbl, width='stretch') if tbl is not None else None
    try:
        st.plotly_chart(fig_bar(tbl.reset_index(), tbl.columns[1], tbl.columns[0], T_FC), width='stretch') if kind == 'chart' and tbl is not None else None
    except Exception:
        pass
    if kind == 'forecast' and tbl is not None:
        st.dataframe(tbl.tail(8), width='stretch')
    sec('9',U(1578,1608,1589,1610,1575,1578))
    dem9 = Q.demand(f, products)
    recs = RC.recommend(f, products, A.monthly_sales(f), N.zscore_flags(N.daily_series(f)), restock_df=dem9)
    lvl = st.selectbox(U(1575,1604,1605,1587,1578,1608,1609), ['all', 'bad', 'warn', 'good'])
    show = recs if lvl == 'all' else recs[recs['level'] == lvl]
    st.dataframe(show, width='stretch')
    bad_n = len(recs[recs['level'] == 'bad'])
    if bad_n:
        st.error(f'{bad_n} critical issues need action')
    sec('10',U(1575,1604,1578,1602,1610,1610,1605,1575,1578))
    upr = st.file_uploader('reviews', type=['xlsx', 'xls', 'csv'], key='u3')
    st.caption('product_id, review')
    # built-in sample sentiment
    try:
        import pandas as _pd
        _sp = Path(__file__).resolve().parent / 'data' / 'raw' / 'sample_reviews.csv'
        if _sp.exists() and upr is None:
            _rdf = _pd.read_csv(_sp, encoding='utf-8-sig')
            _out = SE.analyze(_rdf)
            _h = SE.overall_health(_out['summary'])
            st.info(f"Sample: {_h['total']} reviews | +{_h['pos_pct']}% / -{_h['neg_pct']}% ({_h['verdict']})")
            st.dataframe(_out['summary'], width='stretch')
            st.plotly_chart(fig_bar(_out['summary'], 'n', 'sentiment', T_SEN, color='#e8b64c'), width='stretch')
            st.dataframe(_out.get('by_product'), width='stretch')
    except Exception:
        pass
    if upr is not None:
        nm = upr.name.lower()
        r0 = pd.read_excel(upr) if nm.endswith(('.xlsx', '.xls')) else pd.read_csv(upr, encoding='utf-8-sig')
        tcol = 'review' if 'review' in r0.columns else r0.columns[-1]
        out = SE.analyze(r0, text_col=tcol)
        h = SE.overall_health(out['summary'])
        st.info(f"{h['total']} reviews | +{h['pos_pct']}% / -{h['neg_pct']}% ({h['verdict']})")
        if h['verdict'] == 'critical':
            st.error('Review sentiment is critical - check quality now')
        st.dataframe(out['summary'], width='stretch')
        st.plotly_chart(fig_bar(out['summary'], 'n', 'sentiment', T_SEN, color='#e8b64c'), width='stretch')
        st.dataframe(out.get('by_product'), width='stretch')
    sec('11',U(1575,1604,1585,1576,1581,1610,1577))
    enr=P.enrich(f,products)
    pk=P.kpis(enr)
    q1,q2,q3,q4=st.columns(4)
    kpi_card(q1,U(1589,1575,1601,1610,32,1575,1604,1585,1576,1581),f"{pk['net_profit']:,.0f}")
    kpi_card(q2,U(1607,1575,1605,1588,32,1575,1604,1585,1576,1581),pk['margin_pct'],'teal')
    kpi_card(q3,U(1578,1603,1604,1601,1577,32,1575,1604,1576,1590,1575,1593,1577),f"{pk['cost']:,.0f}",'sky')
    kpi_card(q4,U(1582,1587,1575,1585,1577,32,1575,1604,1605,1585,1578,1580,1593,1575,1578),f"{pk['return_loss']:,.0f}",'rose')
    sec('12',U(1575,1604,1571,1593,1604,1609,32,1585,1576,1581,1575))
    pp=P.by_product(enr,products)
    st.plotly_chart(fig_bar(pp.head(10),'profit','product_name',T_TPP,h=True,color='#2dd4bf'),width='stretch')
    sec('13',U(1587,1604,1577,32,1575,1604,1605,1588,1578,1585,1610,1575,1578))
    pairs=B.cooccurrence(f)
    st.dataframe(pairs.head(15) if len(pairs) else pairs,width='stretch')
    sec('14',U(1575,1604,1575,1581,1578,1601,1575,1592))
    st.dataframe(H.retention(f),width='stretch')
    sec('15',U(1605,1602,1575,1585,1606,1577,32,1601,1578,1585,1578,1610,1606))
    e1,e2=st.columns(2)
    s1=e1.date_input(U(1575,1604,1601,1578,1585,1577,32,1575,1604,1571,1608,1604,1609),value=pd.to_datetime('2025-01-01'))
    e_1=e1.date_input('to',value=pd.to_datetime('2025-06-30'))
    s2=e2.date_input(U(1575,1604,1601,1578,1585,1577,32,1575,1604,1579,1575,1606,1610,1577),value=pd.to_datetime('2025-07-01'))
    e_2=e2.date_input('to',value=pd.to_datetime('2025-12-31'))
    cmp=H.compare_periods(f,(s1,e_1),(s2,e_2))
    st.write(cmp)
    sec('16','جودة البيانات')
    qa=DI.audit_quality(f,products)
    st.dataframe(qa,width='stretch')
    bad_q=qa[qa['status']!='pass']
    if len(bad_q):
        st.error(f'{len(bad_q)} جودة بيانات تحتاج إصلاح')
    else:
        st.success('جودة البيانات جيدة')
    sec('17','خطر التوقف')
    churn,churn_sum=DI.loyalty_deep(f)
    _cs=churn_sum.copy(); _cs['churn_risk']=_cs['churn_risk'].map({'high':'خطر مرتفع','medium':'متوسط','low':'منخفض'})
    st.plotly_chart(fig_bar(_cs,'customers','churn_risk','العملاء حسب خطر التوقف'),width='stretch')
    st.dataframe(churn_sum,width='stretch')
    hi=len(churn[churn['churn_risk']=='high'])
    if hi: st.error(f'{hi} عميل خطر توقف مرتفع')
    sec('18','الحساسية السعرية')
    tiers,tier_corr=DI.price_sensitivity(f,products)
    _t=tiers.copy(); _t['price_tier']=_t['price_tier'].astype(str).map({'luxury':'فاخر','premium':'ممتاز','mid':'متوسط','budget':'اقتصادي'}).fillna(_t['price_tier'].astype(str))
    st.plotly_chart(fig_bar(_t,'revenue','price_tier','الإيراد حسب الشريحة السعرية',h=True),width='stretch')
    st.dataframe(tiers[['price_tier','revenue','profit','margin_pct','share_orders']],width='stretch')
    st.dataframe(tier_corr,width='stretch')
    sec('19','فرص النمو')
    gaps,recoverable,upsell=DI.growth_opportunities(f,products,F.segment_summary(F.compute_rfm(f)))
    if len(gaps):
        st.dataframe(gaps,width='stretch')
    else:
        st.info('لا توجد فئات ناقصة في المدن')
    st.dataframe(pd.DataFrame([upsell]),width='stretch')
    if recoverable is not None and len(recoverable):
        st.dataframe(recoverable,width='stretch')
        st.error(f'قيمة قابلة للاستعادة: {recoverable["revenue"].sum():,.0f}')
@st.cache_data
def get_builtin():
    raw=L.load_all()
    return C.clean_orders(raw['orders']),C.clean_products(raw['products'])
T_DEEP='التحليل العميق'
tab1,tab2,tab3=st.tabs([T_B1,T_B2,T_DEEP])
with tab1:
    o0,p0=get_builtin()
    render_dashboard(o0,p0)
with tab2:
    sec('16',T_B2)
    up1=st.file_uploader(T_UP1,type=['xlsx','xls','csv'],key='u1')
    up2=st.file_uploader(T_UP2,type=['xlsx','xls','csv'],key='u2')
    def read_any(f):
        n=f.name.lower()
        if n.endswith(('.xlsx','.xls')):
            x=pd.ExcelFile(f)
            s=x.sheet_names[0]
            if len(x.sheet_names)>1:
                s=st.selectbox('sheet',x.sheet_names)
            return pd.read_excel(x,sheet_name=s)
        for enc in ['utf-8-sig','utf-8','cp1256']:
            try:
                f.seek(0)
                return pd.read_csv(f,encoding=enc)
            except Exception:
                continue
        f.seek(0)
        return pd.read_csv(f)
    if up1 is not None:
        r0=read_any(up1)
        st.dataframe(r0.head(5),width='stretch')
        df=r0.rename(columns={c:norm_col(c) for c in r0.columns})
        need=['order_id','customer_id','product_id','quantity','price','order_date']
        miss=[c for c in need if c not in df.columns]
        if miss:
            st.error(T_MISS)
            st.write(miss)
        else:
            cl=C.clean_orders(df)
            st.success(f'{T_OK}: {len(cl)}')
            pr=None
            if up2 is not None:
                r1=read_any(up2)
                pr=r1.rename(columns={c:norm_col(c) for c in r1.columns})
                pr=C.clean_products(pr)
            else:
                pr=pd.DataFrame({'product_id':cl['product_id'].unique()})
                pr['product_name']=pr['product_id']
                pr['category']='general'
            render_dashboard(cl, pr)
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as xw:
                pd.DataFrame([A.basic_kpis(cl)]).to_excel(xw, sheet_name='K', index=False)
                A.monthly_sales(cl).to_excel(xw, sheet_name='M', index=False)
                cl.to_excel(xw, sheet_name='C', index=False)
                try:
                    from src import profit as _P, forecast as _O, rfm as _F
                    _enr = _P.enrich(cl, pr)
                    pd.DataFrame([_P.kpis(_enr)]).to_excel(xw, sheet_name='Profit', index=False)
                    _P.by_product(_enr, pr).to_excel(xw, sheet_name='ProfitProducts', index=False)
                    _s, _i = _O.linear_forecast(_O.monthly_series(cl), 3)
                    _s.to_excel(xw, sheet_name='Forecast', index=False)
                    _F.segment_summary(_F.compute_rfm(cl)).to_excel(xw, sheet_name='RFM', index=False)
                except Exception:
                    pass
            st.download_button(T_DL, buf.getvalue(), file_name='report.xlsx')
    else:
        st.info(T_HINT)
with tab3:
    sec('20',T_DEEP)
    o3,p3=get_builtin()
    st.markdown("### " + T_DEEP)
    c1,c2,c3,c4=st.columns(4)
    kpis=A.basic_kpis(o3)
    kpi_card(c1,U(1575,1604,1575,1610,1585,1575,1583),f"{kpis['total_revenue']:,.0f}")
    kpi_card(c2,'الطلبات المكتملة',f"{kpis['completed_orders']}")
    kpi_card(c3,'نسبة الإلغاء',f"{kpis['cancel_rate_pct']:.1f}%",'rose')
    qa=DI.audit_quality(o3,p3)
    bad_q=qa[qa['status']!='pass']
    if len(bad_q):
        kpi_card(c4,'جودة البيانات',f'{len(bad_q)}','rose')
    else:
        kpi_card(c4,'جودة البيانات','جيد','teal')
    sec('21','خطر التوقف')
    churn,churn_sum=DI.loyalty_deep(o3)
    cs3=churn_sum.copy()
    cs3['churn_risk']=cs3['churn_risk'].map({'high':'خطر مرتفع','medium':'متوسط','low':'منخفض'})
    st.plotly_chart(px.pie(cs3,names='churn_risk',values='revenue',title='الإيراد حسب خطر التوقف',template='plotly_dark',height=400),width='stretch')
    hi=churn[churn['churn_risk']=='high']
    if len(hi):
        st.error(f'{len(hi)} عميل بخطر توقف مرتفع — يحتاج تدخلاً فورياً')
        st.dataframe(hi[['customer_id','orders','revenue','days_since_last','churn_risk']].head(10),width='stretch')
    else:
        st.success('لا يوجد خطر توقف مرتفع')
    sec('22','الحساسية السعرية')
    tiers,_=DI.price_sensitivity(o3,p3)
    st.dataframe(tiers[['price_tier','revenue','profit','margin_pct']],width='stretch')
    _t3=tiers.copy(); _t3['price_tier']=_t3['price_tier'].astype(str).map({'luxury':'فاخر','premium':'ممتاز','mid':'متوسط','budget':'اقتصادي'}).fillna(_t3['price_tier'].astype(str))
    st.plotly_chart(fig_bar(_t3,'margin_pct','price_tier','هامش الربح حسب الشريحة',h=True,color='#2dd4bf'),width='stretch')
    sec('23',U(1578,1608,1589,1610,1575,1578))
    dem3=Q.demand(o3,p3)
    recs3=RC.recommend(o3,p3,A.monthly_sales(o3),N.zscore_flags(N.daily_series(o3)),restock_df=dem3)
    bad3=recs3[recs3['level']=='bad']
    if len(bad3):
        st.error(f"{len(bad3)} إجراء فوري مطلوب")
        st.dataframe(bad3.head(10),width='stretch')
    else:
        st.success('لا توجد توصيات حرجة حالياً')
    gaps3,recov3,ups3=DI.growth_opportunities(o3,p3,F.segment_summary(F.compute_rfm(o3)))
    if recov3 is not None and len(recov3):
        st.dataframe(recov3,width='stretch')
        st.error(f'قيمة قابلة للاستعادة: {recov3["revenue"].sum():,.0f}')
    buf3=io.BytesIO()
    with pd.ExcelWriter(buf3,engine='openpyxl') as xw3:
        qa.to_excel(xw3,sheet_name='Quality',index=False)
        churn.to_excel(xw3,sheet_name='ChurnDetail',index=False)
        churn_sum.to_excel(xw3,sheet_name='ChurnSummary',index=False)
        tiers.to_excel(xw3,sheet_name='PriceTiers',index=False)
        if len(gaps3): gaps3.to_excel(xw3,sheet_name='Gaps',index=False)
        if recov3 is not None and len(recov3): recov3.to_excel(xw3,sheet_name='Recoverable',index=False)
        pd.DataFrame([ups3]).to_excel(xw3,sheet_name='Upsell',index=False)
    st.download_button('تحميل تقرير التحليل العميق',buf3.getvalue(),file_name='deep_insights.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
