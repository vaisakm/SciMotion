"""
Represents an RGBA float32 image.

The Image class represents an RGBA float32 image, and stores
its pixel data along with information such as dimensions.
"""

import numpy as np
from typing import Optional


class Image:
    """Represents an RGBA float32 image."""

    _width: int
    _height: int
    _data_bytes: Optional[bytes]
    _data_array: Optional[np.ndarray]

    def __init__(self,
                 width: int,
                 height: int,
                 data_bytes: Optional[bytes] = None,
                 data_array: Optional[np.ndarray] = None):
        self._width = width
        self._height = height
        self._data_bytes = data_bytes
        self._data_array = data_array
        if data_array is None and data_bytes is None:
            self._data_array = np.zeros((height, width, 4), dtype=np.float32)

    def get_width(self) -> int:
        """Return the image width."""
        return self._width

    def get_height(self) -> int:
        """Return the image height."""
        return self._height

    def get_data_bytes(self) -> bytes:
        """Return the image data in bytes."""
        if self._data_bytes is None:
            assert self._data_array is not None, "Both data_bytes and data_array cannot be None"
            self._data_bytes = self._data_array.tobytes()
        return self._data_bytes

    def get_data_array(self) -> np.ndarray:
        """Return the image data as a numpy array."""
        if self._data_array is None:
            assert self._data_bytes is not None, "Both data_bytes and data_array cannot be None"
            self._data_array = np.frombuffer(
                self._data_bytes, dtype=np.float32).reshape(
                    (self._height, self._width, 4))
        return self._data_array


def save_image(data: np.ndarray, file_path: str):
    """
    Save a numpy array as a PNG image.
    
    Args:
        data: numpy array with shape (height, width, 4) containing RGBA float32 data
        file_path: path where to save the image
    """
    try:
        from PIL import Image as PILImage
    except ImportError:
        raise ImportError("PIL (Pillow) is required for saving images. Install it with: pip install Pillow")
    
    # Convert float32 [0, 1] to uint8 [0, 255]
    if data.dtype == np.float32:
        data = np.clip(data * 255, 0, 255).astype(np.uint8)
    
    # Create PIL image and save
    img = PILImage.fromarray(data, mode='RGBA')
    img.save(file_path)
