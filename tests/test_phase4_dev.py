# -*- coding: utf-8 -*-
import pandas as pd
from src import sentiment as T
from src import recommender as R
from src import assistant as S
from src import store_db as D
def _data():
    o = pd.DataFrame({'order_id': ['O1', 'O2', 'O3', 'O4'], 'customer_id': ['C1', 'C1', 'C2', 'C3'],
                      'product_id': ['P1', 'P2', 'P1', 'P1'], 'quantity': [1, 1, 1, 1],
                      'price': [100.0, 200.0, 100.0, 100.0], 'total': [100.0, 200.0, 100.0, 100.0],
                      'status': ['completed'] * 4, 'order_date': pd.to_datetime(['2025-01-05'] * 4),
                      'payment_method': ['mada'] * 4, 'city': ['Riyadh'] * 4, 'month': ['2025-01'] * 4})
    pr = pd.DataFrame({'product_id': ['P1', 'P2'], 'product_name': ['A', 'B'], 'category': ['c1', 'c2'],
                       'price': [100.0, 200.0], 'cost': [95.0, 50.0], 'rating': [4.0, 4.5]})
    return o, pr
def test_arabic_sentiment():
    assert T.score_text('منتج ممتاز ورائع وسريع') == 'positive'
    assert T.score_text('سيء وتالف ومتأخر') == 'negative'
    out = T.analyze(pd.DataFrame({'product_id': ['P1', 'P1'], 'review': ['ممتاز رائع', 'سيء تالف']}), text_col='review')
    assert 'neg_rate' in out['by_product'].columns
    h = T.overall_health(out['summary'])
    assert h['total'] == 2 and h['verdict'] in ('healthy', 'watch', 'critical')
def test_assistant_arabic():
    o, pr = _data()
    assert S.answer('ما الربح في الرياض؟', o, pr)[0] == 'profit'
    assert S.answer('توقع المبيعات؟', o, pr)[0] in ('forecast', 'kpis')
    assert S.answer('شرائح العملاء؟', o, pr)[0] == 'table'
    assert S.answer('المنتجات تحتاج إعادة طلب؟', o, pr)[0] == 'table'
def test_recommender_extended():
    o, pr = _data()
    r = R.recommend(o, pr, restock_df=pd.DataFrame({'product_id': ['P1'], 'product_name': ['A'], 'daily': [2.0], 'reorder_point': [28.0]}))
    assert 'value' in r.columns and len(r) >= 1
def test_store_db_extended(tmp_path=None):
    o, pr = _data()
    p = D.save_run(o, pr, {'total_revenue': 500.0}, tag='test-dev')
    assert 'store.db' in p
    h = D.run_history(5)
    assert len(h) >= 1
