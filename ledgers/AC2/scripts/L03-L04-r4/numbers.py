"""Round-4 independent recomputation of the L03 numbers from the lab's unrounded values."""
import sys
import types
from pathlib import Path

root = Path(sys.argv[1])
mod = types.ModuleType("lab_l03")
sys.modules["lab_l03"] = mod
ns = mod.__dict__
src = (root / "tests/labs/AC2/lab-AC2-L03-1.py").read_text(encoding="utf-8").rsplit("\nmain()", 1)[0]
exec(compile(src, "lab-AC2-L03-1-nomain", "exec"), ns)
st = ns["standardize"](ns["make_filer"]())
ends = list(st)  # 2020..2024
ic_ends = ends[1:]  # 2021..2024 (2020 long-term debt is absent)
oi = {e: st[e]["operating_income"] for e in ends}
ic = {e: ns["invested_capital"](st, e) for e in ic_ends}
print("OI 2021..2024 unrounded (USD m)", [round(oi[e] / 1e6, 4) for e in ic_ends])
print("OI ratio 2024/2023 unrounded", oi["2024-12-31"] / oi["2023-12-31"], "drop %", 100 * (1 - oi["2024-12-31"] / oi["2023-12-31"]))
print("IC unrounded (USD m)", {e: round(ic[e] / 1e6, 4) for e in ic_ends})
avg22 = (ic["2022-12-31"] + ic["2021-12-31"]) / 2
avg23 = (ic["2023-12-31"] + ic["2022-12-31"]) / 2
avg24 = (ic["2024-12-31"] + ic["2023-12-31"]) / 2
print("avg IC 2022, 2023, 2024 (USD m)", avg22 / 1e6, avg23 / 1e6, avg24 / 1e6)
nopat23 = oi["2023-12-31"] * 0.75
nopat24 = oi["2024-12-31"] * 0.75
print("NOPAT23", nopat23 / 1e6, "NOPAT24", nopat24 / 1e6)
r_avg23 = nopat23 / avg23
r_ye23 = nopat23 / ic["2023-12-31"]
print("ROIC23 on average", r_avg23, "on year-end", r_ye23)
print("gap % average vs year-end, unrounded", 100 * (r_avg23 / r_ye23 - 1))
print("gap % from printed 0.1349/0.1294", 100 * (0.1349 / 0.1294 - 1))
print("gap % from unrounded 0.134941/0.129360", 100 * (0.134941 / 0.129360 - 1))
print("Example 3.3 literal arithmetic 140.1/1083.1 =", 140.1 / 1083.1, "; 140.1/1038.3 =", 140.1 / 1038.3)
print("Example 3.3 unrounded NOPAT23/IC23 =", r_ye23, "rounded to 4dp:", round(r_ye23, 4))
r_c = ns["roic"](st, "2023-12-31", 0.25)
no_cash = {e: {**st[e], "cash": 0.0} for e in ends}
r_nc = ns["roic"](no_cash, "2023-12-31", 0.25)
print("ROIC23@25 netted", r_c, "not netted", r_nc, "netted vs not %", 100 * (r_c / r_nc - 1))
print("Remark 3.5 printed 0.1349/0.1239 %", 100 * (0.1349 / 0.1239 - 1))
r24_0 = ns["roic"](st, "2024-12-31", 0.0)
print("ROIC24 zero tax unrounded", r24_0, "printed 0.1299; tau for 10% =", 1 - 0.10 / r24_0, "; with printed 0.1299 =", 1 - 0.10 / 0.1299)
print("ROIC24@25 unrounded", ns["roic"](st, "2024-12-31", 0.25), "ROIC24@30", ns["roic"](st, "2024-12-31", 0.30))
print("ROIC23@30 unrounded", ns["roic"](st, "2023-12-31", 0.30))
print("E1 NOPAT change %", 100 * (nopat24 / nopat23 - 1), "avg IC change %", 100 * (avg24 / avg23 - 1))
print("E1 ROIC ratio exact", ns["roic"](st, "2024-12-31", 0.25) / ns["roic"](st, "2023-12-31", 0.25) - 1)
print("E1 (1-0.222)/(1+0.077)", (1 - 0.222) / (1 + 0.077), " printed-based 0.0974/0.1349-1", 0.0974 / 0.1349 - 1)
print("E3 growth 2022 %", 100 * (ic["2022-12-31"] / ic["2021-12-31"] - 1), "2023 %", 100 * (ic["2023-12-31"] / ic["2022-12-31"] - 1), "2024 %", 100 * (ic["2024-12-31"] / ic["2023-12-31"] - 1))
print("E3 printed 993.5/906.9 =", 993.5 / 906.9, " 1083.1/993.5 =", 1083.1 / 993.5, " 1153.8/1083.1 =", 1153.8 / 1083.1)
print("Remark 2.3 implied rate per year", [round(1 - st[e]["net_income"] / st[e]["operating_income"], 6) for e in ends])
print("M3 tau for 10% from 0.13:", 1 - 0.10 / 0.13)
cases = {"hyp_std": {e: ({**st[e], "long_term_debt": st[e]["long_term_debt"] + 50_000_000.0}) for e in ic_ends}}
print("hyp 50m STD ROIC23@25", ns["roic"](cases["hyp_std"], "2023-12-31", 0.25) if False else "see lab output")
