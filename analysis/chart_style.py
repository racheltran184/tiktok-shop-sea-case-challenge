"""Shared chart style for the case notebook.

Thin marks, hairline grid, one accent hue plus gray for emphasis charts,
blue/orange for two-series charts, text in ink colours (never the series colour).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

SURFACE = "#fcfcfb"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#c9c7bf"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.sans-serif": ["Inter", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "font.size": 10, "text.color": INK, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": GRID, "grid.linewidth": 0.8, "legend.frameon": False,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 6, "ytick.major.pad": 6,
    "text.parse_math": False,  # so "US$" labels print as text, not math
})


def new_chart(title, sub=None, width=8.0, height=3.6, left=1.5, right=0.4, top=0.85, bottom=0.75):
    """Figure with a title block and fixed margins (in inches), so bar ends round in true pixels."""
    fig, ax = plt.subplots(figsize=(width, height))
    fig.subplots_adjust(left=left / width, right=1 - right / width,
                        top=1 - top / height, bottom=bottom / height)
    fig.text(0.1 / width, 1 - 0.12 / height, title, fontsize=12.5, fontweight="semibold", color=INK, va="top")
    if sub:
        fig.text(0.1 / width, 1 - 0.42 / height, sub, fontsize=9.5, color=INK2, va="top")
    return fig, ax


def note(fig, text):
    """Muted source line along the bottom edge."""
    fig.text(0.1 / fig.get_figwidth(), 0.08 / fig.get_figheight(), text, color=MUTED, fontsize=8, va="bottom")


def hbar(ax, y, width, left=0.0, height=0.5, color=BLUE, round_end=True, px=4):
    """Horizontal bar: square at the baseline, 4px rounded corners on the data end.

    Set the axis limits before calling, because the radius is measured in pixels.
    """
    if width <= 0:
        return
    box = ax.get_window_extent()
    x_per_px = (ax.get_xlim()[1] - ax.get_xlim()[0]) / box.width
    y_per_px = abs(ax.get_ylim()[1] - ax.get_ylim()[0]) / box.height
    y0 = y - height / 2
    if not round_end:
        ax.add_patch(Rectangle((left, y0), width, height, facecolor=color, lw=0))
        return
    r = min(px * x_per_px, width / 2)
    ax.add_patch(FancyBboxPatch((left, y0), width, height,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                mutation_aspect=y_per_px / x_per_px, facecolor=color, lw=0))
    ax.add_patch(Rectangle((left, y0), r, height, facecolor=color, lw=0))


def text_after(ax, artist, text, gap_px=6, **kw):
    """Place `text` just to the right of an existing text artist (for two-tone labels)."""
    fig = ax.figure
    fig.canvas.draw()
    bb = artist.get_window_extent(renderer=fig.canvas.get_renderer())
    x, _ = ax.transData.inverted().transform((bb.x1 + gap_px, bb.y0))
    return ax.text(x, artist.get_position()[1], text, va="center", **kw)


def save(fig, name):
    """Write the chart next to the notebook (figures/<name>.png) for the README."""
    fig.savefig(f"figures/{name}.png", dpi=200)
