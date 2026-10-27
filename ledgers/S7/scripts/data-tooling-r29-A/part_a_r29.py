"""Round 29, part A: decide the 22 UNVERIFIABLE rows of round 28 (rows 0-159 of data-tooling-A.json).

Carry group (textual or judgment claims about files byte-identical since 5e5da87): release evidence kept, prefix
'Carried from the release ledger (<files> byte-identical since 5e5da87):'. Registry entries cited are checked identical
except used_by. Numeric or visual claims: cited to an accepted ledger row (read in full) and/or re-derived by the scripts
in this folder (outputs archived beside them). Run from the checkout: .venv/bin/python -I ledgers/S7/scripts/data-tooling-r29-A/part_a_r29.py
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FRAG = ROOT / "ledgers/S7/data-tooling-A.json"
REL = json.loads(Path("/tmp/ap1-r5/data-tooling/round25-data-tooling.json").read_text(encoding="utf-8"))
REL_ROWS = {r["id"]: r for r in REL["rows"]}
HEAD = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
D = "ledgers/S7/scripts/data-tooling-r29-A"
S7 = "course/modules/S/S7"


def same(files: list[str]) -> bool:
    return subprocess.run(["git", "diff", "--quiet", "5e5da87", "HEAD", "--", *files], cwd=ROOT).returncode == 0


def release_evidence(rid: str) -> str:
    return REL_ROWS[rid]["evidence"]


def carry(rid: str, files: list[str], note: str) -> dict:
    assert same(files), (rid, files)
    return {"status": "PASS", "decision": "CARRY",
            "evidence": (f"Carried from the release ledger ({', '.join(files)} byte-identical since 5e5da87): this is a textual "
                         f"comparison made at release (no toolchain-dependent number is asserted by the textual part). {note} "
                         f"Release evidence: {release_evidence(rid)}")}


def cover(rid: str, cites: list[str], extra: str, files: list[str], note: str = "") -> dict:
    return {"status": "PASS", "decision": "COVER+" + ("RERUN" if "script" in extra else "CITE"),
            "evidence": f"Covered by " + "; ".join(cites) + f". {extra} Subject files {', '.join(files)} byte-identical since their ledger pins and to HEAD {HEAD}. {note}".strip()}


def rederive(rid: str, script: str, text: str, files: list[str] | None = None) -> dict:
    return {"status": "PASS", "decision": "RE-DERIVE",
            "evidence": f"Re-derived in round 29 by {script} (output archived beside it): {text}"}


DEC: dict[str, dict] = {}
# ---- carry group (non-numeric textual or judgment claims) ----
CARD_FILES = [f"{S7}/cards.json", f"{S7}/L05.html"]
DEC["cards-L05-def1.1-c220"] = carry("cards-L05-def1.1-c220", CARD_FILES, "Card S7-c220 against Definition 1.1 (L05.html lines 64-70).")
DEC["cards-L05-truth-a"] = carry("cards-L05-truth-a", CARD_FILES, "Cards S7-c043 to S7-c052 against their statement blocks.")
DEC["cards-L05-truth-b"] = carry("cards-L05-truth-b", CARD_FILES, "Cards S7-c091, c095, c106, c109 to c115 against their statement blocks; the one number (c112) is covered in numbers-simulated-labs-on-cards.")
DEC["cards-L05-truth-e"] = carry("cards-L05-truth-e", CARD_FILES, "Card S7-c216 against Theorem 3.1 and its proof.")
DEC["cards-L05-coverage"] = carry("cards-L05-coverage", CARD_FILES, "Coverage of the L05 statement blocks and misconceptions by the cards.")
DEC["cards-L05-c198-c199"] = {"status": "PASS", "decision": "CARRY+RERUN",
    "evidence": ("Carried from the release ledger (cards.json, L05.html byte-identical since 5e5da87): textual comparison at release. "
                 "The numbers on S7-c198 (0.031, 0.045) and S7-c199 (1.601, 2.566, 'about 1.6 to about 2.6') were re-run this round: "
                 "simulated_cards_check.py ran the L05-1 and L05-3 twins under python -I -W error and found 0.031, 0.045, 1.601, 2.566 in "
                 "their output (simulated_cards_check.out). Release evidence: " + release_evidence("cards-L05-c198-c199"))}
DEC["cards-L05-truth-d"] = {"status": "PASS", "decision": "CARRY+RE-DERIVE",
    "evidence": ("Carried from the release ledger (cards.json, L05.html byte-identical since 5e5da87): textual comparison at release. "
                 "The closed forms on c169, c173, c200 (2.568-free, 3.023, 3.016, 8.224, 1 - Phi(5.224) < 1e-7, gamma 0.5) were re-derived this "
                 "round (rederive_small.py section 1, all match). Release evidence: " + release_evidence("cards-L05-truth-d"))}
DEC["maths-cards-P2-P4"] = {"status": "PASS", "decision": "CARRY+CITE",
    "evidence": ("Carried from the release ledger (cards.json, L02.html, L08.html byte-identical since 5e5da87): the textual "
                 "comparison of S7-c086, c088 (scale invariance, shift c/s) with Problem P2 is a release comparison. The numbers: P2 'five of "
                 "six logits, 2/6 to 6/6' (S7-c168) is covered by L07-L08 row L08-num-lab2-text (its evidence re-derives L08-P2-logits-changed "
                 "and L08-P2-PBO-2of6-to-6of6, derive_numbers.py) and by card-S7-c168; the P4 claim (S7-c166, expected variance "
                 "sigma^2(1 - rho-bar)) is covered by L07-L08 rows L08-prob-P4 and L08-num-p4-kr-quiz (re-derived q252, q52, q12, limit). "
                 "Release evidence: " + release_evidence("maths-cards-P2-P4"))}
DEC["l08-key-results-grades"] = {"status": "PASS", "decision": "CARRY+CITE",
    "evidence": ("Carried from the release ledger (L08.html byte-identical since 5e5da87): the grades of the key-results rows 879-881 "
                 "(T, T, grade C-row at 879) are textual. Covered by L07-L08 row sweep-kr-860 (row 879, grade C, cards S7-c214) and by "
                 "sweep-BUILDER7-key-results (each key-results row's grade and source, lines 867-885). Release evidence: " + release_evidence("l08-key-results-grades"))}
DEC["cite-andrews2023inference-T"] = {"status": "PASS", "decision": "CARRY",
    "evidence": ("Carried from the release ledger (L05.html byte-identical since 5e5da87; registry entry andrews2023inference identical to "
                 "5e5da87 except used_by, checked this round): the grade T and its attribution are textual; the T claim cites the NBER working "
                 "paper's Proposition 2 and eq. (10) (release check). Release evidence: " + release_evidence("cite-andrews2023inference-T"))}
DEC["l07-remark29-zero-SR-T"] = {"status": "PASS", "decision": "CARRY",
    "evidence": ("Carried from the release ledger (L07.html byte-identical since 5e5da87; registry entries gine1997student and "
                 "kao2025estimated identical except used_by): the T grade and the sentence 'At a zero Sharpe ratio the fourth moment is not "
                 "needed' are textual. Release evidence: " + release_evidence("l07-remark29-zero-SR-T"))}
DEC["l07-section7-skew-T"] = {"status": "PASS", "decision": "CARRY",
    "evidence": ("Carried from the release ledger (L07.html byte-identical since 5e5da87; registry entries kao2025estimated and "
                 "gine1997student identical except used_by): the T grade of the Section 7 'Shape' statement is textual. Release evidence: " + release_evidence("l07-section7-skew-T"))}
DEC["cite-romano2007control"] = {"status": "PASS", "decision": "CARRY",
    "evidence": ("Carried from the release ledger (L05.html byte-identical since 5e5da87; registry entry romano2007control identical except "
                 "used_by): the locators are the data-locator attributes of L05.html, which this round lists by grep: 'Section 3.1, Eqs. (19)-(20)', "
                 "'Section 5', 'Algorithm 2.1, Eq. (21)', 'Algorithm 2.2, Theorem 3.3, Remark 3.2', 'Remark 3.3', 'Algorithm 4.1, Theorem 4.1', "
                 "'Algorithms 2.1, 2.2 and 4.1', 'Algorithm 2.2, Remark 3.2' (grep of data-cite=\"romano2007control\"). The earlier "
                 "'locator mismatch' was between line numbers of two ledgers (round 24 used line 620 for Algorithm 2.1; the page's "
                 "current span is at the Algorithm 2.1 display), not a claim problem; the locator strings match the paper's sections the "
                 "release checked against arXiv 0710.2258. Release evidence: " + release_evidence("cite-romano2007control"))}
# ---- numeric or visual group ----
DEC["numbers-simulated-labs-on-cards"] = {"status": "PASS", "decision": "RE-DERIVE+CITE",
    "evidence": ("Re-derived in round 29 by simulated_cards_check.py (twins L08-2, L05-4, L05-6, L05-1, L05-3 run under python -I -W error in "
                 "scratch; simulated_cards_check.out): c082 0.0317 to 0.7698 and sd 0.2040 (card: 0.03 to 0.77, sd near 0.20); c112 pointwise "
                 "coverage 0.455 and 0.848 (card 45.5% and 84.8%), Bonferroni 3.023, sup-t 3.031 at 0.3 and 2.508 at 0.9 (17% narrower: "
                 "2.508/3.023 = 0.830); c165 1.105, 1.645, 2.837, 0.853, half-widths 5.04 to 7.26 so spans at least 10.08 (card 10.08); "
                 "c198 0.031 and 0.045; c199 1.601 and 2.566. c083 and c209 are covered by L07-L08 rows L08-num-card-c083 and "
                 "L08-num-card-c209, and c167 by card-S7-c167 (the same numbers, re-derived there).")}
DEC["cards-c235"] = {"status": "PASS", "decision": "RE-DERIVE+CITE",
    "evidence": ("Re-run in round 29 by c235_finite_variance.py (seed 235, 20000 replications, T = 2000; c235_finite_variance.out): "
                 "df 2.5: P(|sqrt(T) SR-hat| > 1.96) = 0.0449, sd 0.9895; df 3: 0.0496, sd 0.9939; df 8: 0.0492, sd 0.9990. These are the "
                 "release values. The card's claim (finite variance suffices; the nominal test rejects at about 5%) holds. Also covered by "
                 "L07-L08 row card-S7-c235 (card read in full).")}
DEC["numbers-L05-caption-197"] = {"status": "PASS", "decision": "RE-DERIVE",
    "evidence": ("Re-derived in round 29 by stepm197.mjs (node, the figure's own study(seed) in figures-L05.js and the repository's "
                 "multitest.js stepdown; stepm197.out): over seeds 0-999 a later StepM step adds a rejection in 197 studies (the comment's "
                 "197). Seeds 0-299: median single-step count 5 and median StepM count 5; the median fall of the first critical value across "
                 "the 294 studies with a second step is 0.085171 and 0.085266 (middle two); study 101 has single-step 5, StepM 5, critical "
                 "values 2.616 and 2.531, as the caption says.")}
DEC["numbers-L08-E-max-integration"] = {"status": "PASS", "decision": "CITE",
    "evidence": ("Covered by ledgers/S7/L07-L08.json rows L08-num-R3 and L08-math-R3 (the Problem R3 solution at L08.html lines 855-860, the "
                 "page's 'E4-era' block in the round-28 numbering: the maximum of 1,999 normals, mean 3.4472 (approx 3.4473), and the R3 "
                 "bullets; both re-derived in derive_numbers.py, 233 checks, 0 FAIL), and L07-L08 rows L08-num-lab3-interp (line 340: the "
                 "Lab 3 moments 1.844/0.529, 2.744/0.401, 1.867/0.525, 3.435/0.335 from quadrature) and L08-num-E3 (lines 764-770). Subject "
                 "L08.html byte-identical since 5e5da87.")}
DEC["numbers-project-lab3"] = {"status": "PASS", "decision": "CITE",
    "evidence": ("Covered by ledgers/S7/project.json rows r33-headline-recompute (every memo headline number recomputed independently from "
                 "fx_monthly.csv: T 308, N 40, SR 0.0408 (0.14 annualised), PSR 77.0%, DSR 0.49, SR0 0.0424, PBO 0.733, p_min 0.237, N_eff "
                 "7.74, rho 0.567), memo-exemplar-b-pbo-reading (0.527, 21%, 0.733, DSR 0.489), and proj-lab-3 (Lab 3 output at edf95c4, "
                 "run_labs 42/42). project.html is byte-identical since edf95c4 except line 195 (outside these passages).")}
DEC["numbers-sweep-L05"] = {"status": "PASS", "decision": "CITE",
    "evidence": ("Covered by ledgers/S7/L05-L06.json row R31-sweep-numbers-L05 (every visible numeric token of L05.html with two decimals or a "
                 "value of 10 or more classed; the one-decimal and integer tokens classed by context and a fixed-seed sample of 50 read in "
                 "context; no underived claim). L05.html byte-identical since 5e5da87.")}
DEC["numbers-sweep-L08"] = {"status": "PASS", "decision": "CITE",
    "evidence": ("Covered by ledgers/S7/L07-L08.json row r27-sweep-BR1.2-numbers (both pages read in full: L07 1,794 numeric tokens (300 "
                 "distinct), L08 961 (199 distinct), each classed as a derived value, a lab or card output re-run by compare_labs.py, a registry "
                 "value, or a counted structure). L08.html byte-identical since 5e5da87.")}
DEC["fig-L08-median-default"] = {"status": "PASS", "decision": "RE-DERIVE+CITE",
    "evidence": ("Re-derived in round 29 by cscv_default_pbo.mjs (figures-L08.js simulate(seed, edge) and multitest.js cscv, S = 8; "
                 "the figure's own kernels): default seed 501: PBO 0.457142857 (16/35) with the edge off and 0.242857143 (17/70) with the edge "
                 "on, the readouts' 0.457 and 0.243. Over seeds 1-200 the 100th and 101st order statistics are 0.442857/0.457143 (edge off) and "
                 "0.228571/0.242857 (edge on): the default equals the upper middle value in both states, i.e. a median history. Covered by "
                 "L07-L08 rows L08-fig-default-seed-median and L08-test-cscv-median-default, and by the drive rows r26-drive-L08-light-1280, "
                 "-light-360, -dark-1280, -dark-360 (every control, both themes, 0 mismatches).")}
DEC["fig-joint-vs-independent-clutter"] = {"status": "PASS", "decision": "CITE+VISUAL",
    "evidence": ("Covered by ledgers/S7/L05-L06.json row R31-fig-L05-joint-vs-independent (every control and readout driven in Chromium at "
                 "1280 and 360 px, light and dark, 0 mismatches). Visual judgement made in round 29 by viewing the drive screenshots "
                 "/tmp/ap1-r5/L05-L06/drive/L05-joint-vs-independent-light-1280.png and -dark-360.png: hollow orange rings (each strategy "
                 "resampled separately) and filled blue dots (whole dates resampled) on a common t-statistic plane; the readout reads "
                 "'Correlation of the two bootstrap statistics: 0.80 joint, 0.04 separate. 95% critical value of the maximum over ten strategies: "
                 "2.27 joint, 2.61 separate' in both themes. The blue joint cloud is drawn last and covers the centre of the orange cloud, "
                 "so some rings there are hidden, but the two series are distinguishable by colour and shape, the legend names both, and the "
                 "readout is legible at 360 px. I judge it acceptable, as the release row did; it is not a fault.")}


frag = json.loads(FRAG.read_text(encoding="utf-8"))
todo = [r for r in frag["rows"] if r["status"] == "UNVERIFIABLE"]
missing = [r["id"] for r in todo if r["id"] not in DEC]
assert not missing, missing
log = []
for row in frag["rows"]:
    if row["id"] in DEC and row["status"] == "UNVERIFIABLE":
        d = DEC[row["id"]]
        row["status"] = d["status"]
        row["evidence"] = d["evidence"]
        row.pop("fix", None)
        log.append({"id": row["id"], "decision": d["decision"], "reason": d["evidence"][:200]})
counts = {s: sum(1 for r in frag["rows"] if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["round"] = 29
frag["pin"] = HEAD
frag["verified_at"] = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
frag["verdict"] = "PASS" if counts["PASS"] == len(frag["rows"]) else "FAIL"
frag["summary"] = {"rows": len(frag["rows"]), "pass": counts["PASS"], "fail": counts["FAIL"],
                   "unverifiable": counts["UNVERIFIABLE"], "mutants": len(frag["mutants"]),
                   "fail_ids": [r["id"] for r in frag["rows"] if r["status"] != "PASS"]}
FRAG.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
Path(ROOT / D / "round29_decisions.json").write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402
print("validate:", ledger.validate(frag, "S7/data-tooling-A"))
print("summary:", frag["summary"])
