"""Verifier r5: does the step-major alternative (alt7) give numbers different from Lab 3's draw order? Seed 0, grids 1, 4, 16."""
import importlib.util
from pathlib import Path
G = Path("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-d/course/modules/SC/SC1/grader")
ALT = Path("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-d/ledgers/SC1/scripts/SC1-d-r5/alternatives/alt7_gauss_step_major.py")
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
inst_mod = load(G / "instance.py", "instance")
ref = load(G / "reference.py", "ref")
alt = load(ALT, "alt7")
inst = inst_mod.make_instance(0)
for g in (1, 4, 16):
    print("grid", g, "reference", ref.discrete_max_exceedance(inst, g), "alt7", alt.discrete_max_exceedance(inst, g))
