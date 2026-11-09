"""Check the reference.py docstring claim: an implementation that keeps the draw order reproduces Lab 3's printed digits.
Usage: docstring_digits_r17.py <checkout root> ; runs reference and two round-17 alternatives on seed 0, prints 6-dp rows."""
import importlib.util, sys
root = sys.argv[1]
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load(f"{root}/course/modules/SC/SC1/grader/reference.py", "ref")
inst_mod = load(f"{root}/course/modules/SC/SC1/grader/instance.py", "inst")
alts = {
    "alt_r17_1": load(f"{root}/ledgers/SC1/scripts/SC1-d-r17/alternatives/alt_r17_1_erf_welford_stride.py", "a1"),
    "alt_r17_5": load(f"{root}/ledgers/SC1/scripts/SC1-d-r17/alternatives/alt_r17_5_cumsum_sd_split.py", "a5"),
}
i = inst_mod.make_instance(0)
for n in (1, 4, 16, 64, 256):
    p, se = ref.discrete_max_exceedance(i, n)
    line = f"n={n} ref est={p:.6f} se={se:.6f}"
    for name, m in alts.items():
        q, s2 = m.discrete_max_exceedance(i, n)
        line += f" | {name} est={q:.6f} se={s2:.6f} same6dp={(f'{q:.6f}', f'{s2:.6f}') == (f'{p:.6f}', f'{se:.6f}')}"
    print(line)
