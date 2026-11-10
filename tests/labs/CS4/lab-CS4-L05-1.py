"""CS4 Lesson 5 Inline Lab 1: Dependency pinning and cryptographic lockfile verification.

Demonstrates exact version pinning and cryptographic artifact integrity verification.
Parses standard pip lockfile entries (name==version --hash=sha256:<digest>).
Computes SHA-256 hashes of simulated package archive byte streams using hashlib.
Detects unpinned floating dependency ranges and catches tampered byte payloads.
"""

from __future__ import annotations

import hashlib
import re
from typing import NamedTuple


class PinnedRequirement(NamedTuple):
    name: str
    version: str
    hashes: tuple[str, ...]


LOCK_LINE_REGEX = re.compile(r"^([A-Za-z0-9_\-\.]+)\s*==\s*([A-Za-z0-9_\-\.]+)(?:\s+--hash=sha256:([a-fA-F0-9]{64}))+$")
UNPINNED_REGEX = re.compile(r"^([A-Za-z0-9_\-\.]+)\s*([><=~^!].*)$")


def parse_lockfile_text(text: str) -> tuple[list[PinnedRequirement], list[str]]:
    """Parse lockfile lines into pinned requirements, flagging syntax and range violations."""
    pinned: list[PinnedRequirement] = []
    errors: list[str] = []

    for line_num, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # Extract all hashes on the line
        parts = line.split()
        pkg_spec = parts[0]
        hash_parts = [p.removeprefix("--hash=sha256:") for p in parts[1:] if p.startswith("--hash=sha256:")]

        if "==" not in pkg_spec:
            errors.append(f"Line {line_num}: Unpinned or invalid package spec '{pkg_spec}'")
            continue

        if not hash_parts:
            errors.append(f"Line {line_num}: Missing cryptographic --hash for '{pkg_spec}'")
            continue

        name, version = pkg_spec.split("==", 1)
        pinned.append(PinnedRequirement(name=name.strip(), version=version.strip(), hashes=tuple(hash_parts)))

    return pinned, errors


def verify_artifact_integrity(wheel_bytes: bytes, expected_hashes: tuple[str, ...]) -> bool:
    """Verify that the SHA-256 digest of artifact bytes matches at least one recorded hash."""
    computed_digest = hashlib.sha256(wheel_bytes).hexdigest().lower()
    return any(computed_digest == h.lower() for h in expected_hashes)


def main() -> None:
    print("Dependency pinning and cryptographic lockfile verification:")

    # Simulated wheel byte streams
    sim_numpy_bytes = b"SIMULATED: numpy wheel archive binary payload v2.0.0"
    sim_numpy_hash = hashlib.sha256(sim_numpy_bytes).hexdigest()

    sim_scipy_bytes = b"SIMULATED: scipy wheel archive binary payload v1.13.0"
    sim_scipy_hash = hashlib.sha256(sim_scipy_bytes).hexdigest()

    # 1. Authentic valid lockfile
    valid_lock = f"""# Production pinned lockfile
numpy==2.0.0 --hash=sha256:{sim_numpy_hash}
scipy==1.13.0 --hash=sha256:{sim_scipy_hash}
"""

    pinned, _ = parse_lockfile_text(valid_lock)
    print(f"Parsed {len(pinned)} pinned dependencies with 0 errors.")

    numpy_valid = verify_artifact_integrity(sim_numpy_bytes, pinned[0].hashes)
    scipy_valid = verify_artifact_integrity(sim_scipy_bytes, pinned[1].hashes)
    print(f"Authentic artifact integrity: numpy={numpy_valid}, scipy={scipy_valid}")

    # 2. Lockfile with unpinned range
    unpinned_lock = """# Flawed lockfile with floating ranges and missing hashes
numpy>=2.0.0
pytest==8.2.0
"""
    _, unpinned_errors = parse_lockfile_text(unpinned_lock)
    print(f"\nUnpinned range evaluation: caught {len(unpinned_errors)} violations:")
    for err in unpinned_errors:
        print(f"  {err}")

    # 3. Tampered payload detection
    tampered_bytes = b"SIMULATED: compromised numpy wheel payload with unauthorized changes"
    tampered_valid = verify_artifact_integrity(tampered_bytes, pinned[0].hashes)
    print(f"\nTampered payload integrity check: {tampered_valid}")
    if not tampered_valid:
        computed = hashlib.sha256(tampered_bytes).hexdigest()
        print("  Tampering detected: computed hash does not match pinned hash.")
        print(f"  Expected: {pinned[0].hashes[0][:16]}...")
        print(f"  Computed: {computed[:16]}...")


main()
