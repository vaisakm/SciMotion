"""
Represents an integer number.

This module defines the Integer DataType, which represents an
integer number. It is stored as a numpy int32 array with 1 entry.
"""

import numpy as np

from data_types.ndarray import NDArray


class Integer(NDArray):
    """Represents an integer number."""

    _value: np.ndarray

    def __init__(self, value: int):
        super().__init__(value, dtype=np.int32, shape=1)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {"value": int(self._value[0])}

    @staticmethod
    def from_dict(data: dict) -> 'Integer':
        """Create Integer from dictionary."""
        return Integer(data.get("value", 0))


Integer.Maximum = Integer(2**31-1)
Integer.Minimum = Integer(-(2**31-1))