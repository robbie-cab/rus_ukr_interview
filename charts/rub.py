from data.econ import rub_exchange
from charts.utils import fig_axes, format_time_axes
from utils import FIG_DIR
import matplotlib
import pandas as pd

START_DATE = "2022-02-01"

def rub_chart(fname):
    df = rub_exchange()
    df['USD_RUB'] = pd.to_numeric(df['USD_RUB'])
    df['RUB_USD'] = 1 / df['USD_RUB']

    fig, ax = fig_axes()
    fig.subplots_adjust(left=0, bottom=0.1, right=1, top=1)

    ax.plot_date(
            x=df['datetime'],
            y=df['RUB_USD'],
            ms=0,
            lw=2,
            ls='-',
    )

    ax = format_time_axes(ax)
    ax.set_xlim(pd.to_datetime(START_DATE), pd.Timestamp.today())

    fig.savefig(FIG_DIR+fname)




