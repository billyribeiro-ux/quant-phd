"""Probe the float alternative (alt A) on the gamma = 1e-6 boundary case (verifier helper, round 10).

Run: python ledgers/M7/scripts/M7-d-r10/gamma_probe_r10.py <alt file>. Prints the reference and alt residuals.
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
    alt = load("alt_m7", Path(sys.argv[1]).resolve())
    ref = load("reference_m7", GRADER / "reference.py")
    inst = load("instance_m7", GRADER / "instance.py")
    case = json.loads(inst.make_instance(0)["payload"])  # type: ignore[attr-defined]
    case["gamma"] = 0.000001
    for name, mod in (("reference", ref), ("alt", alt)):
        try:
            out = mod.allocate(json.loads(json.dumps(case)))  # type: ignore[attr-defined]
            print(name, "weights", [f"{x:.12f}" for x in out["weights"]])
            print(name, "certificate", {k: f"{v:.3e}" for k, v in out["certificate"].items()})
            print(name, "multipliers lower", [f"{x:.3e}" for x in out["multipliers"]["lower"]],
                  "upper", [f"{x:.3e}" for x in out["multipliers"]["upper"]],
                  "turnover_total", f"{out['multipliers']['turnover_total']:.3e}")
        except Exception as exc:  # noqa: BLE001 - probe prints the refusal
            print(name, "raised", type(exc).__name__, str(exc)[:120])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
