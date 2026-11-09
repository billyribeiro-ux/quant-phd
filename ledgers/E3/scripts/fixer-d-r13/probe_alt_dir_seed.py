"""Probe: one alternative directory's estimate on a seed's own participant (exception or fit summary)."""
import json
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
sys.path.insert(0, str(Path(sys.argv[1])))
sys.path.insert(1, str(ROOT / "course/modules/E/E3/grader"))
import elicit as sol  # noqa: E402
from instance import make_instance  # noqa: E402

seed = int(sys.argv[2])
resp = json.loads(str(make_instance(seed)["responses_json"]))
try:
    fit = sol.estimate(resp)
    print("ok", {k: round(v, 5) for k, v in fit.items()})
except Exception as err:  # noqa: BLE001
    print("raised", type(err).__name__, str(err)[:160])
