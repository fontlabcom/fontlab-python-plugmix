# this_file: src/fontlab_plugmix/registry.py
"""Discover reporters and persist their enabled names without host imports."""

import json
import pkgutil
from collections.abc import Callable
from importlib import import_module, metadata
from pathlib import Path
from typing import Any

from .reporter import Reporter

ENTRY_GROUP = "fontlab_plugmix.plugins"
RENAMED = {"nodes_outside_paths": "offcurve_outside_bounds"}
DEFAULT_FILE = (
    Path.home()
    / "Library/Application Support/FontLab/FontLab 9/Data/fontlab-plugmix.json"
)


ErrorSink = Callable[[Exception, object], object]


def _report(error: Exception, source: object, sink: ErrorSink | None) -> None:
    """Report a broken plugin or preference without interrupting discovery."""
    try:
        if sink is None:
            print(f"Plugmix {source}: {error}")
        else:
            sink(error, source)
    except Exception:  # noqa: BLE001, S110 - diagnostics must not block startup
        pass


def _accept(found: dict[str, type[Reporter]], cls: Any) -> None:
    """Add one valid reporter class, preserving the first name owner."""
    if (
        not isinstance(cls, type)
        or not issubclass(cls, Reporter)
        or not cls.name
        or not cls.title
    ):
        raise TypeError(f"Invalid plugmix reporter: {cls!r}")
    if cls.name in found:
        raise ValueError(f"Duplicate plugmix reporter name: {cls.name}")
    found[cls.name] = cls


def discover(error_sink: ErrorSink | None = None) -> dict[str, type[Reporter]]:
    """Find built-in and entry-point Reporter classes on demand."""
    package = import_module(".plugins", "fontlab_plugmix")
    found: dict[str, type[Reporter]] = {}
    for entry in pkgutil.iter_modules(package.__path__):
        try:
            module = import_module(f"{package.__name__}.{entry.name}")
            for cls in vars(module).values():
                if (
                    isinstance(cls, type)
                    and cls.__module__ == module.__name__
                    and issubclass(cls, Reporter)
                ):
                    _accept(found, cls)
        except Exception as error:  # noqa: BLE001 - one plugin cannot block startup
            _report(error, entry.name, error_sink)
    try:
        points = metadata.entry_points().select(group=ENTRY_GROUP)
    except Exception as error:  # noqa: BLE001 - broken entry-point metadata
        _report(error, ENTRY_GROUP, error_sink)
        points = ()
    for point in points:
        try:
            _accept(found, point.load())
        except Exception as error:  # noqa: BLE001 - third-party plugin boundary
            _report(error, point, error_sink)
    return found


class Registry:
    """Own active painter tokens and the one JSON preference file."""

    def __init__(
        self, config_dir: str | Path | None = None, error_sink: ErrorSink | None = None
    ) -> None:
        self.path = (
            DEFAULT_FILE if config_dir is None else Path(config_dir) / DEFAULT_FILE.name
        )
        self._classes: dict[str, type[Reporter]] | None = None
        self._wanted: set[str] = set()
        self._tokens: dict[str, int] = {}
        self._painters: Any = None
        self._qt: Any = None
        self._sink: Any = None
        self._error_sink = error_sink
        self._load()

    def _load(self) -> None:
        """Read persisted names, leaving missing plugin names restorable later."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("enabled"), list):
                raise TypeError(f"Invalid plugmix preferences: {self.path}")
            if any(not isinstance(name, str) for name in data["enabled"]):
                raise ValueError(f"Invalid plugmix enabled names: {self.path}")
        except FileNotFoundError:
            return
        except (OSError, ValueError, TypeError) as error:
            _report(error, self.path, self._error_sink)
            return
        self._wanted = {RENAMED.get(name, name) for name in data["enabled"]}

    def _save(self) -> None:
        """Write one sorted preference document after a user toggle."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"enabled": sorted(self._wanted)}, indent=2) + "\n",
            encoding="utf-8",
        )

    def available(self) -> dict[str, type[Reporter]]:
        """Return known reporters keyed by stable name."""
        if self._classes is None:
            self._classes = discover(self._error_sink)
        return dict(self._classes)

    def enabled(self) -> tuple[str, ...]:
        """Return names requested as enabled, including pending restoration."""
        return tuple(sorted(self._wanted))

    def attach(self, painters: Any, qt: Any, sink: Any) -> None:
        """Bind restored reporters to one App painter owner."""
        if self._painters is painters:
            return
        self.detach()
        self._painters, self._qt, self._sink = painters, qt, sink
        for name in sorted(self._wanted & self.available().keys()):
            try:
                self._activate(name)
            except Exception as error:  # noqa: BLE001 - one plugin cannot block restore
                _report(error, name, self._error_sink)

    def detach(self) -> None:
        """Remove active painters while retaining saved enabled names."""
        if self._painters is not None:
            for token in tuple(self._tokens.values()):
                self._painters.remove(token)
        self._tokens.clear()
        self._painters = self._qt = self._sink = None

    def _activate(self, name: str) -> None:
        """Install a single reporter if a painter owner exists."""
        if self._painters is not None and name not in self._tokens:
            plugin = self.available()[name]()
            self._tokens[name] = plugin.bind(self._painters, self._qt, self._sink)

    def enable(self, name: str) -> bool:
        """Enable a reporter, rolling its overlay back if persistence fails."""
        if name not in self.available():
            raise KeyError(name)
        if name in self._wanted:
            self._activate(name)
            return True
        self._wanted.add(name)
        try:
            self._activate(name)
            self._save()
        except Exception:
            self._wanted.remove(name)
            token = self._tokens.pop(name, None)
            if token is not None and self._painters is not None:
                self._painters.remove(token)
            raise
        return True

    def disable(self, name: str) -> bool:
        """Disable a known reporter and remove its painter token."""
        if name not in self.available():
            raise KeyError(name)
        token = self._tokens.pop(name, None)
        if token is not None and self._painters is not None:
            self._painters.remove(token)
        if name in self._wanted:
            self._wanted.remove(name)
            self._save()
        return False

    def toggle(self, name: str) -> bool:
        """Switch a reporter and return the new checked state."""
        return self.disable(name) if name in self._wanted else self.enable(name)


_current: Registry | None = None


def configure(
    config_dir: str | Path | None = None, error_sink: ErrorSink | None = None
) -> Registry:
    """Select the process registry; boot calls this once per installation."""
    global _current
    _current = Registry(config_dir, error_sink)
    return _current


def current() -> Registry:
    """Lazily create the default registry without writing preferences."""
    global _current
    if _current is None:
        _current = Registry()
    return _current


def available() -> dict[str, type[Reporter]]:
    """Discover all built-in and entry-point reporters."""
    return current().available()


def enabled() -> tuple[str, ...]:
    """Return saved enabled names."""
    return current().enabled()


def enable(name: str) -> bool:
    """Enable a reporter."""
    return current().enable(name)


def disable(name: str) -> bool:
    """Disable a reporter."""
    return current().disable(name)


def toggle(name: str) -> bool:
    """Toggle a reporter."""
    return current().toggle(name)
