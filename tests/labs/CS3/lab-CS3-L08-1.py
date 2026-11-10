"""CS3 Lesson 8 Inline Lab 1: Data manifest and bit-for-bit cryptographic integrity.

Constructs an immutable data manifest with SHA-256 digests over raw payload bytes.
Verifies that flipping a single byte in a payload is detected with 100% certainty.
Data: SIMULATED market snapshots.
"""

from __future__ import annotations

import hashlib
from typing import NamedTuple


class ManifestRecord(NamedTuple):
    dataset_id: str
    source_url: str
    licence: str
    retrieved_utc: str
    n_bytes: int
    n_rows: int
    sha256: str


def compute_manifest_record(
    dataset_id: str,
    source_url: str,
    licence: str,
    retrieved_utc: str,
    payload: bytes,
    n_rows: int,
) -> ManifestRecord:
    digest = hashlib.sha256(payload).hexdigest()
    return ManifestRecord(
        dataset_id=dataset_id,
        source_url=source_url,
        licence=licence,
        retrieved_utc=retrieved_utc,
        n_bytes=len(payload),
        n_rows=n_rows,
        sha256=digest,
    )


def verify_integrity(record: ManifestRecord, current_payload: bytes) -> bool:
    """Verify that current_payload matches the cryptographic digest in record."""
    current_digest = hashlib.sha256(current_payload).hexdigest()
    return current_digest == record.sha256


def main() -> None:
    # SIMULATED CSV payload
    csv_text = "date,yield_10y,yield_3m\n2020-01-02,1.88,1.55\n2020-01-03,1.81,1.53\n2020-01-06,1.81,1.56\n"
    raw_payload = csv_text.encode("utf-8")
    record = compute_manifest_record(
        dataset_id="ust_daily_sample",
        source_url="https://atlas.local/data/ust_sample.csv",
        licence="SIMULATED: generated fixture",
        retrieved_utc="2020-01-07T18:00:00Z",
        payload=raw_payload,
        n_rows=3,
    )

    print(f"Dataset: {record.dataset_id}")
    print(f"Retrieved: {record.retrieved_utc}")
    print(f"Payload size: {record.n_bytes} bytes ({record.n_rows} data rows)")
    print(f"SHA-256 Digest: {record.sha256}")

    # 1. Verification of untouched payload
    clean_check = verify_integrity(record, raw_payload)
    print(f"Untouched payload integrity verified: {clean_check}")
    assert clean_check is True

    # 2. Tamper simulation: flip exactly one bit in payload
    tampered_bytes = bytearray(raw_payload)
    # Find position of '1.88' in payload and mutate character
    tampered_bytes[25] ^= 0x01  # Flip a single bit
    tampered_payload = bytes(tampered_bytes)

    tampered_digest = hashlib.sha256(tampered_payload).hexdigest()
    tampered_check = verify_integrity(record, tampered_payload)

    print(f"Tampered digest: {tampered_digest}")
    print(f"Tampered payload detected (check failed): {not tampered_check}")
    assert tampered_check is False
    print("Bit-for-bit tamper detection successfully triggered: True")


if __name__ == "__main__":
    main()
