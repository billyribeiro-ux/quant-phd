"""Compare make_instance output of the round-2 pin (c737272f) and the current pin for seeds 0..999 (code, not docstring)."""
import importlib.util
import sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

old = load(sys.argv[1], "instance_old")
new = load(sys.argv[2], "instance_new")
diff = [s for s in range(1000) if old.make_instance(s) != new.make_instance(s)]
print("seeds 0..999 with different make_instance output:", len(diff), diff[:10])
