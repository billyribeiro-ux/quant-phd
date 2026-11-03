"""Round-3 verifier h3: builds three variants of the M4 reference in a scratch dir (not in the mutant ledger).

  signt_student_sign_flipped  Student-t loss sign flipped only (the page's 'What the suite does not test' item)
  signt_gaussian_sign_flipped Gaussian loss sign flipped (must be killed: the page grades the Gaussian sign)
  m17_student_normals_seed_plus_one  Student-t normals from Random(seed + 1) (the equivalence candidate)
"""
from __future__ import annotations

import sys
from pathlib import Path

ref = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
old_loss = "        losses.append(round(-total))\n"
old_z = "        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n"
old_rng = "    rng = random.Random(seed)\n"
assert ref.count(old_loss) == 1 and ref.count(old_z) == 1 and ref.count(old_rng) == 1
(out / "signt_student_sign_flipped.py").write_text(
    ref.replace(old_loss, "        losses.append(round(total if student else -total))\n"), encoding="utf-8")
(out / "signt_gaussian_sign_flipped.py").write_text(
    ref.replace(old_loss, "        losses.append(round(total))\n"), encoding="utf-8")
m17 = ref.replace(old_rng, "    rng = random.Random(seed)\n    rng_t = random.Random(seed + 1)\n", 1)
m17 = m17.replace(old_z, "        z = [(rng_t if student else rng).gauss(0.0, 1.0) for _ in range(n)]\n", 1)
(out / "m17_student_normals_seed_plus_one.py").write_text(m17, encoding="utf-8")
print("ok")
