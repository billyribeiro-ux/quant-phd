"""Decompose the memoized LCS calls on ACGTACG / TGCATGC into base, lookup and computed calls (L07 Lab 1 Part C).

Usage: python -I this.py <path-to-twin>. Loads the twin without its final main() call.
"""
import sys
import pathlib
import types

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").rstrip()
src = src[: -len("main()")]
mod = types.ModuleType("twin_noMain")
sys.modules["twin_noMain"] = mod
exec(compile(src, "twin", "exec"), mod.__dict__)
x, y = mod.__dict__["FIXED_X"], mod.__dict__["FIXED_Y"]
base = lookup = computed = 0
cache = {}
calls = 0


def go(i, j):
    global base, lookup, computed, calls
    calls += 1
    if i == 0 or j == 0:
        base += 1
        return 0
    if (i, j) in cache:
        lookup += 1
        return cache[(i, j)]
    computed += 1
    value = go(i - 1, j - 1) + 1 if x[i - 1] == y[j - 1] else max(go(i - 1, j), go(i, j - 1))
    cache[(i, j)] = value
    return value


length = go(len(x), len(y))
print("x", x, "y", y, "LCS", length, "cells", (len(x)) * (len(y)))
print("calls", calls, "base", base, "lookup", lookup, "computed", computed, "stored", len(cache))
print("check sum", base + lookup + computed, "== calls:", base + lookup + computed == calls)
print("mod lcs_memo", mod.__dict__["lcs_memo"](x, y))
