import importlib.util, sys
def load(p, name):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s)
    sys.modules[name] = m; s.loader.exec_module(m); return m
ref = load("/tmp/verify8-M1-d/course/modules/M/M1/grader/reference.py", "ref")
mut = load("/tmp/verify8-M1-d/ledgers/M1/mutants/m48_small_rate_cutoff_loan_over_months.py", "mut")
found = None
for L in (10**8, 10**9, 25*10**6, 3*10**8):
    for rate in (1e-7, 5e-8, 1e-8, 5e-7):
        for n in (12, 120, 240, 360):
            a = ref.level_payment_cents(L, rate, n); b = mut.level_payment_cents(L, rate, n)
            if a != b:
                found = (L, rate, n, a, b); break
        if found: break
    if found: break
print("m48 witness (principal, annual_rate, months, reference, mutant):", found)
