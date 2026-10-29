import sys
sys.path.insert(0, "/tmp/AC4-v/AC4-b/r30/mod")
import l04_mod as m
for label, args in [("uneven pool rate", (10_000_001, 10_000, "pool")), ("exact", (10_000_000, 10_000, "pool"))]:
    try:
        print(label, "->", m.exact_rate(*args))
    except ValueError as e:
        print(label, "-> ValueError:", e)
