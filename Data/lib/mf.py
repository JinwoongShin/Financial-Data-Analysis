import numpy as np
import matplotlib.pyplot as plt


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
