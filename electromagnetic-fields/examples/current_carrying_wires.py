from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.magnetic_field import magnetic_field_wire
from src.visualization import plot_fields

wires = [{"I": 2.0, "x": -0.03, "y": 0.0}, {"I": -2.0, "x": 0.03, "y": 0.0}]
x = y = np.linspace(-0.1, 0.1, 180)
X, Y = np.meshgrid(x, y)
Bx, By = magnetic_field_wire(X, Y, wires)
plot_fields(x, y, np.zeros_like(Bx), np.zeros_like(By), Bx, By, [], wires, mode="magnetic")
