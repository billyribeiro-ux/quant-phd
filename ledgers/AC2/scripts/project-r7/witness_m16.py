"""Witness: two period ends inside the 350-380 day window; reference picks the latest, m16 the earliest."""
import importlib.util, sys
from pathlib import Path
REF = Path("/tmp/verify-ac2r7-p/course/modules/AC/AC2/grader/reference.py")
M16 = Path("/tmp/verify-ac2r7-p/ledgers/AC2/mutants/m16_previous_year_is_earliest_in_window.py")
def load(name, p):
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
ref, m16 = load("ref", REF), load("m16", M16)
st = {
  "2020-12-31": {"total_assets": 100.0, "net_income": 10.0, "revenue": 200.0},
  "2019-12-28": {"total_assets": 90.0},
  "2020-01-02": {"total_assets": 95.0},
}
print("ref  _previous:", ref._previous(st, "2020-12-31"))
print("m16  _previous:", m16._previous(st, "2020-12-31"))
