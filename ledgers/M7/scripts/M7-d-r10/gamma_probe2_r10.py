"""Probe a float alternative at gamma 1e-9 (verifier helper, round 10): prints refusal or the KKT residuals it reaches.

Run: python ledgers/M7/scripts/M7-d-r10/gamma_probe2_r10.py <alt file> [gamma]
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M7/grader"


def load(name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    alt = load("alt_m7b", Path(sys.argv[1]).resolve())
    inst = load("instance_m7b", GRADER / "instance.py")
    gamma = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9
    case = json.loads(inst.make_instance(0)["payload"])  # type: ignore[attr-defined]
    case["gamma"] = gamma
    try:
        out = alt.allocate(json.loads(json.dumps(case)))  # type: ignore[attr-defined]
    except Exception as exc:  # noqa: BLE001 - probe reports the refusal
        print("raised", type(exc).__name__, str(exc)[:120])
        return 0
    print("weights", [f"{x:.10f}" for x in out["weights"]])
    print("certificate", {k: f"{v:.3e}" for k, v in out["certificate"].items()})
    print("budget", f"{out['multipliers']['budget']:.6e}", "lower", [f"{x:.3e}" for x in out["multipliers"]["lower"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
