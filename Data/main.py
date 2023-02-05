from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from lib import mf, set_up
from pandas import DataFrame, Series
import pandas as pd

plt.style.use('seaborn-v0_8')


df = set_up.set_stock_df('nasdaq', '^ixic', '2010-01-01') # format ('name', 'ticker', 2020-01-01)
df_Y = set_up.set_stock_df('10Y', '^TNX', '2010-01-01')

#day_of_week_analysis.effect_day_of_week_rise(df, 'Friday', 3, 'down') # format (df, 'day of week', 'int', 'up or down')
#day_of_week_analysis.day_of_week_rise(df, 'Friday')
#mf.up_leads_up(df, 4)
#mf.down_leads_down(df, -4)
#mf.plot_effect_of_day_before(df, -8, 8, 0.1)
#print(mf.effect_of_vix_down(df, -3, '2010-01-01'))
#print(mf.effect_of_vix_next_day(df, '2010-01-01'))
#print(mf.effect_of_10Y_next_day(df, '2010-01-01'))

#print(mf.effect_of_10Y_next_day(df, 'percentage_change', '2010-01-01'))
#print(df)
print(mf.moving_average(df, 2, 10))
