"""SC1-a round 20: write ledgers/SC1/SC1-a.json from the round-19 rows (carried or re-verified this round) and the
round-20 outputs under ledgers/SC1/scripts/SC1-a-r20/out/. Usage (checkout root): python3 -I <this file>"""
import datetime
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "ledgers", "SC1", "scripts", "SC1-a-r20", "out")
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-a.round19.json", encoding="utf-8"))
S = "ledgers/SC1/scripts/SC1-a-r20/out/"
G = "gate r20 (gates_r20.sh)"

FRESH = {
    "SC1a-gate-check-pages": f"check_pages.py --unit SC1 at d1083bf1: 'check_pages SC1: PASS', rc=0 ({S}check_pages_SC1.out). Covers index.html, L01-L03, cards.json.",
    "SC1a-gate-check-dag": f"check_dag.py --unit SC1 at d1083bf1: 'check_dag SC1: PASS', rc=0 ({S}check_dag_SC1.out).",
    "SC1a-gate-run-labs": f"run_labs.py --unit SC1 --page L01/L02/L03 at d1083bf1: 'run_labs SC1: PASS (1/1)' for each, rc=0 ({S}run_labs_L0{{1,2,3}}.out).",
    "SC1a-gate-page-smoke": f"page_smoke.py --unit SC1 --pages L01 / L02 / L03 alone, and index: each 'page_smoke SC1: PASS', rc=0 ({S}page_smoke_*.out).",
    "SC1a-gate-lint-types-tests": f"ruff check: 'All checks passed!' ({S}ruff_check.out); ruff format --check: '553 files already formatted' ({S}ruff_format.out); mypy --no-incremental: 'Success: no issues found in 385 source files' ({S}mypy.out); pytest -q -k SC1: 11 passed, rc=0 ({S}pytest_SC1.out; collect count {S}collect_SC1.out).",
    "SC1a-gate-verify-refs": f"verify_refs.py --offline: '560 entries, 0 problems', rc=0; verify_refs.py --unit SC1: '1 of 560 entries, 0 problems', rc=0 ({S}verify_refs_offline.out, {S}verify_refs_unit_SC1.out).",
    "SC1a-r7-gate-check-projects": f"check_projects.py --unit SC1: 'check_projects SC1: PASS', rc=0 ({S}check_projects_SC1.out).",
    "SC1a-r7-katex-render": f"page_smoke.py (index, L01, L02, L03 alone) at d1083bf1: PASS. tools/page_smoke.py fails on console errors, page errors, external requests and any .katex-error or strict KaTeX failure (its docstring lines 8-11 and checks at lines 103-123), so PASS covers those checks ({S}page_smoke_*.out).",
    "SC1a-r8-links-anchors": f"check_pages.py --unit SC1 PASS and page_smoke PASS at d1083bf1 ({S}check_pages_SC1.out, {S}page_smoke_*.out); links and anchors are checked by those tools.",
    "SC1a-r15-gate-ruff-check": f"ruff check . at d1083bf1: 'All checks passed!', rc=0 ({S}ruff_check.out); the lab-mutant files pass it too.",
    "SC1a-r15-links-anchors-scripted": f"check_pages.py --unit SC1 PASS at d1083bf1 ({S}check_pages_SC1.out); page_smoke PASS ({S}page_smoke_*.out).",
    "SC1a-r18-page-smoke-alone": f"page_smoke.py --unit SC1 --pages L01|L02|L03 run alone at d1083bf1: PASS for each, rc=0 ({S}page_smoke_L0{{1,2,3}}.out, {S}page_smoke_index.out).",
    "SC1a-r18-page-vs-twin": f"page_vs_twin_r20.py: L01, L02, L03 each 'page code == twin: True; twin rc=0; stderr bytes=0; expected == stdout: True' ({S}page_vs_twin_r20.out).",
    "SC1a-r10-cmd-check_pages": f"see SC1a-gate-check-pages ({S}check_pages_SC1.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-check_dag": f"see SC1a-gate-check-dag ({S}check_dag_SC1.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-check_projects": f"see SC1a-r7-gate-check-projects ({S}check_projects_SC1.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-run_labs": f"see SC1a-gate-run-labs ({S}run_labs_L0{{1,2,3}}.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-page_smoke": f"see SC1a-gate-page-smoke ({S}page_smoke_*.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-twins-python-I-W-error": f"python -I -W error on tests/labs/SC1/lab-SC1-L01/L02/L03-1.py: rc=0 for each, stderr 0 bytes ({S}twin_L0{{1,2,3}}.rc, .stderr).",
    "SC1a-r10-cmd-verify_refs": f"see SC1a-gate-verify-refs ({S}verify_refs_offline.out, {S}verify_refs_unit_SC1.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-ruff-mypy": f"see SC1a-gate-lint-types-tests ({S}ruff_check.out, {S}mypy.out): PASS at d1083bf1.",
    "SC1a-r10-cmd-pytest-SC1": f"see SC1a-gate-lint-types-tests ({S}pytest_SC1.out): 11 passed at d1083bf1.",
    "SC1a-lab-L01-twin": f"run_labs PASS (L01) and twin under python -I -W error rc=0, stderr empty ({S}run_labs_L01.out, {S}twin_L01.*); page_vs_twin L01 True ({S}page_vs_twin_r20.out).",
    "SC1a-lab-L02-twin": f"run_labs PASS (L02) and twin under python -I -W error rc=0, stderr empty ({S}run_labs_L02.out, {S}twin_L02.*); page_vs_twin L02 True ({S}page_vs_twin_r20.out); L02.html:266-278 expected block equals twin stdout.",
    "SC1a-lab-L03-twin": f"run_labs PASS (L03) and twin under python -I -W error rc=0, stderr empty ({S}run_labs_L03.out, {S}twin_L03.*); page_vs_twin L03 True ({S}page_vs_twin_r20.out).",
    "SC1a-r8-lab-mutants": f"kill_lab_mutants_r20.py: 41 of 41 killed, 0 survivors ({S}kill_lab_mutants_r20.out).",
    "SC1a-r10-lab-mutants-4of4": f"kill_lab_mutants_r20.py: the four SC1-a-r10 files KILLED ({S}kill_lab_mutants_r20.out).",
    "SC1a-r11-lab-mutants-6of6": f"kill_lab_mutants_r20.py: the six SC1-a-r11 files KILLED ({S}kill_lab_mutants_r20.out).",
    "SC1a-r14-lab-mutants-new3": f"kill_lab_mutants_r20.py: SC1a-r14-lab-n1..n3 KILLED ({S}kill_lab_mutants_r20.out).",
    "SC1a-r15-lab-mutants-p1-p3": f"kill_lab_mutants_r20.py: SC1a-r15-lab-p1..p3 KILLED ({S}kill_lab_mutants_r20.out).",
    "SC1a-r16-lab-mutants-35": f"kill_lab_mutants_r20.py: all 35 pre-r17 files KILLED, 41/41 total ({S}kill_lab_mutants_r20.out).",
    "SC1a-r16-lab-q1-q3-new": f"kill_lab_mutants_r20.py: SC1a-r16-lab-q1..q3 KILLED ({S}kill_lab_mutants_r20.out).",
    "SC1a-r16-mutants-list": f"kill_lab_mutants_r20.py: ledgers/SC1/lab-mutants/** 41 files, 41 KILLED, 0 survivors ({S}kill_lab_mutants_r20.out).",
    "SC1a-r19-lab-mutants-all-38": f"kill_lab_mutants_r20.py: all 38 r19 files KILLED plus 3 new r20 files (ledgers/SC1/lab-mutants/SC1-a-r20/); 41/41 ({S}kill_lab_mutants_r20.out).",
    "SC1a-r16-L01-lab-output": f"twin_L01.stdout equals the L01.html expected block (page_vs_twin L01 True, {S}page_vs_twin_r20.out).",
    "SC1a-r16-L02-lab-output": f"twin_L02.stdout equals the L02.html:266-278 expected block (page_vs_twin L02 True, {S}page_vs_twin_r20.out).",
    "SC1a-r16-L03-lab-output": f"twin_L03.stdout equals the L03.html expected block (page_vs_twin L03 True, {S}page_vs_twin_r20.out).",
    "SC1a-math-L02-A2-sketch": ("Re-verified: the changed sentence at L02.html:285 (git diff cd4dd7df..d1083bf1, hunk @@ -282,7 +282,7 @@) now says choose dyadic times t^(k) in [t,1] decreasing to t. "
        "Checked: for t in [0,1), x_k=ceil(2^k t)/2^k lies in [t,1], is a dyadic time of depth k, and is non-increasing (ceil(2a)<=2 ceil(a)); for t=1 the constant sequence 1 works. "
        "By Prop 2.4(b) (L02.html:145-165) Sigma(t^(k))->Sigma(t) on Omega*. The sketch still says it skips the limit of characteristic functions and the joint case (text unchanged). Verdict PASS."),
    "SC1a-r10-L03-why-sample-means": ("Re-verified: L03.html:51 (changed line) says Lab 1 prints each sample mean with its standard error, 'an estimated standard deviation of that mean'. "
        f"tests/labs/SC1/lab-SC1-L03-1.py mean_and_standard_error returns sqrt(sum((v-mean)^2)/(n-1)/n) (the SE of the mean) and main() prints 'mean ..., se ..., z ...' for N=2^k, k=0..7 ({S}twin_L03.stdout). PASS."),
    "SC1a-r17-hunk-L03-51": ("Re-verified L03.html:51 after cd4dd7df->d1083bf1. The why-it-matters text: E[squared increment]=interval length, so Q has mean t (Theorem 2.3, L03.html:99-115); the smooth-function sums are bounded by 4H^3|P| (Prop 2.4(a), L03.html:117-129, and P2 at :322), so they shrink as the longest interval shrinks; "
        "'Assumptions 3.1 and 3.2 (stated in §1)': both are stated at L03.html:65 and :70, inside §1 (h2 at :53, next h2 at :74). The lab sentence matches the twin (see SC1a-r10-L03-why-sample-means). PASS."),
    "SC1a-r16-why-words": "Process/why-words check on the changed L03.html:51 line: no process words (round, verifier, ledger, we, this build) and no banned filler; L01.html:51 and L02.html:51 unchanged. grep over index/L01/L02/L03 and twins: no hits (r20 grep). PASS.",
    "SC1a-r17-banned-changed-lines": f"banned_scan_r20.out (course/modules/SC/SC1 index, L01-L03, cards.json, r19 banned list): only hits are the math ellipsis in t_1,…,t_r (cards.json; list-notation, not omitted content). The changed lines L02.html:285 and L03.html:51 contain no banned string. PASS.",
    "SC1a-banned-phrases": f"banned_scan_r20.out: index.html, L01-L03.html: no banned hit; cards.json: only the list ellipsis t_1,…,t_r in math (not omitted content). PASS.",
    "SC1a-r16-banned-phrases": f"banned_scan_r20.out (same list, same result): no banned hit in the pages; PASS.",
    "SC1a-r18-banned-scan": f"banned_scan_r20.out: same result as r19 ({S}banned_scan_r20.out). PASS.",
    "SC1a-process-words": "grep (r20) over index.html, L01-L03.html and tests/labs/SC1/lab-SC1-L0n-1.py for round|builder|verifier|fragment|ledger|reviewer|agent|the learner|the student|we will|we now|as we saw|this build|pending review: no hits. PASS.",
    "SC1a-r10-process-words": "Same grep as SC1a-process-words (r20): no hits. PASS.",
    "SC1a-r16-process-words": "Same grep as SC1a-process-words (r20): no hits in index, L01-L03 or the twins. PASS.",
    "SC1a-r16-scope-words": "Scope words (only|all|always|every|any|same|drives|exactly) counted in L02.html and L03.html (r20 grep). The only changed lines are L02.html:285 (uses 'the same argument' in the skipped-step sentence, which states a gap rather than a universal claim) and L03.html:51 ('the same sums shrink to zero as the longest interval shrinks', a restatement of Prop 2.4(a)). Earlier scope rows evaluated the other hits and those lines are byte-identical. PASS.",
    "SC1a-r16-notation": "Changed lines introduce no symbol: L02.html:285 uses t^(k), s^(k), Sigma, Omega*, already in the same page before cd4dd7df; L03.html:51 uses 2^k, as before. notation/notation.json unchanged since cd4dd7df. PASS.",
    "SC1a-notation-macros": "Notation: only changed lines are L02.html:285 and L03.html:51; neither adds a macro or symbol (diff read). The other lines are byte-identical. PASS.",
    "SC1a-notation-no-registered-collision": "Changed lines add no symbol; notation/notation.json unchanged since cd4dd7df. PASS.",
    "SC1a-notation-T-subscript": "Changed lines add no T subscript; PASS.",
    "SC1a-r10-notation-collisions": "Changed lines add no symbol; notation/notation.json unchanged since cd4dd7df. PASS.",
    "SC1a-r18-notation-macros": "Changed lines add no macro; PASS.",
    "SC1a-r4-notation-S-symbol-L02": "L02.html:285 (changed) has no plain S in math (checked); L03.html:128 is unchanged. PASS.",
    "SC1a-r15-counts": f"cards_struct_r20.out: L01 25, L02 33, L03 24 (82 total); all cards 227 (cards.json); grade distribution T 49, C 6, none 27; index counts unchanged (index.html byte-identical). PASS.",
    "SC1a-r10-cards-dup-hypotheses": f"cards_struct_r20.out: exact duplicate fronts over all 227 cards: none; exact duplicate backs: none (c210's old back 'They are independent.' is replaced). PASS.",
    "SC1a-r11-cards-scan": "cards_L01_L03_r20.txt: all 227 cards parsed, 82 L01-L03 read (ledgers/SC1/scripts/SC1-a-r20/out/cards_L01_L03_r20.txt). PASS.",
    "SC1a-r13-cards-L01-L03-read": "Full read of the 82 L01-L03 cards this round (cards_L01_L03_r20.txt). PASS.",
    "SC1a-r14-cards-L01-L03-changed": f"cards_pin_delta_r20.out: changed L01-L03 cards are c030, c031, c210, c221, c224, c243; each re-read against its lesson this round (see SC1a-r19-card-c243 and the card rows). PASS.",
    "SC1a-r16-cards-L01-L03-full": "All 82 L01-L03 cards read this round (cards_L01_L03_r20.txt); each re-checked against its lesson section (for example c030/c031/c221 against Prop 2.4(b) steps 1-2, L02.html:145-165; c224 against step 3). PASS.",
    "SC1a-r16-cards-grade-field": ("cards_struct_r20.out: 27 L01-L03 cards carry no 'grade' key: c001-c004, c006, c018-c020, c033, c042, c043, c060, c184, c186, c188, c206-c213, c232-c234, c243. "
        "Each is a definition (c001-c004, c006, c018, c019, c042, c043, c184, c186, c243), a hypothesis statement (c020), or an assumption statement (c033, c060, c188, c206-c213, c232-c234), with no graded result; "
        "the card that previously stated a graded theorem without grade (SC1-c243) is now a definition. PASS."),
    "SC1a-r17-card-c017-definition-fixes": "SC1-c017 (cards.json, unchanged since 50559266) read this round: a misconception card with grade T and basis 'Section 4, with Remark 2.6 of Lesson 2 and A1(a), A1(b), A1(e), A2, Assumption 2.1(a)-(c) of Lesson 2'. PASS.",
    "SC1a-r18-card-c017": "Same as SC1a-r17-card-c017-definition-fixes (cards_L01_L03_r20.txt line for SC1-c017). PASS.",
    "SC1a-r18-cards-full-scan": ("Full read of all 82 L01-L03 cards this round (cards_L01_L03_r20.txt). Changed-card check: cards_pin_delta_r20.out lists exactly c030, c031, c210, c221, c224, c243 as changed since cd4dd7df; 76 cards byte-identical. "
        "Each changed card was checked against its lesson: c030 M_m=sqrt(2log2)sqrt(m)2^(-m/2) = lambda_m 2^(-(m+1)/2) with lambda_m=sqrt(4m log2) (H2, L02.html:148; step 1, :159); c031 step 1 (L02.html:159, Lemma 2.2(b)); c210 = A1(e) first sentence (L01.html:78); c221 step 2 (L02.html:161: sqrt m <= m, sum m r^m = r/(1-r)^2); c224 = Prop 2.4(b) hypotheses H1-H3 (L02.html:147-149, H3 'Assuming Assumption 2.1(a)-(c)') and step 3 (L02.html:162). PASS."),
    "SC1a-r19-card-c243": ("cards.json SC1-c243 now: front 'In Lesson 2, how is Σ(t) defined?', back 'Σ(t)=lim_M Σ_M(t), the pointwise limit of the partial sums, on the outcomes where the limit exists.' "
        "One fact (BUILDER_RULES §7); a definition, no graded content, so no grade or basis is required; the probability-one statement is covered by SC1-c032 and SC1-c220 (grade T, basis Prop 2.4). Definition 2.1 (L02.html:63-68) gives the same limit. PASS."),
    "SC1a-r19-c243-proposition-content": "The new SC1-c243 states no Proposition 2.4 content, so the old graded-content defect is gone. Prop 2.4 itself (L02.html:145-165, unchanged) is checked by SC1a-math-L02-prop2.4. PASS.",
    "SC1a-r19-cards-struct": f"cards_struct_r20.out: 227 distinct ids; L01-L03 82; grade/basis paired for all L01-L03 cards; cite lists empty; the four 'not found' items are false positives of the regex: 'Problem R1', 'Problem E3' (SC1-c052) and 'Problem R2' (SC1-c059) are problem titles R1 (L03.html:365), E3 (:354) and R2 (:372). PASS.",
    "SC1a-r19-delta-read": f"Delta read for d1083bf1: git diff cd4dd7df d1083bf1 touches course/modules/SC/SC1/L02.html (line 285), L03.html (line 51) and cards.json (6 cards). Every hunk read (see notes). PASS.",
    "SC1a-r18-delta-read": "See SC1a-r19-delta-read (round-20 delta read covers the same files).",
    "SC1a-r17-delta-read": "See SC1a-r19-delta-read; no other slice file changed since cd4dd7df.",
    "SC1a-r16-delta-read": "See SC1a-r19-delta-read.",
    "SC1a-r15-delta-read": "See SC1a-r19-delta-read.",
    "SC1a-r11-delta-read": "See SC1a-r19-delta-read.",
    "SC1a-r11-numbers-recomputed": "Numbers recomputed this round where they change: L03 |z| values and the 16 z in ±3 (twin_L03.stdout, see SC1a-r18-lab-L03-gap-13.22); no lesson number was changed except the wording at L02:285 and L03:51, which contain no number.",
    "SC1a-r18-lab-L03-gap-13.22": f"twin_L03.stdout: H=2, N=1 se 0.1601 vs formula 2*sqrt(2)/20 = 0.141421: relative gap +13.2%. z range from twin_L03.stdout: largest |z| 2.39 at H=1,N=2 (SC1-c051). PASS.",
    "SC1a-r16-math-proofs": "Math rows: changed line L02.html:285 is the sketch of A2 (re-checked, SC1a-math-L02-A2-sketch); L03.html:51 is the why-it-matters line (re-checked, SC1a-r17-hunk-L03-51). Other proof lines byte-identical. PASS.",
    "SC1a-r10-lab-L01-L02-L03-claims": "Lab docstrings (tests/labs/SC1/lab-SC1-L0n-1.py) byte-identical since cd4dd7df; L02/L03 page claims checked against twin output this round (page_vs_twin_r20.out). PASS.",
    "SC1a-r18-hunk-L02-51": "L02.html:51 byte-identical since cd4dd7df (not in the diff). PASS.",
    "SC1a-r18-hunk-L03-116": "L03.html:116 byte-identical since cd4dd7df. PASS.",
    "SC1a-r18-hunk-L03-260": "L03.html:260 byte-identical since cd4dd7df. PASS.",
    "SC1a-r18-hunk-L03-270": "L03.html:270 byte-identical since cd4dd7df; twin_L03.stdout 'H = 2, N = 128' line checked. PASS.",
    "SC1a-r18-hunk-L03-278": "L03.html:278 byte-identical since cd4dd7df. PASS.",
    "SC1a-hub-data-status": f"page_smoke SC1 PASS at d1083bf1 ({S}page_smoke_*.out); index.html byte-identical; L01.html byte-identical; L02/L03 changed lines carry no data claim. PASS.",
    "SC1a-structure-L01-L03": f"check_pages SC1 PASS and page_smoke PASS at d1083bf1 ({S}check_pages_SC1.out); L01.html byte-identical; L02.html and L03.html differ only at lines 285 and 51, which keep the section structure (no heading or block added). PASS.",
    "SC1a-r10-hub-concept-count": "dfn count on L01/L02/L03.html: 6, 3, 2 (grep this round). No changed line contains a <dfn>, so the concept definitions are unchanged; check_dag SC1 PASS at d1083bf1. PASS.",
}

