import pandas as pd
import requests

from utils import CACHE


@CACHE.memoize(name="rub_exchange")
def rub_exchange():
    url = "https://www.exchangerates.org.uk/USD-RUB-exchange-rate-history.html"
    r = requests.get(url).content
    df = pd.read_html(r, header=1)[0]
    df = df.drop(df.index[-1])
    df["datetime"] = pd.to_datetime(df["Date"])
    df["USD_RUB"] = df["US Dollar to Russian Rouble"].apply(lambda x: x.split()[3])
    return df[["datetime", "USD_RUB"]]
