"""Independent checks for L05 (own code; stdlib only; does not import lab code).

Checks: Definition 3.1 survivors vs the deque after every step (Proposition 3.2 invariant) on random
sequences; outputs vs brute force; while-loop test counts <= 2n (Proposition 3.3); removals <= n;
increasing sequences give n-1 tests for every k (Problem P3); Remark 3.4 single-step removal of k entries;
Example 3.5 and Problem M2 traces; Problem M3 (k=1 and k=n); Remark 2.2 peak; numbers in Problem E1, E3, P1.
Usage: python -I l05_indep.py
"""
import random
from collections import deque

def run(xs, k):
    """Deque method as the page's pseudocode; returns outputs, while-loop tests, back removals, front removals, states."""
    dq = deque()
    out, tests, back_rem, front_rem, states = [], 0, 0, 0, []
    n = len(xs)
    for i in range(1, n + 1):
        x = xs[i - 1]
        while dq:
            tests += 1
            if xs[dq[-1] - 1] <= x:
                dq.pop()
                back_rem += 1
            else:
                break
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
            front_rem += 1
        if i >= k:
            out.append(xs[dq[0] - 1])
        states.append(list(dq))
    return out, tests, back_rem, front_rem, states

def survivors(xs, i, k):
    return [j for j in range(max(1, i - k + 1), i + 1)
            if all(xs[j - 1] > xs[m - 1] for m in range(j + 1, i + 1))]

def brute_outputs(xs, k):
    return [max(xs[i - k:i]) for i in range(k, len(xs) + 1)]

rng = random.Random(12345)
bad_inv = bad_out = bad_bound = bad_rem = 0
trials = 0
for trial in range(3000):
    n = rng.randint(1, 25)
    xs = [rng.randint(0, 9) for _ in range(n)]
    k = rng.randint(1, n)
    out, tests, br, fr, states = run(xs, k)
    trials += 1
    for i in range(1, n + 1):
        if states[i - 1] != survivors(xs, i, k):
            bad_inv += 1
            break
    if out != brute_outputs(xs, k):
        bad_out += 1
    if tests > 2 * n:
        bad_bound += 1
    if br + fr > n or br > n:
        bad_rem += 1
print("random trials", trials, "invariant failures", bad_inv, "output failures", bad_out,
      "2n bound failures", bad_bound, "removal failures", bad_rem)

# Problem P3 and Proposition 3.3 on increasing sequences
ok_p3 = True
for n in range(1, 30):
    xs = list(range(1, n + 1))
    for k in range(1, n + 1):
        out, tests, *_ = run(xs, k)
        if tests != n - 1:
            ok_p3 = False
print("increasing sequences: tests == n-1 for all n<30, k<=n:", ok_p3)

# Remark 3.4: x = (k, k-1, ..., 1, k+1), n = k+1: step k+1 removes k entries in one loop
ok34 = True
for k in range(1, 12):
    xs = list(range(k, 0, -1)) + [k + 1]
    out, tests, br, fr, states = run(xs, k)
    before = states[k - 1]  # deque after step k
    ok34 = ok34 and before == list(range(1, k + 1)) and br == k and sum(1 for _ in before) == k
print("Remark 3.4 example: after step k deque is 1..k, step k+1 removes k back entries:", ok34)

# Example 3.5
xs = [3, 1, 4, 1, 5]
out, tests, br, fr, states = run(xs, 3)
print("Example 3.5 outputs", out, "states", states)
# Problem M2
xs = [2, 5, 1, 0, 3]
out, tests, br, fr, states = run(xs, 2)
print("Problem M2 outputs", out, "states", states)
# Problem M3 k=1 and k=n
xs = [4, 2, 7, 1, 9]
print("M3 k=1 outputs == input:", run(xs, 1)[0] == xs, "k=n outputs", run(xs, len(xs))[0], "== max:", run(xs, len(xs))[0] == [max(xs)])

# Problem P1 and Remark 2.2
for n in (10, 11, 200):
    best = max(range(1, n + 1), key=lambda k: (n - k + 1) * (k - 1))
    print("n", n, "maximising k", best, "count", (n - best + 1) * (best - 1), "n^2/4", n * n / 4)
print("E1: 169*31 =", 169 * 31, " ratio 5239/382 =", round(5239 / 382, 4))
print("E3: 2n =", 400, " 194+200 =", 194 + 200)
print("E2: 193*7 =", 193 * 7)

# Printed seed 5 and seed 6 counts, window 8 and 32, and 200 (own run)
def seq(seed, n=200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]
for seed in (5, 6):
    xs = seq(seed)
    for k in (8, 32, 200):
        out, tests, br, fr, _ = run(xs, k)
        print(f"seed {seed} k {k}: outputs equal brute {out == brute_outputs(xs, k)} tests {tests} pushes 200 pops {br + fr}")
# Part 2 equality for k 1..20 on seed 5
xs = seq(5)
print("seed 5 k 1..20 equal:", all(run(xs, k)[0] == brute_outputs(xs, k) for k in range(1, 21)))
print("seed 5 first five values", xs[:5], "first five maxima k=8", run(xs, 8)[0][:5], "max", max(xs))
