"""Starter template for CS3 Atlas A2 data layer store.

Raises NotImplementedError for all operations. Autograder must reject this starter.
"""

from __future__ import annotations

from dataclasses import dataclass

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")


@dataclass(frozen=True)
class ManifestRow:
    source: str
    sha256: str
    n_bytes: int
    rows: int | None
    retrieved: str
    licence: str
    source_url: str


class Store:
    """Unimplemented store for student completion."""

    def ingest(
        self,
        source: str,
        payload: bytes,
        *,
        retrieved: str,
        licence: str,
        source_url: str,
    ) -> ManifestRow:
        raise NotImplementedError("Store.ingest is not implemented")

    def ingest_raw(
        self,
        source: str,
        payload: bytes,
        *,
        retrieved: str,
        licence: str,
        source_url: str,
    ) -> ManifestRow:
        raise NotImplementedError("Store.ingest_raw is not implemented")

    def asof(self, source: str, series: str, t: str) -> dict[str, str] | None:
        raise NotImplementedError("Store.asof is not implemented")

    def manifest(self) -> list[ManifestRow]:
        raise NotImplementedError("Store.manifest is not implemented")

    def verify(self) -> None:
        raise NotImplementedError("Store.verify is not implemented")

    def close(self) -> None:
        raise NotImplementedError("Store.close is not implemented")


def open_store(path: str, *, engine: str = "sqlite") -> Store:
    raise NotImplementedError("open_store is not implemented")
