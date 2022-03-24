from data.iso import tidy_country_iso
from data.owid import corn_exports

import pandas as pd



def get_corn_data():
    corn = corn_exports()
    iso = tidy_country_iso()

    no_iso = set(corn['Country']) - set(iso['Country'])
    print(no_iso)

    df = pd.merge(corn, iso, how='outer').dropna(subset=['Exports (t)'])

    world = df.set_index('Country').loc['World', 'Exports (t)']
    print(world)
    df['proportion'] = df['Exports (t)'] / world
    print(df.sort_values('proportion').tail(20))
