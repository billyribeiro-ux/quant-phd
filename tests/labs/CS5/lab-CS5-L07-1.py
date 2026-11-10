"""CS5 Lab L07: Array-of-structs (AoS) vs Struct-of-arrays (SoA) cache and bandwidth model.

Standard library only. Deterministic integer counter under Assumption A1 (64-byte cache line).
Evaluates cache lines loaded, memory bus traffic, and cache capacity efficiency when computing
midpoint prices across M order book quote records in AoS vs SoA layouts.
"""

from __future__ import annotations


def run_aos_vs_soa_cache_benchmark() -> None:
    print("CS5 L07: Array-of-Structs (AoS) vs Struct-of-Arrays (SoA) Cache Model (Assumption A1: 64B Line)")

    line_size = 64  # 64-byte hardware cache line
    m_quotes = 1024  # number of market quotes

    # Layout 1: Array-of-Structs (AoS)
    # struct Quote { double bid; double ask; uint32_t bid_sz; uint32_t ask_sz; uint64_t ts; };
    # Size: 8 + 8 + 4 + 4 + 8 = 32 bytes per Quote record.
    quote_size = 32
    line_size // quote_size  # 2 quotes per 64B cache line

    # Midpoint kernel reads only bid (8B) and ask (8B) = 16B useful payload per quote
    useful_bytes_per_quote = 16
    total_useful_payload = m_quotes * useful_bytes_per_quote

    aos_total_bytes = m_quotes * quote_size
    aos_lines_loaded = aos_total_bytes // line_size
    aos_bus_traffic = aos_lines_loaded * line_size
    aos_utilization = total_useful_payload / aos_bus_traffic

    print(f"Array-of-Structs (AoS) Layout (Quote size: {quote_size}B, M={m_quotes}):")
    print(f"  Distinct cache lines loaded: {aos_lines_loaded}")
    print(f"  Total memory bus traffic:    {aos_bus_traffic} bytes")
    print(f"  Useful payload bytes read:   {total_useful_payload} bytes")
    print(f"  Cache line utilization:      {aos_utilization:.1%}")
    print(f"  Wasted unread metadata:      {aos_bus_traffic - total_useful_payload} bytes")

    # Layout 2: Struct-of-Arrays (SoA)
    # struct QuotesSoA { double bids[M]; double asks[M]; ... };
    # bids array: 1024 * 8 = 8192 bytes; asks array: 1024 * 8 = 8192 bytes
    bids_bytes = m_quotes * 8
    asks_bytes = m_quotes * 8
    bids_lines = bids_bytes // line_size
    asks_lines = asks_bytes // line_size

    soa_lines_loaded = bids_lines + asks_lines
    soa_bus_traffic = soa_lines_loaded * line_size
    soa_utilization = total_useful_payload / soa_bus_traffic

    print(f"\nStruct-of-Arrays (SoA) Layout (Contiguous bids[] and asks[], M={m_quotes}):")
    print(f"  Distinct cache lines loaded: {soa_lines_loaded}")
    print(f"  Total memory bus traffic:    {soa_bus_traffic} bytes")
    print(f"  Useful payload bytes read:   {total_useful_payload} bytes")
    print(f"  Cache line utilization:      {soa_utilization:.1%}")
    print(f"  Wasted unread metadata:      {soa_bus_traffic - total_useful_payload} bytes")

    # Relative comparison
    line_reduction_ratio = aos_lines_loaded / soa_lines_loaded
    traffic_reduction_ratio = aos_bus_traffic / soa_bus_traffic
    print("\nComparative Layout Efficiency:")
    print(f"  Cache lines ratio (AoS / SoA): {line_reduction_ratio:.1f}x fewer cache lines loaded in SoA")
    print(f"  Bandwidth ratio  (AoS / SoA): {traffic_reduction_ratio:.1f}x less memory bus traffic in SoA")


def main() -> None:
    run_aos_vs_soa_cache_benchmark()


main()
