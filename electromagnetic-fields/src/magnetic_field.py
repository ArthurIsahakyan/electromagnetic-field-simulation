"""Magnetic field of infinite straight wires perpendicular to the xy plane."""
import numpy as np

MU_0 = 4 * np.pi * 1e-7


def magnetic_field_wire(X, Y, wires):
    """Return (Bx, By) in tesla by superposition of straight-wire fields.

    Wire dictionaries contain I [A], x [m], and y [m]. Positive current points
    out of the page. The original denominator floor (r^2 >= 1e-20 m^2) remains.
    """
    X, Y = np.broadcast_arrays(np.asarray(X, dtype=float), np.asarray(Y, dtype=float))
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    for wire in wires:
        dx = X - float(wire["x"])
        dy = Y - float(wire["y"])
        r_squared = np.maximum(dx**2 + dy**2, 1e-20)
        factor = MU_0 * float(wire["I"]) / (2 * np.pi * r_squared)
        Bx += -factor * dy
        By += factor * dx
    return Bx, By
