import json, sys
C7 = "Carried from round 7 (cited subject lines byte-identical since the round-7 pin 7aa909e; round-8 delta hunks are index.html:62,159; L01.html:51; L02.html:121; L04.html:214,222,327,355,371, none inside the cited lines; tests/labs/M5 L01-L04 twins unchanged): "
rows = []
def R(id, check, loc, status, ev, fix=None):
    r = {"id": id, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)
def carry(id, check, loc, prior):
    R(id, check, loc, "PASS", C7 + prior)

# ---- gates (run fresh this round)
R("M5a-gate-check-pages", "check_pages --all, M5 entry", "tools/check_pages.py", "PASS",
  "Run this round: 'check_pages M5: PASS' (ledgers/M5/scripts/M5-a-r8/gates.out).")
R("M5a-gate-check-dag", "check_dag --all, M5 entry", "tools/check_dag.py", "PASS",
  "Run this round: 'check_dag M5: PASS' (gates.out).")
R("M5a-gate-check-projects", "check_projects --all, M5 entry", "tools/check_projects.py", "PASS",
  "Run this round: 'check_projects M5: PASS' (gates.out).")
R("M5a-gate-run-labs", "run_labs --unit M5 (twin==page code, twin run, expected==output)", "tools/run_labs.py", "PASS",
  "Run this round: 'run_labs M5: PASS (13/13)' (gates.out).")
R("M5a-twins-isolated", "Each twin under venv python -I -W error, empty env, empty stderr",
  "tests/labs/M5/lab-M5-L01-1.py..L04-1.py", "PASS",
  "Run this round: env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 .venv/bin/python -I -W error on all four: exit 0, stderr 0 bytes (L01.err, L02.err, L03.err, L04.err); stdout 17, 7, 5, 11 lines (L0n.out).")
R("M5a-gate-page-smoke", "page_smoke --unit M5 --pages index L01 L02 L03 L04 --skip-sweep",
  "tools/page_smoke.py", "PASS",
  "Run this round: 'page_smoke M5: PASS' (gates.out). Figure control-state sweep skipped (no figures in M5 slice pages).")
R("M5a-gate-ruff-mypy-pytest", "ruff check ; ruff format --check ; mypy --no-incremental ; pytest test_labs -k M5 ; pytest test_page_checks + test_docs_figures",
  "repo gates", "PASS",
  "Run this round: ruff 'All checks passed!' (ruff.out); format '362 files already formatted'; mypy 'Success: no issues found in 255 source files' (mypy.out); pytest test_labs -k M5 '13 passed, 227 deselected' (pytest_labs_M5.out); page_checks+docs_figures '55 passed' (pytest_page_docs.out).")
R("M5a-gate-verify-refs-offline", "verify_refs --offline", "tools/verify_refs.py", "PASS",
  "Run this round: 'offline integrity: 560 entries, 0 problems'. Live Crossref run not performed.")
R("M5a-gate-build-site-check", "build_site --check (concept index and site data current after L04 and L02 edits)",
  "tools/build_site.py", "PASS",
  "Run this round: 'site data current: 6 outputs', exit 0 (ledgers/M5/scripts/M5-a-r8/build_site_check.out).")

# ---- hub
carry("M5a-hub-numbers", "Hub numbers recomputed", "course/modules/M/M5/index.html:71,97,101,106,111,116,121",
  "Delta does not touch these lines. 7/9=77.78%, 8/9=88.89%; 1/1.05=0.9523809 vs 0.952381 diff 4.8e-8; 2^k sum k=0..3=15; sum (1/2)^n n=0..4=31/16=1.9375.")
carry("M5a-hub-hours", "Hub hours arithmetic", "course/modules/M/M5/index.html:29,31,40,42,131",
  "Hub hours lines untouched by the round-8 delta. 6*10+4*11=104; 104+26=130; 26/130=20%.")
carry("M5a-hub-placement-crossrefs", "Hub (M1, Lesson n) and M2 concept citations", "course/modules/M/M5/index.html:80,89,94,99,104,109,114,119,124",
  "Citation lines untouched by the round-8 delta.")
R("M5a-hub-data-claims", "Hub data claims (changed line 159 re-verified)", "course/modules/M/M5/index.html:37,159", "PASS",
  "Fresh: index.html:159 now reads 'Where a lesson shows numbers from a generated case, it labels them SIMULATED (Lessons 8 to 10 do)'. grep -c SIMULATED: L08.html:138 (simulated-label), L09.html:132, L10.html:177 each carry one label; L01-L07 pages carry none, and their twins draw no random numbers (grep 'random|seed' over tests/labs/M5/lab-M5-L0[1-7]-1.py: only 'No randomness'/'No random draws' statements; L08 twin seed at lab-M5-L08-1.py:23 is labelled on L08). No currency token in any M5 page text (python scan of all course/modules/M/M5/*.html for $ EUR GBP dollar currency cents: no hits). index.html:37 unchanged ('Data: none').")
