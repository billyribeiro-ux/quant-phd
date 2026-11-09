"""Writes four verifier-authored student-error mutants (round 14) as complete modules into ledgers/E3/mutants/.

Each is reference.py with one small change; the first docstring line names the student error. The script asserts that
every patch applies exactly once.
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"
REF_FIRST = (
    '"""Reference solution for the E3 project: elicit.py, the preference-elicitation engine.'
)


def patched(first_line: str, edits: list[tuple[str, str]]) -> str:
    text = REF
    assert text.count(REF_FIRST) == 1, "reference docstring changed"
    text = text.replace(REF_FIRST, '"""' + first_line + "\n\nReference solution for the E3 project, with one student error.", 1)
    for old, new in edits:
        assert text.count(old) == 1, f"patch does not apply exactly once: {old[:60]!r}"
        text = text.replace(old, new)
    return text


MUTANTS = {
    "r14d_01_estimate_uses_only_the_first_twelve_responses.py": patched(
        "Estimate reads only the first twelve responses (the size of the worked example) and ignores the rest.",
        [("    parsed = [_parse(r) for r in responses]\n    if not any(", "    parsed = [_parse(r) for r in responses[:12]]\n    if not any(")],
    ),
    "r14d_02_crra_log_case_takes_logs_of_final_wealth_minus_wealth.py": patched(
        "CRRA log case (gamma = 1) takes the logs of the prizes instead of the logs of final wealth.",
        [
            (
                "        return math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, finals, strict=True))) - wealth",
                "        return math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, prizes, strict=True))) - wealth",
            )
        ],
    ),
    "r14d_03_estimate_memoised_by_response_count.py": patched(
        "Estimate is memoised by the number of responses, so a second participant with the same count gets the first answer.",
        [
            (
                "def estimate(responses: list[dict[str, object]]) -> dict[str, float]:\n",
                "_CACHE: dict[int, dict[str, float]] = {}\n\n\n"
                "def estimate(responses: list[dict[str, object]]) -> dict[str, float]:\n"
                "    if len(responses) not in _CACHE:\n"
                "        _CACHE[len(responses)] = _estimate_uncached(responses)\n"
                "    return dict(_CACHE[len(responses)])\n\n\n"
                "def _estimate_uncached(responses: list[dict[str, object]]) -> dict[str, float]:\n",
            )
        ],
    ),
    "r14d_04_standard_errors_scaled_by_root_n.py": patched(
        "Standard errors are multiplied by the square root of the number of responses, as if they were a mean's.",
        [
            (
                '        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),',
                '        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0] * len(parsed)),',
            ),
            ('        "se_lambda": lam * math.sqrt(cov_diag[1]),', '        "se_lambda": lam * math.sqrt(cov_diag[1] * len(parsed)),'),
            ('        "se_kappa": kappa * math.sqrt(cov_diag[2]),', '        "se_kappa": kappa * math.sqrt(cov_diag[2] * len(parsed)),'),
        ],
    ),
}

if __name__ == "__main__":
    for name, text in MUTANTS.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", OUT / name)
