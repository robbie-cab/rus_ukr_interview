import matplotlib

def fig_axes(width=4, height=2.7):
    fig = matplotlib.figure.Figure(figsize=(width, height), frameon=True)
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.3, bottom=0, right=0.9, top=1)

    spines = set(["bottom", "top", "left", "right"])
    show = set([])
    for spine in show:
        ax.spines[spine].set_edgecolor("lightgray")
        ax.spines[spine].set_linewidth(1)
    for spine in spines - show:
        ax.spines[spine].set_visible(False)

    ax.tick_params(axis="both", which="both", color="lightgray")
    ax.grid(which="both", axis="both", visible=False)

    return fig, ax