R("M5a-hub-prereq-M2-definite-integral", "Hub prerequisite bullet is consistent with Lesson 10 use of M2 definite integral", "course/modules/M/M5/index.html:62 vs course/modules/M/M5/L10.html:78-117 (Section 2) and L10.html:80,96,111,114", "PASS",
  "Round-7 FAIL resolved. index.html:62 now says Lesson 10 'its proofs use the M2 Darboux definition of the definite integral for the ordinary integral (Lesson 10, Section 2)'. L10.html:78 is the Section 2 heading; L10.html:80 'The proofs below use the definite integral of M2 in its Darboux form'; L10.html:96,111,114 cite M2 Lesson 9 Definition 1.3, which is the Darboux definition (course/modules/M/M2/L09.html:85 Definition 1.3, :90 Remark 1.4 'the definition is the Darboux form'). Scope note (not a FAIL): Section 3 proofs (L10.html:131 onward) integrate ordinary integrals without naming Darboux; the sentence's locator (Section 2) bounds the claim.")
R("M5a-hub-theorems-proved-L1-4", "Hub claim that every theorem in Lessons 1-4 is proved on its page (changed proof L02.html:121 re-checked)", "course/modules/M/M5/index.html:168; L01-L04 blocks", "PASS",
  "Fresh: L02.html:121 proof of the greatest-lower-bound theorem is still present and complete after the C->D rename (see M5a-L02-thm-2.5-and-remark-2.6). No other theorem block of L01-L04 changed in the delta.")
carry("M5a-hub-prose-objectives-cards", "Hub objectives and card prose", "course/modules/M/M5/index.html:49-55,133-142",
  "Objective list and card lines untouched (line 62 is not in 49-55 or 133-142).")
carry("M5a-hub-P0.1-links", "P0.1 placeholder links", "course/modules/M/M5/index.html:35,64",
  "Lines 35 and 64 untouched by the round-8 delta.")
carry("M5a-hub-grade-legend-cosmetic", "Grade-legend wording (observation)", "course/modules/M/M5/L04.html:44-49 vs L01.html:43-48",
  "Lines untouched by the round-8 delta.")
carry("M5a-hub-skill-check-rung2", "Rung-2 skill-check explain text, changed line", "course/modules/M/M5/index.html:124",
  "index.html:124 not in the round-8 delta.")

# ---- notation
R("M5a-notation-registry", "Symbols vs notation/notation.json (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q)", "course/modules/M/M5/index.html, L01-L04", "PASS",
  "Fresh: notation/notation.json holds 8 symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}). The round-8 changed lines introduce only ell^infty(S), D and '(§3)'; neither ell^infty nor D is registered (grep 'ell' over notation.json: 0 hits), both are defined where used (L04.html:214; L02.html:121). No registered symbol takes a new meaning.")

# ---- L01
R("M5a-L01-why-it-matters", "Why-it-matters sentence (changed) and its cross-references", "course/modules/M/M5/L01.html:51", "PASS",
  "Fresh: L01.html:51 now reads 'a rational supremum would have square 2 by Proposition 1.7 (§3), which M1, Lesson 2, Corollary 2.6 rules out'. Proposition 1.7 is at L01.html:234 inside section 3 (h2 id=s3 at L01.html:110; section 4 starts at L01.html:251), so '(§3)' is correct. '(defined in §1)' and '(defined in §3)' unchanged and correct.")
R("M5a-L01-M1-cor-2.6-citation", "M1 Lesson 2 Corollary 2.6 citation in L01 why-it-matters", "course/modules/M/M5/L01.html:51; course/modules/M/M1/L02.html:132-133", "PASS",
  "Fresh: course/modules/M/M1/L02.html:132-133 'Corollary 2.6 (no rational number has square 2): There is no rational number r with r^2 = 2.' The cited sentence in L01.html:51 is accurate.")
carry("M5a-L01-lab-1", "Lab 1 bisection predictions, twin, expected block", "course/modules/M/M5/L01.html lab section; tests/labs/M5/lab-M5-L01-1.py",
  "Lab section and twin unchanged in the round-8 delta; run_labs and isolated twin run re-run this round (gates.out, L01.out).")
