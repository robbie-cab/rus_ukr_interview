from data.iso import tidy_country_iso
from data.owid import corn_exports

import pandas as pd

def get_corn_data():
    exports = corn_exports()
    imports = corn_imports()
    iso = tidy_country_iso()

    no_iso = set(exports['Country']) - set(iso['Country'])
    print(no_iso)

    df = pd.merge(exports, imports, how='outer')
    df = pd.merge(df, iso, how='outer')

    world = df.set_index('Country').loc['World', 'Exports (t)']
    df['export %'] = df['Exports (t)'] / world
    return df
