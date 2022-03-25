import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from data.econ import gas_price
from utils import FIG_DIR, RESOURCE_DIR


def gas_data():
    df = gas_price()
    print(df)


def gas_map(df, metric, fname):
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
