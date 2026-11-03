# this_file: src/fontlab_plugmix/registry.py
"""Discover plugin kinds and persist reporter, filter and palette preferences."""

import json
import pkgutil
from collections.abc import Callable
from importlib import import_module, metadata
from pathlib import Path
from typing import Any

from .filter import Filter
from .palette import Palette
from .plugin import Plugin
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


def _accept(found: dict[str, type[Plugin]], cls: Any) -> None:
    """Add one valid plugin class, preserving the first name owner."""
    if (
        not isinstance(cls, type)
        or not issubclass(cls, Plugin)
        or cls.kind not in {"reporter", "filter", "palette"}
        or (cls.kind == "reporter" and not issubclass(cls, Reporter))
        or (cls.kind == "filter" and not issubclass(cls, Filter))
        or (cls.kind == "palette" and not issubclass(cls, Palette))
        or not cls.name
        or not cls.title
    ):
        raise TypeError(f"Invalid plugmix plugin: {cls!r}")
    if cls.name in found:
        raise ValueError(f"Duplicate plugmix plugin name: {cls.name}")
    found[cls.name] = cls


def _scan(
    package_name: str, found: dict[str, type[Plugin]], sink: ErrorSink | None
) -> None:
    """Discover one built-in package, isolating broken modules."""
    package = import_module(f".{package_name}", "fontlab_plugmix")
    for entry in pkgutil.iter_modules(package.__path__):
        try:
            module = import_module(f"{package.__name__}.{entry.name}")
            for cls in vars(module).values():
                if (
                    isinstance(cls, type)
                    and cls.__module__ == module.__name__
                    and issubclass(cls, Plugin)
                ):
                    _accept(found, cls)
        except Exception as error:  # noqa: BLE001 - one plugin cannot block startup
            _report(error, entry.name, sink)


