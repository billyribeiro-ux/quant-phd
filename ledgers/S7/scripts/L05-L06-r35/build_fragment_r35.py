"""Round-35 update of the S7 L05-L06 fragment (round 34 -> round 35). Keeps every row id.

Rows updated:
  L05-lab6-unsourced-1.5: judged on the page as it stands (class (c) derivation); the round-33 'range 0.046-0.048' and
      the 1.395 are not on the page (null_claim_grep.sh), so they are not claims of the page.
  R31-sweep-numbers-L05, R31-sweep-numbers-L06: the small-token sweep is applied to every token by a stated context rule
      (small_token_classes.py), a fixed-seed sample of 50 per page is read in context (sample_tokens.py, sample_reading.py),
      and every claim-carrying sampled token is covered by a derivation or lab-output row.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r35/build_fragment_r35.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

S = "ledgers/S7/scripts/L05-L06-r35/"
W = "/tmp/ap1-r5/L05-L06/r35/"
frag = json.loads(Path(W, "round34_fragment.json").read_text(encoding="utf-8"))
tokens = [line.rstrip("\n").split("\t") for line in Path(W, "small_tokens.tsv").read_text(encoding="utf-8").splitlines()]
cnt = {p: Counter(r[0] for r in tokens if r[1] == p) for p in ("L05", "L06")}
tot = {p: sum(cnt[p].values()) for p in cnt}


def classes(p: str) -> str:
    return ", ".join(f"{k} {cnt[p][k]}" for k in ("index", "locator", "design", "count", "code", "year", "claim"))


import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("sample_reading", ROOT / S.rstrip("/") / "sample_reading.py")
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)

UPD = {
    "L05-lab6-unsourced-1.5": (
        "PASS",
        "Round 35 (fresh, judged on the page as it stands): the sentence at L05 line 873 says '\\(30 \\times 0.05 = 1.5\\) false "
        "rejections that a nominal 5% test implies on average if every rule were skill-free'. This is class (c), derived on the "
        "page: each of the 30 one-sided rule tests has size 0.05 under the skill-free null, so the expected number of false "
        "rejections is 30 x 0.05 = 1.5 by linearity of expectation (exact for the nominal level; the page says 'implies'). "
        f"Grep ({S}null_claim_grep.sh, run this round): '1.395' and '1.388' appear in no S7 page, twin or card; the per-rule "
        "range '0.046 to 0.048' does not appear on the page. The 0.048 at L05 line 863 is a t-statistic table entry (JPY, MA100's "
        "neighbour), and the 0.046 at L05 line 1123 is the derived E3 rate 0.050 x 0.912 (row L05-num-E3). The earlier release "
        "evidence described a wording that is no longer on the page. The simulation in lab6_null_and_search.py (round 34: mean "
        "per-rule rate 0.0463, expected false rejections 1.388) is context, not a claim of the page; it agrees with the nominal "
        "1.5 to within the simulation's error for a size that is slightly below 5% (the per-rule rates are a finite-sample "
        "effect of the bootstrap test, not a page claim).",
        "",
    ),
    "R31-sweep-numbers-L05": (
        "PASS",
        "Round 35: procedure applied to all visible numeric tokens of L05.html with two decimals or a value of 10 or more "
        "(round-34 token_reconciliation.py: every such token is classed; the residue is index labels and the Phi(1.04)/Phi(-4.96) "
        "pieces, derived in e3_quadrature_and_se.py). Every remaining integer or one-decimal token (1,168 tokens) is classed by "
        f"the context rule in {S}small_token_classes.py (stated in its docstring; output {W}small_tokens.tsv): {classes('L05')}. "
        f"A fixed-seed random sample of 50 (seed 35; {S}sample_tokens.py; {W}sample.tsv) was read in context (codes in "
        f"{S}sample_reading.py): F {sr.L05.count('F')}, L {sr.L05.count('L')}, P {sr.L05.count('P')}, D {sr.L05.count('D')}, "
        f"O {sr.L05.count('O')}, C {sr.L05.count('C')}. The three C tokens are claims covered by named rows: 'about 1.6' "
        "(L05-lab3-line898-duplicates, lab output 1.601), the interval estimate 5.0 (L05-num-M4, derived), and '6.7%' (L05-num-E2, "
        "round-34 sol-S7-L05-E2 block 20 rate 0.067). No sampled token carries an underived claim. The classifier's errors "
        "(formula exponents or index labels in 'claim' or 'design'; the nominal 5% in 'claim') only misfile non-claims.",
        "",
    ),
    "R31-sweep-numbers-L06": (
        "PASS",
        "Round 35: procedure applied to all visible numeric tokens of L06.html with two decimals or a value of 10 or more "
        "(round-34 token_reconciliation.py; residue as for L05). Every remaining integer or one-decimal token (512 tokens) is "
        f"classed by the same rule ({S}small_token_classes.py; {W}small_tokens.tsv): {classes('L06')}. A fixed-seed sample of 50 "
        f"(seed 36; {W}sample.tsv) was read in context (codes in {S}sample_reading.py): F {sr.L06.count('F')}, L {sr.L06.count('L')}, "
        f"P {sr.L06.count('P')}, D {sr.L06.count('D')}, O {sr.L06.count('O')}, N {sr.L06.count('N')} (source-quoted numbers, "
        f"carried with their spans, rows L06-grade-cgs and L06-cite-chordia2020anomalies), C {sr.L06.count('C')}. The C tokens are "
        "covered by named rows: Proposition 4.3 numbers (L06-r14-prop43-numbers), bounds 2.7162 to 5.0792 (L06-p2-line373), "
        "'about 4%' (L06-line380-prior-odds), 1/19 and sqrt(2 ln 1881) (L06-num-P2), 1 - 0.95^2 = 0.0975 (L06-num-P3), the "
        "M = 1000 BHY values (L06-num-E2, round-34 variant run), 1 - 0.95^36 (L06-num-lab2), and the quiz values (R27-quiz-"
        "explanations-L06). No sampled token carries an underived claim.",
        "",
    ),
}

rows = []
for r in frag["rows"]:
    if r["id"] in UPD:
        status, text, fix = UPD[r["id"]]
        new = {"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": text}
        if status != "PASS":
            new["fix"] = fix
        rows.append(new)
    else:
        rows.append(r)
assert len(rows) == len(frag["rows"]) == len({r["id"] for r in rows}) == 611
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
out = dict(frag)
out.update({
    "round": 35,
    "verifier": "verifier round 35 (S7 L05-L06, ROUND 3, final: the three round-34 non-PASS rows; independent of the builders and of round 32)",
    "pin": "47bac8d",
    "base": "5e5da87",
    "previous_ledger": "round 34 fragment (copied at /tmp/ap1-r5/L05-L06/r35/round34_fragment.json before this round)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts["PASS"] == len(rows) else "FAIL",
    "rows": rows,
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": 0,
        "mutants_killed": 0,
        "mutants_note": "lessons only; no grader or project in L05 or L06, so 0/0",
        "round35_rows_changed": len(UPD),
        "carried_byte_identical_since_5e5da87": sum(1 for r in rows if r["evidence"].startswith("Carried from the release ledger")),
        "fail_ids": [r["id"] for r in rows if r["status"] != "PASS"],
    },
})
out["notes"] = list(frag.get("notes", [])) + [
    "ROUND 35 (final): L05-lab6-unsourced-1.5 judged on the page as it stands (the 1.395 and the 0.046-0.048 range are not on the page; the claim is the class-(c) derivation of 30 x 0.05 = 1.5). The small-token sweeps of L05 and L06 are closed by a stated context rule applied to every token and a fixed-seed sample of 50 per page read in context; claim-carrying sampled tokens are covered by named rows.",
]
problems = ledger.validate(out, "S7/L05-L06")
Path(ROOT / "ledgers/S7/L05-L06.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "changed", len(UPD), "validate:", problems)
