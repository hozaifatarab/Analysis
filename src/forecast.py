# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
def monthly_series(orders):
    done = orders[orders['status'] == 'completed'].copy()
    done['order_date'] = pd.to_datetime(done['order_date'], errors='coerce')
    done = done.dropna(subset=['order_date'])
    done['month'] = done['order_date'].dt.to_period('M').astype(str)
    g = done.groupby('month')['total'].sum().reset_index()
    g['ds'] = pd.to_datetime(g['month'])
    return g.sort_values('ds').rename(columns={'total': 'y'})
def linear_forecast(series, periods=3):
    y = series['y'].to_numpy(float)
    x = np.arange(len(y))
    a, b = np.polyfit(x, y, 1)
    fut_x = np.arange(len(y), len(y) + periods)
    fut_y = a * fut_x + b
    last = series['ds'].max()
    fut_ds = [last + pd.offsets.MonthBegin(i + 1) for i in range(periods)]
    hist = series[['ds', 'y']].copy()
    hist['kind'] = 'actual'
    fut = pd.DataFrame({'ds': fut_ds, 'y': np.maximum(fut_y, 0), 'kind': 'forecast'})
    resid = y - (a * x + b)
    mae = float(np.mean(np.abs(resid)))
    return pd.concat([hist, fut], ignore_index=True), {'slope': float(a), 'intercept': float(b), 'mae': round(mae, 2)}
