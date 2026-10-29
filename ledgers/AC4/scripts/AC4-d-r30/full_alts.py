import pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
L07 = (root / "tests/labs/AC4/lab-AC4-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/AC4/lab-AC4-L08-1.py").read_text(encoding="utf-8")
base = {"L07": subprocess.run([sys.executable, "-I", "-W", "error", "-c", L07], capture_output=True, text=True).stdout,
        "L08": subprocess.run([sys.executable, "-I", "-W", "error", "-c", L08], capture_output=True, text=True).stdout}
cases = {
 "L07 displaced min form": ("L07", "return max(0, c.q + c.external - c.capacity)", "return c.external - min(c.external, c.capacity - c.q)"),
 "L07 nonempty via surplus sign": ("L07", "return t_min(c) <= t_max(c)", "return firm_surplus(c) >= 0"),
 "L08 RI via integer scaling": ("L08", "return Fraction(d.oi) - Fraction(RATE_BP, 10_000) * d.invested", "return Fraction(d.oi * 10_000 - RATE_BP * d.invested, 10_000)"),
 "L08 EVA via NOPAT then charge": ("L08", "nopat = Fraction(d.oi) * (10_000 - TAX_BP) / 10_000", "nopat = Fraction(d.oi * (10_000 - TAX_BP), 10_000)"),
 "L07 midpoint via lower end plus half width": ("L07", "return (t_min(c) + t_max(c)) / 2", "return t_min(c) + (t_max(c) - t_min(c)) / 2"),
}
for name, (k, old, new) in cases.items():
    src = L07 if k == "L07" else L08
    assert src.count(old) == 1, (name, src.count(old))
    out = subprocess.run([sys.executable, "-I", "-W", "error", "-c", src.replace(old, new)], capture_output=True, text=True)
    print(f"{name}: exit={out.returncode} {'SAME-AS-TWIN' if out.stdout == base[k] else 'DIFFERENT'}")
    if out.returncode: print(out.stderr.strip().splitlines()[-1])
