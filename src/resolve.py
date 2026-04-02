"""Path resolution — converts relative config paths to absolute using project root."""
from __future__ import annotations

from pathlib import Path


def resolve_path(project_dir: Path, raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else project_dir / p
