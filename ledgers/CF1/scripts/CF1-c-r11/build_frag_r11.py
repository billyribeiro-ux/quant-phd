"""Builds ledgers/CF1/CF1-c.json for round 11 from the round-10 fragment plus this round's fresh rows."""
import json

R10 = "/tmp/fanout-frags/CF1-c.round10.json"
OUT = "/tmp/verify11-CF1-c/ledgers/CF1/CF1-c.json"
CARRY = ("Carried from round 10 (tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py, and the L05.html/L06.html "
         "passages cited here, byte-identical since the previous pin af08ad1; the only changed L05/L06 lines are "
         "meta line 7, Section 4 line 236 and L06 line 223, none of them cited below; cards.json changed only card "
         "CF1-c012 of L01):")
FRESH = {
    "CF1-c-hub-L05-card-two-sided": ("PASS", "course/modules/CF/CF1/index.html line 142 (L05 hub card body)",
        "Re-verified in round 11: the round-10 FAIL is fixed. Line 142 now ends 'and why this lesson states no finding "
        "from the registered source on firm use'. That matches L05.html line 233 ('This lesson states no finding from "
        "it'). The card title 'Payback and What Firms Actually Use' equals the L05.html h1 (line 36). 'Simple and "
        "discounted payback on one project, what payback ignores after the cut-off' is supported by Propositions 2.1 "
        "and 2.2 (L05 lines 75-92). The phrase 'does and does not establish' no longer occurs in the card. "
        "Checked by sed/grep on the pin (scripts/CF1-c-r11/)."),
    "CF1-c-cmd-pin": ("PASS", "git rev-parse HEAD in /tmp/verify11-CF1-c", "91946cfce0c3efe5a3c91215ab7b31faecf53061 "
        "(detached); git diff --stat af08ad1 91946cf lists the changed files that were read for this delta."),
    "CF1-c-cmd-check_pages": ("PASS", "tools/check_pages.py --all", "rc=0; output 'check_pages CF1: PASS', "
        "'check_pages AP1: PASS' (scripts/CF1-c-r11/check_pages.out)."),
    "CF1-c-cmd-check_dag": ("PASS", "tools/check_dag.py --all", "rc=0; 'check_dag CF1: PASS', 'check_dag AP1: PASS' "
        "(scripts/CF1-c-r11/check_dag.out)."),
    "CF1-c-cmd-run_labs": ("PASS", "tools/run_labs.py --unit CF1", "rc=0; 'run_labs CF1: PASS (9/9)' "
        "(scripts/CF1-c-r11/run_labs.out)."),
    "CF1-c-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit CF1 --pages L05 L06", "rc=0; 'page_smoke "
        "modules/CF/CF1/L05.html: PASS' and 'page_smoke modules/CF/CF1/L06.html: PASS', lab-CF1-L05-1 0.0 s, "
        "lab-CF1-L06-1 0.3 s; 'page_smoke CF1: PASS' (scripts/CF1-c-r11/smoke.out). Pyodide timing not separately "
        "measured; the tool's own figures are under 10 s."),
    "CF1-c-cmd-ruff-mypy-labs": ("PASS", "twins tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py",
        "ruff check: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental on "
        "both twins: 'Success: no issues found in 2 source files'; all rc=0 (scripts/CF1-c-r11/ruff.out, mypy.out)."),
    "CF1-c-cmd-pytest-labs": ("PASS", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py",
        "rc=0; final progress line '...  [100%]' with no failures (scripts/CF1-c-r11/pytest.out)."),
    "CF1-c-cmd-verify_refs": ("PASS", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1",
        "'offline integrity: 560 entries, 0 problems' (rc=0); 'live re-verification of CF1: 2 of 560 entries, 0 problems' "
        "(rc=0) (scripts/CF1-c-r11/vr_offline.out, vr_live.out). Only the registry entries cited by CF1 were re-checked live."),
    "CF1-c-cmd-twin-vs-page": ("PASS", "L05.html and L06.html pre.run and pre.expected vs the twins",
        "The page data-run block equals the twin text except for one trailing newline that the page omits (both twins "
        "end 'main()'). The pre.expected block of L05 (10 lines) equals the stdout of 'python -I -W error' on the twin, "
        "and that of L06 (12 lines) too (scripts/CF1-c-r11/twin_vs_page.py, twin_L05.out, twin_L06.out)."),
    "CF1-c-lab-L05-1-run": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py; L05.html section.lab",
        "'python -I -W error tests/labs/CF1/lab-CF1-L05-1.py' rc=0; output begins 'rate 0.1 seed 2026 tails 1000 units "
        "cents' and equals the L05 pre.expected (scripts/CF1-c-r11/twin_L05.out)."),
    "CF1-c-lab-L06-1-run": ("PASS", "tests/labs/CF1/lab-CF1-L06-1.py; L06.html section.lab",
        "'python -I -W error tests/labs/CF1/lab-CF1-L06-1.py' rc=0; output equals the L06 pre.expected (12 lines) "
        "(scripts/CF1-c-r11/twin_L06.out)."),
    "CF1-c-twin-freshness": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py",
        "'git diff --quiet af08ad1 91946cf -- tests/labs/CF1' exits 0: both twins are byte-identical to the previous pin."),
    "CF1-c-struct-L05": ("PASS", "L05.html whole page",
        "The round-11 diff of L05.html against af08ad1 has two changed lines (meta line 7 and line 236), each a single text line, and adds no tag, section, "
        "dfn, pre or script (checked by grep on the diff). Section order: 1 (line 54), 2 (72), lab (99), 3 (205), 4 (221, canon-breaks at 223), 5 (239), "
        "problem-set (256), key-results (361). check_pages and page_smoke pass."),
    "CF1-c-struct-L06": ("PASS", "L06.html whole page",
        "The diff against af08ad1 changes one text line (line 223, the Section 4 intro paragraph) and adds no tag, "
        "section, dfn, pre or script. check_pages and page_smoke pass. Section 4 structure (canon-breaks section, list "
        "of four bullets, closing paragraph) is unchanged."),
    "CF1-c-banned-scan": ("PASS", "L05.html and L06.html learner text (whole page)",
        "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add "
        "more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, About 6%, "
        "roughly half, historically, build, builder, verifier, round N, REQUESTS, unit report, ellipsis. Hits: L05 "
        "lines 126-128 are the Python type hints 'tuple[int, ...]' inside a code block; L06 line 111 has 'roughly' in "
        "the lab hypothesis ('falls roughly as the square root of n'), a qualitative prediction that the lab output "
        "(se 4400.22, 1544.09, 489.81, 221.01 at n = 100, 1000, 10000, 50000) supports within its sampling noise; "
        "no banned phrase is hit."),
    "CF1-c-concepts": ("PASS", "L05.html dfn payback-period; L06.html dfn monte-carlo-npv; check_dag",
        "grep: one dfn id in each page; 'tools/check_dag.py --all' rc=0 (scripts/CF1-c-r11/check_dag.out)."),
    "CF1-c-hours": ("PASS", "L05.html and L06.html data-hours; index.html data-hours-lessons and eyebrow",
        "grep: data-hours=\"8\" in L05.html and L06.html, unchanged by this round's diff (no data-hours line in the "
        "diff). The hub hours passage (index.html) is not changed for these lessons. Hours are design targets "
        "(architect ruling); no pace estimate is failed."),
    "CF1-c-cards-duplicates": ("PASS", "course/modules/CF/CF1/cards.json (all 100 cards)",
        "Re-scanned in round 11: 100 cards, no duplicate id, no duplicate front (scripts/CF1-c-r11/cards_dup.py). "
        "The only card changed by this round is CF1-c012 (lesson L01, not in this slice)."),
    "CF1-c-prose-process-path": ("PASS", "L05.html and L06.html learner text; cards.json L05 and L06 cards",
        "grep for builder, verifier, round N, REQUESTS and unit report in both pages: no hit (scripts/CF1-c-r11/)."),
}
NEW = [
    {"id": "CF1-c-meta-L05-description", "check": "2.9-prose", "location": "L05.html line 7 (meta description)",
     "status": "PASS",
     "evidence": "Changed this round to 'Simple and discounted payback: their definitions, the proof that payback ignores "
                 "cash flows after its payback year, a SIMULATED comparison with NPV on the same flows, and why this lesson "
                 "states no finding on firm practice.' Each clause is supported: Proposition 2.1 (line 75-76) says that "
                 "flows after the payback year do not change simple payback; Lab 1 (line 101) is SIMULATED and compares "
                 "payback with NPV on the same flows; Section 4 (line 233) states no finding. No banned phrase; no number."},
    {"id": "CF1-c-prose-L05-section4-registered-source", "check": "2.9-prose",
     "location": "L05.html line 236 (paragraph after the canon-breaks section)", "status": "PASS",
     "evidence": "Changed from 'read the survey' to 'read the registered source'. Graham and Harvey (2001) is the registered "
                 "source named in line 233; the new wording makes no claim about its content, so no grade or passage is "
                 "needed. The paragraph's remaining claim, that a reader must locate the passage and grade it, is a "
                 "procedure, not a finding."},
    {"id": "CF1-c-scope-L06-section4-intro", "check": "2.9-prose", "location": "L06.html line 223 (Section 4 intro paragraph) "
     "against bullets at lines 226-229", "status": "FAIL",
     "evidence": "New sentence (changed this round): 'Propositions 2.1 and 2.3 hold for the model they are stated for. The "
                 "limits below concern the model and its inputs, except the quantile bullet, which concerns the estimator.' "
                 "The first sentence is supported: Proposition 2.1 (line 72) needs iid draws with finite variance, Proposition "
                 "2.3 (line 92) needs independent receipts with mean mu and variance sigma^2, and their proofs (lines 77, 101) "
                 "follow. The second sentence is not. Bullet 2 (line 227, 'Sampling error is not model error.') opens with "
                 "'Proposition 2.1 shows that more draws shrink the standard error', a statement about the sampling error of "
                 "the estimator, and bullet 3 (line 228) is about the sampling error of tail quantiles. Only bullet 3 is "
                 "excepted, so the sentence says that bullet 2 concerns the model and its inputs, which the bullet's own text "
                 "does not say.",
     "fix": "On L06.html line 223, replace 'except the quantile bullet, which concerns the estimator' with 'except the second "
            "and third bullets, which concern the sampling error of the estimator', or delete the second sentence. Then "
            "re-run tools/check_pages.py --all and page_smoke for L06."},
    {"id": "CF1-c-num-recompute-r11", "check": "2.2-numbers", "location": "L06.html line 111 (hypothesis), line 96 (Prop 2.3); "
     "L05.html Section 3 (line 217) and lab hypothesis (line 101)", "status": "PASS",
     "evidence": "Independent recomputation (scripts/CF1-c-r11/recompute_r11.py, output recompute_r11.out) with exact fractions: "
                 "mu = a + (m-1)/2 = 100000 cents; Var = (m^2-1)/12 * sum v_t^2; E[NPV] = 79078.6769... -> 79078.68; SD = "
                 "49379.8445... -> 49379.84. L05 constants exec'd from the twin: NPV at 10% A 289367.40, B -96168.29, gap "
                 "385535.69 cents, matching the page output; simple payback A and B 2.75, D 2.00."},
]
d = json.load(open(R10, encoding="utf-8"))
rows = []
seen = set()
for r in d["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in FRESH:
        st, loc, ev = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev})
        continue
    if r["status"] != "PASS":
        raise SystemExit("unexpected non-PASS carried row " + rid)
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": CARRY + " " + r["evidence"]})
assert set(FRESH) <= seen, set(FRESH) - seen
rows += NEW
missing = [i for i in FRESH if i not in seen]
frag = {
    "unit": "CF1", "slice": "CF1-c", "round": 11,
    "verifier": "independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 11; did not build CF1; "
                "no shared context with builders or earlier verifiers",
    "pin": "91946cfce0c3efe5a3c91215ab7b31faecf53061",
    "base": "af08ad1e1458e56314bd70c2b82bd37b154e2beb",
    "checkout": "/tmp/verify11-CF1-c (detached worktree at 91946cf; .venv symlinked)",
    "scratch": "/tmp/cf1-v/CF1-c-r11",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "mutants": [],
    "registry_flags": ["glasserman2003monte: registry used_by is ['M8'] but CF1 L06 cites this key; used_by not updated "
                       "(generated registry, not edited by the verifier). Not a row failure."],
    "freshness_flags": [],
    "notes": "Delta from af08ad1 (round-10 pin) to 91946cf for this slice: L05.html (meta line 7; line 236), L06.html (line "
             "223), index.html (L05 card, line 142; the L03 card title also changed, outside this slice, not checked here), "
             "cards.json (CF1-c012 of L01 only). tests/labs/CF1 twins byte-identical. Command rows re-run on the pin. Mutants: "
             "not required (lesson and lab slice). Alternative implementations: not applicable. Not checked: Graham and Harvey "
             "(2001) and Glasserman (2003) were not read (no publisher access attempted), so no passage-level claim is "
             "verified; the pages make none beyond the registry record. Hours not failed on pace (architect ruling). Whole-page "
             "structure rows rest on the diff (text-only changes) plus check_pages and page_smoke, not on a fresh full re-read.",
    "summary": "CF1-c round 11: rows {n} (pass {p}, fail {f}, unverifiable 0). One FAIL: L06.html line 223 says only the "
               "quantile bullet concerns the estimator, but bullet 2 (line 227) is about sampling error of the estimator. The "
               "round-10 FAIL (L05 hub card) is fixed and verified.",
    "rows": rows,
}
n = len(rows)
p = sum(1 for r in rows if r["status"] == "PASS")
f = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = frag["summary"].format(n=n, p=p, f=f)
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", n, "pass", p, "fail", f, "missing-from-r10", missing)
