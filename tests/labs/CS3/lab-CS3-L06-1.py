"""CS3 Lesson 6 Inline Lab 1: Database index vs full scan search complexity.

Counts row comparisons and records touched in a full table scan versus a sorted-key index.
Demonstrates O(N) linear scan versus O(log N) indexed search complexity deterministically.
Data: SIMULATED limit order book entries.
"""

from __future__ import annotations

import math
from typing import NamedTuple


class BookEntry(NamedTuple):
    order_id: int
    symbol: str
    price: float
    qty: int


def full_scan_search(table: list[BookEntry], target_id: int) -> tuple[BookEntry | None, int]:
    """Perform sequential full table scan, counting rows touched."""
    comparisons = 0
    for row in table:
        comparisons += 1
        if row.order_id == target_id:
            return row, comparisons
    return None, comparisons


def index_binary_search(
    sorted_index: list[tuple[int, int]], table: list[BookEntry], target_id: int
) -> tuple[BookEntry | None, int]:
    """Perform indexed binary search over sorted (order_id, row_ptr), counting comparisons."""
    low = 0
    high = len(sorted_index) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        key, row_ptr = sorted_index[mid]
        if key == target_id:
            return table[row_ptr], comparisons
        elif key < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None, comparisons


def main() -> None:
    # Build SIMULATED table of 10,000 order records
    n_records = 10000
    # Predictable spaced order IDs: 1000, 1002, 1004, ...
    table: list[BookEntry] = [
        BookEntry(order_id=1000 + 2 * i, symbol="AAPL", price=150.0 + (i % 100) * 0.01, qty=100)
        for i in range(n_records)
    ]

    # Build primary index: list of (order_id, row_index) sorted by order_id
    sorted_index = [(entry.order_id, idx) for idx, entry in enumerate(table)]

    # Test cases:
    # 1. Target near end of table (worst case for full scan)
    target_late = table[9500].order_id
    # 2. Target near middle of table
    target_mid = table[5000].order_id
    # 3. Missing target (table exhausted)
    target_missing = 999999

    targets = [
        ("Near End", target_late),
        ("Near Mid", target_mid),
        ("Unmatched Key", target_missing),
    ]

    print(f"Total database table rows: {n_records}")
    print(f"Index structure: Sorted array index over primary key ({n_records} entries)")

    for label, target_id in targets:
        row_scan, scan_touches = full_scan_search(table, target_id)
        row_idx, idx_touches = index_binary_search(sorted_index, table, target_id)

        # Verify results match
        assert (row_scan is None and row_idx is None) or (
            row_scan is not None and row_idx is not None and row_scan.order_id == row_idx.order_id
        )

        max_expected_idx_touches = math.ceil(math.log2(n_records)) + 1
        print(
            f"Search [{label:13s} id={target_id:6d}]: "
            f"Full Scan Touches = {scan_touches:5d} | "
            f"Index Touches = {idx_touches:2d} | "
            f"Speedup Factor = {scan_touches / idx_touches:6.1f}x"
        )
        assert idx_touches <= max_expected_idx_touches

    # Scan touches for missing key must equal total rows N
    _, missing_scan_touches = full_scan_search(table, target_missing)
    assert missing_scan_touches == n_records
    print(f"Exhaustive full scan touched exactly all {n_records} rows: True")


if __name__ == "__main__":
    main()