def discover(error_sink: ErrorSink | None = None) -> dict[str, type[Plugin]]:
    """Find built-in classes and third-party entry points on demand."""
    found: dict[str, type[Plugin]] = {}
    for package_name in ("plugins", "filters", "palettes"):
        _scan(package_name, found, error_sink)
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
        self._classes: dict[str, type[Plugin]] | None = None
        self._wanted: set[str] = set()
        self._filter_wanted: set[str] | None = None
        self._palette_wanted: set[str] | None = None
        self._params: dict[str, dict[str, Any]] = {}
        self._extras: dict[str, Any] = {}
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
            filters = data.get("enabled_filters")
            palettes = data.get("enabled_palettes")
            params = data.get("params", {})
            if filters is not None and (
                not isinstance(filters, list)
                or any(not isinstance(n, str) for n in filters)
            ):
                raise ValueError(f"Invalid plugmix enabled filters: {self.path}")
            if palettes is not None and (
                not isinstance(palettes, list)
                or any(not isinstance(n, str) for n in palettes)
            ):
                raise ValueError(f"Invalid plugmix enabled palettes: {self.path}")
            if not isinstance(params, dict) or any(
                not isinstance(v, dict) for v in params.values()
            ):
                raise ValueError(f"Invalid plugmix params: {self.path}")
        except FileNotFoundError:
            return
        except (OSError, ValueError, TypeError) as error:
            _report(error, self.path, self._error_sink)
            return
        self._wanted = {RENAMED.get(name, name) for name in data["enabled"]}
        self._filter_wanted = None if filters is None else set(filters)
        self._palette_wanted = None if palettes is None else set(palettes)
        self._params = params
        self._extras = {
            k: v
            for k, v in data.items()
            if k not in {"enabled", "enabled_filters", "enabled_palettes", "params"}
        }

    def _save(self) -> None:
        """Write one sorted preference document after a user toggle."""
        data = {**self._extras, "enabled": sorted(self._wanted), "params": self._params}
        if self._filter_wanted is not None:
            data["enabled_filters"] = sorted(self._filter_wanted)
        if self._palette_wanted is not None:
            data["enabled_palettes"] = sorted(self._palette_wanted)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, indent=2) + "\n",
            encoding="utf-8",
        )

    def available(self, kind: str | None = None) -> dict[str, type[Plugin]]:
        """Return all known classes or only one kind, keyed by stable name."""
        if self._classes is None:
            self._classes = discover(self._error_sink)
        return {
            name: cls
            for name, cls in self._classes.items()
            if kind is None or cls.kind == kind
        }

    def enabled_filters(self) -> tuple[str, ...]:
        """Default new filters on; an explicit saved list controls their menu."""
        names = (
            self.available("filter").keys()
            if self._filter_wanted is None
            else self._filter_wanted
        )
        return tuple(sorted(names))

    def enabled_palettes(self) -> tuple[str, ...]:
        """Return shown palettes; old preference files default to hidden."""
        return tuple(sorted(self._palette_wanted or ()))

    def set_palette_enabled(self, name: str, enabled: bool) -> None:
        """Persist an explicit panel visibility choice, rolling back on failure."""
        if name not in self.available("palette"):
            raise KeyError(name)
        previous = self._palette_wanted
        wanted = set(self.enabled_palettes())
        wanted.add(name) if enabled else wanted.discard(name)
        self._palette_wanted = wanted
        try:
            self._save()
        except Exception:
            self._palette_wanted = previous
            raise

    def values(self, name: str) -> dict[str, Any]:
        """Return validated saved filter values, falling back to defaults."""
        cls = self.available("filter")[name]
        try:
            return cls.validate(self._params.get(name, {}))
        except (TypeError, ValueError, OverflowError) as error:
            _report(error, name, self._error_sink)
            return cls.validate({})

    def set_params(self, name: str, values: dict[str, Any]) -> None:
        """Validate and persist last-used filter values, rolling back on I/O failure."""
        cls = self.available("filter")[name]
        previous = self._params.get(name)
        self._params[name] = cls.validate(values)
        try:
            self._save()
        except Exception:
            if previous is None:
                del self._params[name]
            else:
                self._params[name] = previous
            raise

    def set_filter_enabled(self, name: str, enabled: bool) -> None:
        """Persist whether a filter contributes its Glyph-menu command."""
        if name not in self.available("filter"):
            raise KeyError(name)
        previous = self._filter_wanted
        wanted = set(self.enabled_filters())
        wanted.add(name) if enabled else wanted.discard(name)
        self._filter_wanted = wanted
        try:
            self._save()
        except Exception:
            self._filter_wanted = previous
            raise

    def enabled(self) -> tuple[str, ...]:
        """Return names requested as enabled, including pending restoration."""
        return tuple(sorted(self._wanted))

    def attach(self, painters: Any, qt: Any, sink: Any) -> None:
        """Bind restored reporters to one App painter owner."""
        if self._painters is painters:
            return
        self.detach()
        self._painters, self._qt, self._sink = painters, qt, sink
        for name in sorted(self._wanted & self.available("reporter").keys()):
            try:
                self._activate(name)
            except Exception as error:  # noqa: BLE001 - one plugin cannot block restore
                _report(error, name, self._error_sink)

    def detach(self) -> None:
        """Remove active painters while retaining saved enabled names."""
        try:
            if self._painters is not None:
                for token in tuple(self._tokens.values()):
                    try:
                        self._painters.remove(token)
                    except Exception as error:  # noqa: BLE001 - teardown boundary
                        _report(error, token, self._error_sink)
        finally:
            self._tokens.clear()
            self._painters = self._qt = self._sink = None

    def _activate(self, name: str) -> None:
        """Install a single reporter if a painter owner exists."""
        if self._painters is not None and name not in self._tokens:
            plugin = self.available()[name]()
            self._tokens[name] = plugin.bind(self._painters, self._qt, self._sink)

    def enable(self, name: str) -> bool:
        """Enable a reporter, rolling its overlay back if persistence fails."""
        if name not in self.available("reporter"):
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
                try:
                    self._painters.remove(token)
                except Exception as error:  # noqa: BLE001 - retain save error
                    _report(error, token, self._error_sink)
            raise
        return True

    def disable(self, name: str) -> bool:
        """Disable a known reporter and remove its painter token."""
        if name not in self.available("reporter"):
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


def available(kind: str | None = None) -> dict[str, type[Plugin]]:
    """Discover all plugins or only those of one kind."""
    return current().available(kind)


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
