import importlib.util, sys
spec = importlib.util.spec_from_file_location("twin3", sys.argv[1])
m = importlib.util.module_from_spec(spec); sys.modules["twin3"] = m; spec.loader.exec_module(m)
f = m.make_filer()
st = m.standardize(f)
ends = ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"]
ic = {e: m.invested_capital(st, e) for e in ends}
for e in ends: print("IC", e, repr(ic[e]))
g22 = ic["2022-12-31"]/ic["2021-12-31"]-1; g23 = ic["2023-12-31"]/ic["2022-12-31"]-1; g24 = ic["2024-12-31"]/ic["2023-12-31"]-1
print("growth 2022 %.4f%%  2023 %.4f%%  2024 %.4f%%" % (100*g22, 100*g23, 100*g24))
n23 = m.nopat(st, "2023-12-31", 0.25); n24 = m.nopat(st, "2024-12-31", 0.25)
avg23 = (ic["2022-12-31"]+ic["2023-12-31"])/2; avg24 = (ic["2023-12-31"]+ic["2024-12-31"])/2
r23 = n23/avg23; r24 = n24/avg24
print("NOPAT chg %.3f%%  avgIC chg %.3f%%  ROIC23 %.5f ROIC24 %.5f ROIC chg %.3f%%" % (100*(n24/n23-1), 100*(avg24/avg23-1), r23, r24, 100*(r24/r23-1)))
ic24cf = ic["2023-12-31"]*(1+g23); avgcf = (ic["2023-12-31"]+ic24cf)/2
print("counterfactual ROIC chg %.3f%%" % (100*((n24/avgcf)/r23-1)))
