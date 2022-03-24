from data.econ import rub_exchange
from charts.utils import fig_axes, format_time_axes
from utils import FIG_DIR
import matplotlib
import pandas as pd

START_DATE = "2022-02-15"
DATE_FMT = "%d %b"

YMIN = 0.005
YMAX = 0.015

def add_annotation(ax, date, y, text, ypos):
    dpage = YMAX - YMIN
    linespace = 0.05 * dpage
    ypos = YMIN + ypos * dpage

    dx = pd.Timedelta(2, unit='day')
    ax.plot_date(
            [date, date],
            [y, ypos],
            ms=0,
            ls=':',
            lw=2,
            c='lightgrey',
            zorder=0,
    )
    ax.plot_date(
            [date-dx, date+dx],
            [ypos, ypos],
            ms=0,
            ls='-',
            lw=2,
            c='lightgrey',
            zorder=0,
    )
    
    if y < ypos:
        date_y = ypos + 2 * linespace
        text_y = ypos + linespace
    else:
        date_y = ypos - linespace
        text_y = ypos - 2 * linespace

    ax.text(date, date_y, date.strftime(DATE_FMT), ha="center", va="center", fontweight='bold')
    ax.text(date, text_y, text, ha="center", va="center")


def rub_chart(fname):
    df = rub_exchange()
    df['USD_RUB'] = pd.to_numeric(df['USD_RUB'])
    df['RUB_USD'] = 1 / df['USD_RUB']
    df = df.set_index('datetime')

    fig, ax = fig_axes(width=6, height=4)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.plot_date(
            x=df.index,
            y=df['RUB_USD'],
            ms=0,
            lw=2,
            ls='-',
    )

    ax = format_time_axes(ax)
    print(df['RUB_USD'].min(),df['RUB_USD'].max())
    ax.set_xlim(pd.to_datetime(START_DATE), pd.Timestamp.today())
    ax.set_ylim(YMIN, YMAX)

    annotations = {
            "SWIFT blocked": {
                'date': "2022-02-27",
                'y': 0.85,
            },
            "Russia invade Ukraine": {
                'date': "2022-02-24",
                'y': 0.2,
            },
            "Ban transactions with russian central bank": {
                'date': "2022-02-28",
                'y': 0.7,
            },
 
    }
    for text, d in annotations.items():
        date = pd.to_datetime(d['date'])
        y = df.loc[date, 'RUB_USD']
        add_annotation(ax, date, y, text, d['y'])

    fig.savefig(FIG_DIR+fname)




