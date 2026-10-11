"""Registry entries: construction from Crossref works, stable keys, and I/O."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .crossref import Work
from .text import ascii_fold

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "references" / "references.json"
_STOPWORDS = frozenset(
    [
        "a",
        "an",
        "the",
        "of",
        "on",
        "in",
        "for",
        "and",
        "to",
        "with",
        "from",
        "by",
        "at",
        "as",
        "is",
        "are",
        "do",
        "does",
        "what",
        "why",
        "how",
        "when",
        "its",
    ]
)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", ascii_fold(text).lower())


def base_key(work: Work, family_override: str | None = None) -> str:
    """Stable human-readable key: firstauthorfamily + year + first significant title word.

    ``family_override`` replaces a malformed Crossref surname (recorded in the entry's notes).
    """
    family_source = family_override or (work.authors[0].family if work.authors else "")
    family = _slug(family_source.split()[-1]) if family_source else "anon"
    words = [_slug(w) for w in re.split(r"[\s\-:/]+", work.title)]
    word = next((w for w in words if w and w not in _STOPWORDS), "untitled")
    return f"{family}{work.year or 'nd'}{word[:16]}"


@dataclass
class Entry:
    key: str
    work: Work
    status: str
    origin: str
    source_strings: list[str]
    used_by: list[str]
    corrections: dict[str, dict[str, str]]
    resolved_at: str
    notes: dict[str, dict[str, str]] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        w = self.work
        return {
            "key": self.key,
            "doi": w.doi,
            "type": w.type,
            "title": w.title,
            "authors": [{"family": a.family, "given": a.given} for a in w.authors],
            "year": w.year,
            "container": w.container[0] if w.container else None,
            "volume": w.volume,
            "issue": w.issue,
            "pages": w.pages,
            "isbn": list(w.isbn),
            "publisher": w.publisher,
            "status": self.status,
            "origin": self.origin,
            "source_strings": sorted(set(self.source_strings)),
            "used_by": sorted(set(self.used_by)),
            "corrections": self.corrections,
            "notes": self.notes,
            "resolved_at": self.resolved_at,
        }


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def assign_keys(entries: list[Entry]) -> None:
    """Assign unique keys deterministically: collisions are suffixed b, c, ... in DOI order."""
    groups: dict[str, list[Entry]] = {}
    for entry in entries:
        override = entry.notes.get("crossref_author_name", {}).get("curriculum")
        groups.setdefault(base_key(entry.work, override), []).append(entry)
    for base, group in groups.items():
        group.sort(key=lambda e: e.work.doi)
        for index, entry in enumerate(group):
            entry.key = base if index == 0 else f"{base}{chr(ord('a') + index)}"


def load(path: Path = REGISTRY) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    entries: list[dict[str, Any]] = data["entries"]
    return entries


def save(entries: list[dict[str, Any]], path: Path = REGISTRY) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": 1,
        "generated_at": now(),
        "count": len(entries),
        "entries": sorted(entries, key=lambda e: e["key"]),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
