import numpy as np
import matplotlib.pyplot as plt
from lib import set_up
import pandas as pd


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