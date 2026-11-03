# this_file: src/fontlab_plugmix/menu.py
"""Install checkable reporter actions in a Plugmix section of View."""

from typing import Any


def install(owner: Any, registry: Any) -> dict[str, int]:
    """Add one owned QAction per reporter and return action tokens."""
    tokens = {}
    for name, cls in sorted(registry.available().items()):
        action_token = owner.add_action(
            "View",
            f"Plugmix: Show {cls.title}",
            lambda name=name: _toggle(owner, registry, tokens[name], name),
            checkable=True,
        )
        tokens[name] = action_token
        owner.action(action_token).setChecked(name in registry.enabled())
    return tokens


def _toggle(owner: Any, registry: Any, token: int, name: str) -> None:
    """Restore QAction state if activation or persistence fails."""
    action = owner.action(token)
    try:
        registry.toggle(name)
    finally:
        if action is not None:
            action.setChecked(name in registry.enabled())
