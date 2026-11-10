"""QR1 Lesson 3 Inline Lab 1: Pure-Python ASOF join with deterministic tie-breaking.

Demonstrates temporal ASOF matching between evaluation query timestamps and
asynchronous right-side information records with sequence-number tie-breaking,
and verifies binary-search implementation against an exhaustive brute-force oracle.
Data: SIMULATED trades and quotes event streams.
"""

from __future__ import annotations

import bisect
from typing import NamedTuple


class InfoRecord(NamedTuple):
    timestamp: str  # YYYY-MM-DDTHH:MM:SSZ
    seq: int  # Ingestion sequence counter (tie-breaker)
    key: str  # (timestamp, seq) key for total ordering
    value: float


class QueryRecord(NamedTuple):
    query_id: int
    timestamp: str


def make_info_record(timestamp: str, seq: int, value: float) -> InfoRecord:
    key = f"{timestamp}:{seq:08d}"
    return InfoRecord(timestamp, seq, key, value)


def asof_join_binary_search(
    queries: list[QueryRecord],
    records: list[InfoRecord],
) -> list[tuple[int, float | None]]:
    """O(N log M) ASOF join using binary search on sorted (timestamp, seq) keys."""
    sorted_records = sorted(records, key=lambda r: (r.timestamp, r.seq))
    record_timestamps = [r.timestamp for r in sorted_records]

    results: list[tuple[int, float | None]] = []
    for q in queries:
        # bisect_right finds insertion point after all records with timestamp <= q.timestamp
        idx = bisect.bisect_right(record_timestamps, q.timestamp)
        if idx == 0:
            results.append((q.query_id, None))
        else:
            # The record immediately preceding idx is the latest published at or before q.timestamp
            results.append((q.query_id, sorted_records[idx - 1].value))
    return results


def asof_join_brute_force(
    queries: list[QueryRecord],
    records: list[InfoRecord],
) -> list[tuple[int, float | None]]:
    """O(N * M) oracle scan: exhaustively evaluates all eligible records."""
    results: list[tuple[int, float | None]] = []
    for q in queries:
        eligible = [r for r in records if r.timestamp <= q.timestamp]
        if not eligible:
            results.append((q.query_id, None))
        else:
            best = max(eligible, key=lambda r: (r.timestamp, r.seq))
            results.append((q.query_id, best.value))
    return results


def main() -> None:
    # SIMULATED right-side records, including simultaneous timestamps with distinct seq
    records: list[InfoRecord] = [
        make_info_record("2026-03-01T09:30:00Z", 1, 100.50),
        make_info_record("2026-03-01T09:30:00Z", 2, 100.55),  # Tie at 09:30:00, seq 2 wins
        make_info_record("2026-03-01T09:35:00Z", 3, 101.20),
        make_info_record("2026-03-01T09:40:00Z", 4, 101.80),
        make_info_record("2026-03-01T09:45:00Z", 5, 102.10),
        make_info_record("2026-03-01T09:45:00Z", 6, 102.15),  # Tie at 09:45:00, seq 6 wins
        make_info_record("2026-03-01T10:00:00Z", 7, 103.00),
    ]

    # SIMULATED left-side query points (some before any record, some exact matches, some interior)
    queries: list[QueryRecord] = [
        QueryRecord(1, "2026-03-01T09:25:00Z"),  # Prior to first record -> None
        QueryRecord(2, "2026-03-01T09:30:00Z"),  # Exact match on tie -> 100.55
        QueryRecord(3, "2026-03-01T09:32:00Z"),  # Interior -> 100.55
        QueryRecord(4, "2026-03-01T09:35:00Z"),  # Exact match -> 101.20
        QueryRecord(5, "2026-03-01T09:44:59Z"),  # Immediately before 09:45 -> 101.80
        QueryRecord(6, "2026-03-01T09:45:00Z"),  # Exact match on tie -> 102.15
        QueryRecord(7, "2026-03-01T10:15:00Z"),  # Subsequent -> 103.00
    ]

    print(f"Total information records: {len(records)}")
    print(f"Total query evaluation points: {len(queries)}")

    bs_results = asof_join_binary_search(queries, records)
    bf_results = asof_join_brute_force(queries, records)

    print("\nQuery results (Binary Search vs Brute Force Oracle):")
    mismatches = 0
    for (qid, bs_val), (_, bf_val) in zip(bs_results, bf_results, strict=True):
        q = next(q for q in queries if q.query_id == qid)
        match = bs_val == bf_val
        if not match:
            mismatches += 1
        val_str = f"{bs_val:.2f}" if bs_val is not None else "None"
        print(f"  Query {qid} at {q.timestamp}: matched={val_str} (consistent: {match})")

    print(f"\nTotal verification queries: {len(queries)}")
    print(f"Algorithm comparison mismatches: {mismatches}")


main()
