"""Independent split of the L07 memo recursion calls on ACGTACG / TGCATGC: base calls, lookups, stored, computed."""
x, y = "ACGTACG", "TGCATGC"
cache = {}
calls = base = lookups = computed = 0


def go(i, j):
    global calls, base, lookups, computed
    calls += 1
    if i == 0 or j == 0:
        base += 1
        return 0
    if (i, j) in cache:
        lookups += 1
        return cache[(i, j)]
    computed += 1
    value = go(i - 1, j - 1) + 1 if x[i - 1] == y[j - 1] else max(go(i - 1, j), go(i, j - 1))
    cache[(i, j)] = value
    return value


print("length", go(len(x), len(y)), "stored", len(cache), "calls", calls, "base", base, "lookups", lookups, "computed", computed)
print("check calls = stored + base + lookups:", calls == len(cache) + base + lookups)
