"""Build ledgers/M4/M4-a.json (closing delta, round 1, verifier verifyG1-M4-a).

Carried rows take the base fragment's evidence under the carry prefix; every other row is fresh evidence
computed this round (scripts and outputs under ledgers/M4/scripts/M4-a-r1/).
"""
import json
import sys

BASE = "/Users/billyribeiro/.fanout/frags/F2-M4-a.round1.json"
OUT = "ledgers/M4/M4-a.json"
S = "ledgers/M4/scripts/M4-a-r1"

base = json.load(open(BASE, encoding="utf-8"))
brows = {r["id"]: r for r in base["rows"]}


def carry(rid, files, override=None):
    ev = override if override is not None else brows[rid]["evidence"]
    return {
        "id": rid,
        "check": brows[rid]["check"],
        "location": brows[rid]["location"],
        "status": "PASS",
        "evidence": f"Carried from round 1 ({files} byte-identical since the previous pin 95f3f8cb): " + ev,
    }


def fresh(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row


M4 = "course/modules/M/M4"
SRC_UNCHANGED = "course/modules/M/M4/L02.html, L03.html, L04.html and project.html"
LAB = "tests/labs/M4/*.py"
GATE_UNCHANGED = "tests/labs/M4/*.py, tools/*, notation/notation.json, references/references.json, curriculum/01-foundations.yaml"

rows = []
# ---- gates (re-run this round) ----
rows.append(fresh("A-G01", "2.9 structure gate", "tools/check_pages.py --unit M4",
    f"tools/check_pages.py --unit M4 -> 'check_pages M4: PASS', exit 0 ({S}/check_pages.out)"))
rows.append(fresh("A-G02", "2.9 DAG gate", "tools/check_dag.py --unit M4",
    f"tools/check_dag.py --unit M4 -> 'check_dag M4: PASS', exit 0 ({S}/check_dag.out)"))
rows.append(fresh("A-G03", "2.6 projects gate (command row; project.html outside slice a)", "tools/check_projects.py --unit M4",
    f"tools/check_projects.py --unit M4 -> 'check_projects M4: PASS', exit 0 ({S}/check_projects.out); project.html is byte-identical since 95f3f8cb"))
rows.append(fresh("A-G04", "2.5 labs", "tools/run_labs.py --unit M4",
    f"tools/run_labs.py --unit M4 -> 'run_labs M4: PASS (13/13)', exit 0 ({S}/run_labs.out)"))
rows.append(carry("A-G05", f"{LAB} and the lab code blocks of L02, L03, L04.html",
    override=brows["A-G05"]["evidence"] + ". Re-run this round: python -I -W error tests/labs/M4/lab-M4-L01-1.py exit 0, output in "
    f"{S}/twin_L01.out; L01 lab code blocks unchanged (the delta touches L01.html:277 and :280 only, outside the lab at L01.html:138-271)."))
rows.append(fresh("A-G06", "2.9 page_smoke (pages alone)", "tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04",
    f"tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04 -> 'page_smoke M4: PASS', exit 0 ({S}/page_smoke.out)"))
rows.append(carry("A-G07", GATE_UNCHANGED + " (no .py changed under tests/labs/M4 or course/modules/M/M4)"))
rows.append(carry("A-G08", GATE_UNCHANGED + " (no .py changed since the previous pin)"))
rows.append(fresh("A-G09", "repository state", "git status after all gate runs",
    "git status in the checkout after the gates: tracked changes only under ledgers/M4/scripts/M4-a-r1/ (this round's scratch "
    "outputs, overwriting same-named files at the pin); untracked .venv symlink. No course, tool, test, reference, curriculum "
    "or notation file is modified. Nothing committed or pushed."))
rows.append(carry("A-G10", "tools/ and tests/ (no test or tool under the M4 slice changed)",
    override=brows["A-G10"]["evidence"] + ". Not re-run this round: no test or tool file consumed by the M4 slice changed; "
    "the test_page_checks path was exercised through check_pages (A-G01)."))
rows.append(carry("A-G11", "references/references.json and tools/verify_refs.py",
    override=brows["A-G11"]["evidence"] + ". Re-run this round: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 "
    f"({S}/verify_refs_offline.out). The live Crossref run was not repeated this round (see freshness_flags)."))
rows.append(fresh("A-G12", "2.7 card numbers; no dangling card ids", "course/modules/M/M4/cards.json vs L01..L04.html",
    "Re-run: cards.json holds 219 ids (M4-c001..c263 with gaps). No page or card in M4 names M4-c014, M4-c028, M4-c065, "
    "M4-c219 or M4-c244 (grep of course/modules/M/M4/ and tests/labs/M4 returns no hit; the ids are absent at HEAD and at 95f3f8cb). "
    "Per-card lesson references checked by script (see CARDS-NUMBERS)."))
rows.append(fresh("A-G13", "2.8 generated site data (not edited)", "tools/build_site.py --check",
    f"tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 ({S}/build_site_check.out)"))
rows.append(fresh("A-G14", "2.8 data manifest", "tools/fetch_data.py --check",
    f"tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 ({S}/fetch_data_check.out)"))
rows.append(fresh("A-G15", "generated curriculum current", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
    "tools/render_curriculum.py exit 0, then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (no diff)"))

# ---- hub (index.html) ----
rows.append(fresh("A-H01", "2.9 structure: hub", "course/modules/M/M4/index.html:29-184",
    "index.html changed only at line 135 (the rung-1 explain paragraph, see A-H16). Sections, classes and data attributes at :29-184 are byte-identical to 95f3f8cb; check_pages M4 PASS (A-G01)."))
rows.append(carry("A-H02", "index.html:29 and the lesson data-hours attributes",
    override=brows["A-H02"]["evidence"] + " (line 29 not in the delta)."))
rows.append(carry("A-H03", "index.html:48-56"))
rows.append(carry("A-H04", "index.html:58-66 and curriculum/01-foundations.yaml"))
rows.append(fresh("A-H05", "DAG: no M3 concept by name", "course/modules/M/M4/index.html (whole file)",
    "The only changed hub text (index.html:135) introduces 'rank', 'sorted losses' and 'distinct', none of which is an M3 concept name. M4 prerequisites are [M2] (curriculum/01-foundations.yaml:195). The hub's M3 mention (index.html:64) is byte-identical."))
rows.append(fresh("A-H06", "placement structure", "course/modules/M/M4/index.html:68-143",
    "index.html:68-143 re-read: the quiz section, ten items and their data attributes are unchanged except the explain text at :135 (A-H16). Structure unchanged."))
rows.append(carry("A-H07", "index.html:73-131"))
rows.append(carry("A-H08", "index.html:140, course/modules/M/M4/L06.html and index.html line 140"))
rows.append(fresh("A-H09", "2.9 placement skill check 1 (rung 1) key", "course/modules/M/M4/index.html:133-135",
    "Key re-derived: values 0, 1, 2 with probabilities 1/4, 1/2, 1/4 -> F(0)=1/4 < 1/2 <= 3/4=F(1); the 0.5 quantile under Definition 3.1 is 1. "
    "index.html:133 data-answer=\"1\" data-tolerance=\"0\" matches. The explain sentences on F and Proposition 3.2 are correct (values distinct, Proposition 3.2 hypotheses hold). "
    "The residual 'same convention as rung 1' sentence in the same paragraph is recorded under A-H16."))
rows.append(carry("A-H10", "index.html:147-160 and L01..L04.html headings"))
rows.append(carry("A-H11", "index.html:70, :164 and course/modules/M/M4/project.html:42"))
rows.append(carry("A-H12", "index.html:37, :175, :187 and L02.html:146, L03.html:122"))
rows.append(carry("A-H13", "index.html:181-183 and references/references.json (key blitzstein2019introduction)"))
rows.append(carry("A-H14", "curriculum/01-foundations.yaml:190-194"))
rows.append(carry("A-H15", "index.html:162-170 and project.html:42-47"))
rows.append(fresh("A-H16", "hub claim: rung 1 worked example (round-1 FAIL; closing delta)", "course/modules/M/M4/index.html:135",
    "The base defect is fixed: the paragraph no longer cites Proposition 3.4 for rung 1. Residual defect: the sentence 'The same convention as rung 1 applies: the quantile is the least value whose distribution function reaches the level (Lesson 1, Proposition 3.2)' asserts that rung 1's rank rule is the Definition 3.1 quantile, but Proposition 3.2 (L01.html:103, 'with distinct values') and Proposition 3.4 (L01.html:119, 'distinct real numbers') both require distinct values, and rung 1's losses are whole cents that repeat: I ran the rung-1 code of project.html (its data-run block 1, output matching its expected block) and counted 616 extra copies in the Gaussian sample and 680 in the Student-t sample. The same paragraph concedes Proposition 3.4 covers distinct values only, so the identity for repeated losses is asserted and not proved on any M4 page (project.html:441 sits inside Exemplar B, an annotated exemplar, not a proof). The paragraph is internally inconsistent: it asserts the equivalence and then says the proposition does not cover it.",
    status="FAIL",
    fix="In course/modules/M/M4/index.html:135 delete the sentence 'The same convention as rung 1 applies: the quantile is the least value whose distribution function reaches the level (Lesson 1, Proposition 3.2).' and end the paragraph with: 'Rung 1 takes the rank \\(\\lceil 0.99\\, n \\rceil\\) of its sorted losses (project.html, Rungs 1 and 2). Proposition 3.4 proves that rank for distinct values only, and the whole-cent losses of rung 1 can repeat, so this lesson does not prove the rank for repeated values.' Keep the first sentences on F and Proposition 3.2 unchanged. Then re-run check_pages --unit M4 and page_smoke for index."))

# ---- lesson L01 (only the Proposition 3.4 hunk changed) ----
rows.append(carry("L01-PROSE", "course/modules/M/M4/L01.html:51-99", override=brows["L01-PROSE"]["evidence"] + " (lines 51-99 not in the delta)."))
rows.append(carry("L01-MATH", "course/modules/M/M4/L01.html:80-135 (Proposition 3.4 statement at :119 unchanged)"))
rows.append(carry("L01-DELTA-86", "course/modules/M/M4/L01.html:85-86"))
rows.append(carry("L01-PROBLEMS", "course/modules/M/M4/L01.html:302-404 (includes the forty-value problem at :326, which says 'forty distinct values')"))
rows.append(carry("L01-QUIZ", "course/modules/M/M4/L01.html:424-494"))
rows.append(carry("L01-GRADES", "course/modules/M/M4/L01.html:43-48, :103, :113, :119, :413-418"))
rows.append(carry("L01-FWD", "course/modules/M/M4/L01.html:37-38, :95, :505"))
rows.append(carry("L01-LAB", "course/modules/M/M4/L01.html:138-271 and tests/labs/M4/lab-M4-L01-1.py"))
rows.append(fresh("L01-P34-HYP", "every use of Proposition 3.4 states or meets its distinct-values hypothesis (the Prop 3.4 hypothesis is the subject changed by this delta)",
    "course/modules/M/M4/L01.html:297 (misconception 3); Prop 3.4 statement at L01.html:119; other uses at :277, :280, :326, :416, :452, :457 and the cards at cards.json lines 68, 75, 96, 97",
    "L01.html:297 reads 'Proposition 3.4 gives the index ... The 149th value is the one whose distribution function reaches 0.99 in the list of 150 equally likely values.' Proposition 3.4 (L01.html:119) requires n distinct real numbers, and the sentence omits 'distinct'. Every other use checked: :277 and :280 (this delta, now 'distinct'), :326 ('forty distinct values'), :416 ('For n distinct equally likely values'), :452 and :457 ('distinct losses'), cards.json lines 68, 75, 96, 97 ('distinct'). Only :297 omits the hypothesis.",
    status="FAIL",
    fix="In course/modules/M/M4/L01.html:297 change 'in the list of 150 equally likely values' to 'in the list of 150 equally likely distinct values' (and, if the quoted wrong claim is read as a 150-value list, state it as 'for 150 equally likely distinct values'). Then re-run check_pages --unit M4 and page_smoke for L01."))
rows.append(fresh("DELTA-L01-P34-DISTINCT", "delta: Proposition 3.4 'distinct' wording in the canon-breaks list",
    "course/modules/M/M4/L01.html:277 and :280",
    "Changed hunk (git diff 95f3f8cb..2a805c83, L01.html @@ -274,10 +274,10 @@). :277 'Proposition 3.4 is Definition 3.1 applied to equally likely distinct values, and it gives the ceiling index' and :280 'Proposition 3.4 is an exact statement about n equally likely distinct values' match the Proposition 3.4 statement at L01.html:119 ('n >= 1 distinct real numbers'). The Example 3.6 claim at :277 (Q(3/5)=0 under Definition 3.1; strict rule gives 1) matches L01.html:134-137 and the twin output (Q(3/5) = 0)."))

# ---- lessons L02, L03, L04 (unchanged) ----
for rid in [r for r in brows if r.startswith(("L02-", "L03-", "L04-"))]:
    rows.append(carry(rid, "course/modules/M/M4/" + rid[:3] + ".html and tests/labs/M4/lab-M4-" + rid[:3] + "-1.py"))

# ---- cards ----
rows.append(fresh("CARDS-DUP", "2.7 duplicate cards (full scan of the slice cards)", "course/modules/M/M4/cards.json",
    "Script (ledgers/M4/scripts/M4-a-r1/): no exact duplicate front text among 219 cards. Near-duplicate scan (difflib ratio > 0.6) for the changed or added cards: M4-c258 vs M4-c062 (0.76; c062 asks E[X|Y=0], c258 asks whether E[X|Y=y] is constant in y), M4-c263 vs M4-c012 (0.95; Q(1/2)), M4-c245 (0.92; Q(3/5)), M4-c192 (0.78; for which p). Different questions, not duplicates. M4-c028 and M4-c065 are absent (no duplicate pair remains)."))
rows.append(fresh("CARDS-L01", "2.7 cards L01 (verdict and listing re-derived)", "course/modules/M/M4/cards.json (lesson L01)",
    "24 L01 cards at HEAD: M4-c001..c013, c015, c016, c173, c192..c195, c197, c198, c245, c263 (the base listing included c014, which is absent at both pins). Added card M4-c263 verified (DELTA-CARD-C263). The other 23 cards are byte-identical since 95f3f8cb (not in the id diff) and carry the base verdict."))
rows.append(fresh("CARDS-L02", "2.7 cards L02 (listing corrected)", "course/modules/M/M4/cards.json (lesson L02)",
    "20 L02 cards at HEAD: M4-c017..c027, c029..c033, c181, c182, c199, c243 (M4-c028 is absent at both pins; the base listing included it). No L02 card changed in this delta; verdict carried from round 1 (cards byte-identical since 95f3f8cb). Carried from round 1: " + brows["CARDS-L02"]["evidence"]))
rows.append(carry("CARDS-L03", "course/modules/M/M4/cards.json lesson L03 entries (27 cards, none changed)"))
rows.append(fresh("CARDS-L04", "2.7 cards L04 (listing corrected; new card verified)", "course/modules/M/M4/cards.json (lesson L04)",
    "19 L04 cards at HEAD: M4-c049..c064, c201, c204, c258 (M4-c065 is absent at both pins; the base listing included it). Added card M4-c258 verified (DELTA-CARD-C258). The other 18 cards are byte-identical since 95f3f8cb and carry the base verdict."))
rows.append(fresh("CARDS-DELTA", "delta: cards changed or added in this range", "course/modules/M/M4/cards.json (git diff 95f3f8cb..2a805c83)",
    "Id-level diff of cards.json: removed ids none; added M4-c258 (L04), M4-c259 (L09), M4-c260, c261, c262 (L10), M4-c263 (L01); changed M4-c079 (L05). The L09 and L10 cards are outside this slice (see notes) and are not verified here. The base row's delta description (c023 text, c192 hypotheses, c244 deleted, c245 added) does not match this range and is not used."))
rows.append(fresh("CARDS-NUMBERS", "2.7 card numbers appear in their lesson", "course/modules/M/M4/cards.json (90 slice cards: L01 24, L02 20, L03 27, L04 19) vs L01..L04.html",
    "Script: every 'Example x.y', 'Proposition x.y', 'Remark x.y', 'Definition x.y', 'Lab n', 'Problem X' and 'Assumption n' reference in the 90 slice cards occurs in its lesson text, except 'Problem P3' in M4-c064, which is the heading 'P3 · Disjoint events have a negative covariance' (L04.html:376-377). Not a defect."))
rows.append(fresh("CARD-M4-c219", "round-11 row kept by id", "course/modules/M/M4/cards.json",
    "M4-c219 is absent at HEAD (script: id not present in the 219-card set), as it was at 95f3f8cb."))
rows.append(fresh("DELTA-CARD-C079", "delta: card M4-c079 (lesson L05) text", "course/modules/M/M4/cards.json (M4-c079); L05.html:118, :281, :293, :483, :422",
    "Front 'Does a zero correlation show that there is no nonlinear relation between X and Y?' and back 'No. Remark 1.8 gives Y = X^2 with X uniform on {-1, 0, 1}: the correlation is 0, while Y is a function of X. Correlation measures only linear association.' matches L05.html:293 (the same example, correlation 0, Y a function of X) and the Remark 1.8 title at :118 ('correlation measures linear association'); L05.html:422 grades it T. Scope word 'only' is the standard gloss of a linear measure; not a computed claim beyond Remark 1.8 (see notes)."))
rows.append(fresh("DELTA-CARD-C258", "delta: new card M4-c258 (L04)", "course/modules/M/M4/cards.json (M4-c258); L04.html:168-172 (Example 2.5), :326",
    "Example 2.5 table (L04.html:169): p(0,0)=1/10, p(0,1)=3/10, p(1,0)=2/10, p(1,1)=2/10, p(2,0)=1/10, p(2,1)=1/10. Recomputed: P(Y=0)=2/5, P(Y=1)=3/5, E[X]=4/5, E[X|Y=0]=1, E[X|Y=1]=2/3, and the conditional expectations differ, so E[X|Y=y] is not constant in y. The back 'No. E[X | Y = 0] = 1 and E[X | Y = 1] = 2/3, while E[X] = 4/5 (Example 2.5)' matches. Grade T is arithmetic on a finite table. L04.html:326 states the same three values."))
rows.append(fresh("DELTA-CARD-C263", "delta: new card M4-c263 (L01)", "course/modules/M/M4/cards.json (M4-c263); L01.html:134-137 (Example 3.6)",
    "Example 3.6 (L01.html:134-137): F(0)=3/5, F(1)=4/5, so 3/5 < 61/100 <= 4/5 = F(1); Proposition 3.2 gives Q(61/100)=1. Card back '1, because F(0) = 3/5 < 61/100 <= 4/5 = F(1) (Example 3.6)' matches. Twin output 'Q(61/100) = 1' (scripts/twin_L01.out). Grade T from Proposition 3.2 (L01.html:103, data-grade T)."))
rows.append(carry("DELTA-CARD-C023", "course/modules/M/M4/cards.json (M4-c023 is not in the id diff)"))
rows.append(fresh("DELTA-CARD-REMOVALS", "delta: removed duplicate cards M4-c028 and M4-c065", "course/modules/M/M4/cards.json",
    "No removal occurs in 95f3f8cb..2a805c83 (id diff: removed none). M4-c028 and M4-c065 are absent at both pins and no M4 page or card names them (A-G12). No duplicate remains (CARDS-DUP)."))

# ---- notation, process, scope, numbers, grades, structure, DAG, data ----
rows.append(fresh("NOTATION-A", "2.4 / notation registry (changed lines)", "course/modules/M/M4/index.html:135; L01.html:277, :280; notation/notation.json",
    "Changed lines use only symbols already in the base line 135 and L01 (F, Q, p, n, \\lceil \\rceil, \\tfrac, \\ge). notation/notation.json is byte-identical since 95f3f8cb. Observation (not a delta defect, unchanged from base): \\lceil and \\rceil have no notation.json entry at either pin."))
rows.append(carry("NOTATION-REG", "course/modules/M/M4/L03.html:75-86 and notation/notation.json"))
rows.append(fresh("NOTATION-MACRO", "registered macros only (changed lines)", "course/modules/M/M4/index.html:135; L01.html:277, :280",
    "The macros in the changed lines (\\lceil, \\rceil, \\tfrac, \\ge, \\(, \\)) are the same set as in the base line 135; no new macro introduced."))
rows.append(fresh("PROCESS-A", "2.9 process words in learner text (changed text)", "course/modules/M/M4/index.html:135; L01.html:277, :280; cards.json M4-c079, c258, c263",
    "No process word (build, agent, verifier, round, ruling, delta, check-list) in the changed text."))
rows.append(fresh("SCOPE-A", "scope words (changed text)", "course/modules/M/M4/index.html:135; L01.html:277, :280; cards.json M4-c079, c258, c263",
    "Scope words in the changed text: 'same' at L01.html:277 ('the strict rule returns 1 at the same p', true at p = 3/5 by Example 3.6 and the twin output 'Q(3/5)=0' vs strict rule 1); 'same' removed from index.html:135 by the A-H16 fix; 'only' in M4-c079 back ('measures only linear association', see DELTA-CARD-C079, a gloss, not a computed claim)."))
rows.append(carry("DATA-A", "course/modules/M/M4/index.html:37, :175, :187 and L02.html:146, :507, L03.html:122, :477 (no data-files attribute added)"))
rows.append(carry("STRUCT-A", "course/modules/M/M4/L01..L04.html structure and section tags (the L01 delta is text inside existing <li> elements at :277 and :280)"))
rows.append(fresh("NUM-A", "2.2 numbers in prose (changed text)", "course/modules/M/M4/index.html:135; L01.html:277; cards M4-c079, c258, c263",
    "index.html:135: F(0)=1/4 < 1/2, F(1)=3/4 >= 1/2, quantile 1 (re-derived). L01.html:277: Q(3/5)=0 (Example 3.6, twin output). Cards: c258 values 1, 2/3, 4/5 (re-derived); c263 Q(61/100)=1 (Example 3.6); c079 correlation 0 for Y=X^2 with X uniform on {-1,0,1} (E[X]=0, E[XY]=E[X^3]=0)."))
rows.append(carry("GRADE-A", "course/modules/M/M4/index.html, L01..L04.html grade tables and cards.json (unchanged entries)",
    override=brows["GRADE-A"]["evidence"] + ". Changed or added cards graded here: M4-c079 T (L05.html:422 grade table T), M4-c258 T (finite-table arithmetic), M4-c263 T (Proposition 3.2)."))
rows.append(carry("ASSUMP-A", "course/modules/M/M4/index.html:138-140 and L01..L04.html (no assumption added by the delta)"))
rows.append(fresh("DAG-A", "2.9 DAG and definitions once", "check_dag.py --unit M4; L01..L04.html dfn tags",
    f"tools/check_dag.py --unit M4 -> 'check_dag M4: PASS' ({S}/check_dag.out). The delta adds no <dfn> element and no concept link (grep of the changed hunks)."))
rows.append(carry("DAG-HUB-PREVIEW", "course/modules/M/M4/index.html:147-160"))
rows.append(carry("DAG-L02-L04-USES", "course/modules/M/M4/L02.html, L03.html, L04.html meta lines 37-39"))
rows.append(carry("DAG-SD-TWICE", "course/modules/M/M5/L05 path course/modules/M/M4/L05.html:79-80 and L02.html:100-101 (both byte-identical)".replace("course/modules/M/M5/L05 path ", "")))
rows.append(carry("DELTA-L01-META", "course/modules/M/M4/L01.html:7"))
rows.append(carry("DELTA-HUB-LADDER-LINK", "course/modules/M/M4/index.html:70"))

rows = [r for r in rows if r is not None]
# drop duplicate ids (DELTA-CARD-C023 was added once above)
seen = set()
uniq = []
for r in rows:
    if r["id"] in seen:
        continue
    seen.add(r["id"])
    uniq.append(r)
rows = uniq

missing = [rid for rid in brows if rid not in seen]
if missing:
    sys.exit(f"base ids not covered: {missing}")

counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows)}
verdict = "PASS" if counts["FAIL"] == 0 else "FAIL"

