import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from src.electric_field import electric_field
from src.magnetic_field import magnetic_field_wire
from src.verification import electric_curl_z, magnetic_divergence


class VerificationTests(unittest.TestCase):
    def test_point_charge_curl_is_small_away_from_singularity(self):
        x = y = np.linspace(-0.5, 0.5, 301)
        X, Y = np.meshgrid(x, y)
        charges = [{"q": 1e-9, "x": 0.0, "y": 0.0}]
        Ex, Ey = electric_field(X, Y, charges)
        result = electric_curl_z(x, y, Ex, Ey, charges, exclusion_radius=0.12)
        self.assertGreater(result["n_valid"], 0)
        self.assertLess(result["rms"], 2e-3 * np.max(np.hypot(Ex, Ey)) / (x[1] - x[0]))
        self.assertFalse(result["valid_mask"][0, :].any())
        self.assertFalse(result["valid_mask"][:, 0].any())

    def test_straight_wire_divergence_is_small_away_from_wire(self):
        x = y = np.linspace(-0.5, 0.5, 301)
        X, Y = np.meshgrid(x, y)
        wires = [{"I": 2.0, "x": 0.0, "y": 0.0}]
        Bx, By = magnetic_field_wire(X, Y, wires)
        result = magnetic_divergence(x, y, Bx, By, wires, exclusion_radius=0.12)
        self.assertGreater(result["n_valid"], 0)
        self.assertLess(result["rms"], 2e-3 * np.max(np.hypot(Bx, By)) / (x[1] - x[0]))
        self.assertFalse(result["valid_mask"][-1, :].any())

    def test_verification_rejects_invalid_grid_and_shape(self):
        coords = np.linspace(0, 1, 4)
        zeros = np.zeros((4, 4))
        with self.assertRaises(ValueError):
            electric_curl_z(coords[:2], coords[:2], zeros[:2, :2], zeros[:2, :2])
        with self.assertRaises(ValueError):
            magnetic_divergence(coords, coords, zeros[:3, :], zeros)

    def test_verification_ignores_nonfinite_samples_and_source_neighborhood(self):
        coords = np.linspace(-1, 1, 9)
        values = np.zeros((9, 9))
        values[4, 4] = np.nan
        result = magnetic_divergence(coords, coords, values, np.zeros_like(values), [{"x": 0, "y": 0}], exclusion_radius=0.2)
        self.assertGreater(result["n_valid"], 0)
        self.assertTrue(np.isfinite(result["rms"]))
        self.assertFalse(result["valid_mask"][4, 4])


if __name__ == "__main__":
    unittest.main()
