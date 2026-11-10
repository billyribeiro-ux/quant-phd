"""CS5 Lab L06: Memory hierarchy, cache line utilization, and false sharing model.

Standard library only. Deterministic integer counter under Assumption A1 (64-byte cache line).
Models sequential vs strided traversal cache line misses, byte traffic, and multi-core
cache line invalidations caused by false sharing.
"""

from __future__ import annotations


def run_cache_hierarchy_model() -> None:
    print("CS5 L06: Memory Hierarchy and Cache Line Access Model (Assumption A1: 64B Line)")

    line_size = 64  # bytes per cache line
    element_size = 8  # sizeof(double) = 8 bytes
    elements_per_line = line_size // element_size  # 8 doubles per line
    n_elements = 1024  # 8192 total bytes = 128 cache lines

    # Traversal 1: Sequential access (stride = 1)
    seq_lines_touched = set()
    seq_bytes_transferred = 0
    for i in range(n_elements):
        byte_offset = i * element_size
        line_idx = byte_offset // line_size
        if line_idx not in seq_lines_touched:
            seq_lines_touched.add(line_idx)
            seq_bytes_transferred += line_size

    useful_bytes_seq = n_elements * element_size
    seq_miss_rate = len(seq_lines_touched) / n_elements

    print(f"Sequential Scan (N={n_elements} doubles, stride=1):")
    print(f"  Distinct cache lines loaded: {len(seq_lines_touched)}")
    print(f"  Total memory traffic:        {seq_bytes_transferred} bytes")
    seq_util = useful_bytes_seq / seq_bytes_transferred
    print(f"  Useful payload bytes:        {useful_bytes_seq} bytes (utilization: {seq_util:.1%})")
    print(f"  Cold miss rate:              {seq_miss_rate:.3f} (1 miss per {elements_per_line} accesses)")

    # Traversal 2: Strided access (stride = 8, stepping across cache lines)
    stride = 8
    strided_indices = list(range(0, n_elements, stride))  # 128 reads
    strided_lines_touched = set()
    strided_bytes_transferred = 0
    for idx in strided_indices:
        byte_offset = idx * element_size
        line_idx = byte_offset // line_size
        if line_idx not in strided_lines_touched:
            strided_lines_touched.add(line_idx)
            strided_bytes_transferred += line_size

    useful_bytes_strided = len(strided_indices) * element_size
    strided_miss_rate = len(strided_lines_touched) / len(strided_indices)

    print(f"Strided Scan (N={len(strided_indices)} doubles, stride={stride}):")
    print(f"  Distinct cache lines loaded: {len(strided_lines_touched)}")
    print(f"  Total memory traffic:        {strided_bytes_transferred} bytes")
    strided_util = useful_bytes_strided / strided_bytes_transferred
    print(f"  Useful payload bytes:        {useful_bytes_strided} bytes (utilization: {strided_util:.1%})")
    print(f"  Cold miss rate:              {strided_miss_rate:.3f} (1 miss per access)")

    # Traversal 3: False sharing model
    # Two adjacent int64 variables at offsets 0 and 8 (same 64B cache line)
    # vs padded variables at offsets 0 and 64 (separate cache lines)
    unpadded_line_var1 = 0 // line_size
    unpadded_line_var2 = 8 // line_size
    padded_line_var1 = 0 // line_size
    padded_line_var2 = 64 // line_size

    unpadded_invalidations = 100 if unpadded_line_var1 == unpadded_line_var2 else 0
    padded_invalidations = 100 if padded_line_var1 == padded_line_var2 else 0

    print("Multi-core False Sharing (100 alternating ping-pong writes):")
    print(f"  Unpadded (same 64B line):   {unpadded_invalidations} cache line invalidation transfers")
    print(f"  Padded (alignas(64)):       {padded_invalidations} cache line invalidation transfers")


def main() -> None:
    run_cache_hierarchy_model()


main()
