"""Minimal YAML stub for tests (uses JSON under the hood)."""
from __future__ import annotations

import json
from typing import Any, IO


def safe_load(stream: str | IO[str]) -> Any:
    if hasattr(stream, "read"):
        content = stream.read()
    else:
        content = str(stream)
    return json.loads(content)


def dump(data: Any, stream: IO[str] | None = None, **kwargs: Any) -> str | None:
    if stream is None:
        return json.dumps(data)
    json.dump(data, stream)
    return None
