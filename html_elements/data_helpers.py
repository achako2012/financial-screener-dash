import pandas as pd

def clear_table(table_name):
    # skip first row with ad link
    data = pd.read_csv('data/{}.csv'.format(table_name), skiprows=1)

    # delete unnecassery columns
    data.drop(['unix', 'Volume {}'.format(table_name[:3]),
              'Volume {}'.format(table_name[3:6])], axis=1, inplace=True)

    # reverse data frames
    data = data.iloc[::-1]

    # remove unnecessary data. we need only date starts on 2019
    data = data[data['date'] > '2018-31-12']

    return data


def clear_data(array):
    data = {}

    for elem in array:
        data[elem] = clear_table(elem)

    return data


def get_filter_data(coin_pair, timeframe, select_year, data):
    # we need to chouse which data frame we'll use
    if coin_pair == 'btceur':
        df = data["BTCEUR_1h"], data["BTCEUR_d"]
    elif coin_pair == 'btcusd':
        df = data["BTCUSD_1h"], data["BTCUSD_d"]
    elif coin_pair == 'ethbtc':
        df = data["ETHBTC_1h"], data["ETHBTC_d"]
    else:
        df = data["ETHEUR_1h"], data["ETHEUR_d"]

    # Since we have 2 timeframes for each data frame we need to chose which one we take
    if timeframe == 'hour':
        df = df[0]
    else:
        df = df[1]

    filtered_df = df.loc[(df['date'] > '{}-12-31 00:00:00'.format(select_year-1))
                         & (df['date'] < '{}-01-01 00:00:00'.format(select_year+1))]

    return filtered_df