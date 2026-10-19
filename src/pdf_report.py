# -*- coding: utf-8 -*-
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import settings as S
def build(kpis, profit, pngs, out=None, recs=None, sentiment_health=None, title='Weekly summary'):
    out = Path(out) if out else (S.DATA_REPORTS_DIR / 'weekly_report.pdf')
    S.DATA_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with PdfPages(out) as pdf:
        # page 1: KPI cover
        fig, ax = plt.subplots(figsize=(8.5, 5))
        ax.axis('off')
        lines = [f"Revenue: {kpis.get('total_revenue', 0):,.0f}",
                 f"Orders: {kpis.get('completed_orders', 0)} / {kpis.get('total_orders', 0)}",
                 f"AOV: {kpis.get('aov', 0):,.0f} | Cancel: {kpis.get('cancel_rate_pct', 0)}%",
                 f"Net profit: {profit.get('net_profit', 0):,.0f} | Margin: {profit.get('margin_pct', 0)}%" if profit else '']
        if sentiment_health:
            lines.append(f"Reviews: {sentiment_health.get('total', 0)} | +{sentiment_health.get('pos_pct', 0)}% / -{sentiment_health.get('neg_pct', 0)}% ({sentiment_health.get('verdict', '')})")
        ax.text(0.08, 0.75, '\n'.join([l for l in lines if l]), fontsize=13, family='monospace')
        if recs is not None and len(recs):
            ax.text(0.08, 0.30, 'Top actions:', fontsize=12, weight='bold')
            for i, t in enumerate(recs['text'].head(5)):
                ax.text(0.08, 0.22 - i * 0.07, f"- {str(t)[:95]}", fontsize=8, family='monospace')
        ax.set_title(title, fontsize=16, weight='bold')
        pdf.savefig(fig)
        plt.close(fig)
        for p in pngs:
            try:
                import matplotlib.image as mpimg
                img = mpimg.imread(p)
                fig2, ax2 = plt.subplots(figsize=(8.5, 6))
                ax2.imshow(img)
                ax2.axis('off')
                ax2.set_title(Path(p).stem, fontsize=11)
                pdf.savefig(fig2)
                plt.close(fig2)
            except Exception:
                continue
    return str(out)

