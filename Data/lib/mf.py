import numpy as np
import matplotlib.pyplot as plt
from lib import set_up
import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def effect_day_of_week_rise(df, day, change, direction):

    days_down = 0
    days_up = 0
    if direction == 'up':
        for idx in df.index:
            if  df.at[idx, 'percentage_change'] > 0 and df.shift().at[idx, 'percentage_change'] > change and df.shift().at[idx, 'day_name'] == day:
                days_up = days_up + 1
            elif df.at[idx, 'percentage_change'] < 0 and df.shift().at[idx, 'percentage_change'] > change and df.shift().at[idx, 'day_name'] == day:
                days_down = days_down + 1

    if direction == 'down':
        change = -change
        for idx in df.index:
            if  df.at[idx, 'percentage_change'] > 0 and df.shift().at[idx, 'percentage_change'] < change and df.shift().at[idx, 'day_name'] == day:
                days_up = days_up + 1
            elif df.at[idx, 'percentage_change'] < 0 and df.shift().at[idx, 'percentage_change'] < change and df.shift().at[idx, 'day_name'] == day:
                days_down = days_down + 1
    probability = days_up/(days_up + days_down)*100
    #print('{}에 {}% 변화했다면, 다음날 상승할 확률은 {}%입니다.'.format(day, change, probability))
    return probability


def day_of_week_rise(df, day):
    days_down = 0
    days_up = 0
    for idx in df.index:
        if  df.at[idx, 'percentage_change'] > 0 and df.at[idx, 'day_name'] == day:
            days_up = days_up + 1
        elif df.at[idx, 'percentage_change'] < 0 and df.at[idx, 'day_name'] == day:
            days_down = days_down + 1
    probability = days_up/(days_up + days_down)*100
    #print('{}에 상승할 확률은 {}%입니다.'.format(day, probability))
    return probability


def down_leads_down(df, change):
    days_down = 0
    days_up = 0
    for idx in df.index:
        if df.at[idx, 'percentage_change'] < change and df.shift(-1).at[idx, 'percentage_change'] < 0:
            days_down = days_down +1
        elif df.at[idx, 'percentage_change'] < change and df.shift(-1).at[idx, 'percentage_change'] > 0:
            days_up = days_up + 1
    probability = days_up/(days_up + days_down)*100
    #print('{}이상 하락했을 때, 다음날 상승할 확률은 {}%입니다'.format(change, probability))
    return probability




def up_leads_up(df, change):
    days_down = 0
    days_up = 0
    for idx in df.index:
        if df.at[idx, 'percentage_change'] > change and df.shift(-1).at[idx, 'percentage_change'] < 0:
            days_down = days_down +1
        elif df.at[idx, 'percentage_change'] > change and df.shift(-1).at[idx, 'percentage_change'] > 0:
            days_up = days_up + 1
    probability = days_up/(days_up + days_down)*100
    #print('{}이상 상승했을 때, 다음날 상승할 확률은 {}%입니다'.format(change, probability))
    return probability
# monday 3% down
# day_before, day

def plot_effect_of_day_before(df, start, end, interval):
    spectrum = np.arange(start, end, interval)
    data = []
    for i in spectrum:
        if i < 0:
            data.append(down_leads_down(df, i))
        else:
            data.append(up_leads_up(df, i))

    plt.figure()
    plt.plot(spectrum, data)
    plt.ylabel('probability')
    plt.xlabel('% change')
    plt.show()

def effect_of_vix_up (df_stock, vix_change, start_date):
    days_down = 0
    days_up = 0
    df_vix = set_up.set_stock_df('vix', '^VIX', start_date)
    for idx in df_stock.index:
        if df_vix.at[idx, 'percentage_change'] > vix_change and df_stock.at[idx, 'percentage_change'] < 0:
            days_down = days_down +1
        elif df_vix.at[idx, 'percentage_change'] > vix_change and df_stock.at[idx, 'percentage_change'] > 0:
            days_up = days_up + 1
    probability = days_up/(days_up + days_down)*100
    return probability

def effect_of_vix_down (df_stock, vix_change, start_date):
    days_down = 0
    days_up = 0
    df_vix = set_up.set_stock_df('vix', '^VIX', start_date)
    for idx in df_stock.index:
        if df_vix.at[idx, 'percentage_change'] < vix_change and df_stock.at[idx, 'percentage_change'] < 0:
            days_down = days_down +1
        elif df_vix.at[idx, 'percentage_change'] < vix_change and df_stock.at[idx, 'percentage_change'] > 0:
            days_up = days_up + 1
    probability = days_up/(days_up + days_down)*100
    return probability

def effect_of_vix_next_day(df_stock, start_date):
    days_down = 0
    days_up = 0
    df_vix = set_up.set_stock_df('vix', '^VIX', start_date)
    for idx in df_stock.index:
        if df_vix.at[idx, 'percentage_change'] < 0 and df_stock.at[idx, 'percentage_change'] < 0:
            if df_stock.shift(-1).at[idx, 'percentage_change']>0:
                days_up = days_up + 1
            else:
                days_down = days_down + 1
    probability = days_up/(days_up + days_down)*100
    return probability



            
