"""Round 19 PC3-b: Problem P3 and Proposition 3.3 bounds, run on the page's pseudocode order (while-loop, append, expiry, output)."""
from collections import deque


def run(xs, k):
    dq: deque[int] = deque()
    tests = pushes = pops = 0
    outs = []
    for i in range(1, len(xs) + 1):
        while dq:
            tests += 1
            if xs[dq[-1] - 1] <= xs[i - 1]:
                dq.pop()
                pops += 1
            else:
                break
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:
            dq.popleft()
            pops += 1
        if i >= k:
            outs.append(xs[dq[0] - 1])
    return tests, pushes, pops, outs


bad_p3 = []
for n in range(1, 31):
    xs = list(range(1, n + 1))
    for k in range(1, n + 1):
        tests, *_ = run(xs, k)
        if tests != n - 1:
            bad_p3.append((n, k, tests))
print("P3 strictly increasing: n-1 tests for all 1<=n<=30, 1<=k<=n:", not bad_p3, bad_p3[:5])
viol = []
import random  # noqa: E402

rng = random.Random(19)
for trial in range(2000):
    n = rng.randint(1, 40)
    k = rng.randint(1, n)
    xs = [rng.randint(0, 9) for _ in range(n)]
    tests, pushes, pops, outs = run(xs, k)
    ref = [max(xs[i - k:i]) for i in range(k, n + 1)]
    if outs != ref or tests > 2 * n or pushes != n or pops > n:
        viol.append((xs, k))
print("random trials: outputs equal max, comparisons <= 2n, pushes = n, pops <= n:", not viol, len(viol))
print("Remark 3.4 example k=1..6: removals in step k+1 =", [run(list(range(k, 0, -1)) + [k + 1], k)[2] - run(list(range(k, 0, -1)), k)[2] for k in range(1, 7)])
