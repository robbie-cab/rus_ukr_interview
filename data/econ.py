import pandas as pd
import requests
from bs4 import BeautifulSoup

from data.iso import tidy_country_iso
from utils import CACHE, CACHE_TIME_LIMIT, RESOURCE_DIR


@CACHE.memoize(name="rub_exchange", expire=CACHE_TIME_LIMIT)
def rub_exchange():
    url = "https://www.exchangerates.org.uk/USD-RUB-exchange-rate-history.html"
    r = requests.get(url).content
    df = pd.read_html(r, header=1)[0]
    df = df.drop(df.index[-1])
    df["datetime"] = pd.to_datetime(df["Date"])
    df["USD_RUB"] = df["US Dollar to Russian Rouble"].apply(lambda x: x.split()[3])
    return df[["datetime", "USD_RUB"]]


@CACHE.memoize(name="gas_price", expire=CACHE_TIME_LIMIT)
def gas_price():
    url = "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/systemaveragepricesapofgas"  # noqa
    site_html = requests.get(url)
    soup = BeautifulSoup(site_html.text, "html.parser")
    # first xlsx link is the most up to date
    for html in soup.find_all(name="a"):
        if "xlsx" in html.text:
            break

    ons_root = "https://www.ons.gov.uk"
    excel_url = ons_root + html["href"]
    headers = {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
    }
    excel_data = requests.get(excel_url, headers=headers)

    df = pd.read_excel(excel_data.content, sheet_name="System Average Price", header=1)
    df = df[df.columns[0:2]]
    df.columns = ["Date", "Value (p/kWh)"]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna()
    return df

def gas_imports():
    # https://aegis.acer.europa.eu/chest/dataitems/214/view
    df = pd.DataFrame()
    data = pd.read_excel(
        RESOURCE_DIR + "Estimated number and diversity of supply sources  2020.xlsx",
        header=10,
    )
    source_cols = [col for col in data.columns if "Origin" in col]
    perc_cols = [col for col in data.columns if "%" in col]
    for country in data["MS"].unique():
        cdf = data[data["MS"] == country]
        latest = cdf["Year"].max()
        cdf = cdf.set_index("Year")
        for i, col in enumerate(source_cols):
            if cdf.loc[latest, col] == "RU":
                df.loc[country, "russian_gas"] = cdf.loc[latest, perc_cols[i]]
                df.loc[country, "year"] = latest
    df = df.sort_values("russian_gas")
    iso = tidy_country_iso()

    df = pd.merge(df, iso, left_index=True, right_on="iso2", how="left")
    return df
