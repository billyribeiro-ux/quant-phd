# Real-valued check (payment normalised to 1): does pattern F expense equal the payment in some year t for some n, r?
def ann(r, k):
    return k if r == 0 else (1 - (1 + r) ** -k) / r
found = []
for n in range(2, 8):
    for i in range(1, 20001):
        r = i / 100000  # 0.00001 .. 0.2
        L0 = ann(r, n)
        for t in range(1, n + 1):
            Lprev = ann(r, n - t + 1)          # opening liability of year t, per unit payment
            ef = r * Lprev + L0 / n            # interest + straight-line amortization
            if abs(ef - 1) < 1e-9:
                found.append((n, r, t, ef))
print(len(found), found[:10])
# sign change scan of ef - 1 across r for each n,t
for n in range(2, 8):
    for t in range(1, n + 1):
        prev = None
        for i in range(1, 20001):
            r = i / 100000
            g = (r * ann(r, n - t + 1) + ann(r, n) / n) - 1
            if prev is not None and (g > 0) != (prev > 0):
                print("sign change n", n, "t", t, "near r", r)
            prev = g
