import pandas as pd

from utils import RESOURCE_DIR


def corn_imports():
    df = pd.read_csv(RESOURCE_DIR + "global-food.csv")
    metrics = ["Imports per capita (kg)", "Imports (t)"]
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