rows = []
carried_prefix_files = ("index.html", "L01.html", "L02.html", "L03.html", "tests/labs", "ledgers", "notation", "references", "tools")
for r in PREV["rows"]:
    rid = r["id"]
    if rid in FRESH:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": FRESH[rid]})
    else:
        files = []
        for token in ("index.html", "L01.html", "L02.html", "L03.html"):
            if token in r["location"]:
                files.append(token)
        if "tests/labs" in r["location"] or "lab-SC1" in r["location"]:
            files.append("tests/labs/SC1 twins")
        if "ledgers/SC1/lab-mutants" in r["location"]:
            files.append("ledgers/SC1/lab-mutants (pre-r20 files)")
        if "notation/" in r["location"] or "notation.json" in r["location"]:
            files.append("notation/notation.json")
        if "references" in r["location"]:
            files.append("references/references.json")
        if "curriculum" in r["location"]:
            files.append("curriculum")
        if "BLUEPRINT" in r["location"]:
            files.append("BLUEPRINT.md")
        assert r["status"] == "PASS", rid
        scope = (" (only the cited spans; no cited span contains L02.html:285 or L03.html:51, the only changed lines in those pages since cd4dd7df)"
                 if any(t in files for t in ("L02.html", "L03.html")) else "")
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": f"Carried from round 19 ({', '.join(sorted(set(files))) or 'cited files'} byte-identical since the previous pin cd4dd7df{scope}): " + r["evidence"]})

