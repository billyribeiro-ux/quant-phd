"""Diagnose float alternatives on the gamma boundary: run allocate on the seed case with gamma set, print outcome."""
import importlib.util, json, sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve()
ALT = Path(sys.argv[2]).resolve()
GAMMA = float(sys.argv[3])
SEED = int(sys.argv[4])
sys.path.insert(0, str(ROOT / "course/modules/M/M7/grader"))
spec_i = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/M/M7/grader/instance.py")
inst = importlib.util.module_from_spec(spec_i); sys.modules["instance"] = inst; spec_i.loader.exec_module(inst)
spec = importlib.util.spec_from_file_location("alt", ALT)
alt = importlib.util.module_from_spec(spec); sys.modules["alt"] = alt; spec.loader.exec_module(alt)
case = json.loads(inst.make_instance(SEED)["payload"])
case["gamma"] = GAMMA
try:
    out = alt.allocate(case)
    print("certificate:", out["certificate"])
    print("weights:", out["weights"])
except Exception as exc:
    print("RAISED", type(exc).__name__, str(exc)[:200])