carry("M5a-L01-prop-1.7", "Proposition 1.7 and the interpretation paragraph after its proof", "course/modules/M/M5/L01.html:233-248 and :248",
  "L01.html:233-248 untouched by the round-8 delta (the only L01 hunk is line 51).")
carry("M5a-L01-theorems-1.2-1.6-cor1.4-lemma1.5", "Theorems 1.2-1.6, Corollary 1.4, Lemma 1.5", "course/modules/M/M5/L01.html:66-135",
  "Lines 66-135 untouched by the round-8 delta.")
carry("M5a-L01-quiz-q5-explain", "Retrieval quiz Q5 explain text", "course/modules/M/M5/L01.html:439-440",
  "Lines 439-440 untouched by the round-8 delta (the L01 hunk at 439 is from round 7 and is not in this delta).")
carry("M5a-L01-E1-E2-E3", "Problem set E1-E3", "course/modules/M/M5/L01.html problem section", "Problem section untouched by the round-8 delta.")
carry("M5a-L01-problems-mech-proof-research", "Problems: mechanical, proof, research", "course/modules/M/M5/L01.html problem section", "Problem section untouched by the round-8 delta.")
carry("M5a-L01-canon-misconceptions", "Canon breaks and misconceptions L01", "course/modules/M/M5/L01.html:251-278", "Lines 251-278 untouched by the round-8 delta.")
carry("M5a-L01-key-results-and-statements", "Key results and statements L01", "course/modules/M/M5/L01.html:384-400", "Lines 384-400 untouched by the round-8 delta.")

# ---- L02
R("M5a-L02-why-it-matters", "Why-it-matters sentence", "course/modules/M/M5/L02.html:51", "PASS",
  "L02.html:51 is not in the round-8 delta (the only L02 hunk is line 121); cited sentence byte-identical since the round-7 pin.")
R("M5a-L02-thm-2.5-and-remark-2.6", "Lemma 2.4, Theorem 2.5 (greatest lower bound), Remark 2.6 (changed proof at line 121 re-verified)", "course/modules/M/M5/L02.html:111-146", "PASS",
  "Fresh: L02.html:121 now defines D = {-b : b in B} where it previously used C. Trace: D nonempty since B nonempty; a lower bound m of B gives -m upper bound of D, so D bounded above and t = sup D exists by (H2); -b <= t gives -t <= b, so -t is a lower bound; for any lower bound u, -u is an upper bound of D so t <= -u, i.e. u <= -t; hence L = -t is the greatest lower bound; the eta-clause follows from L being the greatest lower bound. Symbol C is used in L02 only at L02.html:102,107,135 for unrelated constants; D is used nowhere else in L02. Statement L02.html:112-116 unchanged.")
carry("M5a-L02-lab-1", "Lab 1 expected block and interpretation paragraph", "course/modules/M/M5/L02.html:265-292 and tests/labs/M5/lab-M5-L02-1.py",
  "L02.html:265-292 and the L02 twin untouched in the round-8 delta; run_labs and isolated twin run re-run this round (L02.out, 7 lines).")
carry("M5a-L02-prop-3.3-lemma-3.4-prop-3.5", "Proposition 3.3, Lemma 3.4, Proposition 3.5", "course/modules/M/M5/L02.html:169-210", "Lines 169-210 untouched by the round-8 delta.")
carry("M5a-L02-R3-geometric-decay", "Problem R3 geometric decay bound", "course/modules/M/M5/L02.html:418-421", "Lines 418-421 untouched by the round-8 delta.")
carry("M5a-L02-canon-misconceptions-problems", "Canon breaks, misconceptions, problems L02", "course/modules/M/M5/L02.html:295-427", "Lines 295-427 untouched by the round-8 delta (line 121 is in the proof block at 118-124, checked above).")
carry("M5a-L02-quiz-and-key-results", "Quiz and key results L02", "course/modules/M/M5/L02.html:428-535", "Lines 428-535 untouched by the round-8 delta.")

