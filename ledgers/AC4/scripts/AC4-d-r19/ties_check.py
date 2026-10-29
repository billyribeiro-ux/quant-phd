"""Count tie pairs (RI equal or OI/C equal) among the 8 seed-20261027 divisions; check the C column is all distinct."""

import sys
from pathlib import Path

root = Path(sys.argv[1])
import types

src = (root / "tests/labs/AC4/lab-AC4-L08-1.py").read_text(encoding="utf-8").rsplit("\nmain()", 1)[0]
mod = types.ModuleType("l08")
sys.modules["l08"] = mod
exec(compile(src, "l08", "exec"), mod.__dict__)
divs = mod.generate(mod.SEED, mod.N_DIVISIONS)
ties = 0
for i, a in enumerate(divs):
    for b in divs[i + 1 :]:
        if mod.residual_income(a) == mod.residual_income(b) or mod.return_ratio(a) == mod.return_ratio(b):
            ties += 1
print("tie pairs (equal RI or equal OI/C) among 28:", ties)
print("distinct C values:", len({d.invested for d in divs}), "of", len(divs))
print("self-pair RI and ratio differences are zero, so a<=b pairing adds no discordance: ",
      all(mod.residual_income(d) - mod.residual_income(d) == 0 for d in divs))
