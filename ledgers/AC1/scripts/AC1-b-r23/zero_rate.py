import sys, types
src = open("/tmp/verify23-AC1-b/tests/labs/AC1/lab-AC1-L06-1.py").read().replace("\nmain()\n", "\n")
mod = types.ModuleType("L6"); sys.modules["L6"] = mod
exec(compile(src, "lab", "exec"), mod.__dict__)
L = mod.Lease(term_years=7, payment_cents=13034272, rate_bps=0)
init = mod.present_value_cents(L)
years, adj = mod.roll_forward(L, init)
print("rate_bps 0: initial", init, "adjustment", adj)
for t, y in enumerate(years, 1):
    print(t, "payment", y.payment, "expense_F", y.interest + y.amortization)
