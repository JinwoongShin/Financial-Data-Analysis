from datetime import date, datetime
from lib import day_of_week_analysis
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from pandas import DataFrame, Series
from lib import set_up
plt.style.use('seaborn-v0_8')

# today = datetime.now().date().strftime("%Y-%m-%d")

#종목의 티커를 설정하는 부분입니다.
# nasdaq = yf.Ticker('^ixic')

# ##종목 조회 기간 설정
# df = nasdaq.history(start="2007-01-01", end=today)

# stock_date = df.index
# price = df['Close']


# yesterday_price = df['Close'].shift()
# poc = (price-yesterday_price)/yesterday_price*100
# df['percentage_change'] = poc
# df['day'] = df.index
# df['day_name'] = df['day'].dt.day_name()

#start date should be in form of 2007-01-01
df = set_up.set_stock_df('nasdaq', '^ixic', '2010-01-01')
day_of_week_analysis.check_day_of_week_rise(df, 'Friday', 0, 'up')