def merge(df1, df2, factor):
    df1_adding = df1[factor]
    df2_adding = df2[factor]
    df_merged = pd.concat([df1_adding, df2_adding], axis=1)
    df_merged.columns = ['{}_stock'.format(factor)], ['{}_control'.format(factor)]
    return df_merged

def effect_of_10Y_next_day(df_stock, factor, start_date):
    #10년물 금리와 주가를 비교하기 전에, 휴장일을 반영하기 위해 날짜에 맞추어 데이터를 정리해준다.
    df_10y = set_up.set_stock_df('10Y', '^TNX', start_date)
    df_stock_adding = df_stock[factor]
    df_10y_adding = df_10y[factor]
    df_arranged = pd.concat([df_stock_adding, df_10y_adding], axis=1)
    df_arranged.columns = ['{}_stock'.format(factor), '{}_control'.format(factor)]

    days_down = 0
    days_up = 0
    #금리와 주가가 모두 상승한 조건에서 다음날 오른 경우와 하락한 경우 파악
    for idx in df_arranged.index:
        if df_arranged.at[idx, '{}_stock'.format(factor)] > 0 and df_arranged.at[idx, '{}_control'.format(factor)] >0:
            if df_arranged.shift(-1).at[idx, '{}_control'.format(factor)] > 0:
                days_up = days_up + 1
            else:
                days_down = days_down + 1
                
    probability = days_up/(days_up + days_down)*100
    return probability

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#이동평균선 매매 전략
def moving_average(df_stock, short_term, long_term):
    long_term_mean = df_stock['Close'].rolling(long_term).mean()
    short_term_mean = df_stock['Close'].rolling(short_term).mean()
    df_stock['Long Term MA'] = long_term_mean
    df_stock['Short Term MA'] = short_term_mean
    return df_stock

def cross_point(df_MA, short, long):
    df_next_day = df_MA.shift(-1)
    cross_point = pd.DataFrame({'Date':[], 'Close':[], 'Type':[]})
    for i in df_MA.index:
        if i >= long-1:
            if df_MA.at[i, 'Long Term MA'] > df_MA.at[i, 'Short Term MA'] and df_next_day.at[i, 'Long Term MA'] < df_next_day.at[i, 'Short Term MA']:
                new_df = pd.DataFrame({'Date':[df_next_day.at[i, 'Date']], 'Close':[df_next_day.at[i, 'Close']], 'Type':['Golden Cross']})
                cross_point = cross_point.append(new_df, ignore_index = True)
            elif df_MA.at[i, 'Long Term MA'] < df_MA.at[i, 'Short Term MA'] and df_next_day.at[i, 'Long Term MA'] > df_next_day.at[i, 'Short Term MA']:
                new_df = pd.DataFrame({'Date':[df_next_day.at[i, 'Date']], 'Close':[df_next_day.at[i, 'Close']], 'Type':['Death Cross']})
                cross_point = cross_point.append(new_df, ignore_index = True)
    return cross_point


def test_cross_point_strategy(df_cross_point, initial, stop_loss_):
    number_of_shares_held = 0
    balance = initial
    print(df_cross_point.iloc[0]['Date'], balance, df_cross_point.iloc[0]['Type'])
    for i in df_cross_point.index:
        if i > 0:
            if df_cross_point.at[i, 'Type'] == 'Golden Cross':
                percentage_change = (df_cross_point.iloc[i]['Close']-df_cross_point.iloc[i-1]['Close'])/df_cross_point.iloc[i-1]['Close']
                balance = balance*(1-percentage_change)
                print(df_cross_point.iloc[i]['Date'], balance, 'Golden Cross')

            if df_cross_point.at[i, 'Type'] == 'Death Cross':
                percentage_change = (df_cross_point.iloc[i]['Close']-df_cross_point.iloc[i-1]['Close'])/df_cross_point.iloc[i-1]['Close']
                balance = balance*(1+percentage_change)
                print(df_cross_point.iloc[i]['Date'], balance, 'Death Cross')
    return
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#연속 상승, 하락한 이후 조정 매매 투자법
def correction_move_strategy(df, day):
    day_range = range(day)
    count = 0
    correction_move_point = pd.DataFrame({'Date':[], 'Close':[], 'Type':[]})

    i=0
    while i < len(df)-day+1:
        for j in list(day_range):
            if df.iloc[i+j]['percentage_change'] > 0:
               count = count + 1
        if count/day == 1:
            add_df = pd.DataFrame({'Date':[df.iloc[i+day-1]['Date']], 'Close':[df.iloc[i+day-1]['Close']], 'Type':['Over Bought']})
            correction_move_point = correction_move_point.append(add_df, ignore_index = True)
            i = i + day
        else:
            i = i + 1
        count = 0
    return correction_move_point

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#터틀매매법
#4주 고점&저점, 2주 고점&저점 생성함수
#4주 고점&저점 돌파 확인 함수
#손절매 확인 함수 설정
#매매 함수 설정
def turtle_line(df, long_term_week, short_term_week):
    #기간동안의 최댓값을 구하는 함수
    #list.pop[index]
    #list.append로 추가
    long_term_block_high = [0 for i in range(long_term_week)]
    long_term_block_low = [10000000 for i in range(long_term_week)]
    short_term_block_high = [0 for i in range(short_term_week)]
    short_term_block_low = [10000000 for i in range(short_term_week)]

    long_term_high = []
    long_term_low = []
    short_term_high= []
    short_term_low= []
    max_min_line_df = pd.DataFrame()

    for i in df.index:
        long_term_block_high.pop(0)
        long_term_block_low.pop(0)
        short_term_block_high.pop(0)
        short_term_block_low.pop(0)
        
        long_term_block_high.append(df.iloc[i]['High'])
        long_term_block_low.append(df.iloc[i]['Low'])
        short_term_block_high.append(df.iloc[i]['High'])
        short_term_block_low.append(df.iloc[i]['Low']) 
        
        long_term_high.append(max(long_term_block_high))
        long_term_low.append(min(long_term_block_low))
        short_term_high.append(max(short_term_block_high))
        short_term_low.append(min(short_term_block_low))
    max_min_line_df['Date'] = df['Date']
    max_min_line_df['Long Term High']=long_term_high
    max_min_line_df['Long Term Low']=long_term_low
    max_min_line_df['Short Term High']=short_term_high
    max_min_line_df['Short Term Low']=short_term_low
    return max_min_line_df

