"""Round-10 verifier (E3-d): three new student-error mutants of the reference elicit.py (each a full module)."""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d")
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
_f = REF.index(chr(34) * 3); REF = REF[REF.index(chr(34) * 3, _f + 3) + 3:].lstrip(chr(10))
DEST = ROOT / "ledgers/E3/mutants"

MUTANTS = {
    "d10_01_identification_reads_only_the_b_lotteries.py": (
        "Loss-aversion identification counts a mixed lottery only on the B side of each question, so a set whose only mixed lottery is A is refused.",
        ('    if not any(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):',
         '    if not any(_mixed(b, pb) for a, pa, b, pb, _ in parsed):'),
    ),
    "d10_02_likelihood_uses_crra_certainty_equivalents.py": (
        "The logit likelihood takes its certainty equivalents from the CRRA model at the current gamma (wealth fixed at 1000 dollars) instead of the prospect value.",
        ('        ce_a = _prospect_ce(prizes_a, probs_a, gamma, lam)\n        ce_b = _prospect_ce(prizes_b, probs_b, gamma, lam)',
         '        ce_a = _crra_change(prizes_a, probs_a, gamma, 100_000)\n        ce_b = _crra_change(prizes_b, probs_b, gamma, 100_000)'),
    ),
    "d10_03_estimate_drops_the_pure_responses_first.py": (
        "The estimator discards every response whose two lotteries are both pure before maximising, so the likelihood uses only the mixed questions.",
        ('    xi = _maximise(parsed)\n',
         '    parsed = [p for p in parsed if _mixed(p[0], p[1]) or _mixed(p[2], p[3])]\n    xi = _maximise(parsed)\n'),
    ),
}

for name, (doc, (old, new)) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new, 1)
    text = f'"""{doc}"""\n' + text
    (DEST / name).write_text(text, encoding="utf-8")
    print("wrote", DEST / name)
