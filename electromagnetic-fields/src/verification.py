"""Finite-difference diagnostics for electrostatic and magnetostatic fields."""
import numpy as np


def _grid_inputs(x, y, Fx, Fy):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    Fx = np.asarray(Fx, dtype=float)
    Fy = np.asarray(Fy, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size < 3 or y.size < 3:
        raise ValueError("x and y must be 1-D coordinate arrays with at least 3 points")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("grid coordinates must be finite")
    if not (np.all(np.diff(x) > 0) or np.all(np.diff(x) < 0)) or not (np.all(np.diff(y) > 0) or np.all(np.diff(y) < 0)):
        raise ValueError("grid coordinates must be strictly monotonic")
    expected = (y.size, x.size)
    if Fx.shape != expected or Fy.shape != expected:
        raise ValueError(f"field arrays must have shape {expected} (y, x)")
    return x, y, Fx, Fy


def _source_mask(x, y, sources, exclusion_radius):
    if exclusion_radius < 0:
        raise ValueError("exclusion_radius must be non-negative")
    X, Y = np.meshgrid(x, y)
    mask = np.ones(X.shape, dtype=bool)
    for source in sources or []:
        mask &= (X - float(source["x"]))**2 + (Y - float(source["y"]))**2 > exclusion_radius**2
    return mask


def _report(values, mask, name):
    valid = mask & np.isfinite(values)
    if not np.any(valid):
        raise ValueError("no finite, non-singular interior grid points remain")
    samples = values[valid]
    return {"field": name, "values": values, "valid_mask": valid,
            "max_abs": float(np.max(np.abs(samples))),
            "rms": float(np.sqrt(np.mean(samples**2))),
            "n_valid": int(samples.size)}


def electric_curl_z(x, y, Ex, Ey, charges=None, exclusion_radius=0.0):
    """Estimate (curl E)z = dEy/dx - dEx/dy in SI units.

    Uses second-order centered finite differences inside the grid; boundaries
    are excluded from metrics. Remove a radius around each point charge.
    """
    x, y, Ex, Ey = _grid_inputs(x, y, Ex, Ey)
    dEy_dx = np.gradient(Ey, x, axis=1, edge_order=2)
    dEx_dy = np.gradient(Ex, y, axis=0, edge_order=2)
    values = dEy_dx - dEx_dy
    mask = np.zeros(values.shape, dtype=bool)
    mask[1:-1, 1:-1] = True
    mask &= _source_mask(x, y, charges, exclusion_radius)
    return _report(values, mask, "curl_E_z")


def magnetic_divergence(x, y, Bx, By, wires=None, exclusion_radius=0.0):
    """Estimate dBx/dx + dBy/dy in tesla/m on the xy plane.

    Uses second-order centered finite differences inside the grid; boundaries
    are excluded from metrics. Remove a radius around each ideal wire.
    """
    x, y, Bx, By = _grid_inputs(x, y, Bx, By)
    dBx_dx = np.gradient(Bx, x, axis=1, edge_order=2)
    dBy_dy = np.gradient(By, y, axis=0, edge_order=2)
    values = dBx_dx + dBy_dy
    mask = np.zeros(values.shape, dtype=bool)
    mask[1:-1, 1:-1] = True
    mask &= _source_mask(x, y, wires, exclusion_radius)
    return _report(values, mask, "div_B")
