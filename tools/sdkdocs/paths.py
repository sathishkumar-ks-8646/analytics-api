"""Where the SDK sources live, for the version currently being built.

This module is the only thing in the generator that knows the repository
layout. Everything else asks it for a path.

The generator itself is version-agnostic, like every other tool in `tools/`:
it takes `--version` and reads `<repo>/<version>/sdk/`. The parts that really
are tied to an API version live in `tools/sdkdocs/<version>/` - today that is
just `snippets.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

# tools/sdkdocs/paths.py -> tools/sdkdocs -> tools -> the repository root
REPO = Path(__file__).resolve().parents[2]

_version: str | None = None


def default_version() -> str:
    """The `latest` version named in the repository manifest."""
    return json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))["latest"]


def set_version(version: str) -> None:
    """Choose the version to build. Call once, before anything else."""
    global _version
    root = REPO / version / "sdk"
    if not root.is_dir():
        raise SystemExit(
            "no SDK tree for %s: %s does not exist" % (version, root)
        )
    _version = version


def version() -> str:
    if _version is None:
        raise RuntimeError("paths.set_version() has not been called")
    return _version


def sdk_root() -> Path:
    """`<repo>/<version>/sdk` - the parent of the seven language folders."""
    return REPO / version() / "sdk"


def version_dir() -> Path:
    """`tools/sdkdocs/<version>` - the version-specific generator inputs."""
    return Path(__file__).resolve().parent / version()