# ---- L03 (no L03 hunk in round-8 delta)
carry("M5a-L03-line-62-after-definition", "Sentence after Definition 1.1", "course/modules/M/M5/L03.html:62", "L03.html:62 untouched by the round-8 delta.")
carry("M5a-L03-line-64-proof-description", "Sentence before Proposition 1.4", "course/modules/M/M5/L03.html:64", "L03.html:64 untouched by the round-8 delta.")
carry("M5a-L03-prop-1.4-lemma-1.3-prop-1.5", "Lemma 1.3, Proposition 1.4, Proposition 1.5", "course/modules/M/M5/L03.html:67-102", "Lines 67-102 untouched by the round-8 delta.")
carry("M5a-L03-prop-2.1-2.2-3.1", "Propositions 2.1, 2.2, 3.1", "course/modules/M/M5/L03.html:172-214", "Lines 172-214 untouched by the round-8 delta.")
carry("M5a-L03-E1-E2-E3", "Problem set E1-E3", "course/modules/M/M5/L03.html:299-317", "Lines 299-317 untouched by the round-8 delta.")
carry("M5a-L03-R1-R2-R3", "Problem set R1-R3", "course/modules/M/M5/L03.html:323-343", "Lines 323-343 untouched by the round-8 delta.")
carry("M5a-L03-canon-misconceptions", "Canon-breaks bullets and misconceptions", "course/modules/M/M5/L03.html:215-240 (219,229)", "Lines 215-240 untouched by the round-8 delta.")
carry("M5a-L03-lab-1", "Lab 1 and expected block", "course/modules/M/M5/L03.html lab section; tests/labs/M5/lab-M5-L03-1.py", "Lab section and twin untouched; run_labs and isolated twin re-run this round (L03.out, 5 lines).")
carry("M5a-L03-quiz", "Retrieval quiz L03", "course/modules/M/M5/L03.html:364-443", "Lines 364-443 untouched by the round-8 delta.")

# ---- L04
carry("M5a-L04-quiz-q5-distractor", "Quiz Q5 options and explain", "course/modules/M/M5/L04.html:425-429", "L04.html:425-429 not in the round-8 delta (round-8 L04 hunks are 214,222,327,355,371).")
carry("M5a-L04-quiz-q8-explain", "Quiz Q8 explain", "course/modules/M/M5/L04.html:449-451", "L04.html:449-451 not in the round-8 delta.")
carry("M5a-L04-lab-1", "Lab 1 twin and expected block", "course/modules/M/M5/L04.html lab section; tests/labs/M5/lab-M5-L04-1.py", "Lab section and twin untouched; run_labs and isolated twin re-run this round (L04.out, 11 lines).")
carry("M5a-L04-prop-1.4-lagrange", "Proposition 1.4 (Euclidean metric)", "course/modules/M/M5/L04.html:79-98", "Lines 79-98 untouched by the round-8 delta.")
R("M5a-L04-example-1.5-prop-1.7", "Example 1.5, Example 1.6, Proposition 1.7 (rename B(S)->ell^infty(S) re-verified in L04)", "course/modules/M/M5/L04.html:99-237 (hunks 214,222)", "PASS",
  "Fresh, in-slice: L04.html:214 defines ell^{\\infty}(S) before its first use; L04.html:222-223 Proposition 1.7 uses ell^{\\infty}(S) consistently in name, hypotheses and conclusion; proof L04.html:225-229 uses no B(S) and is unchanged. Within L04 no B(S) remains (xref_bS.out). The cross-lesson consequence of the rename is recorded in M5a-L04-B-S-rename-consistency.")
carry("M5a-L04-remark-2.2-prop-2.1", "Remark 2.2, Proposition 2.1", "course/modules/M/M5/L04.html:243-256", "Lines 243-256 untouched by the round-8 delta.")
carry("M5a-L04-section-3-props", "Section 3 definitions and Propositions 3.3, 3.4, Remark 3.5, Example 3.6", "course/modules/M/M5/L04.html:257-298", "Lines 257-298 untouched by the round-8 delta.")
carry("M5a-L04-section-4-props", "Section 4 Proposition 4.2 and Example 4.3", "course/modules/M/M5/L04.html:299-322", "Lines 299-322 untouched by the round-8 delta.")
carry("M5a-L04-F-facts-section-1", "Facts stated in Section 1", "course/modules/M/M5/L04.html:54-98", "Lines 54-98 untouched by the round-8 delta.")
R("M5a-L04-canon-misconceptions", "Canon breaks and misconceptions L04 (line 327 re-verified)", "course/modules/M/M5/L04.html:323-340 (327)", "PASS",
  "Fresh: L04.html:327 now says 'So f is excluded from ell^{\\infty}(R), and Proposition 1.7 is stated on ell^{\\infty}(S)', consistent with L04.html:214 and :222. Its claims (|x| unbounded, sup = +infinity) are unchanged. Other lines untouched.")
R("M5a-L04-problems", "Problem set L04 (Proof 3 at 355 and Research 3 at 371 re-verified)", "course/modules/M/M5/L04.html:341-376 (355,371)", "PASS",
  "Fresh: L04.html:355 Proof 3 'Let f_n, f in ell^{\\infty}(S)'; its solution (L04.html:356-357) cites d_inf and needs no B(S). L04.html:371 Research 3 'C subseteq ell^{\\infty}([0,1])', kappa: R -> C; its solution (L04.html:372) uses only d_inf and L02 (Cauchy in R converges). Other problems (Proof 2 at L04.html:353, Empirical 1-3, Research 1-2) untouched and re-read.")
