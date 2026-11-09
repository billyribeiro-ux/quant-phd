"""Independent re-derivation of L06 Lab 1 Part A (bisection on the 4096-term prefix), different code path from the twin."""
from fractions import Fraction as F
vals = {n: F((n * n) % 1000, 1000) for n in range(1, 4097)}
lo, hi = F(0), F(1)
last = 0
chosen = []
for step in range(1, 9):
    mid = (lo + hi) / 2
    cand = sorted(n for n in vals if n > last and lo <= vals[n] <= hi)
    left = [n for n in cand if vals[n] < mid]
    right = [n for n in cand if vals[n] >= mid]
    if len(left) >= len(right):
        hi, pick = mid, left
    else:
        lo, pick = mid, right
    last = pick[0]
    chosen.append((last, vals[last]))
    print(f"step {step} interval [{lo}, {hi}] width {hi - lo} chosen_index {last}")
ok = all(
    (lambda j: all(
        (ivs[j][0] <= v <= ivs[j][1]) for _, v in chosen[j:]
    ))(j)
    for j in range(8)
) if (ivs := None) else None
ivals = []
lo, hi = F(0), F(1)
last = 0
for step in range(8):
    mid = (lo + hi) / 2
    cand = sorted(n for n in vals if n > last and lo <= vals[n] <= hi)
    left = [n for n in cand if vals[n] < mid]
    right = [n for n in cand if vals[n] >= mid]
    if len(left) >= len(right):
        hi = mid; last = left[0]
    else:
        lo = mid; last = right[0]
    ivals.append((lo, hi))
nested = all(ivals[j][0] <= vals[chosen[k][0]] <= ivals[j][1] for j in range(8) for k in range(j, 8))
print("tail_values_in_their_interval", nested)
print("subsequence_indices", " ".join(str(i) for i, _ in chosen))
print("grid tenths max", max(F(k,10)*(1-F(k,10)) for k in range(11)), "sevenths max", max(F(k,7)*(1-F(k,7)) for k in range(8)), "argmax first", min((F(k,7) for k in range(8) if F(k,7)*(1-F(k,7)) == max(F(j,7)*(1-F(j,7)) for j in range(8))))) 
print("pairs", len([(i,j) for i in range(10) for j in range(i+1,10)]))
