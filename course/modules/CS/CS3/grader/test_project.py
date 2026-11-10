"""Pytest test suite for CS3 Atlas A2 data layer store (atlas.dataset).

Tests ingestion across all five sources, point-in-time asof queries,
cryptographic manifest integrity, idempotence, and conflict detection.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

# Ensure workspace root is importable
workspace_dir = Path(__file__).parent
if str(workspace_dir) not in sys.path:
    sys.path.insert(0, str(workspace_dir))

import pytest  # noqa: E402

try:
    from atlas.dataset import ManifestRow, Store, open_store  # type: ignore[import-not-found]
except ImportError:
    from reference import ManifestRow, Store, open_store  # type: ignore[import-not-found]
from instance import make_instance  # type: ignore[import-not-found]  # noqa: E402


@pytest.fixture(scope="module")
def instance_data() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    inst = make_instance(seed)
    payload = json.loads(str(inst["payload"]))
    return payload  # type: ignore[no-any-return]


@pytest.fixture
def store(tmp_path: Path) -> Store:
    db_file = tmp_path / "test_store.db"
    st = open_store(str(db_file), engine="sqlite")
    yield st
    st.close()


def test_open_store_invalid_path() -> None:
    with pytest.raises(ValueError, match="path"):
        open_store("")
    with pytest.raises(ValueError, match="path"):
        open_store("   ")


def test_open_store_invalid_engine() -> None:
    with pytest.raises(ValueError, match="engine"):
        open_store(":memory:", engine="postgres")


def test_ingest_all_five_sources(store: Store, instance_data: dict[str, Any]) -> None:
    licence = "SIMULATED: generated fixture, no issuer licence applies"
    url = "https://atlas.local/fixtures"

    # 1. FRED CSV
    fred_bytes = bytes.fromhex(instance_data["fred_csv_hex"])
    row_fred = store.ingest(
        "fred",
        fred_bytes,
        retrieved=instance_data["fred_retrieved"],
        licence=licence,
        source_url=url,
    )
    assert isinstance(row_fred, ManifestRow)
    assert row_fred.source == "fred"
    assert row_fred.sha256 == instance_data["fred_sha256"]
    assert row_fred.n_bytes == len(fred_bytes)
    assert row_fred.rows == instance_data["fred_rows"]
    assert row_fred.retrieved == instance_data["fred_retrieved"]

    # 2. Treasury CSV
    ust_bytes = bytes.fromhex(instance_data["treasury_csv_hex"])
    row_ust = store.ingest(
        "treasury",
        ust_bytes,
        retrieved=instance_data["treasury_retrieved"],
        licence=licence,
        source_url=url,
    )
    assert row_ust.source == "treasury"
    assert row_ust.sha256 == instance_data["treasury_sha256"]
    assert row_ust.rows == instance_data["treasury_rows"]

    # 3. French CSV
    fr_bytes = bytes.fromhex(instance_data["french_csv_hex"])
    row_fr = store.ingest(
        "french",
        fr_bytes,
        retrieved=instance_data["french_retrieved"],
        licence=licence,
        source_url=url,
    )
    assert row_fr.source == "french"
    assert row_fr.sha256 == instance_data["french_sha256"]

    # 4. Shiller CSV
    sh_bytes = bytes.fromhex(instance_data["shiller_csv_hex"])
    row_sh = store.ingest(
        "shiller",
        sh_bytes,
        retrieved=instance_data["shiller_retrieved"],
        licence=licence,
        source_url=url,
    )
    assert row_sh.source == "shiller"
    assert row_sh.sha256 == instance_data["shiller_sha256"]

    # 5. EDGAR raw
    edgar_bytes = bytes.fromhex(instance_data["edgar_raw_hex"])
    row_ed = store.ingest_raw(
        "edgar",
        edgar_bytes,
        retrieved=instance_data["edgar_retrieved"],
        licence=licence,
        source_url=url,
    )
    assert row_ed.source == "edgar"
    assert row_ed.sha256 == instance_data["edgar_sha256"]
    assert row_ed.rows is None


def test_idempotence_and_conflict(store: Store, instance_data: dict[str, Any]) -> None:
    licence = "SIMULATED: test licence"
    url = "https://atlas.local"
    fred_bytes = bytes.fromhex(instance_data["fred_csv_hex"])
    retrieved = instance_data["fred_retrieved"]

    r1 = store.ingest("fred", fred_bytes, retrieved=retrieved, licence=licence, source_url=url)
    # Re-ingest exact same bytes and timestamp -> should return existing ManifestRow
    r2 = store.ingest("fred", fred_bytes, retrieved=retrieved, licence=licence, source_url=url)
    assert r1 == r2

    # Ingest different bytes at same (source, retrieved) -> must raise ValueError naming conflict
    diff_bytes = b"date,DGS10\n2020-01-01,1.99\n"
    with pytest.raises(ValueError, match="Conflict"):
        store.ingest("fred", diff_bytes, retrieved=retrieved, licence=licence, source_url=url)


def test_point_in_time_asof(store: Store, instance_data: dict[str, Any]) -> None:
    licence = "SIMULATED: test licence"
    url = "https://atlas.local"

    # Ingest original FRED and Treasury
    store.ingest(
        "fred",
        bytes.fromhex(instance_data["fred_csv_hex"]),
        retrieved=instance_data["fred_retrieved"],
        licence=licence,
        source_url=url,
    )
    store.ingest(
        "treasury",
        bytes.fromhex(instance_data["treasury_csv_hex"]),
        retrieved=instance_data["treasury_retrieved"],
        licence=licence,
        source_url=url,
    )

    # Ingest revised FRED data released later
    store.ingest(
        "fred",
        bytes.fromhex(instance_data["fred_rev_csv_hex"]),
        retrieved=instance_data["fred_rev_retrieved"],
        licence=licence,
        source_url=url,
    )

    # Run query checks from instance
    for q in instance_data["expected_asof_queries"]:
        ans = store.asof(q["source"], q["series"], q["t"])
        expected = q["expected"]
        if expected is None:
            assert ans is None, f"Query {q['desc']} expected None, got {ans}"
        else:
            assert ans is not None, f"Query {q['desc']} expected dict, got None"
            assert ans["source"] == expected["source"]
            assert ans["series"] == expected["series"]
            assert ans["date"] == expected["date"]
            assert ans["value"] == expected["value"]
            assert ans["retrieved"] == expected["retrieved"]

    # Unknown source raises ValueError
    with pytest.raises(ValueError, match="Unknown source"):
        store.asof("crypto_unknown", "BTC", "2020-02-01T00:00:00Z")

    # Unknown series returns None
    assert store.asof("fred", "NONEXISTENT_SERIES", "2020-02-20T00:00:00Z") is None


def test_manifest_and_tamper_verification(tmp_path: Path, instance_data: dict[str, Any]) -> None:
    db_file = tmp_path / "tamper_test.db"
    store = open_store(str(db_file), engine="sqlite")
    licence = "SIMULATED: test licence"
    url = "https://atlas.local"

    fred_bytes = bytes.fromhex(instance_data["fred_csv_hex"])
    store.ingest("fred", fred_bytes, retrieved=instance_data["fred_retrieved"], licence=licence, source_url=url)

    # Clean verification passes
    store.verify()

    rows = store.manifest()
    assert len(rows) == 1
    assert rows[0].source == "fred"
    assert rows[0].sha256 == instance_data["fred_sha256"]

    store.close()

    # Now tamper with the payload blob directly in SQLite database
    conn = sqlite3.connect(str(db_file))
    cur = conn.execute("SELECT seq, body FROM payloads WHERE seq = 1")
    seq, body = cur.fetchone()
    tampered_body = bytearray(body)
    tampered_body[0] ^= 0xFF  # Flip first byte
    conn.execute("UPDATE payloads SET body = ? WHERE seq = ?", (bytes(tampered_body), seq))
    conn.commit()
    conn.close()

    # Reopen store and run verify; must raise ValueError
    store2 = open_store(str(db_file), engine="sqlite")
    try:
        with pytest.raises(ValueError, match="Integrity check failed"):
            store2.verify()
    finally:
        store2.close()


def test_invalid_inputs(store: Store) -> None:
    url = "https://atlas.local"
    lic = "SIMULATED"

    # Malformed timestamp
    with pytest.raises(ValueError):
        store.ingest("fred", b"date,x\n2020-01-01,1\n", retrieved="2020-01-01 12:00:00", licence=lic, source_url=url)

    # Empty licence
    with pytest.raises(ValueError, match="licence"):
        store.ingest("fred", b"date,x\n2020-01-01,1\n", retrieved="2020-01-01T12:00:00Z", licence="  ", source_url=url)

    # Empty source_url
    with pytest.raises(ValueError, match="source_url"):
        store.ingest("fred", b"date,x\n2020-01-01,1\n", retrieved="2020-01-01T12:00:00Z", licence=lic, source_url="")

    # Malformed CSV: first column not date
    with pytest.raises(ValueError, match="First column"):
        store.ingest("fred", b"ticker,val\nAAPL,100\n", retrieved="2020-01-01T12:00:00Z", licence=lic, source_url=url)

    # Malformed CSV: duplicate series name
    with pytest.raises(ValueError, match="Duplicate"):
        store.ingest(
            "fred", b"date,DGS10,DGS10\n2020-01-01,1,2\n", retrieved="2020-01-01T12:00:00Z", licence=lic, source_url=url
        )

    # Malformed CSV: invalid date format in row
    with pytest.raises(ValueError, match="Observation date"):
        store.ingest(
            "fred", b"date,DGS10\n01/01/2020,1.5\n", retrieved="2020-01-01T12:00:00Z", licence=lic, source_url=url
        )
