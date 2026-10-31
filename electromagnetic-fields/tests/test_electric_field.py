import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.electric_field import K_COULOMB, electric_field


class ElectricFieldTests(unittest.TestCase):
    def test_single_point_charge_magnitude_and_direction(self):
        x, y, q = 0.2, -0.1, 3e-9
        Ex, Ey = electric_field(np.array([[x]]), np.array([[y]]), [{"q": q, "x": 0.0, "y": 0.0}])
        radius = np.hypot(x, y)
        magnitude = K_COULOMB * q / radius**2
        np.testing.assert_allclose(Ex[0, 0], magnitude * x / radius)
        np.testing.assert_allclose(Ey[0, 0], magnitude * y / radius)

    def test_electric_superposition(self):
        X, Y = np.meshgrid([0.2, -0.4], [0.3, 0.1])
        a = [{"q": 2e-9, "x": 0.0, "y": 0.0}]
        b = [{"q": -4e-9, "x": 0.1, "y": -0.2}]
        combined = electric_field(X, Y, a + b)
        ea, eb = electric_field(X, Y, a), electric_field(X, Y, b)
        np.testing.assert_allclose(combined[0], ea[0] + eb[0])
        np.testing.assert_allclose(combined[1], ea[1] + eb[1])


if __name__ == "__main__":
    unittest.main()
