"""CS5 Lab L05: STL container operation cost model on financial order streams.

Standard library only. Deterministic integer operation counter. Tracks comparisons,
element shifts, and allocations across std::vector, std::unordered_map, and std::priority_queue
implementations processing an identical seeded order stream.
"""

from __future__ import annotations

import bisect
import heapq
import random


class TracedOrder:
    def __init__(self, order_id: int, price: float, qty: int) -> None:
        self.order_id = order_id
        self.price = price
        self.qty = qty

    def __lt__(self, other: TracedOrder) -> bool:
        return self.price < other.price


def run_stl_container_benchmark() -> None:
    print("CS5 L05: STL Container Operation Model on Order Event Stream")

    # Generate 100 deterministic pseudo-random order events from seed 42
    rng = random.Random(42)
    orders = [TracedOrder(i, round(rng.uniform(95.0, 105.0), 2), rng.randint(1, 50)) for i in range(100)]

    # Model 1: Sorted std::vector (binary search insertion via std::lower_bound)
    vec: list[TracedOrder] = []
    vec_comparisons = 0
    vec_element_shifts = 0

    for ord_item in orders:
        # Binary search (bisect) makes ~ceil(log2(len)) comparisons
        pos = bisect.bisect_left(vec, ord_item)
        if len(vec) > 0:
            vec_comparisons += len(vec).bit_length()
        vec_element_shifts += len(vec) - pos
        vec.insert(pos, ord_item)

    print("std::vector (sorted order book, N=100):")
    print(f"  Total element comparisons (binary search): {vec_comparisons}")
    print(f"  Total element shift moves:                 {vec_element_shifts}")

    # Model 2: std::unordered_map (hash table key lookup by order_id)
    # 100 insertions + 100 lookups
    hash_lookups = 0
    hash_collisions = 0
    bucket_count = 128
    buckets: list[list[int]] = [[] for _ in range(bucket_count)]

    for ord_item in orders:
        h = hash(ord_item.order_id) % bucket_count
        if buckets[h]:
            hash_collisions += len(buckets[h])
        buckets[h].append(ord_item.order_id)
        hash_lookups += 1

    print("std::unordered_map (hash table, N=100, buckets=128):")
    print(f"  Total bucket lookup probes:                {hash_lookups}")
    print(f"  Total hash bucket collisions:              {hash_collisions}")

    # Model 3: std::priority_queue (binary max-heap by price)
    heap: list[float] = []
    heap_comparisons = 0
    for ord_item in orders:
        heapq.heappush(heap, -ord_item.price)
        # heappush does at most ceil(log2(len)) comparisons
        heap_comparisons += len(heap).bit_length()

    for _ in range(50):
        heapq.heappop(heap)
        heap_comparisons += 2 * len(heap).bit_length()

    print("std::priority_queue (binary heap, 100 pushes, 50 pops):")
    print(f"  Total heap sift comparisons:               {heap_comparisons}")


def main() -> None:
    run_stl_container_benchmark()


main()
