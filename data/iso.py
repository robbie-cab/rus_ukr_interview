import pandas as pd
import requests

from utils import CACHE


@CACHE.memoize(name="country_iso")
def country_iso():
    url = "https://www.iban.com/country-codes"
    html = requests.get(url).content
    return pd.read_html(html)[0]

def tidy_country_iso():
    df = country_iso()
    to_owid = {
            'Russian Federation (the)': 'Russia',
            'Moldova (the Republic of)': 'Moldova',
            'Viet Nam': 'Vietnam',
            "Korea (the Democratic People's Republic of)": "North Korea",
            "Korea (the Republic of)": "South Korea",
            "Netherlands (the)": "Netherlands",
            "United Kingdom of Great Britain and Northern Ireland (the)": "United Kingdom",
            "United States of America (the)": "United States",
    }
    return df.replace(to_owid)
