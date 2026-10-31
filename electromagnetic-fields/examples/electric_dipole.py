from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.electric_field import electric_field
from src.visualization import plot_fields

charges = [{"q": 2e-6, "x": -0.03, "y": 0.0}, {"q": -2e-6, "x": 0.03, "y": 0.0}]
wires = []
x = y = np.linspace(-0.1, 0.1, 180)
X, Y = np.meshgrid(x, y)
Ex, Ey = electric_field(X, Y, charges)
plot_fields(x, y, Ex, Ey, np.zeros_like(Ex), np.zeros_like(Ey), charges, wires, mode="electric")
