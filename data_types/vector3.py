"""
Represents a floating point 3D vector.

This module defines the Vector3 DataType, which represents a floating
point 3D vector. It is stored as a numpy float32 array with 3 entries.
"""

import numpy as np

from data_types.ndarray import NDArray


class Vector3(NDArray):
    """Represents a floating point 3D vector."""

    _value: np.ndarray

    def __init__(self, *values):
        super().__init__(*values, dtype=np.float32, shape=3)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "x": float(self._value[0]),
            "y": float(self._value[1]),
            "z": float(self._value[2])
        }

    @staticmethod
    def from_dict(data: dict) -> 'Vector3':
        """Create Vector3 from dictionary."""
        return Vector3(
            data.get("x", 0),
            data.get("y", 0),
            data.get("z", 0)
        )
