import pandas as pd
import warnings
import datetime

warnings.filterwarnings("ignore")


def per_hour(df, color_name):
    result = []
    total, aux = 0, 0

    for n in range(df.shape[0]):            
        if df['Cor'][n] == color_name:
            aux += 1
        
        total += 1
        
        try:
            result.append(aux / total)
        except:
            result.append(result[n - 1])

        if n > 0:
            if df['Minute'][n] == 0 and df['Hour'][n] != df['Hour'][n-1]:
                aux = 0
                total = 0

    return result


def clean_data_today():
    now = datetime.datetime.now()
    uthDir = r'\blaze_algorithm\database\today.xlsx'
    df = pd.read_excel(uthDir)

    def minute_to_hour(minute) -> int:
        return int(minute[:2])


    def minute_to_minute(minute) -> int:
        return int(minute[3:])


    def correct_data(data):
        return int(data[5:7])

    def correct_price(price):
        price = price.replace('.', '')
        price = price.replace(',', '.')

        return float(price[3:])
        

    df['Hour'] = df[['Minuto']].apply(lambda minute: minute_to_hour(minute.Minuto), axis=1)
    df['Minute'] = df[['Minuto']].apply(lambda minute: minute_to_minute(minute.Minuto), axis=1)

    df['Day'] = df[['Data']].apply(lambda data: correct_data(data.Data), axis=1)
    df = df.loc[df.Day == now.day, :]

    df['Red bet'] = df[['Apostas no Vermelho']].apply(lambda x: correct_price(x['Apostas no Vermelho']), axis=1)
    df['White bet'] = df[['Apostas no Branco']].apply(lambda x: correct_price(x['Apostas no Branco']), axis=1)
    df['Black bet'] = df[['Apostas no Preto']].apply(lambda x: correct_price(x['Apostas no Preto']), axis=1)

    df.drop(['Data', 'Minuto', 'Apostas no Vermelho', 'Apostas no Branco', 'Apostas no Preto'], axis=1, inplace=True)
    df.sort_values(by=['Day', 'Hour', 'Minute'], inplace=True)

    df['Balance'] = 0

    df.loc[(df['Número'] >= 8), 'Balance'] = df['Red bet'] + df['White bet'] + df['Black bet'] - 2 * df['Black bet']
    df.loc[(df['Número'] >= 1)&(df['Número'] <= 7), 'Balance'] = df['White bet'] + df['Black bet'] + df['Red bet'] - 2 * df['Red bet']
    df.loc[(df['Número'] == 0), 'Balance'] = df['Red bet'] + df['Black bet'] + df['White bet'] - 14 * df['White bet']

    df['Wallet'] = 0
    df.reset_index(drop=True, inplace=True)
    df.iloc[0, 10] = df.iloc[0, 9]

    for n in range(1, df.shape[0]):
        if df['Hour'][n] == 0 and df['Minute'][n] == 0 and df['Hour'][n-1] == 23:
            df.iloc[n, 10] == df.iloc[n, 9]

        else:
            df.iloc[n, 10] = df.iloc[n-1, 10] + df.iloc[n, 9]

    df = df[['Hour', 'Minute', 'Balance', 'Wallet']]

    df.to_csv(r'\blaze_algorithm\JS\today-CLEAN.csv')



def update_today(df_today, df_now):
    now = datetime.datetime.now()
    df_today1 = df_today.loc[(df_today.Hour < df_now.Hour.max())]
    df_today2 = df_today.loc[(df_today.Hour == df_now.Hour.max())&(df_today.Minute < df_now.Minute.min())]
    df_today = pd.concat([df_today1, df_today2], axis=0)
    today_size = df_today.shape[0]

    df_now['Wallet'] = 0

    df_today = pd.concat([df_today, df_now[['Hour', 'Minute', 'Balance', 'Wallet']]], axis=0)
    df_today.reset_index(drop=True)
    df_today = df_today.fillna(0)

    for n in range(today_size, df_today.shape[0]):
        df_today.iloc[n, 3] = df_today.iloc[n-1, 3] + df_today.iloc[n, 2]

    df_today.sort_values(by=['Hour', 'Minute'], inplace=True)


    df_today.to_csv(r'\blaze_algorithm\JS\today-CLEAN.csv')
