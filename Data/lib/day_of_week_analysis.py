def check_day_of_week_rise(df, day, change, direction):

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
    print('{}에 {}% 변화했다면, 다음날 상승할 확률은 {}%입니다.'.format(day, change, probability))
# monday 3% down
# day_before, day