carry("M5a-L04-key-results", "Key results L04", "course/modules/M/M5/L04.html:377-393", "Lines 377-393 untouched by the round-8 delta; L04 key-results text contains no B(S).")

# ---- NEW FAIL
R("M5a-L04-B-S-rename-consistency", "Rename of the bounded-function space B(S) to ell^infty(S) in L04 must not leave dangling or conflicting names in the module (rule 10 cards and cross-lesson prose)",
  "course/modules/M/M5/L04.html:214,222,223,327,355,371 vs course/modules/M/M5/L05.html:227,234,284,300-301; course/modules/M/M5/L06.html:272,277,288; course/modules/M/M5/cards.json:402 (card M5-c056, lesson L04)", "FAIL",
  "Round-8 delta renamed B(S) to ell^{\\infty}(S) throughout L04 (xref_bS.out: no B(S) left in L04). But L05.html:227 still reads '(2) B(S) is the set of bounded real functions on S with the metric d_inf of L04, Example 1.6', L05.html:284, :300-301 and L06.html:272 ('B(N) ... which is B(S) of L04, Example 1.6') and L06.html:277,288 still use B(S)/B(N). So the cross-reference points to an L04 example that no longer carries that name, and B(S) is an undefined term in the module. cards.json:402 (card M5-c056, lesson L04, basis 'Proof in Section 1 (Proposition 1.7)') back reads '(B(S), d_inf) is a metric space', while L04.html:222-223 now concludes '(ell^infty(S), d_inf) is a metric space'; the card disagrees with the current lesson text.",
  "Pick one name and apply it module-wide: either restore B(S) in L04 (Example 1.6, Proposition 1.7, Proof 3, Research 3, L04.html:327) or change L05.html:227,234,284,300-301, L06.html:272,277,288 and cards.json:402 (and cards.json:559-560 if the name changes) to ell^infty(S). Cards must be fixed in their source and regenerated per CLAUDE.md, not hand-edited. Then re-run check_pages, build_site --check and the L05/L06 slice verifiers.")

rows_out = rows
frag = {
  "unit": "M5",
  "slice": "a",
  "round": 8,
  "verifier": "verifier-B8 (Haiku 5.5, independent)",
  "pin": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
  "base": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M5-a",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyB8-M5-a/ledgers/M5/scripts/M5-a-r8",
  "verified_at": "2026-10-28T23:59:00Z",
  "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows_out) else "PASS",
  "rows": rows_out,
  "mutants": [],
  "registry_flags": ["notation/notation.json: no registry change needed; ell^infty(S) and D are local symbols defined at use, not registered"],
  "freshness_flags": ["Cross-slice: L05.html and L06.html (other slices) still use B(S); cards.json card M5-c056 (outside slice a) disagrees with L04 Proposition 1.7 text."],
  "notes": [
    "Round-8 delta (7aa909e..ce7b382) restricted to slice files: index.html:62,159; L01.html:51; L02.html:121; L04.html:214,222,223,327,355,371. tests/labs/M5 L01-L04 twins unchanged. tests/labs/M5/lab-M5-L07-1.py changed (outside slice a, not verified here).",
    "Every changed hunk and the round-7 FAIL (M5a-hub-prereq-M2-definite-integral) re-verified from scratch. Carried rows cite lines outside the hunks and are carried with their round-7 evidence.",
    "Lab-only slice: no project grader, so no student-error mutants and no alternative implementations apply (rules: mutation testing applies to project graders only).",
    "Not checked: cards.json entries outside this slice's pages (card-number cross-checks not redone except card M5-c056 for the L04 rename); lessons L05-L10 and project.html except where cited for cross-reference; live verify_refs (only --offline); run_graders/mutate_graders (project slice only); page_smoke figure sweep (skipped, no figures in slice); 360px visual render; the L07 twin change."
  ],
  "summary": None
}
n = len(rows_out); f = sum(1 for r in rows_out if r["status"] != "PASS")
frag["summary"] = f"M5-a round 8: {n} rows, {n-f} PASS, {f} FAIL (M5a-L04-B-S-rename-consistency). Round-7 FAIL M5a-hub-prereq-M2-definite-integral re-verified PASS: index.html:62 now matches L10.html Section 2 Darboux usage. All mechanical gates for the slice PASS on the venv interpreter."
out = sys.argv[1]
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(out, n, f, frag["verdict"])
