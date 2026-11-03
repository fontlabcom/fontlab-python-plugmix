# this_file: src/fontlab_plugmix/filter.py
"""Pure Filter contract and declarative, validated parameter values."""

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Any, ClassVar, Literal

from .plugin import Plugin
from .snapshot import Anchor, Contour, GlyphSnapshot


@dataclass(frozen=True)
class Param:
    """One typed dialog field with an optional numeric range."""

    key: str
    label: str
    kind: Literal["float", "int", "bool", "choice"]
    default: float | int | bool | str
    minimum: float | None = None
    maximum: float | None = None
    choices: tuple[str, ...] = ()

    def parse(self, value: Any) -> float | int | bool | str:
        """Reject wrong types and values outside the declared domain."""
        valid = {
            "float": (int, float),
            "int": (int,),
            "bool": (bool,),
            "choice": (str,),
        }
        if self.kind not in valid or type(value) not in valid[self.kind]:
            raise ValueError(f"{self.label}: expected {self.kind}")
        if self.kind == "choice":
            if value not in self.choices:
                raise ValueError(f"{self.label}: unknown choice {value}")
            return value
        if self.kind == "bool":
            return value
        number = float(value)
        if (
            not isfinite(number)
            or (self.minimum is not None and number < self.minimum)
            or (self.maximum is not None and number > self.maximum)
        ):
            raise ValueError(f"{self.label}: outside allowed range")
        return number if self.kind == "float" else value


@dataclass(frozen=True)
class LayerEdit:
    """Replacement layer values; None leaves the corresponding value intact."""

    contours: tuple[Contour, ...] | None = None
    advance: float | None = None
    anchors: tuple[Anchor, ...] | None = None


class Filter(Plugin):
    """Compute a layer edit from a frozen snapshot and typed values."""

    kind = "filter"
    params: ClassVar[tuple[Param, ...]] = ()

    @classmethod
    def validate(cls, values: Mapping[str, Any]) -> dict[str, Any]:
        """Fill defaults and reject unknown or invalid parameters."""
        keys = {param.key for param in cls.params}
        unknown = set(values) - keys
        if unknown:
            raise ValueError(f"Unknown {cls.name} parameters: {sorted(unknown)}")
        return {
            param.key: param.parse(values.get(param.key, param.default))
            for param in cls.params
        }

    def compute(self, snapshot: GlyphSnapshot, values: Mapping[str, Any]) -> LayerEdit:
        """Return a pure proposed edit for one layer."""
        raise NotImplementedError
