import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from charts.utils import fig_axes
from data.iso import tidy_country_iso
from data.owid import corn_exports, corn_imports
from utils import FIG_DIR, RESOURCE_DIR


def get_corn_data():
    exports = corn_exports()
    imports = corn_imports()
    iso = tidy_country_iso()

    no_iso = set(exports["Country"]) - set(iso["Country"])
    print(no_iso)

    df = pd.merge(exports, imports, how="outer")
    df = pd.merge(df, iso, how="outer")

    world = df.set_index("Country").loc["World", "Exports (t)"]
    df["export %"] = 100 * df["Exports (t)"] / world
    return df


def corn_map(df, metric, fname):
    gdf = gpd.read_file(RESOURCE_DIR + "worldmap.json")

    gdf = pd.merge(gdf, df, left_on="iso_a3", right_on="iso3", how="inner")

    fig, ax = plt.subplots(figsize=(12, 8))
    gdf.plot(
        column=metric,
        cmap="Reds",
        linewidth=1,
        ax=ax,
        edgecolor="0.9",
        # legend = False,
        aspect="equal",
    )
    ax.axis("off")

    lat = 48
    lon = 31
    lat_window = 30
    lon_window = 50
    ax.set_xlim(lon - lon_window, lon + lon_window)
    ax.set_ylim(lat - lat_window, lat + lat_window)

    fig.savefig(FIG_DIR + fname)


def corn_hbar(df, metric, fname, n=7):
    df = df.dropna(subset=["iso3", metric])
    df = df.sort_values(metric, ascending=True).tail(n)

    fig, ax = fig_axes(width=3.5, height=3)
    fig.subplots_adjust(left=0.3, bottom=0, right=0.9, top=1)
    ax.barh(df["Country"], df[metric])

    gap = df[metric].max() * 0.05
    for i in df.index:
        value = df.loc[i, metric]
        ax.text(value + gap, df.loc[i, "Country"], f"{value:.0f}%", ha="left", va="center")

    fig.savefig(FIG_DIR + fname)