def test_turtle_strategy(df, df_turtle, initial_capital):
    df_list_of_trade = pd.DataFrame()
    Long_condition = 0
    Short_condition = 0
    for i in df.index:
        if i < 19:
            continue
        #롱 진입
        if df.iloc[i]['High']>df_turtle.iloc[i-1]['Long Term High'] and Long_condition == 0 and Short_condition == 0:
            Long_condition = 1
            add_df = pd.DataFrame({'Date':[df.iloc[i]['Date']], 'Position':['Long'], 'Buying Price':[df_turtle.iloc[i-1]['Long Term High']], 'Selling Price':[0]})
            df_list_of_trade = df_list_of_trade.append(add_df, ignore_index = True)
            continue

        #롱 정리 혹은 손절
        if df.iloc[i]['Low']<df_turtle.iloc[i-1]['Short Term Low'] and Long_condition == 1 and Short_condition == 0:
            Long_condition = 0
            add_df = pd.DataFrame({'Date':[df.iloc[i]['Date']], 'Position':['Sell'], 'Buying Price':[0], 'Selling Price':[df_turtle.iloc[i-1]['Short Term Low']]})
            df_list_of_trade = df_list_of_trade.append(add_df, ignore_index = True)
            continue
        
        #숏 진입
        if df.iloc[i]['Low']<df_turtle.iloc[i-1]['Long Term Low'] and Short_condition == 0 and Long_condition == 0:
            Short_condition = 1
            add_df = pd.DataFrame({'Date':[df.iloc[i]['Date']], 'Position':['Short'], 'Buying Price':[0], 'Selling Price':[df_turtle.iloc[i-1]['Long Term Low']]})
            df_list_of_trade = df_list_of_trade.append(add_df, ignore_index = True)
            continue
        #숏 정리 혹은 손절
        if df.iloc[i]['High']>df_turtle.iloc[i-1]['Short Term High'] and Short_condition ==1 and Long_condition == 0:
            Short_condition = 0
            add_df = pd.DataFrame({'Date':[df.iloc[i]['Date']], 'Position':['Buy'], 'Buying Price':[df_turtle.iloc[i-1]['Short Term High']], 'Selling Price':[0]})
            df_list_of_trade = df_list_of_trade.append(add_df, ignore_index = True)
            continue
    
    capital = initial_capital
    list_capital= []
    i = 1
    while i < len(df_list_of_trade):
        if df_list_of_trade.iloc[i]['Position']=='Sell':
            list_capital.append(capital)
            percentage_change = (df_list_of_trade.iloc[i]['Selling Price']-df_list_of_trade.iloc[i-1]['Buying Price'])/df_list_of_trade.iloc[i-1]['Buying Price']
            capital = capital*(1+percentage_change)
            list_capital.append(capital)
            i = i +2
        elif df_list_of_trade.iloc[i]['Position']=='Buy':
            list_capital.append(capital)
            percentage_change = (df_list_of_trade.iloc[i-1]['Selling Price'] - df_list_of_trade.iloc[i]['Buying Price'])/df_list_of_trade.iloc[i-1]['Selling Price']
            capital = capital*(1+percentage_change)
            list_capital.append(capital)
            i = i + 2
        if i ==len(df_list_of_trade):
            list_capital.append(capital)
            break
    df_list_of_trade['Capital'] = list_capital
    
    return df_list_of_trade
#3,000,000 9개의 거래