import pandas as pd

from data.iso import country_iso

RESOURCE_DIR = "data/resources/"

def corn_imports():
    df = pd.read_csv(RESOURCE_DIR + "global-food.csv")
    metrics = ['Imports per capita (kg)', 'Imports (t)']
    corn = df["Product"] == "Maize"
    df = df.loc[corn].dropna(subset=metrics)
    latest = df["Year"] == df["Year"].max()
    df = df.loc[latest, ["Country"] + metrics]
    return df.sort_values(metrics[0])


def corn_exports():
    # https://ourworldindata.org/explorers/global-food?tab=chart&time=1998..latest&facet=none&Food=Maize+%28Corn%29&Metric=Exports&Per+Capita=false&country=USA~DEU~FRA~GBR~BRA~ZAF
    df = pd.read_csv(RESOURCE_DIR + "global-food.csv")
    metric = "Exports (t)"
    corn = df["Product"] == "Maize"
    df = df.loc[corn].dropna(subset=[metric])
    latest = df["Year"] == df["Year"].max()
    df = df.loc[latest, ["Country", "Exports (t)"]]
    return df.sort_values("Exports (t)")


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
    iso = country_iso()

    df = pd.merge(df, iso, left_index=True, right_on="Alpha-2 code", how="left")
    return df
