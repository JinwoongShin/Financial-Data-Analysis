from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from lib import mf, set_up
from pandas import DataFrame, Series
import pandas as pd

plt.style.use('seaborn-v0_8')


df = set_up.set_stock_df('S&P', '^ixic', '2012-09-20') # format ('name', 'ticker', 2020-01-01)
#df_Y = set_up.set_stock_df('10Y', '^TNX', '2010-01-01')

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
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#이동평균선 매매법
#df_MA = mf.moving_average(df, 50, 200)
#print(df)
#df_cross_point = mf.cross_point(df_MA, 50, 200)
#print(df_cross_point)
#print(df_MA.at['2010-01-04', 'Long Term MA'])
#mf.test_cross_point_strategy(df_cross_point, 100, 0)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#조정 매매법
#print(mf.correction_move_strategy(df, 3))

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#터틀매매
turtle_df = mf.turtle_line(df, 20, 10)
# x = list(newdf.index)
# LH = list(newdf['Long Term High'])
# LL = list(newdf['Long Term Low'])
# SH = list(newdf['Short Term High'])
# SL = list(newdf['Short Term Low'])

# plt.plot(x, LH, color="green")
# plt.plot(x, LL, color="green")å
# plt.plot(x, SH, color="red")
# plt.plot(x, SL, color="red")

# plt.show()
# print(newdf)
list_of_trade = mf.test_turtle_strategy(df,turtle_df, 1000)
pd.set_option('display.max_rows', None)
print(list_of_trade)