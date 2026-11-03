"""Writes four round-3 student-error mutants (single-change copies of the reference) into ledgers/E3/mutants/."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
REF = ROOT / "course/modules/E/E3/grader/reference.py"
OUT = ROOT / "ledgers/E3/mutants"
ref = REF.read_text(encoding="utf-8")

def make(name, doc, old, new, count=1):
    assert ref.count(old) == count, (name, ref.count(old))
    text = ref.replace(old, new)
    head, _, rest = text.partition('"""')
    _, _, body = rest.partition('"""')
    out = '"""%s\n\nSingle-change copy of the reference solution (verifier E3-d, round 3).\n"""%s' % (doc, body)
    (OUT / name).write_text(out, encoding="utf-8")
    print("wrote", name)

make("e3d3v_01_crra_inverse_divides_expected_utility_by_one_minus_gamma.py",
     "CRRA certainty equivalent divides the expected utility by (1 - gamma) before the inverse power, applying the factor twice.",
     "    expected = sum(float(p) * w ** (1.0 - gamma) for p, w in zip(probs, finals, strict=True))\n    return math.pow(expected, 1.0 / (1.0 - gamma)) - wealth",
     "    expected = sum(float(p) * w ** (1.0 - gamma) for p, w in zip(probs, finals, strict=True))\n    return math.pow(expected / (1.0 - gamma), 1.0 / (1.0 - gamma)) - wealth")

make("e3d3v_02_log_likelihood_reads_kappa_from_the_lambda_key.py",
     "log_likelihood reads the choice precision from the lambda key of params, a key-name slip, so kappa is set to lambda.",
     '    kappa = float(params["kappa"])\n    _check_prospect(gamma, lam)',
     '    kappa = float(params["lambda"])\n    _check_prospect(gamma, lam)')

make("e3d3v_03_estimate_trusts_the_probabilities_it_reads.py",
     "estimate reads each response without checking that its probabilities are non-negative and sum to exactly 1 (log_likelihood still checks).",
     "    parsed = [_parse(r) for r in responses]\n    if not any(",
     "    parsed = [_parse_trusting(r) for r in responses]\n    if not any(")
# add the trusting parser before estimate
p = OUT / "e3d3v_03_estimate_trusts_the_probabilities_it_reads.py"
t = p.read_text(encoding="utf-8")
helper = '''def _parse_trusting(response: Mapping[str, Any]) -> Parsed:
    prizes_a = _check_prizes(response["prizes_a"])
    probs_a = [Fraction(str(s)) for s in response["probs_a"]]
    prizes_b = _check_prizes(response["prizes_b"])
    probs_b = [Fraction(str(s)) for s in response["probs_b"]]
    return prizes_a, probs_a, prizes_b, probs_b, str(response["choice"])


def estimate('''
assert t.count("def estimate(") == 1
p.write_text(t.replace("def estimate(", helper, 1), encoding="utf-8")
print("patched helper")

make("e3d3v_04_hessian_cross_terms_by_forward_differences.py",
     "Observed information cross terms use forward differences (one-sided, step 1e-5) instead of central differences; the diagonal stays central.",
     "            value = (\n                f(shifted((i, _H), (j, _H)))\n                - f(shifted((i, _H), (j, -_H)))\n                - f(shifted((i, -_H), (j, _H)))\n                + f(shifted((i, -_H), (j, -_H)))\n            ) / (4.0 * _H * _H)",
     "            value = (\n                f(shifted((i, _H), (j, _H)))\n                - f(shifted((i, _H), (j, 0.0)))\n                - f(shifted((i, 0.0), (j, _H)))\n                + f(shifted((i, 0.0), (j, 0.0)))\n            ) / (_H * _H)")
