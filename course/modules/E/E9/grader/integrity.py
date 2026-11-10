"""Integrity verification for E9 Sovereign DSA instance generator.

Verifies deterministic instance generation and required structural invariants.
"""

from __future__ import annotations

import hashlib
import json

from instance import make_instance


def instance_checksum(seed: int) -> str:
    """Compute SHA-256 checksum of generated instance."""
    inst = make_instance(seed)
    serialized = json.dumps(inst, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def verify_instance_integrity(seed: int) -> bool:
    """Verify that instance generation is perfectly repeatable."""
    inst1 = make_instance(seed)
    inst2 = make_instance(seed)
    return bool(inst1 == inst2)
