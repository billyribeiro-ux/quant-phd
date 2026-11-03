import sys, importlib.util
from fractions import Fraction
G = sys.argv[1]
spec = importlib.util.spec_from_file_location("instance", f"{G}/instance.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
N = int(sys.argv[2])
strict_viol = []
accepted = 0
parity_resid_max = Fraction(0)
for seed in range(N):
    inst = m.make_instance(seed)
    accepted += 1
    S = inst["spot_cents"]; df = inst["df_ppm"]
    for K, C, P in zip(inst["strikes_cents"], inst["call_cents"], inst["put_cents"]):
        disc = Fraction(K * df, m.PPM)
        bad = []
        if C > S: bad.append("C<=S")
        if C < max(S - disc, 0): bad.append("C>=max(S-Kdf,0)")
        if P < 0: bad.append("P>=0")
        if P > disc: bad.append("P<=Kdf")
        if P < max(disc - S, 0): bad.append("P>=max(Kdf-S,0)")
        if bad:
            strict_viol.append((seed, K, C, P, bad))
    for K, C, P in zip(inst["strikes_cents"], inst["call_cents"], inst["put_cents"]):
        g = Fraction(C) - Fraction(P) - (Fraction(S) - Fraction(K * df, m.PPM))
        parity_resid_max = max(parity_resid_max, abs(g))
print("instances accepted:", accepted, "of seeds 0..", N - 1)
print("strict Theorem 2.2 bound violations in accepted chains:", len(strict_viol))
for v in strict_viol[:10]:
    print("  seed", v[0], "strike", v[1], "call", v[2], "put", v[3], v[4])
print("max |parity residual| (cents):", float(parity_resid_max))
