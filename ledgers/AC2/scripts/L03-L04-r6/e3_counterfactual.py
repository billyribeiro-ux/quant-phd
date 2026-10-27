# Recompute the L03 E3 figures from the twin's own functions (unrounded), independent of the page text.
import sys
src = open(sys.argv[1], encoding="utf-8").read()
import types
mod = types.ModuleType("twin"); sys.modules["twin"] = mod; ns = mod.__dict__
exec(compile(src.split("\ndef main")[0], sys.argv[1], "exec"), ns)
st = ns["standardize"](ns["make_filer"]())
ends = ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"]
ic = {e: ns["invested_capital"](st, e) for e in ends}
for e in ends:
    print("IC", e, round(ic[e], 6))
g = {}
for a, b in zip(ends, ends[1:]):
    g[b] = ic[b] / ic[a] - 1
    print("growth", b, f"{g[b]*100:.4f}%")
t = 0.25
nopat23 = ns["nopat"](st, "2023-12-31", t)
nopat24 = ns["nopat"](st, "2024-12-31", t)
avg23 = (ic["2022-12-31"] + ic["2023-12-31"]) / 2
avg24 = (ic["2023-12-31"] + ic["2024-12-31"]) / 2
r23 = nopat23 / avg23; r24 = nopat24 / avg24
print("ROIC23", round(r23, 6), "ROIC24", round(r24, 6), "fall", f"{(r24/r23-1)*100:.4f}%")
print("NOPAT change", f"{(nopat24/nopat23-1)*100:.4f}%", "avgIC23", round(avg23, 4), "avgIC24", round(avg24, 4), "avg change", f"{(avg24/avg23-1)*100:.4f}%")
# counterfactual: IC grows at the 2023 rate (growth into 2023 = g['2023-12-31']) from 2023 year-end
gr = g["2023-12-31"]
print("2023 growth rate", f"{gr*100:.4f}%")
ic24_cf = ic["2023-12-31"] * (1 + gr)
avg24_cf = (ic["2023-12-31"] + ic24_cf) / 2
r24_cf = nopat24 / avg24_cf
print("CF avg24", round(avg24_cf, 4), "CF ROIC24", round(r24_cf, 6), "CF fall vs 2023", f"{(r24_cf/r23-1)*100:.4f}%")
print("flat-capital fall", f"{(nopat24/nopat23-1)*100:.4f}%")
# also: growth 2023 vs 2022 via printed values
print("printed-value growth 2022", f"{(993.5/906.9-1)*100:.2f}%")
