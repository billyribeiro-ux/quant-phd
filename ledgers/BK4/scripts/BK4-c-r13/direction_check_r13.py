"""Round-13 BK4-c: numeric check of the directional limit claims on project.html (rule 7 of VERIFIER_RULES 2.9/9).

Claim 1: adding loss to every scenario (a second default, or losses grown in a close-out) never lowers the sized margin
and never raises the cover at a fixed margin. Claim 2 (stress): a margin that rose in stress raises the real cover above
the simulated one at the simulated margin; one that fell lowers it.
Run: python3 -I ledgers/BK4/scripts/BK4-c-r13/direction_check_r13.py
"""

import random

rng = random.Random(13)
bad = 0
trials = 0
for _ in range(3000):
    S = rng.randint(40, 80)
    base = [rng.randint(0, 150_000) for _ in range(S)]
    add = [rng.randint(0, 40_000) for _ in range(S)]
    grown = [a + b for a, b in zip(base, add)]
    for target in (9000, 9500, 9750, 10000):
        k = -((-target * S) // 10_000)
        m0 = sorted(base)[k - 1]
        m1 = sorted(grown)[k - 1]
        trials += 1
        if not m1 >= m0:
            bad += 1
    for margin in (rng.randint(0, 150_000) for _ in range(3)):
        c0 = 10_000 * sum(1 for x in base if x <= margin) // S
        c1 = 10_000 * sum(1 for x in grown if x <= margin) // S
        trials += 1
        if not c1 <= c0:
            bad += 1
print("claim 1 (losses grow): trials", trials, "violations", bad)
assert bad == 0

# Claim 2: stress direction. Simulated cover uses a fixed margin M; the real margin is M + delta (delta may be < 0).
bad2 = 0
for _ in range(3000):
    S = rng.randint(40, 80)
    losses = [rng.randint(0, 150_000) for _ in range(S)]
    M = rng.randint(0, 150_000)
    delta = rng.randint(-20_000, 20_000)
    sim = 10_000 * sum(1 for x in losses if x <= M) // S
    real = 10_000 * sum(1 for x in losses if x <= M + delta) // S
    if delta > 0 and not real >= sim:
        bad2 += 1
    if delta < 0 and not real <= sim:
        bad2 += 1
print("claim 2 (margins move in stress): violations", bad2)
assert bad2 == 0
print("DIRECTION CHECKS PASSED")
