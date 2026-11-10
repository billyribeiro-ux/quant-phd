"""CS1 lab L02: Built-in data structures (list, tuple, dict, set).

Standard library only. Tests mutability, sequence slicing, hashability invariants,
and operation counts for membership lookup.
SIMULATED synthetic market order identifiers.
"""

from __future__ import annotations


def count_list_scans(items: list[str], target: str) -> int:
    """Count comparisons required in a linear scan of a list."""
    steps = 0
    for item in items:
        steps += 1
        if item == target:
            break
    return steps


def main() -> None:
    # 1. Tuples: immutable sequences
    fixed_pair: tuple[str, float] = ("EURUSD", 1.0850)
    print(f"tuple pair: symbol={fixed_pair[0]}, quote={fixed_pair[1]:.4f}")

    # 2. Lists: mutable dynamic arrays
    order_queue: list[str] = ["ord_001", "ord_002", "ord_003"]
    order_queue.append("ord_004")
    popped = order_queue.pop(0)
    print(f"popped order: {popped}")
    print(f"remaining queue length: {len(order_queue)}")

    # 3. Sets: unique, unordered collections with O(1) average hash lookup
    seen_ids: set[str] = {"ord_002", "ord_003", "ord_004"}
    seen_ids.add("ord_002")  # duplicate insertion has no effect
    print(f"set size after duplicate addition: {len(seen_ids)}")
    print(f"ord_003 in set: {'ord_003' in seen_ids}")

    # 4. Dicts: key-value mapping with unique hashable keys
    book_depth: dict[str, float] = {
        "ord_002": 100.0,
        "ord_003": 250.0,
        "ord_004": 75.0,
    }
    book_depth["ord_005"] = 300.0
    print(f"dict entry ord_003 quantity: {book_depth['ord_003']:.1f}")
    print(f"total depth across keys: {sum(book_depth.values()):.1f}")

    # 5. Comparing search steps: linear scan vs hash lookup
    symbols = [f"SYM_{i:04d}" for i in range(1000)]
    symbol_set = set(symbols)
    target = "SYM_0750"

    list_steps = count_list_scans(symbols, target)
    set_has = target in symbol_set
    print(f"linear scan steps to find target at index 750: {list_steps}")
    print(f"set membership found target: {set_has}")
    print(f"tuple is hashable: {isinstance(hash(fixed_pair), int)}")


main()
