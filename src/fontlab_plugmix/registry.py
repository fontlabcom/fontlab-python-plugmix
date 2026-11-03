# this_file: src/fontlab_plugmix/registry.py
"""Discover reporters and persist their enabled names without host imports."""

import json
import pkgutil
from importlib import import_module, metadata
from pathlib import Path
from typing import Any

from .reporter import Reporter

ENTRY_GROUP = "fontlab_plugmix.plugins"
DEFAULT_FILE = (
    Path.home()
    / "Library/Application Support/FontLab/FontLab 9/Data/fontlab-plugmix.json"
)


def discover() -> dict[str, type[Reporter]]:
    """Find built-in and entry-point Reporter classes on demand."""
    package = import_module(".plugins", "fontlab_plugmix")
    found: dict[str, type[Reporter]] = {}
    modules = pkgutil.iter_modules(package.__path__)
    classes = []
    for entry in modules:
        module = import_module(f"{package.__name__}.{entry.name}")
        classes.extend(
            value
            for value in vars(module).values()
            if isinstance(value, type)
            and value.__module__ == module.__name__
            and issubclass(value, Reporter)
        )
    classes.extend(
        ep.load() for ep in metadata.entry_points().select(group=ENTRY_GROUP)
    )
    for cls in classes:
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
    return found


class Registry:
    """Own active painter tokens and the one JSON preference file."""

    def __init__(self, config_dir: str | Path | None = None) -> None:
        self.path = (
            DEFAULT_FILE if config_dir is None else Path(config_dir) / DEFAULT_FILE.name
        )
        self._classes: dict[str, type[Reporter]] | None = None
        self._wanted: set[str] = set()
        self._tokens: dict[str, int] = {}
        self._painters: Any = None
        self._qt: Any = None
        self._sink: Any = None
        self._load()

    def _load(self) -> None:
        """Read persisted names, leaving missing plugin names restorable later."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return
        if not isinstance(data, dict) or not isinstance(data.get("enabled"), list):
            raise ValueError(f"Invalid plugmix preferences: {self.path}")  # noqa: TRY004
        if any(not isinstance(name, str) for name in data["enabled"]):
            raise ValueError(f"Invalid plugmix enabled names: {self.path}")
        self._wanted = set(data["enabled"])

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
            self._classes = discover()
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
            self._activate(name)

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
        """Enable a known reporter and persist once activation succeeds."""
        if name not in self.available():
            raise KeyError(name)
        if name in self._wanted:
            self._activate(name)
            return True
        self._activate(name)
        self._wanted.add(name)
        self._save()
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


def configure(config_dir: str | Path | None = None) -> Registry:
    """Select the process registry; boot calls this once per installation."""
    global _current
    _current = Registry(config_dir)
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
