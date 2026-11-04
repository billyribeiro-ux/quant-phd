# Counterexample for card BK4-c033 ("netting reduces the amount that must move"), from the lesson's own M3 (L02 lines 302-308).
# Stdlib only. Trades: member 1 owes member 2 100 dollars; member 1 owes member 3 100 dollars (cents below).
trades = [(1, 2, 10000), (1, 3, 10000)]
members = (1, 2, 3)
G = sum(a for _, _, a in trades)
rec = {m: sum(a for _, r, a in trades if r == m) for m in members}
pay = {m: sum(a for p, _, a in trades if p == m) for m in members}
n = {m: rec[m] - pay[m] for m in members}
A = sum(max(0, n[m]) for m in members)
both = [m for m in members if rec[m] > 0 and pay[m] > 0]
print("G", G, "A", A, "n", n, "sum n", sum(n.values()))
print("members that both receive and pay:", both)
print("netting leaves the amount unchanged (A == G):", A == G)
print("Proposition 2.3 predicts A == G exactly when no member both receives and pays:", (A == G) == (not both))
print("reduction in bps:", (10000 * (G - A)) // G)
