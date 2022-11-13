import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
from pandas import Series, DataFrame
plt.style.use('seaborn-v0_8')

nasdaq = yf.Ticker('^ixic')

# stockinfo = msft.info
# for key, value in stockinfo.items():
#     print(key, ":", value)
today = datetime.now().date().strftime("%Y-%m-%d")

df = nasdaq.history(start="2007-01-01", end=today)

stock_date = df.index
price = df['Close']


y_price = df['Close'].shift()
poc = (price-y_price)/y_price*100
df['percentage_change'] = poc
df['day'] = df.index
# print(df)
# print(poc)
# print(df['Open'])
#f['day_name'] = df.datetime.dt.day_name()

df['day_name'] = df['day'].dt.day_name()
print(df.info())

# def check_day_of_weeks_effect(data):
#      for idx in df.index:
#           if df.shift().iloc[3994]['day_name'] == 'Friday' and df.iloc[3994]['percentage_change']<0 and df.shift().iloc[3994]['percentage_change']<0:
#            count = count + 1
#      return count


# friday = 0
# for idx in df.index:
#           if df.at[idx, 'day_name'] == 'Friday':
#                friday = friday + 1

# percentage = fridaydown_mondaydown/friday*100
# print('금요일에 하락하고 월요일에 하락할 확률은 {}%입니다'.format(percentage))

fd_md = 0
fd_mu = 0
monday = 0
for idx in df.index:
     if df.shift().at[idx, 'day_name'] == 'Friday' and df.at[idx, 'percentage_change']<0 and df.shift().at[idx, 'percentage_change']>1.8:
          fd_md = fd_md + 1


for idx in df.index:
     if df.shift().at[idx, 'day_name'] == 'Friday' and df.at[idx, 'percentage_change']>0 and df.shift().at[idx, 'percentage_change']>1.8:
          fd_mu = fd_mu + 1

prb_fd_mu = fd_mu/(fd_mu+fd_md)*100



# md=0
# mu=0
# for idx in df.index:
#      if df.at[idx, 'day_name'] == 'Friday' and df.at[idx, 'percentage_change']<0:
#           md = md + 1


# for idx in df.index:
#      if df.at[idx, 'day_name'] == 'Friday' and df.at[idx, 'percentage_change']>0:
#           mu = mu + 1
# prb_mp = mu/(mu+md)*100
# print('월요일에 주식이 오를 확률은 {}%입니다'.format(prb_mp))
print('금요일에 1.8%이상 상승했다면, 월요일에 오를 확률은 {}%입니다'.format(prb_fd_mu))