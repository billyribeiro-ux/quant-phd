"""Rebuild the four half-cent equivalents from the CURRENT reference by swapping only the body of _half_up."""
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
REF = ROOT / "course/modules/E/E3/grader/reference.py"
EQ = ROOT / "ledgers/E3/equivalent"
BLOCK = re.compile(r"def _half_up\(y: float\) -> int:\n.*?(?=\n\n\ndef )", re.S)

ref = REF.read_text(encoding="utf-8")
assert len(BLOCK.findall(ref)) == 1
for name in ("f05_half_cent_goes_toward_minus_infinity.py", "m06_half_cent_rounded_to_even.py",
             "r13n01_half_cent_rounded_half_to_even.py", "w05_half_cent_away_from_zero.py"):
    old = (EQ / name).read_text(encoding="utf-8")
    old_block = BLOCK.findall(old)
    assert len(old_block) == 1, name
    new = BLOCK.sub(lambda _m: old_block[0], ref, count=1)
    (EQ / name).write_text(new, encoding="utf-8")
    print("rebuilt", name, "| differs from reference only in _half_up:", new.replace(old_block[0], BLOCK.findall(ref)[0]) == ref)
