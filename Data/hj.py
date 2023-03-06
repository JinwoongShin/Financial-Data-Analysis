
def gdcross(ticker, period):
    import pyupbit
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    ticker = ticker
    count = period

    df = pyupbit.get_ohlcv(ticker, count = count)

    # 50일 200일 이동평균값
    ma50 = df['close'].rolling(window=50).mean()
    ma200 = df['close'].rolling(window=200).mean()

    # 데이터 프레임에 열 추가
    df['ma50'] = ma50
    df['ma200'] = ma200

    # null 삭제
    df = df.dropna()

    buy = []
    sell = []
    def chkCross(df):
        chk = 0
        for i in range(len(df)):
                buy.append(False)
                sell.append(False)
                # hpr.append(1)
                
                if df['ma200'][i] < df['ma50'][i] and chk == 0:
                    print('Golden cross ', str(df.index[i])[:10], df['close'].iloc[i])
                    chk = 1 # 이걸로 ma200<ma50 이어도 이 if문을 넘어가버리게 만든다..
                    buy[i] = True 
                
                elif df['ma200'][i] > df['ma50'][i] and chk == 1:
                    print('Death cross ', str(df.index[i])[:10], df['close'].iloc[i])
                    chk = 0
                    sell[i] = True 

    # 골든크로스/데드크로스 함수 실행
    chkCross(df)        

    # df에 buy, sell 열 추가
    df['buy'] = buy
    df['sell'] = sell

    # 매수 조건 매도 조건 정의
    buy_cond = df['buy'] == True
    sell_cond = df['sell'] == True

    # 매매별 수익률
    ror = df.loc[sell_cond, 'close'].reset_index(drop=True)/df.loc[buy_cond, 'close'].reset_index(drop=True)

    # 누적 수익률
    hpr = ror.cumprod()

    # 최종 누적 수익률
    fhpr = hpr.iloc[-1]

    if fhpr < 1:
        fhpr = - (1 - fhpr)
    else:
        pass

    print(ticker, '총 수익률:', fhpr*100, '%')

import pyupbit

coins = pyupbit.get_tickers(fiat = 'KRW')

gdcross("KRW-BTC", 800)


# # # draw down 계산 
# # df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# # print("MDD(%): ", df['dd'].max())


# df.to_excel("KRW-BTC_50,200일_이평선_크로스_백테스팅5.xlsx")

# # %matplotlib inline
# fig = plt.figure(figsize=(15, 8))
# plt.plot(df['close'],label='close') #### 헐 시발 그냥 이렇게 종가 이은게 스윙차트인가봐!!!!!
# plt.plot(df['ma50'],label='ma50')
# plt.plot(df['ma200'],label='ma200')
# plt.plot(df.ma50[df.buy == True], '^', markersize=10, color='r')     # 매수지점 Marking
# plt.plot(df.ma50[df.sell == True], 'v', markersize=10, color='b')    # 매도지점 Marking

# # 매도, 매수 시점에 종가 Text 보여 주기. +500은 Text가 조금 높게 보이도록 함
# for i in range(len(df)):
#     if df.buy[i] == True:
#         # (X, Y, Text), X는 index, Y는 ma20 값에 + 500
#         plt.text(df.index[i], int(df['ma120'][i]) + 100, str(df['close'][i]))

#     if df.sell[i] == True:
#         plt.text(df.index[i], int(df['ma120'][i]) + 100, str(df['close'][i]))

# plt.legend()
# plt.grid()
# plt.tight_layout()
# plt.show()

# # #수익률 계산 코딩하기
