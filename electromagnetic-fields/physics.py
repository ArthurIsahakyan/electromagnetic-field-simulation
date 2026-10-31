"""Backward-compatible imports for the original project layout."""
from src.electric_field import K_COULOMB, electric_field
from src.magnetic_field import MU_0, magnetic_field_wire

__all__ = ["K_COULOMB", "MU_0", "electric_field", "magnetic_field_wire"]
