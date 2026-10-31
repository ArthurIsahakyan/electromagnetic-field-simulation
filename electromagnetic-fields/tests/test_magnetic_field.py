import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.magnetic_field import MU_0, magnetic_field_wire


class MagneticFieldTests(unittest.TestCase):
    def test_straight_wire_magnitude_and_direction(self):
        radius, current = 0.25, 3.2
        Bx, By = magnetic_field_wire(np.array([[radius]]), np.array([[0.0]]), [{"I": current, "x": 0.0, "y": 0.0}])
        expected = MU_0 * current / (2 * np.pi * radius)
        np.testing.assert_allclose(Bx[0, 0], 0.0, atol=1e-20)
        np.testing.assert_allclose(By[0, 0], expected)

    def test_current_sign_reverses_magnetic_direction(self):
        coords, y = np.array([[0.3]]), np.array([[0.0]])
        positive = magnetic_field_wire(coords, y, [{"I": 1.0, "x": 0.0, "y": 0.0}])
        negative = magnetic_field_wire(coords, y, [{"I": -1.0, "x": 0.0, "y": 0.0}])
        np.testing.assert_allclose(positive[1], -negative[1])


if __name__ == "__main__":
    unittest.main()
