import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from data.iso import tidy_country_iso
from data.owid import corn_exports, corn_imports
from utils import RESOURCE_DIR, FIG_DIR


def get_corn_data():
    exports = corn_exports()
    imports = corn_imports()
    iso = tidy_country_iso()

    no_iso = set(exports["Country"]) - set(iso["Country"])
    print(no_iso)

    df = pd.merge(exports, imports, how="outer")
    df = pd.merge(df, iso, how="outer")

    world = df.set_index("Country").loc["World", "Exports (t)"]
    df["export %"] = df["Exports (t)"] / world
    return df


def corn_map(df, metric):
    gdf = gpd.read_file(RESOURCE_DIR + 'worldmap.json')

    gdf = pd.merge(gdf, df, left_on='iso_a3', right_on='iso3', how='inner')

    fig, ax = plt.subplots(figsize=(12,8))
    gdf.plot(
            column=metric,
            cmap='Reds',
            linewidth=1, 
            ax=ax, 
            edgecolor='0.9', 
            #legend = False,
            aspect = 'equal',
    )
    ax.axis('off')

    #lat = 48
    #lon = 31
    #ax.set_xlim(lon-15, lon+15)
    #ax.set_ylim(lat-10, lat+10)

    fig.savefig(FIG_DIR+'corn_map.pdf')

