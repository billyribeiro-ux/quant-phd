"""Build the round-7 student-error mutants of reference.py, one edit each (each edit asserted to match once)."""
import pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE7-E4-d")
REF = (ROOT / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E4/mutants"
EDITS = [
    ("mutant_r7_01_reports_bracket_lower_end.py",
     "Reports the lower end of the final bracket as the informed fraction, not its midpoint (the page says midpoint).",
     "        lam = 0.5 * (low + high)\n",
     "        lam = low\n"),
    ("mutant_r7_02_rejects_noise_above_one.py",
     "Rejects a finite noise volume above 1 with the noise-volume message; the page names only non-positive or non-finite noise volumes.",
     "    if not (math.isfinite(sd) and sd > 0.0):\n",
     "    if not (math.isfinite(sd) and 0.0 < sd <= 1.0):\n"),
    ("mutant_r7_03_rejects_cost_above_one.py",
     "Rejects a finite information cost above 1 with the cost message; the page names only negative costs.",
     "    if not (math.isfinite(cost) and cost >= 0.0):\n",
     "    if not (math.isfinite(cost) and 0.0 <= cost <= 1.0):\n"),
]
for name, desc, old, new in EDITS:
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    doc_old = REF.split('"""', 2)[1]
    head = '"""' + desc + "\n\nVerifier mutant (E4 slice d, round 7). Built from reference.py by one edit.\n\n" + doc_old + '"""'
    text = head + body[len('"""' + doc_old + '"""'):]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
