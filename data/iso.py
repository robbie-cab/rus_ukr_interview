import pandas as pd
import requests

from utils import CACHE


@CACHE.memoize(name="country_iso")
def country_iso():
    url = "https://www.iban.com/country-codes"
    html = requests.get(url).content
    return pd.read_html(html)[0]
