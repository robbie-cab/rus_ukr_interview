import matplotlib
import pandas as pd

from charts.utils import fig_axes, format_time_axes
from data.econ import rub_exchange
from utils import FIG_DIR

START_DATE = "2022-02-10"
DATE_FMT = "%d %b"

YMIN = 0.005
YMAX = 0.015


def add_annotation(ax, date, y, text, ypos, color):
    dpage = YMAX - YMIN
    linespace = 0.04 * dpage
    ypos = YMIN + ypos * dpage

    dx = pd.Timedelta(2, unit="day")
    ax.plot_date(
        [date, date],
        [y, ypos],
        ms=0,
        ls=":",
        lw=2,
        c=color,
        zorder=0,
    )
    ax.plot_date(
        [date - dx, date + dx],
        [ypos, ypos],
        ms=0,
        ls="-",
        lw=2,
        c=color,
        zorder=0,
    )

    lineb = "\n" in text
    if y < ypos:
        # above line
        date_y = ypos + (2 + lineb) * linespace
        text_y = ypos + (1 + lineb * 0.5) * linespace
        va = "center"
    else:
        # below line
        date_y = ypos - linespace
        text_y = ypos - (2 + lineb * 0.5) * linespace
        va = "center"

    ax.text(date, date_y, date.strftime(DATE_FMT), ha="center", va=va, fontweight="bold")
    ax.text(date, text_y, text, ha="center", va=va)


def rub_chart(fname):
    df = rub_exchange()
    df["USD_RUB"] = pd.to_numeric(df["USD_RUB"])
    df["RUB_USD"] = 1 / df["USD_RUB"]
    df = df.set_index("datetime")

    cmap = matplotlib.cm.get_cmap("magma")

    fig, ax = fig_axes(width=7, height=4)
    fig.subplots_adjust(left=0.1, bottom=0, right=1, top=1)

    ax.axes.yaxis.set_visible(False)
    start_y = df.loc[START_DATE, "RUB_USD"]
    ax.text(
        pd.to_datetime(START_DATE),
        start_y,
        "Ruble\nvalue",
        ha="right",
        va="bottom",
        fontsize="x-large",
        color=cmap(0.3),
        fontweight="bold",
    )

    ax.plot_date(x=df.index, y=df["RUB_USD"], ms=0, lw=2, ls="-", c=cmap(0.3))

    ax = format_time_axes(ax)
    ax.set_xlim(pd.to_datetime(START_DATE), pd.Timestamp.today())
    ax.set_ylim(YMIN, YMAX)

    annotations = {
        "German chancellor travels\nto Moscow for peace talks": {
            "date": "2022-02-15",
            "y": 0.3,
        },
        "Five Russian banks\nsanctioned by UK": {
            "date": "2022-02-22",
            "y": 0.6,
        },
        "Russia invade Ukraine": {
            "date": "2022-02-24",
            "y": 0.85,
            "color": cmap(0.7),
        },
        "SWIFT blocked": {
            "date": "2022-02-27",
            "y": 0.17,
        },
        # "Russian ships banned\nfrom ports": {
        #     'date': "2022-03-01",
        #     'y': 0.2,
        # },
        "Germany push back on\noil sanctions": {
            "date": "2022-03-07",
            "y": 0.5,
        },
        "Asset freeze on Chelsea\nowner Abramovich": {
            "date": "2022-03-10",
            "y": 0.7,
        },
        "UK freezes 350 new\n private assets": {
            "date": "2022-03-15",
            "y": 0.2,
        },
    }
    for text, d in annotations.items():
        date = pd.to_datetime(d["date"])
        y = df.loc[date, "RUB_USD"]
        color = d.get("color", "lightgrey")
        add_annotation(ax, date, y, text, d["y"], color)

    fig.savefig(FIG_DIR + fname)