fragment = {
    "unit": "M4",
    "slice": "a",
    "round": 1,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyG1-M4-a)",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-M4-a",
    "scratch": "ledgers/M4/scripts/M4-a-r1/",
    "verified_at": "2026-11-09",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"],
    "freshness_flags": [
        "tools/verify_refs.py live (Crossref) run not repeated this round; A-G11 live half is carried from the base fragment (references/references.json byte-identical since 95f3f8cb)."
    ],
    "notes": (
        "Closing delta (rulings 30, 37) of slice a, base F2-M4-a.round1 at 95f3f8cb, pin 2a805c83. "
        "Delta computed by git diff 95f3f8cb..2a805c83 over course/modules/M/M4 (only L01.html :277 and :280, index.html :135, cards.json: M4-c079 changed, M4-c258..c263 added; no removals). "
        "The base fragment's notes described a delta from another lineage (pin 329c1d7f: index.html:70, L01.html:7, L02.html:151-158, lab-M4-L02-1 docstring, cards c023 text, c028/c065 removal); none of those hunks exists in 95f3f8cb..2a805c83 (verified: L02.html, L03.html, tests/labs/M4 and index.html:70 are byte-identical). "
        "The base card listings contained ids absent at both pins (M4-c014, c028, c065); corrected above. Base slice-card total 90 is correct at HEAD (L01 24, L02 20, L03 27, L04 19). "
        "Scope: slice a = course/modules/M/M4/index.html, L01..L04.html, cards.json for L01..L04 and the changed M4-c079; not verified here: L05..L10 pages and cards (except the cross-reference and the M4-c079 card), project.html content, and the new L09 and L10 cards M4-c259 to c262 (outside slice a per the base scope). "
        "Observations, not rows (ruling 30): cards.json M4-c079 back uses the word 'only'; notation/notation.json has no entry for \\lceil or \\rceil (same at both pins); the scratch .out files at ledgers/M4/scripts/M4-a-r1/ are tracked at HEAD and were overwritten by this round's outputs, not committed. "
        "Mutants: slice a has no grader; ruling 37 writes no mutants and the standing set for slice a is empty. "
        "Ruling 26 kinds found: two FAIL rows (A-H16, L01-P34-HYP), both missing-hypothesis / unproved-application defects in the Proposition 3.4 and rung-1 wording. Both need a fix and a delta re-verification under ruling 30."
    ),
    "summary": (
        f"Closing delta round 1 at 2a805c83 (base 95f3f8cb): {len(rows)} rows; {counts['PASS']} PASS, {counts['FAIL']} FAIL, 0 UNVERIFIABLE. "
        "The base A-H16 defect (Proposition 3.4 cited for rung 1 with repeated losses) is removed, but the paragraph still asserts the least-value convention for repeated losses, which no M4 page proves. "
        "New FAIL L01-P34-HYP: L01.html:297 applies Proposition 3.4 to '150 equally likely values' without 'distinct'. Verdict FAIL."
    ),
}

problems = __import__("json").dumps(fragment)  # sanity: serialisable
json.dump(fragment, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", OUT, "rows", len(rows), counts, verdict)
