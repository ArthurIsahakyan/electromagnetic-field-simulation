"""Plot electric, magnetic, or combined field streamlines with source markers."""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import numpy as np


def _draw(ax, x, y, Ex, Ey, Bx, By, charges, wires, mode):
    ax.clear()
    active_e = mode in ("electric", "combined")
    active_b = mode in ("magnetic", "combined")
    if active_e and np.any(np.hypot(Ex, Ey) > 0):
        ax.streamplot(x, y, Ex, Ey, color="#1769aa", density=1.15, linewidth=0.9, arrowsize=1.0)
    if active_b and np.any(np.hypot(Bx, By) > 0):
        ax.streamplot(x, y, Bx, By, color="#d1495b", density=1.15, linewidth=0.9, arrowsize=1.0)

    if active_e:
        for charge in charges:
            q, x0, y0 = charge["q"], charge["x"], charge["y"]
            if q == 0:
                continue
            color, mark = ("#1769aa", "+") if q > 0 else ("#30343b", "−")
            ax.scatter(x0, y0, s=100, color=color, edgecolor="white", linewidth=0.8, zorder=5)
            ax.text(x0, y0, mark, color="white", fontsize=13, weight="bold", ha="center", va="center", zorder=6)
    if active_b:
        for wire in wires:
            current = wire["I"]
            if current == 0:
                continue
            x0, y0 = wire["x"], wire["y"]
            ax.scatter(x0, y0, marker="o", facecolors="white", edgecolors="#d1495b", s=125, linewidths=2, zorder=7)
            ax.text(x0, y0, "⊙" if current > 0 else "⊗", color="#d1495b", fontsize=12, ha="center", va="center", zorder=8)

    titles = {"electric": "Electric Field", "magnetic": "Magnetic Field", "combined": "Electric and Magnetic Fields"}
    ax.set_title(titles[mode])
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.22)
    handles = []
    if active_e:
        handles.append(Line2D([0], [0], color="#1769aa", label="Electric field; +/− charges"))
    if active_b:
        handles.append(Line2D([0], [0], color="#d1495b", label="Magnetic field; ⊙ out / ⊗ in"))
    ax.legend(handles=handles, loc="upper right")


def plot_fields(x, y, Ex, Ey, Bx, By, charges=None, wires=None, mode="combined", interactive=False, show=True):
    """Create and display a field plot. mode is electric, magnetic, or combined.

    With interactive=True, add Matplotlib buttons that switch modes in place.
    Returns (figure, axes) so callers can save or further customize the plot.
    """
    if mode not in {"electric", "magnetic", "combined"}:
        raise ValueError("mode must be 'electric', 'magnetic', or 'combined'")
    charges, wires = charges or [], wires or []
    fig, ax = plt.subplots(figsize=(10, 7))
    if interactive:
        fig.subplots_adjust(bottom=0.17)
    _draw(ax, x, y, Ex, Ey, Bx, By, charges, wires, mode)
    if interactive:
        callbacks = []
        for pos, label, selected in [(0.20, "Electric Field", "electric"), (0.43, "Magnetic Field", "magnetic"), (0.66, "Combined View", "combined")]:
            button_ax = fig.add_axes([pos, 0.035, 0.19, 0.07])
            button = Button(button_ax, label)
            button.on_clicked(lambda _event, value=selected: (_draw(ax, x, y, Ex, Ey, Bx, By, charges, wires, value), fig.canvas.draw_idle()))
            callbacks.append(button)
        fig._field_mode_buttons = callbacks
    if interactive:
        fig.subplots_adjust(top=0.93, left=0.10, right=0.97, bottom=0.18)
    else:
        fig.tight_layout()
    if show:
        plt.show()
    return fig, ax


def plot_electric_field(x, y, Ex, Ey, charges):
    zeros = np.zeros_like(Ex)
    return plot_fields(x, y, Ex, Ey, zeros, zeros, charges, [], mode="electric")


def plot_magnetic_field(x, y, Bx, By, wires):
    zeros = np.zeros_like(Bx)
    return plot_fields(x, y, zeros, zeros, Bx, By, [], wires, mode="magnetic")


def plot_both_fields(x, y, Ex, Ey, Bx, By, charges, wires):
    return plot_fields(x, y, Ex, Ey, Bx, By, charges, wires, mode="combined")

