"""Alternative 5 (wording probe): the reference arithmetic, with explanations worded 'Short the call' and 'Parity:'/'Convexity:'."""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

_REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-FC2-d/course/modules/FC/FC2/grader/reference.py")
_spec = importlib.util.spec_from_file_location("_ref_for_probe", _REF)
assert _spec is not None and _spec.loader is not None
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)

parity_gap_cents = _ref.parity_gap_cents
convexity_violations = _ref.convexity_violations


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    rows = _ref.scan(chain)
    for row in rows:
        if row["kind"] == "parity":
            short = "Short the call" if "sell the call" in row["explanation"] else "Long the call"
            row["explanation"] = (
                f"Parity: {short}, long the put and the underlying, financed at the discounted strike, under "
                f"P1, P2, P3, P4 and P6; net {row['net_cents']} cents."
            )
        else:
            row["explanation"] = (
                f"Convexity: the middle call is above its chord, under P1, P2, P5 and P6; net {row['net_cents']} cents."
            )
    return rows
