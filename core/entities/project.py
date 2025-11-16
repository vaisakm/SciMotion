"""
Represents the project within the app.

The Project class represents the currently open project,
and holds a dict of sequences, media, and parameters.
"""

from core.entities.sequence import Sequence


class Project:
    """Represents the project within the app."""

    _next_sequence_id: int = 0
    _sequence_dict: dict[int, Sequence] = dict()
    _title: str = "Untitled Project"

    @classmethod
    def get_sequence_dict(cls) -> dict[int, Sequence]:
        """Return a reference to the sequence dict."""
        return cls._sequence_dict

    @classmethod
    def get_next_sequence_id(cls):
        """Return a new unique sequence id."""
        _id = cls._next_sequence_id
        cls._next_sequence_id += 1
        return _id
    
    @classmethod
    def get_title(cls) -> str:
        """Return the project title."""
        return cls._title
    
    @classmethod
    def set_title(cls, title: str):
        """Set the project title."""
        cls._title = title
    
    @classmethod
    def get_sequences(cls) -> list[Sequence]:
        """Return list of all sequences in the project."""
        return list(cls._sequence_dict.values())
    
    @classmethod
    def reset(cls):
        """Reset the project to initial state."""
        cls._sequence_dict.clear()
        cls._next_sequence_id = 0
        cls._title = "Untitled Project"