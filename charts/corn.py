import geopandas as gpd
import matplotlib
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

    gdf = pd.merge(gdf, df, left_on="iso_a3", right_on="iso3", how="outer")

    fig, ax = plt.subplots(figsize=(12, 8))

    gdf.plot(
        linewidth=1,
        ax=ax,
        edgecolor="0.9",
        aspect="equal",
        color="lightgrey",
    )

    gdf = gdf.dropna(subset=[metric])
    gdf[metric] /= 1e6
    if "Exports" in metric:
        vmax = gdf.loc[gdf["Country"] == "United States", metric]
    else:
        vmax = gdf.loc[gdf["Country"] == "Netherlands", metric]

    gdf.plot(
        column=metric,
        cmap="magma_r",
        linewidth=1,
        ax=ax,
        edgecolor="0.9",
        aspect="equal",
        vmax=vmax,
    )
    ax.axis("off")

    lat = 50
    lon = 17
    lat_window = 25
    lon_window = 30
    ax.set_xlim(lon - lon_window, lon + lon_window)
    ax.set_ylim(lat - lat_window, lat + lat_window)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    fig.savefig(FIG_DIR + fname)


def corn_hbar(df, metric, fname, n=7):
    df = df.dropna(subset=["iso3", metric])
    df = df.sort_values(metric, ascending=True).tail(n)

    fig, ax = fig_axes(width=3.5, height=3)
    fig.subplots_adjust(left=0.3, bottom=0, right=0.85, top=1)

    cmap = matplotlib.cm.get_cmap("magma_r")
    for i in df.index:
        color = cmap(0.3)
        if df.loc[i, "Country"] in ["Russia", "Ukraine"]:
            color = cmap(0.75)
        ax.barh(df.loc[i, "Country"], df.loc[i, metric], color=color)

    if "Exports" in metric:
        suffix = "%"
    else:
        suffix = " kg"
    gap = df[metric].max() * 0.05
    for i in df.index:
        value = df.loc[i, metric]
        ax.text(value + gap, df.loc[i, "Country"], f"{value:.0f}{suffix}", ha="left", va="center")

    fig.savefig(FIG_DIR + fname)
