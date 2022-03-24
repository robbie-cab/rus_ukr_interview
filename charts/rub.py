from data.econ import rub_exchange
from charts.utils import fig_axes
from utils import FIG_DIR
import matplotlib
import pandas as pd

def rub_chart(fname):
    df = rub_exchange()
    df['USD_RUB'] = pd.to_numeric(df['USD_RUB'])
    df['RUB_USD'] = 1 / df['USD_RUB']
    print(df.head(30))

    fig, ax = fig_axes()

    ax.plot_date(
            x=df['datetime'],
            y=df['RUB_USD'],
    )

    fig.savefig(FIG_DIR+fname)




