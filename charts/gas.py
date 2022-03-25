import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point

from data.econ import gas_price
from utils import FIG_DIR, RESOURCE_DIR

RUSSIA = [40, 60]

cmap = matplotlib.cm.get_cmap("magma_r")


def draw_gas_line(row):
    center = row.loc["geometry"].centroid
    gas = row.loc["russian_gas"] * 100
    country = row.loc["Country"]

    if "North Macedonia" in country:
        country = "North Macedonia"
    if country == "France":
        center = Point(2.2, 46.2)
    if country == "Slovenia":
        return

    if (center.x > RUSSIA[0]) or (gas < 1):
        return
    xs = [RUSSIA[0], center.x]
    y1s = [RUSSIA[1], center.y - 0.01 * gas]
    y2s = [RUSSIA[1], center.y + 0.01 * gas]
    plt.fill_between(xs, y1s, y2s, color=cmap(gas / 100), alpha=0.6, lw=0)

    plt.text(xs[1], center.y, f"{country}", ha="right", va="bottom", fontweight="bold")
    plt.text(xs[1], center.y, f"{gas:.0f}%", ha="right", va="top")


def gas_map(df, metric, fname):
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
    """
    gdf.plot(
        column=metric,
        cmap="magma_r",
        linewidth=1,
        ax=ax,
        edgecolor="0.9",
        # legend = False,
        aspect="equal",
    )
    """
    gdf = gdf.dropna(subset=[metric, "geometry"])
    for i, row in gdf.iterrows():
        draw_gas_line(row)
    plt.plot(RUSSIA[0], RUSSIA[1], marker="o", ms=100, c=cmap(0.75))
    plt.text(RUSSIA[0], RUSSIA[1], f"Russian\ngas", ha="center", va="center", color="white")

    ax.axis("off")

    # gdf.plot(ax=ax, column='center')

    # plt.gcf().set_size_inches(20, 10)

    lat = 50
    lon = 18
    lat_window = 15
    lon_window = 30
    ax.set_xlim(lon - lon_window, lon + lon_window)
    ax.set_ylim(lat - lat_window, lat + lat_window)

    plt.savefig(FIG_DIR + fname)
