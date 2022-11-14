from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from lib import mf, set_up
from pandas import DataFrame, Series

plt.style.use('seaborn-v0_8')


df = set_up.set_stock_df('nasdaq', '^ixic', '2010-01-01') # format ('name', 'ticker', 2020-01-01)
#day_of_week_analysis.effect_day_of_week_rise(df, 'Friday', 3, 'down') # format (df, 'day of week', 'int', 'up or down')
#day_of_week_analysis.day_of_week_rise(df, 'Friday')
# mf.up_leads_up(df, 4)
# mf.down_leads_down(df, -4)
# data = []
# for i in list(np.arange(-10, 0, 0.1)):
#     data.append(mf.down_leads_down(df, i))

# plt.figure()
# plt.plot(list(np.arange(-10, 0, 0.1)), data)
# plt.ylabel('probability')
# plt.xlabel('% Drop')
# plt.show()
mf.plot_effect_of_day_before(df, -8, 8, 0.1)