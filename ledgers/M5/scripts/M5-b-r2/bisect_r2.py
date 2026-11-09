from fractions import Fraction as F
N = 4096
vals = {n: F((n * n) % 1000, 1000) for n in range(1, N + 1)}
a, b = F(0), F(1)
last = 0
chosen = []
ivs = []
for step in range(1, 9):
    m = (a + b) / 2
    cand = [n for n in range(last + 1, N + 1) if a <= vals[n] <= b]
    left = [n for n in cand if vals[n] < m]
    right = [n for n in cand if vals[n] >= m]
    if len(left) >= len(right):
        b = m; pick = left
    else:
        a = m; pick = right
    idx = pick[0]
    last = idx
    chosen.append(idx); ivs.append((a, b))
    print(f"step {step} interval [{a}, {b}] width {b-a} chosen_index {idx}")
ok = all(ivs[j][0] <= vals[chosen[i]] <= ivs[j][1] for j in range(8) for i in range(j, 8))
print("tail_values_in_their_interval", ok)
print("subsequence_indices", " ".join(map(str, chosen)))
