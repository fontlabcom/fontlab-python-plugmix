#!/bin/sh
# this_file: test.sh
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir"
UV_CACHE_DIR="${UV_CACHE_DIR:-${TMPDIR:-/tmp}/fontlab-plugmix-uv-cache}"
export UV_CACHE_DIR
if [ -n "${PLUGMIX_FONTLABAPP_SOURCE:-}" ]; then
    source_dir="$PLUGMIX_FONTLABAPP_SOURCE"
else
    source_dir="$script_dir/../fontlab-fontlabapp"
    if [ -f "$source_dir/pyproject.toml" ]; then
        source_dir=$(CDPATH= cd -- "$source_dir" && pwd)
    else
        common_git_dir=$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)
        if [ -n "$common_git_dir" ]; then
            source_dir=$(dirname "$(dirname "$common_git_dir")")/fontlab-fontlabapp
        else
            source_dir="<checkout unavailable outside git>"
        fi
    fi
fi
if [ ! -f "$source_dir/pyproject.toml" ]; then
    printf 'fontlab-fontlabapp checkout not found: %s\nSet PLUGMIX_FONTLABAPP_SOURCE to its directory.\n' "$source_dir" >&2
    exit 2
fi
fly_source="${PLUGMIX_FLY_SOURCE:-$script_dir/../fontlab-fly}"
pens_source="${PLUGMIX_PENS_SOURCE:-$script_dir/../fontlab-python-pens}"
if [ ! -f "$fly_source/src/fly/__init__.py" ]; then
    printf 'fontlab-fly source not found: %s\nSet PLUGMIX_FLY_SOURCE to its checkout (Fly >=1.3.0).\n' "$fly_source" >&2
    exit 2
fi
if [ ! -f "$pens_source/pyproject.toml" ]; then
    printf 'fontlab-python-pens checkout not found: %s\nSet PLUGMIX_PENS_SOURCE to its checkout.\n' "$pens_source" >&2
    exit 2
fi
fly_source=$(CDPATH='' cd -- "$fly_source" && pwd)
pens_source=$(CDPATH='' cd -- "$pens_source" && pwd)
PLUGMIX_FLY_SOURCE="$fly_source"
PLUGMIX_PENS_SOURCE="$pens_source"
PLUGMIX_FONTLABAPP_SOURCE="$source_dir"
PYTHONPATH="$fly_source/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH PLUGMIX_FLY_SOURCE PLUGMIX_PENS_SOURCE PLUGMIX_FONTLABAPP_SOURCE
uv run --no-project --python cpython-3.11-macos-aarch64-none --with pytest --with pytest-cov --with-editable . \
    --with-editable "$pens_source" \
    --with "fontlab-fontlabapp @ file://${source_dir}" python -m pytest "$@"
if [ "$#" -eq 0 ]; then
    python3 tests/check_coverage.py coverage.json
fi
