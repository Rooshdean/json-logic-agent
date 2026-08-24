import json
from pathlib import Path
from typing import Any

from .models import ProjectScanResult, ScannedJsonFile


DEFAULT_IGNORES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
}


def _guess_kind(path: Path, data: Any) -> tuple[str, str]:
    name = path.name.lower()
    keys = set(data.keys()) if isinstance(data, dict) else set()

    if name == "package.json":
        return "node-package-manifest", "Node.js package metadata, scripts, and dependencies"
    if "schema" in name or {"$schema", "properties"} & keys:
        return "schema", "Schema or validation-oriented JSON"
    if "workflow" in name or {"trigger", "rules", "steps", "actions"} & keys:
        return "workflow-or-automation", "Likely contains executable workflow or automation logic"
    if "permission" in name or "role" in name or {"roles", "permissions", "policies"} & keys:
        return "access-policy", "Likely describes roles, permissions, or policy rules"
    if "config" in name or "settings" in name:
        return "configuration", "Application or tool configuration"
    if isinstance(data, list):
        return "data-collection", "Top-level JSON array; likely records or ordered data"
    if isinstance(data, dict):
        return "object-or-configuration", "JSON object requiring semantic inspection"
    return "data", "Primitive JSON data"


def scan_project(
    root: str | Path,
    max_bytes: int = 1_000_000,
    ignores: set[str] | None = None,
) -> ProjectScanResult:
    root_path = Path(root).resolve()
    ignored = DEFAULT_IGNORES | (ignores or set())
    result = ProjectScanResult(root=str(root_path))

    if root_path.is_file():
        candidates = [root_path]
    else:
        candidates = sorted(
            p for p in root_path.rglob("*.json")
            if not any(part in ignored for part in p.relative_to(root_path).parts)
        )

    for path in candidates:
        try:
            size = path.stat().st_size
        except OSError:
            continue

        display_path = path.name if root_path.is_file() else str(path.relative_to(root_path))
        if size > max_bytes:
            result.skipped_large_files.append(display_path)
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            result.skipped_invalid_json.append(display_path)
            continue

        kind, note = _guess_kind(path, data)
        keys = list(data.keys())[:20] if isinstance(data, dict) else []
        result.files.append(
            ScannedJsonFile(
                path=display_path,
                size_bytes=size,
                top_level_type=type(data).__name__,
                top_level_keys=keys,
                likely_kind=kind,
                note=note,
            )
        )

    return result
