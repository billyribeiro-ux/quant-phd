"""Writes three verifier-authored student-error mutants (round 3, slice e) as single-change copies of the reference."""
import pathlib, sys
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD3-E3-e")
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

def module_doc_replace(src: str, new_doc: str) -> str:
    # the reference opens with a module docstring; replace only that first triple-quoted block
    start = src.index('"""')
    end = src.index('"""', start + 3) + 3
    return src[:start] + '"""' + new_doc + '"""' + src[end:]

def patch(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, (src.count(old), old[:80])
    return src.replace(old, new)

MUTANTS = {
    "e3e3_01_choice_probability_naive_logistic.py": (
        "Choice log-probability written as log of the logistic 1/(1+exp(-z)), which overflows for large negative z.",
        [(
            "        total += -_log1pexp(-z) if choice == \"A\" else -_log1pexp(z)\n",
            "        p_a = 1.0 / (1.0 + math.exp(-z))\n"
            "        total += math.log(p_a) if choice == \"A\" else math.log(1.0 - p_a)\n",
        )],
    ),
    "e3e3_02_estimates_rounded_to_four_decimals.py": (
        "The estimate fields are rounded to four decimals before they are returned, to match the printed output.",
        [(
            "    return {\n        \"gamma_hat\": gamma,\n        \"lambda_hat\": lam,\n        \"kappa_hat\": kappa,\n"
            "        \"se_gamma\": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),\n"
            "        \"se_lambda\": lam * math.sqrt(cov_diag[1]),\n"
            "        \"se_kappa\": kappa * math.sqrt(cov_diag[2]),\n",
            "    return {\n        \"gamma_hat\": round(gamma, 4),\n        \"lambda_hat\": round(lam, 4),\n        \"kappa_hat\": round(kappa, 4),\n"
            "        \"se_gamma\": round(gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]), 4),\n"
            "        \"se_lambda\": round(lam * math.sqrt(cov_diag[1]), 4),\n"
            "        \"se_kappa\": round(kappa * math.sqrt(cov_diag[2]), 4),\n",
        )],
    ),
    "e3e3_03_logit_sum_skips_the_first_response.py": (
        "The likelihood sum starts at the second response, so the first choice is left out of every likelihood.",
        [(
            "    for prizes_a, probs_a, prizes_b, probs_b, choice in parsed:\n        ce_a = _prospect_ce(prizes_a, probs_a, gamma, lam)\n",
            "    for prizes_a, probs_a, prizes_b, probs_b, choice in parsed[1:]:\n        ce_a = _prospect_ce(prizes_a, probs_a, gamma, lam)\n",
        )],
    ),
}

for name, (doc, edits) in MUTANTS.items():
    src = REF
    for old, new in edits:
        src = patch(src, old, new)
    src = module_doc_replace(src, doc)
    (OUT / name).write_text(src, encoding="utf-8")
    print("wrote", name, len(src))
