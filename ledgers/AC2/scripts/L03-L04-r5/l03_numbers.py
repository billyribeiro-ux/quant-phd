# Round-5 verifier: load the L03 twin's functions without running main(), print unrounded invested capital and E3 growth.
import sys, runpy, types
src = open(sys.argv[1], encoding="utf-8").read()
assert src.rstrip().endswith("main()")
src = src.rstrip()[: -len("main()")]
mod = types.ModuleType("twin"); sys.modules["twin"] = mod
exec(compile(src, "twin", "exec"), mod.__dict__)
st = mod.standardize(mod.make_filer())
ends = list(st)
ic = {e: mod.invested_capital(st, e) for e in ends if "long_term_debt" in st[e]}
for e in ends:
    print(e, "IC", ic.get(e), "OI", st[e].get("operating_income"), "NI", st[e].get("net_income"), "equity", st[e].get("equity"), "ltd", st[e].get("long_term_debt"), "cash", st[e].get("cash"))
print("ends", ends)
ks = ["2021-12-31", "2022-12-31", "2023-12-31", "2024-12-31"]
for a, b in zip(ks, ks[1:]):
    if a in ic and b in ic:
        print(f"growth {a}->{b}: {ic[b]/ic[a]-1:.6%}  ({ic[b]/ic[a]-1:.4%})")
print("printed-value growth 2022->2023 (906.9->993.5):", f"{993.5/906.9-1:.6%}")
print("printed-value growth 2023->2024 (993.5->1083.1):", f"{1083.1/993.5-1:.6%}")
print("printed-value growth 2024->2025 (1083.1->1153.8):", f"{1153.8/1083.1-1:.6%}")