MUT_NAMES = {}
mutants = []
kill_lines = open(os.path.join(OUT, "kill_lab_mutants_r20.out"), encoding="utf-8").read().splitlines()
for line in kill_lines:
    m = re.match(r"KILLED (\S+) \((L0\d)\): (.*)", line)
    if not m:
        continue
    path, lab, why = m.group(1), m.group(2), m.group(3)
    name = os.path.basename(path)
    if "SC1-a-r20/" in path:
        desc = {
            "r20-s1-L03-printed-sd-not-se.py": "Student error (L03): prints the sample standard deviation of the paths as 'se', not the standard error of the mean.",
            "r20-s2-L03-increment-variance-inverted.py": "Student error (L03): simulates increments with variance steps/horizon (reciprocal of the step length).",
            "r20-s3-L03-z-scaled-by-sqrt-paths.py": "Student error (L03): z computed with se/sqrt(PATHS), so every printed z is multiplied by 20.",
        }[name]
    else:
        desc = f"lab-twin mutant (demonstration, not a grader mutant): {name}"
    mutants.append({"id": path, "description": desc, "killed_by": f"kill_lab_mutants_r20.py: KILLED {path} ({lab}): {why}"})
n_killed = len(mutants)
assert n_killed == 41, n_killed

fragment = {
    "unit": "SC1",
    "slice": "a",
    "round": 20,
    "verifier": "Haiku 5.5 independent verifier, SC1-a round 20 (did not build SC1; no context shared with the builders)",
    "pin": "d1083bf1",
    "base": "cd4dd7df (round-19 pin). Round-19 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round19.json used as context. Row rule: carried only where the cited spans are byte-identical; every changed subject re-verified this round.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE20-SC1-a (detached at d1083bf1; .venv symlinked; vendor copied)",
    "scratch": "none; cards read with git show inside cards_pin_delta_r20.py (no temp files kept). Scripts under ledgers/SC1/scripts/SC1-a-r20/, outputs under ledgers/SC1/scripts/SC1-a-r20/out/. New lab mutants under ledgers/SC1/lab-mutants/SC1-a-r20/.",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "ROUND 20 at d1083bf1. Delta from cd4dd7df (round-19 pin), read hunk by hunk: course/modules/SC/SC1/L02.html line 285 (the A2 sketch: dyadic times t^(k) in [t,1] decreasing to t, plus the t=1 case); "
        "course/modules/SC/SC1/L03.html line 51 (why-it-matters wording); course/modules/SC/SC1/cards.json: SC1-c030, c031 ('Under H1 and H2'), c210 (A1(e) back), c221 ('H1 and H2'), c224 ('Assumption 2.1(a)-(c)'), c243 (rewritten as a definition). "
        "Unchanged since cd4dd7df (checked by git diff --stat restricted to paths): course/index.html and course/modules/SC/SC1/index.html, L01.html, L04-L08.html, project.html; tests/labs/SC1; ledgers/SC1/lab-mutants and mutants (pre-r20 files); notation/; references/; tools/; curriculum/; atlas/. "
        "Round-19 FAIL rows SC1a-r16-cards-grade-field, SC1a-r18-cards-full-scan, SC1a-r19-card-c243 are PASS now: c243 is a definition with no graded content; the 27 ungraded cards are all definitions, hypotheses or assumption statements. "
        "Plans/FINAL-ARCHITECT-RULINGS.md ruling 25 changed (E4 grader equivalence): not in slice a. "
        "Re-read this round: every changed hunk, all 82 L01-L03 cards, the 6 changed cards against the lesson text, the two changed lesson lines, the L03 twin output and expected blocks, all gates. "
        "Carried by byte-identity (not re-read line by line this round): the unchanged prose of index.html, L01.html, L02.html and L03.html, whose rows are carried with the span rule above. "
        "Lab twins: 41 mutants, 41 killed (38 carried from round 19, 3 new student-error mutants SC1-a-r20 r20-s1..s3). "
        "Not run: run_graders and mutate_graders (no grader in slice a); render_curriculum, build_site --check, fetch_data --check (outside slice a); the rendering in a browser (page_smoke Pyodide/Chromium output is the evidence). "
        "Not re-run this round: verify_refs live full registry (only --unit SC1 live and --offline)."
    ),
    "summary": {"text": "SC1-a round 20 at d1083bf1: PASS. Round-19 FAIL rows resolved; no new defect in the delta. Row count below.",
                "counts": {"PASS": len(rows), "FAIL": 0, "UNVERIFIABLE": 0}, "mutants": "41 of 41 lab-twin mutants killed"},
}
path = os.path.join(ROOT, "ledgers", "SC1", "SC1-a.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", path, "rows", len(rows), "mutants", len(mutants))
