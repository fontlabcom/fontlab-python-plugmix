#!/bin/sh
# this_file: test.sh
set -eu
UV_CACHE_DIR="${UV_CACHE_DIR:-${TMPDIR:-/tmp}/fontlab-plugmix-uv-cache}"
export UV_CACHE_DIR
if [ -n "${PLUGMIX_FONTLABAPP_SOURCE:-}" ]; then
    source_dir="$PLUGMIX_FONTLABAPP_SOURCE"
else
    common_git_dir=$(git rev-parse --path-format=absolute --git-common-dir)
    source_dir=$(dirname "$(dirname "$common_git_dir")")/fontlab-fontlabapp
fi
if [ ! -f "$source_dir/pyproject.toml" ]; then
    printf 'fontlab-fontlabapp checkout not found: %s\nSet PLUGMIX_FONTLABAPP_SOURCE to its directory.\n' "$source_dir" >&2
    exit 2
fi
uv run --no-project --python 3.11 --with pytest --with pytest-cov --with-editable . \
    --with "fontlab-fontlabapp @ file://${source_dir}" python -m pytest "$@"
python3 tests/check_coverage.py coverage.json

