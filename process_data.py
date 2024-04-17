import pandas as pd

df = pd.read_csv(r'data.csv')

df["date"] = pd.to_datetime(df["date"], format='%d.%m.%Y')


# converting degrees Celsius to Fahrenheit
def converttemp(x):
    try:
        x = (int(x) * 1.8) + 32
        return float(x)
    except:
        x = (-int(x.replace(x[0], '')) * 1.8) + 32
        return float(x)


df["temp"] = df["temp"].apply(converttemp)

with open(r'data_processed.csv', 'w') as f:
    for date, temp in zip(df["date"].values, df["temp"].values):
        f.write("{},{}\n".format(date, temp))
