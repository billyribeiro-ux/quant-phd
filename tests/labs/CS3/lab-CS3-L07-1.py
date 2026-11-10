"""CS3 Lesson 7 Inline Lab 1: Columnar storage vs row layout projection pruning.

Measures memory buffers and bytes scanned for a single-column analytical aggregation
under row-oriented (NSM) versus columnar (DSM) physical layouts.
Data: SIMULATED trade records.
"""

from __future__ import annotations

import struct
from typing import NamedTuple


class RowTrade(NamedTuple):
    trade_id: int  # int64 (8 bytes)
    timestamp_ns: int  # int64 (8 bytes)
    price_cents: int  # int64 (8 bytes)
    qty: int  # int32 (4 bytes)
    venue_id: int  # int32 (4 bytes)
    trader_id: int  # int32 (4 bytes)
    account_id: int  # int32 (4 bytes)
    flags: int  # int32 (4 bytes)
    # Total row size: 8 + 8 + 8 + 4 + 4 + 4 + 4 + 4 = 44 bytes


ROW_FORMAT = "=qqqiiiii"
ROW_SIZE = struct.calcsize(ROW_FORMAT)  # 44 bytes


def simulate_row_store(n_rows: int) -> bytes:
    """Serialize n_rows into a contiguous row-major binary buffer."""
    buf = bytearray()
    for i in range(n_rows):
        packed = struct.pack(
            ROW_FORMAT,
            100000 + i,  # trade_id
            1600000000000000000 + i * 1000,  # timestamp_ns
            15025 + (i % 50),  # price_cents
            100 + (i % 10) * 10,  # qty
            1,  # venue_id
            42,  # trader_id
            999,  # account_id
            0,  # flags
        )
        buf.extend(packed)
    return bytes(buf)


def simulate_column_store(n_rows: int) -> dict[str, bytes]:
    """Serialize n_rows into individual column vectors."""
    trade_ids = bytearray()
    timestamps = bytearray()
    prices = bytearray()
    qtys = bytearray()
    venues = bytearray()
    traders = bytearray()
    accounts = bytearray()
    flags = bytearray()

    for i in range(n_rows):
        trade_ids.extend(struct.pack("=q", 100000 + i))
        timestamps.extend(struct.pack("=q", 1600000000000000000 + i * 1000))
        prices.extend(struct.pack("=q", 15025 + (i % 50)))
        qtys.extend(struct.pack("=i", 100 + (i % 10) * 10))
        venues.extend(struct.pack("=i", 1))
        traders.extend(struct.pack("=i", 42))
        accounts.extend(struct.pack("=i", 999))
        flags.extend(struct.pack("=i", 0))

    return {
        "trade_id": bytes(trade_ids),
        "timestamp_ns": bytes(timestamps),
        "price_cents": bytes(prices),
        "qty": bytes(qtys),
        "venue_id": bytes(venues),
        "trader_id": bytes(traders),
        "account_id": bytes(accounts),
        "flags": bytes(flags),
    }


def main() -> None:
    n_rows = 10000
    row_buffer = simulate_row_store(n_rows)
    column_store = simulate_column_store(n_rows)

    print(f"Total simulated rows: {n_rows}")
    print(f"Row layout record size: {ROW_SIZE} bytes")
    print(f"Total row buffer size: {len(row_buffer)} bytes ({len(row_buffer) / 1024:.1f} KiB)")

    # Analytical query: SELECT AVG(price_cents) FROM trades
    # 1. In row-store: must stream all records; each price requires stride through row buffer
    row_bytes_read = len(row_buffer)  # I/O subsystem must scan entire row blocks
    price_sum_row = 0
    for i in range(n_rows):
        offset = i * ROW_SIZE
        # price_cents is 3rd field: offset + 8 (trade_id) + 8 (timestamp_ns) = offset + 16
        price_cents = struct.unpack_from("=q", row_buffer, offset + 16)[0]
        price_sum_row += price_cents
    avg_price_row = price_sum_row / n_rows

    # 2. In column-store: projection pruning reads ONLY the price_cents vector
    price_vector = column_store["price_cents"]
    column_bytes_read = len(price_vector)
    price_sum_col = 0
    for i in range(n_rows):
        price_cents = struct.unpack_from("=q", price_vector, i * 8)[0]
        price_sum_col += price_cents
    avg_price_col = price_sum_col / n_rows

    assert avg_price_row == avg_price_col

    print(f"Calculated average price: {avg_price_row:.2f} cents")
    print(f"Row store bytes scanned: {row_bytes_read} bytes")
    print(f"Column store bytes scanned: {column_bytes_read} bytes")
    print(f"I/O Reduction Factor: {row_bytes_read / column_bytes_read:.2f}x")
    print(f"Exact theoretical savings: {(1.0 - column_bytes_read / row_bytes_read) * 100:.1f}% bandwidth pruned")
    assert column_bytes_read == n_rows * 8
    assert row_bytes_read == n_rows * 44


main()
