import matplotlib


def fig_axes(width=4, height=2.7, axes=[]):
    fig = matplotlib.figure.Figure(figsize=(width, height), frameon=True)
    ax = fig.add_subplot(111)

    spines = set(["bottom", "top", "left", "right"])
    show = set(axes)
    for spine in show:
        ax.spines[spine].set_edgecolor("lightgray")
        ax.spines[spine].set_linewidth(1)
    for spine in spines - show:
        ax.spines[spine].set_visible(False)

    ax.tick_params(axis="both", which="both", color="lightgray")
    ax.grid(which="both", axis="both", visible=False)

    return fig, ax


def format_time_axes(pax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
    locator = matplotlib.dates.AutoDateLocator(minticks=4, maxticks=12)
    formatter = matplotlib.dates.ConciseDateFormatter(locator)
    pax.xaxis.set_major_locator(locator)
    pax.xaxis.set_major_formatter(formatter)
    return pax
