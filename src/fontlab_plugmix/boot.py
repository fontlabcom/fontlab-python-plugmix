# this_file: src/fontlab_plugmix/boot.py
"""One-call FontLab startup and explicit teardown."""

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any

from . import menu, registry
from .backend import select_backend
from .filters.host import FilterHost
from .kinds import Services


@dataclass
class _State:
    """Keep every Qt owner alive until uninstall has detached its signals."""

    config_dir: Path | None
    reporters: registry.Registry
    painters: Any
    menus: Any
    filters: FilterHost


_state: _State | None = None


def _error(error: Exception, source: object) -> None:
    """Log host errors without raising through native Qt callbacks."""
    try:
        print(f"Plugmix {type(source).__name__}: {error}")
    except Exception:  # noqa: BLE001, S110 - native callback boundary
        pass


def _runtime() -> tuple[Any, Any, Any]:
    """Import PythonQt, FontLab and owned menus only inside FontLab."""
    qt = import_module("PythonQt")
    fontlab = import_module("fontlab")
    menus_cls = import_module("fontlabapp.owned_menus").OwnedMenus
    return qt, fontlab, menus_cls


def install(config_dir: str | Path | None = None) -> None:
    """Idempotently restore enabled reporters and add their View actions."""
    global _state
    path = None if config_dir is None else Path(config_dir)
    if _state is not None:
        if path != _state.config_dir:
            raise ValueError(
                "Plugmix is already installed with another config directory"
            )
        return
    qt, fontlab, menus_cls = _runtime()
    reporters = registry.configure(path, error_sink=_error)
    painters = select_backend(qt, fontlab, _error)
    menus = None
    filters = None
    try:
        menus = menus_cls(qt, fontlab, error_sink=_error, owned_title="Plugmix")
        reporters.attach(painters, qt, _error)
        menu.install(menus, reporters)
        filters = FilterHost(Services(qt, fontlab, menus, painters, _error), reporters)
        filters.install()
    except Exception:
        try:
            reporters.detach()
        finally:
            try:
                try:
                    if filters is not None:
                        filters.close()
                finally:
                    if menus is not None:
                        menus.close()
            finally:
                painters.close()
        raise
    _state = _State(path, reporters, painters, menus, filters)


def uninstall() -> None:
    """Remove actions and overlays while preserving saved enable choices."""
    global _state
    if _state is None:
        return
    state, _state = _state, None
    try:
        try:
            state.filters.close()
        finally:
            state.menus.close()
    finally:
        try:
            state.reporters.detach()
        finally:
            state.painters.close()
