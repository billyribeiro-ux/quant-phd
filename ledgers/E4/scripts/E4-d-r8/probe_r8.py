"""Probe the reference and the round-8 mutant on finite inputs the page calls valid (verifier scratch)."""
import sys
sys.path.insert(0, sys.argv[1])
import importlib
ref = importlib.import_module(sys.argv[2])
def t(sd, c):
    try:
        o = ref.solve_model(sd, c)
        return "ok " + repr(o)
    except Exception as e:
        return f"EXC {type(e).__name__}: {e}"
for sd, c in [(1e-30, 0.13), (1e-40, 0.13), (0.6, 354.0), (0.6, 355.0), (0.6, 1000.0), (1e153, 0.13), (1e154, 0.13), (1e200, 0.13), (1000.0, 0.13), (0.6, 50.0)]:
    print(f"sd={sd!r} cost={c!r} ->", t(sd, c))
