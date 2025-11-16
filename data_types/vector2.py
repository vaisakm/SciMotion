"""
Represents a floating point 2D vector.

This module defines the Vector2 DataType, which represents a floating
point 2D vector. It is stored as a numpy float32 array with 2 entries.
"""

import numpy as np

from data_types.number import Number
from data_types.ndarray import NDArray


class Vector2(NDArray):
    """Represents a floating point 2D vector."""

    _value: np.ndarray

    def __init__(self, *values):
        super().__init__(*values, dtype=np.float32, shape=2)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "x": float(self._value[0]),
            "y": float(self._value[1])
        }

    @staticmethod
    def from_dict(data: dict) -> 'Vector2':
        """Create Vector2 from dictionary."""
        return Vector2(
            data.get("x", 0),
            data.get("y", 0)
        )


Vector2.Infinity = Vector2(float("inf"))
Vector2.negInfinity = Vector2(float("-inf"))