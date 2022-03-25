import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point, LineString

import cartopy.feature as cfeature
import pandas as pd
import geoplot

from data.econ import gas_price, gas_imports
from utils import FIG_DIR, RESOURCE_DIR

RUSSIA = [35, 60]

cmap = matplotlib.cm.get_cmap("magma_r")

def draw_gas_line(row):
    center = row.loc['geometry'].centroid
    gas = row.loc['russian_gas'] * 100
    if (center.x > RUSSIA[0]) or (gas < 1): return
    xs = [RUSSIA[0], center.x]
    ys = [RUSSIA[1], center.y]
    plt.plot(xs, ys, ls='-', lw=0.05*gas, color=cmap(gas/100))
    plt.text(xs[1], ys[1], f"{row.loc['Country']}\n{gas:.0f}%", ha='right', va='center')


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

    gdf = gdf.dropna(subset=[metric, 'geometry'])
    for i, row in gdf.iterrows():
        draw_gas_line(row)

    ax.axis("off")

    #gdf.plot(ax=ax, column='center')
    
    #plt.gcf().set_size_inches(20, 10)

    lat = 50
    lon = 15
    lat_window = 20
    lon_window = 30
    ax.set_xlim(lon - lon_window, lon + lon_window)
    ax.set_ylim(lat - lat_window, lat + lat_window)

    plt.savefig(FIG_DIR + fname)
