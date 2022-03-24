import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils import CACHE, CACHE_TIME_LIMIT


@CACHE.memoize(name="rub_exchange", expire=CACHE_TIME_LIMIT)
def rub_exchange():
    url = "https://www.exchangerates.org.uk/USD-RUB-exchange-rate-history.html"
    r = requests.get(url).content
    df = pd.read_html(r, header=1)[0]
    df = df.drop(df.index[-1])
    df["datetime"] = pd.to_datetime(df["Date"])
    df["USD_RUB"] = df["US Dollar to Russian Rouble"].apply(lambda x: x.split()[3])
    return df[["datetime", "USD_RUB"]]


def oil_price():
    url = "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/systemaveragepricesapofgas"
    site_html = requests.get(url)
    soup = BeautifulSoup(site_html.text, "html.parser")
    for html in soup.find_all(name="a"):
        if "xlsx" in html.text:
            break

    ons_root = "https://www.ons.gov.uk"
    excel_url = ons_root + html["href"]
    print(excel_url)

    headers = {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
    }
    excel_data = requests.get(excel_url, headers=headers)
    df = pd.read_excel(excel_data.content, sheet_name="System Average Price", header=1)
    df = df[df.columns[0:2]]
    df.columns = ["Date", "Value (p/kWh)"]
    return df
