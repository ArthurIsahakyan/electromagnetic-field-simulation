"""Electric field of point charges in the xy plane."""
import numpy as np

K_COULOMB = 8.9875517923e9


def electric_field(X, Y, charges):
    """Return (Ex, Ey) in N/C by superposing point-charge fields.

    Charge dictionaries contain q [C], x [m], and y [m]. The original
    near-source denominator floor (r^2 >= 1e-12 m^2) is retained.
    """
    X, Y = np.broadcast_arrays(np.asarray(X, dtype=float), np.asarray(Y, dtype=float))
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    for charge in charges:
        dx = X - float(charge["x"])
        dy = Y - float(charge["y"])
        r_squared = np.maximum(dx**2 + dy**2, 1e-12)
        r_cubed = r_squared**1.5
        scale = K_COULOMB * float(charge["q"]) / r_cubed
        Ex += scale * dx
        Ey += scale * dy
    return Ex, Ey
