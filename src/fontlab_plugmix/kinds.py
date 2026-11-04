# this_file: src/fontlab_plugmix/kinds.py
"""Runtime services and the shared native callback boundary."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Services:
    """Host objects owned by boot, passed to kind-specific binders."""

    qt: Any
    fontlab: Any
    menus: Any
    painters: Any
    sink: Callable[[Exception, object], object]


def guarded(
    plugin: object,
    sink: Callable[[Exception, object], object],
    action: Callable[[], Any],
) -> Any:
    """Never let a plugin or diagnostic failure escape into Qt dispatch."""
    try:
        return action()
    except Exception as error:  # noqa: BLE001 - native callback boundary
        try:
            sink(error, plugin)
        except Exception:  # noqa: BLE001, S110 - sink is also untrusted
            pass
        return None
