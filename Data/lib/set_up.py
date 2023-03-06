from datetime import date, datetime
import pandas as pd
import yfinance as yf
#종목의 티커를 설정하는 부분입니다.
today = datetime.now().date().strftime("%Y-%m-%d")

def set_stock_df(stock, ticker, start_date):
    
    stock = yf.Ticker(ticker)

    ##종목 조회 기간 설정
    df = stock.history(start=start_date, end=today)

    price = df['Close']
    yesterday_price = df['Close'].shift()
    poc = (price-yesterday_price)/yesterday_price*100
    df['percentage_change'] = poc
    df['date'] = df.index
    df['day_name'] = df['date'].dt.day_name()
    df.reset_index(drop=False, inplace=True)
    return df
