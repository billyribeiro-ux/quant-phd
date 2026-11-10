"""CS3 Lesson 3 Inline Lab 1: SQL window functions and frame aggregations.

Demonstrates rolling window sum using SQLite OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN).
Verifies the rolling aggregate values against an independent self-join reference.
Data: SIMULATED daily desk PnL records.
"""

from __future__ import annotations

import sqlite3


def main() -> None:
    conn = sqlite3.connect(":memory:")

    with conn:
        conn.execute(
            """
            CREATE TABLE daily_pnl (
                desk TEXT NOT NULL,
                day_seq INT NOT NULL,
                pnl_cents INT NOT NULL
            )
            """
        )

        # SIMULATED PnL data for two desks over 5 days
        pnl_records = [
            ("RATES", 1, 100000),
            ("RATES", 2, -25000),
            ("RATES", 3, 50000),
            ("RATES", 4, 80000),
            ("RATES", 5, -10000),
            ("EQUITY", 1, 40000),
            ("EQUITY", 2, 60000),
            ("EQUITY", 3, -15000),
            ("EQUITY", 4, -30000),
            ("EQUITY", 5, 95000),
        ]
        conn.executemany("INSERT INTO daily_pnl VALUES (?, ?, ?)", pnl_records)

    cur = conn.cursor()

    # 1. Compute rolling 3-day sum using SQL window function
    cur.execute(
        """
        SELECT
            desk,
            day_seq,
            pnl_cents,
            SUM(pnl_cents) OVER (
                PARTITION BY desk
                ORDER BY day_seq
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) AS rolling_3d_pnl
        FROM daily_pnl
        ORDER BY desk, day_seq
        """
    )
    window_results = cur.fetchall()

    # 2. Compute rolling 3-day sum using independent self-join reference
    cur.execute(
        """
        SELECT
            a.desk,
            a.day_seq,
            a.pnl_cents,
            SUM(b.pnl_cents) AS ref_rolling_3d_pnl
        FROM daily_pnl a
        JOIN daily_pnl b
          ON a.desk = b.desk
         AND b.day_seq BETWEEN a.day_seq - 2 AND a.day_seq
        GROUP BY a.desk, a.day_seq, a.pnl_cents
        ORDER BY a.desk, a.day_seq
        """
    )
    self_join_results = cur.fetchall()

    print(f"Total evaluated rows: {len(window_results)}")
    all_matched = True
    for w_row, s_row in zip(window_results, self_join_results, strict=True):
        desk, day, pnl, win_sum = w_row
        ref_desk, ref_day, ref_pnl, ref_sum = s_row
        assert desk == ref_desk and day == ref_day and pnl == ref_pnl
        match = win_sum == ref_sum
        if not match:
            all_matched = False
        print(f"Desk {desk} Day {day}: PnL={pnl} -> Rolling 3d Window={win_sum}, Self-join={ref_sum}")

    print(f"Window function matches self-join reference on all rows: {all_matched}")
    conn.close()


main()
