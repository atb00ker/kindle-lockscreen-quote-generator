"""Generate package for quote image generation."""

from .directory import generate_from_folder
from .adhoc import generate_adhoc

__all__ = [
    "generate_from_folder",
    "generate_adhoc",
]
