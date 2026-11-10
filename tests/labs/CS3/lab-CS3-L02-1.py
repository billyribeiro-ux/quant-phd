"""CS3 Lesson 2 Inline Lab 1: SQL joins and key multiplicity identities.

Demonstrates inner, left, right, and full outer joins using SQLite in-memory tables.
Verifies the duplicate-key multiplication identity:
    |L bowtie R| = sum_k n_L(k) * n_R(k)
Data: SIMULATED trade allocations and broker routing records.
"""

from __future__ import annotations

import sqlite3
from collections import Counter


def main() -> None:
    conn = sqlite3.connect(":memory:")

    with conn:
        conn.execute("CREATE TABLE trades (trade_id INT, symbol TEXT, qty INT)")
        conn.execute("CREATE TABLE broker_routes (route_id INT, symbol TEXT, broker TEXT)")

        # SIMULATED multiset:
        # trades: AAPL x3, MSFT x2, GOOG x1, TSLA x1
        trades_data = [
            (1, "AAPL", 100),
            (2, "AAPL", 200),
            (3, "AAPL", 150),
            (4, "MSFT", 50),
            (5, "MSFT", 80),
            (6, "GOOG", 20),
            (7, "TSLA", 10),
        ]
        # routes: AAPL x2, MSFT x3, NVDA x2
        routes_data = [
            (101, "AAPL", "BROKER_A"),
            (102, "AAPL", "BROKER_B"),
            (103, "MSFT", "BROKER_A"),
            (104, "MSFT", "BROKER_B"),
            (105, "MSFT", "BROKER_C"),
            (106, "NVDA", "BROKER_A"),
            (107, "NVDA", "BROKER_C"),
        ]

        conn.executemany("INSERT INTO trades VALUES (?, ?, ?)", trades_data)
        conn.executemany("INSERT INTO broker_routes VALUES (?, ?, ?)", routes_data)

    # 1. Multiplicity calculations
    l_counts = Counter(row[1] for row in trades_data)
    r_counts = Counter(row[1] for row in routes_data)
    all_keys = set(l_counts.keys()) | set(r_counts.keys())

    expected_inner_count = sum(l_counts[k] * r_counts[k] for k in all_keys)
    unmatched_left = sum(l_counts[k] for k in all_keys if r_counts[k] == 0)
    unmatched_right = sum(r_counts[k] for k in all_keys if l_counts[k] == 0)

    expected_left_count = expected_inner_count + unmatched_left
    expected_right_count = expected_inner_count + unmatched_right
    expected_full_count = expected_inner_count + unmatched_left + unmatched_right

    # 2. Execute SQL joins
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM trades t INNER JOIN broker_routes r ON t.symbol = r.symbol")
    actual_inner = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM trades t LEFT JOIN broker_routes r ON t.symbol = r.symbol")
    actual_left = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM trades t RIGHT JOIN broker_routes r ON t.symbol = r.symbol")
    actual_right = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM trades t FULL OUTER JOIN broker_routes r ON t.symbol = r.symbol")
    actual_full = cur.fetchone()[0]

    print(f"Table trades rows: {len(trades_data)}")
    print(f"Table broker_routes rows: {len(routes_data)}")
    print(f"Inner join rows: {actual_inner} (expected: {expected_inner_count})")
    print(f"Left join rows: {actual_left} (expected: {expected_left_count})")
    print(f"Right join rows: {actual_right} (expected: {expected_right_count})")
    print(f"Full outer join rows: {actual_full} (expected: {expected_full_count})")

    # Invariant checks
    assert actual_inner == expected_inner_count
    assert actual_left == expected_left_count
    assert actual_right == expected_right_count
    assert actual_full == expected_full_count

    print(f"Duplicate-key multiplication identity verified: {actual_inner == 12}")
    conn.close()


main()
