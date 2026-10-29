import sys; sys.path.insert(0, "/tmp/fc2d-r7-alt7b")
import random, scanner, reference
r = random.Random(7)
bad = 0; n_find = 0
for _ in range(4000):
    n = r.randint(3, 8)
    ks = sorted(r.sample(range(1000, 20000), n))
    cs = [r.randint(0, 15000) for _ in ks]
    ps = [r.randint(0, 15000) for _ in ks]
    ch = {"strikes_cents": ks, "call_cents": cs, "put_cents": ps, "spot_cents": r.randint(1000, 20000),
          "df_ppm": r.randint(1, 1000000),
          "cost": {"fee_cents_per_contract": r.randint(0, 30), "half_spread_cents": r.randint(0, 30)}}
    a = scanner.scan(ch); b = reference.scan(ch)
    n_find += len(b)
    if a != b:
        bad += 1
print("chains compared 4000, findings in reference", n_find, "disagreements", bad)
