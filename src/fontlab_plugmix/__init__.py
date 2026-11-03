# this_file: src/fontlab_plugmix/__init__.py
"""Small lazy public API for native FontLab reporter plugins."""

from importlib import import_module
from typing import Any

__all__ = ["Mark", "Reporter", "install", "registry"]


def __getattr__(name: str) -> Any:
    """Load FontLab-free definitions only when requested."""
    if name in {"Reporter", "Mark"}:
        return getattr(import_module(".reporter", __name__), name)
    if name == "registry":
        return import_module(".registry", __name__)
    if name == "install":
        return import_module(".boot", __name__).install
    raise AttributeError(name)
