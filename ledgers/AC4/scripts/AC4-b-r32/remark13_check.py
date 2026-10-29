import pathlib, sys, types
src = pathlib.Path("/tmp/verify32-AC4-b/tests/labs/AC4/lab-AC4-L04-1.py").read_text(encoding="utf-8")
lines = src.rstrip("\n").split("\n")
assert lines[-1] == "main()", lines[-1]
mod = types.ModuleType("lab_twin_no_main")
sys.modules[mod.__name__] = mod
exec(compile("\n".join(lines[:-1]), mod.__name__, "exec"), mod.__dict__)
try:
    mod.exact_rate(10_000_001, 10_000, "pool")
    print("uneven division: NO error raised")
except ValueError as e:
    print("uneven division raises ValueError:", e)
print("exact division returns", mod.exact_rate(10_000_000, 10_000, "pool"))
