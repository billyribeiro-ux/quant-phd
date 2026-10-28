"""CS2 lab L02: probe counts of a chained hash table with a fixed number of buckets.

Standard library only. The keys are seeded (random.Random(2026)), so the output is the same on every run.
The table has m = 64 buckets and no resizing. The bucket of a key is ((key * 2654435761) mod 2**32) mod 64,
a multiplicative hash that is fixed in this file. One probe is one key comparison inside a chain. A successful
search stops at the matching key, and an unsuccessful search compares the key with every key in its chain.

The model values printed next to the measured ones are exact expectations under simple uniform hashing,
which assumes that each key lands in a bucket chosen uniformly and independently of the other keys. This hash
is not that random model, so the measured and model values can differ. The output prints both values.
"""

from __future__ import annotations

import random

BUCKETS = 64
MULTIPLIER = 2654435761


def bucket_of(key: int, m: int) -> int:
    """The bucket of an integer key in a table of m buckets: ((key * MULTIPLIER) mod 2**32) mod m."""
    if m < 1:
        raise ValueError(f"bucket_of needs m >= 1, got {m}")
    return ((key * MULTIPLIER) % 2**32) % m


class ChainedHashTable:
    """A hash table of distinct integer keys in m buckets, each bucket a chain in insertion order."""

    def __init__(self, m: int) -> None:
        if m < 1:
            raise ValueError(f"ChainedHashTable needs m >= 1, got {m}")
        self.m = m
        self.chains: list[list[int]] = [[] for _ in range(m)]

    def insert(self, key: int) -> None:
        """Append key to the end of its chain. A key already present is not inserted twice."""
        chain = self.chains[bucket_of(key, self.m)]
        if key not in chain:
            chain.append(key)

    def lookup(self, key: int) -> tuple[bool, int]:
        """Return (found, probes): the number of key comparisons made in the key's chain."""
        probes = 0
        for stored in self.chains[bucket_of(key, self.m)]:
            probes += 1
            if stored == key:
                return True, probes
        return False, probes


def chain_formula(table: ChainedHashTable) -> int:
    """The total probes of one successful lookup of every stored key: the sum of L(L + 1) / 2 over the chains."""
    return sum(len(chain) * (len(chain) + 1) // 2 for chain in table.chains)


def main() -> None:
    rng = random.Random(2026)
    keys = rng.sample(range(10**9), 256)
    stored_all = set(keys)
    absent = [x for x in rng.sample(range(10**9), 2000) if x not in stored_all][:500]
    print(f"buckets m = {BUCKETS}; keys are seeded, distinct, below 10**9; absent test keys: {len(absent)}")
    for n in (16, 32, 64, 128, 256):
        table = ChainedHashTable(BUCKETS)
        for key in keys[:n]:
            table.insert(key)
        alpha = n / BUCKETS
        successful = sum(table.lookup(key)[1] for key in keys[:n])
        unsuccessful = sum(table.lookup(key)[1] for key in absent)
        found_all = all(table.lookup(key)[0] for key in keys[:n])
        none_found = not any(table.lookup(key)[0] for key in absent)
        longest = max(len(chain) for chain in table.chains)
        model_successful = 1 + (n - 1) / (2 * BUCKETS)
        print(
            f"alpha={alpha:5.2f} n={n:3d} successful average probes={successful / n:.4f} "
            f"(model {model_successful:.4f}) unsuccessful average probes={unsuccessful / len(absent):.4f} "
            f"(model {alpha:.4f}) longest chain={longest}"
        )
        print(
            f"  every stored key found: {found_all}; no absent key found: {none_found}; "
            f"successful total equals sum of L(L+1)/2: {successful == chain_formula(table)}"
        )
    colliding = [64 * j for j in range(1, 51)]
    table = ChainedHashTable(BUCKETS)
    for key in colliding:
        table.insert(key)
    buckets = {bucket_of(key, BUCKETS) for key in colliding}
    successful = sum(table.lookup(key)[1] for key in colliding)
    miss_found, miss_probes = table.lookup(64 * 51)
    print(f"colliding keys 64 * j for j = 1 to 50 occupy buckets {sorted(buckets)}")
    print(
        f"colliding set: successful total probes={successful}, average={successful / len(colliding):.4f}; "
        f"unsuccessful search for key {64 * 51}: found={miss_found}, probes={miss_probes}"
    )


main()
