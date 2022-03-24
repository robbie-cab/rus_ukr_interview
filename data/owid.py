import pandas as pd

RESOURCE_DIR = 'data/resources/'

# https://ourworldindata.org/explorers/global-food?tab=chart&time=1998..latest&facet=none&Food=Maize+%28Corn%29&Metric=Exports&Per+Capita=false&country=USA~DEU~FRA~GBR~BRA~ZAF
def corn_exports():
    df = pd.read_csv(RESOURCE_DIR+'global-food.csv')
    metric = 'Exports (t)'
    corn = df['Product'] == 'Maize'
    df = df.loc[corn].dropna(subset=[metric])
    latest = df['Year'] == df['Year'].max()
    df = df.loc[latest, ['Country', 'Exports (t)']]
    return df.sort_values('Exports (t)')
