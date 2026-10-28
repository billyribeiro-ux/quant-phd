"""CS2 lab L03 (the curriculum lab): a binary-heap event queue against a sorted list, on one seeded event stream.

Standard library only. No wall-clock time is measured. Both structures are counted in the same model:
a comparison is one test of two event keys, and a move is one assignment of an event key into a slot of
the array that holds the structure. An event key is a pair (time, sequence number), so all keys are distinct
and the order is total. The sorted list keeps its keys in descending order, so its minimum is the last element.

For each N the stream is the same for both structures: N events are inserted with seeded random times, then N
hold steps each pop the earliest event and insert one new event at its time plus a seeded delay, then the
remaining N events are popped. The popped sequences of the two structures are compared element by element.
The lab checks two bounds: each heap operation stays within its comparison bound, and the heap total stays
within 6 * N * floor(log2 N), which is proved on the page.
"""

from __future__ import annotations

import random

Key = tuple[int, int]


class CountingHeap:
    """An array-based binary min-heap of event keys that counts comparisons and moves."""

    def __init__(self) -> None:
        self.items: list[Key] = []
        self.comparisons = 0
        self.moves = 0
        self.bound_violations = 0

    def __len__(self) -> int:
        return len(self.items)

    def push(self, key: Key) -> None:
        before = self.comparisons
        self.items.append(key)
        self.moves += 1
        i = len(self.items) - 1
        while i > 0:
            parent = (i - 1) // 2
            self.comparisons += 1
            if self.items[i] < self.items[parent]:
                self.items[i], self.items[parent] = self.items[parent], self.items[i]
                self.moves += 2
                i = parent
            else:
                break
        if self.comparisons - before > (len(self.items)).bit_length() - 1:
            self.bound_violations += 1

    def pop(self) -> Key:
        if not self.items:
            raise IndexError("pop from an empty event queue")
        before = self.comparisons
        size_before = len(self.items)
        top = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self.moves += 1
            i = 0
            n = len(self.items)
            while True:
                left, right = 2 * i + 1, 2 * i + 2
                smallest = i
                if left < n:
                    self.comparisons += 1
                    if self.items[left] < self.items[smallest]:
                        smallest = left
                if right < n:
                    self.comparisons += 1
                    if self.items[right] < self.items[smallest]:
                        smallest = right
                if smallest == i:
                    break
                self.items[i], self.items[smallest] = self.items[smallest], self.items[i]
                self.moves += 2
                i = smallest
        if self.comparisons - before > 2 * (size_before.bit_length() - 1):
            self.bound_violations += 1
        return top


class CountingSortedList:
    """A list of event keys in descending order, so the minimum is last. Insertion finds the place by binary search."""

    def __init__(self) -> None:
        self.items: list[Key] = []
        self.comparisons = 0
        self.moves = 0

    def __len__(self) -> int:
        return len(self.items)

    def push(self, key: Key) -> None:
        lo, hi = 0, len(self.items)
        while lo < hi:
            mid = (lo + hi) // 2
            self.comparisons += 1
            if self.items[mid] > key:
                lo = mid + 1
            else:
                hi = mid
        self.moves += len(self.items) - lo + 1
        self.items.insert(lo, key)

    def pop(self) -> Key:
        if not self.items:
            raise IndexError("pop from an empty event queue")
        return self.items.pop()


def run_hold(queue: CountingHeap | CountingSortedList, n: int, seed: int) -> list[Key]:
    """Insert n seeded events, run n hold steps, then drain. Return the popped keys in order."""
    rng = random.Random(seed)
    for seq in range(n):
        queue.push((rng.randrange(1_000_000), seq))
    delays = [rng.randint(1, 1000) for _ in range(n)]
    popped: list[Key] = []
    for step in range(n):
        time, _ = event = queue.pop()
        popped.append(event)
        queue.push((time + delays[step], n + step))
    while len(queue) > 0:
        popped.append(queue.pop())
    return popped


def main() -> None:
    print("hold model: N events, N hold steps (pop, then push one later event), then N drain pops")
    previous: tuple[int, int, int, int] | None = None
    all_equal = True
    bounds_ok = True
    for k in range(4, 13):
        n = 2**k
        heap = CountingHeap()
        heap_popped = run_hold(heap, n, 2026)
        sorted_list = CountingSortedList()
        sorted_popped = run_hold(sorted_list, n, 2026)
        equal = heap_popped == sorted_popped
        nondecreasing = all(heap_popped[i] <= heap_popped[i + 1] for i in range(len(heap_popped) - 1))
        within = heap.comparisons <= 6 * n * (n.bit_length() - 1)
        all_equal = all_equal and equal
        bounds_ok = bounds_ok and heap.bound_violations == 0 and within
        print(
            f"N={n:5d} operations={4 * n:6d} heap comparisons={heap.comparisons:7d} heap moves={heap.moves:7d} "
            f"sorted-list comparisons={sorted_list.comparisons:7d} sorted-list moves={sorted_list.moves:9d}"
        )
        print(
            f"  pop orders equal: {equal}; popped times nondecreasing: {nondecreasing}; "
            f"heap comparisons within 6*N*floor(log2 N): {within}"
        )
        current = (heap.comparisons, heap.moves, sorted_list.comparisons, sorted_list.moves)
        if previous is not None:
            print(
                f"  N doubled from the row above: heap comparison ratio {current[0] / previous[0]:.4f}, "
                f"heap move ratio {current[1] / previous[1]:.4f}, "
                f"sorted-list move ratio {current[3] / previous[3]:.4f}"
            )
        previous = current
    print(f"pop orders equal for every N: {all_equal}")
    print(f"every heap operation within its comparison bound, and every total within its bound: {bounds_ok}")


main()
