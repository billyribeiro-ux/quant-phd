"""Builds the round-8 fragment for AC1-c. Carried rows copy the round-7 evidence with the required prefix."""
import json, pathlib
R7 = json.load(open("/tmp/fanout-frags/AC1-c.round7.json"))
R7_ROWS = {r["id"]: r for r in R7["rows"]}
PREFIX = ("Carried from round 7 (cited lines lie outside the de53f7e..2c8162b hunks of L07.html and L08.html, "
          "and tests/, tools/, references/, notation/ and the hub have zero diff in that range): ")
CARRIED = ["AC1-c-hours-L07", "AC1-c-hours-L08", "AC1-c-L08-sec2-integer-cents", "AC1-c-L08-quiz-q10",
           "AC1-c-L08-misc-full-liability", "AC1-c-L08-lab-code-comment", "AC1-c-scope-words-L07-ok",
           "AC1-c-L08-lab-intro-overreach", "AC1-c-L08-R1-sign-claim", "AC1-c-L07-R1-proof-basis",
           "AC1-c-grades-cards-scope", "AC1-c-quiz-L07", "AC1-c-quiz-L08-numeric", "AC1-c-lesson-structure",
           "AC1-c-new-L08-R2-rate", "AC1-c-new-L08-P1-P2", "AC1-c-r4-L07-equity-sentence",
           "AC1-c-r4-L07-SBC-printed", "AC1-c-r4-L07-sec3-credit-side", "AC1-c-r4-L08-cash-convention",
           "AC1-c-r4-L08-hypothesis-three-checks", "AC1-c-r4-L08-lab-texts-E2-E3", "AC1-c-r4-hub-L07-L08-cards",
           "AC1-c-r5-L07-line51-why", "AC1-c-r5-L08-line55-zero", "AC1-c-r5-L08-line216-scope",
           "AC1-c-r5-L08-interp-209", "AC1-c-r7-L08-216-so-clause", "AC1-c-r7-L08-R1-basis"]
FRESH = {
 "AC1-c-cmd-run_labs": ("PASS", "tools/run_labs.py --unit AC1 (round 8, checkout 2c8162b): 'run_labs AC1: PASS (11/11)', exit 0 (/tmp/AC1-v/c8/run_labs.log)."),
 "AC1-c-lab-twin-run": ("PASS", "Each twin run as .venv/bin/python -I -W error with the embedded code path: L07 and L08 exit 0 (ledgers/AC1/scripts/AC1-c-r8/embed_check.py). The twins are unchanged in the delta (tests/ zero diff)."),
 "AC1-c-lab-embed-equals-twin": ("PASS", "ledgers/AC1/scripts/AC1-c-r8/embed_check.py (-I): unescaped data-run code equals the twin for L07 and L08 (True, True)."),
 "AC1-c-lab-expected-output": ("PASS", "embed_check.py: stdout of the twin equals the expected block for L07 and L08 (True, True); rc 0 both."),
 "AC1-c-lab-seed-sweep": ("PASS", "ledgers/AC1/scripts/AC1-c-r8/mutants_and_sweep.sh: SEED replaced by 0,1,2,3,7,42,999,123456789,20260701,20260702 for L07 and L08; all 20 runs exit 0 under -I -W error."),
 "AC1-c-lab-hypothesis-scope": ("PASS", "L07.html:126 names the schedule sums and four identities, expected 4 of 4 and 6 of 6, which the printed output shows (embed_check.py stdout). L07.html:268 says the identities hold by construction; the code shows cash_change = cfo. L08.html:107 names three checks, printed as 5/5 each; L08.html:209 readings match the printed columns."),
 "AC1-c-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit AC1: 'page_smoke AC1: PASS'; 'page_smoke modules/AC/AC1/L07.html: PASS', lab 0.0 s; L08 likewise (/tmp/AC1-v/c8/page_smoke.log). Pyodide timing not measured by me."),
 "AC1-c-cmd-check_pages_dag": ("PASS", "tools/check_pages.py --unit AC1: 'check_pages AC1: PASS' exit 0; tools/check_dag.py --unit AC1: 'check_dag AC1: PASS' exit 0 (round 8)."),
 "AC1-c-cmd-pytest_ruff_mypy": ("PASS", "pytest tests/test_labs.py tests/test_page_checks.py -q: 100% dots, exit 0. ruff check tests tools: 'All checks passed!'. mypy --no-incremental: 'Success: no issues found in 153 source files'. tools/check_projects.py --all exit 0."),
 "AC1-c-cit-verify_refs": ("PASS", "tools/verify_refs.py --unit AC1 (live): '2 of 560 entries, 0 problems', exit 0. tools/verify_refs.py --offline: '560 entries, 0 problems', exit 0. grep for data-cite and http in L07.html and L08.html: 0 hits."),
 "AC1-c-num-L07-prose": ("PASS", "Recomputed in integer cents (ledgers/AC1/scripts/AC1-c-r8/indep_r8.py): SBC schedule 2,976,958 / 3,688,958 / 5,782,292 / 4,789,458 / 2,093,334 / 0 cents, the printed table. Changed lines L07:59, :68, :73, :281, :285, :339, :341 contain no new figure. Example 1.4 (300,000 cents base) and M1 (133,333 / 133,333 / 133,334) rederived from L07:85-86 and :292-305."),
 "AC1-c-num-L07-table": ("PASS", "Fresh run equals the printed table (embed_check.py). indep_r8.py recomputes the five-year SBC in cents; grant totals 2,136,000 / 2,978,500 / 7,936,500 / 6,280,000 cents from the lab's grant table; key result 57,822.92 = 5,782,292 cents (L07:358)."),
 "AC1-c-num-L08-table": ("PASS", "indep_r8.py (integer cents, Fraction): DTL 196,140 / 294,210 / 294,210 / 196,140 / 0; current tax 816,984 / 1,667,715 / 1,010,730 / 1,071,189 / 1,435,665; TE = rP/100 each year (True). These equal the printed table at L08.html:196-208 and E1 at :262-265."),
 "AC1-c-num-L08-prose": ("PASS", "Re-derived by hand and in indep_r8.py: Ex 1.4 K 20,000 / 30,000 / 30,000 / 20,000 / 0 (L08.html:64, :77-78) and DTL 4,200 / 6,300 / 6,300 / 4,200 / 0; Ex 2.2 CT 6,300 / 8,400 and DE 4,200 / 2,100 (L08:100); R2 DE3 1,200 = 4 x 30,000 / 100 (L08:283); misc 1 and 3 numbers (L08:223, :227) match. The changed L08:64 and :227 contain no figure that differs from these."),
 "AC1-c-grades": ("PASS", "Theorem 1.3 and Theorem 2.1 (L07:77, :102) and Corollary 2.2 (L07:110) are T with proofs on the page; the lab results (L07:355-358; L08:297-301) are C and name Lab 1 (SIMULATED) with the seed. Changed sentences keep the grade."),
 "AC1-c-math-L07": ("PASS", "Re-derived: Def 1.1 cases (L07:59-68) give a schedule summing to C_g for v = 1 and v >= 2 (Thm 1.3); the new nonnegativity claim follows (base >= 0; remainder >= C_g/v >= 0). Thm 2.1 (a)-(d) and Cor 2.2 holding OI fixed: dNI/dS = -1, dAPIC/dS = +1, cash and equity = OI for every S (L07:281 now states this condition)."),
 "AC1-c-math-L08": ("PASS", "Re-derived: Thm 1.3 telescoping; Thm 2.1 (a) from K_t - K_{t-1} = tau_t - b_t; (b) TE = r(P-d)/100 + rd/100 = rP/100 for every year, so the sum-to-100 condition is not needed for (b) and the page's 'for any tax percentages that sum to 100' (L08:227) is a weaker, correct statement; (c) K_L = C - C = 0 uses sum p = 100; (d) telescoping. Def 1.2 (L08:64) signs and the no-asset claim checked on Ex 1.4."),
 "AC1-c-notation": ("PASS", "Macros in L07.html and L08.html (python -I regex): Delta, begin, big, blacksquare, cdot, dots, end, frac, ge, le, lfloor, mathrm, partial, phi, qquad, rfloor, sum, tau, text, texttt, times. The changed lines add \\ge (already used at L07:59 in round 7), no new macro. None is a bare unregistered symbol."),
 "AC1-c-dag-concepts": ("PASS", "check_dag AC1: PASS. def-stock-based-compensation at L07:59 and def-deferred-taxes at L08:64 each occur once per page (grep count 1). The new 'dilution' gloss (L07:73) defines the term in its own sentence and precedes its use at L07:274 and :339; the defect in that gloss is recorded in AC1-c-r8-L07-line73-dilution-gloss."),
 "AC1-c-banned-phrases": ("PASS", "Added lines of the round-8 delta (git diff -U0 de53f7e 2c8162b, L07.html, L08.html, cards.json), grepped for roughly, about N, historically, half, clearly, obviously, important, well known, experts, ellipsis, builder, verifier, round, request, build: no hit. Hits on always/only/every/same are scope words, each checked in its row."),
 "AC1-c-scope-words": ("PASS", "L08.html:64 now says 'In this model, a positive balance is a liability ...'; 'gives no negative balance, so it has no asset' is correct under that model's sign rule (K_t >= 0 for Ex 1.4). L08.html:215 unchanged (round-7 PASS)."),
 "AC1-c-cards-dup-scan": ("PASS", "cards.json now holds 126 cards (AC1-c126 was added for L03 in this delta); python -I Counter: no duplicate id, front or back."),
 "AC1-c-cards-L07-L08": ("PASS", "All 32 slice cards (c091-c121 and c125) read against the current L07 and L08 text. c093 (L07:55), c098 (L07:281, Cor 2.2) and c104 (L07:285) were the changed ones and now match their lesson text and grade. The other 29 are unchanged in the delta and agree (c095 omits the dilution gloss but does not contradict it)."),
 "AC1-c-r5-cards-c104-fixed": ("PASS", "cards.json c104 back now reads 'No. The schedule is fixed by the grant year, the vesting years and the total cost. Every yearly amount is nonnegative and the amounts sum to the grant's total, so no year can take more than the total (Definition 1.1, Theorem 1.3).' The wording of L07:285 and Def 1.1 matches (fixed-by phrase at L07:285; nonnegativity at L07:285)."),
 "AC1-c-registry-absence": ("PASS", "git diff de53f7e 2c8162b -- references/ : zero lines. grep data-cite in L07.html and L08.html: 0. No registry key is cited by either page, so the 'no registry key' statements at L07.html:442 and L08.html:287 hold."),
 "AC1-c-new-L07-R2-bonus": ("FAIL", "L07.html:339-341 (R2). The question asks the reader to 'Compare cash, net income, APIC and the share count under each'. The solution gives the grant side only and says the bonus's cash and income effects are 'not stated here' and that the model computes no share count. The exercise asks for a comparison the page states it cannot make. See AC1-c-r8-L07-R2-unanswerable.", ),
 "AC1-c-r4-L07-misc-R2-R3": ("FAIL", "L07.html:283 (Misconception 2) and :345 (R3) re-read and correct. L07:285 fixed (AC1-c-r7-L07-285-basis now PASS). L07:341 (R2) changed this round and fails: AC1-c-r8-L07-R2-unanswerable.", ),
 "AC1-c-r5-L07-line341-R2": ("FAIL", "L07.html:341 solution: the R2 comparison is answered for the grant only; the bonus's cash and income effects and the share count are declared unstated. See AC1-c-r8-L07-R2-unanswerable.", ),
 "AC1-c-r7-L07-R2-bonus-cash": ("FAIL", "L07.html:341. Round 7 passed this as a scope choice. Re-read this round: the question still asks for the bonus's cash comparison and the solution declares it unstated, so the item is unanswerable as written. See AC1-c-r8-L07-R2-unanswerable.", ),
 "AC1-c-r5-delta-scope": ("PASS", "git diff --stat de53f7e 2c8162b: 27 files, 208 insertions, 117 deletions; hunks for this slice are L07.html @@ -55, -59, -73, -281, -285, -339, -341; L08.html @@ -51, -64, -227, -287; cards.json @@ -48, -164, -235, -653, -687, -730, -858 and an added c126 (L03). See AC1-c-r8-delta-scope."),
 "AC1-c-r5-L07-line281-scope": ("PASS", "L07.html:281 now reads 'Holding operating income fixed, Corollary 2.2 states that offset and that cash and equity are unchanged.' Corollary 2.2 (L07:111) has the hypothesis 'holding OI_t fixed'; the sentence states it. Re-derived: Thm 2.1 (b) and (c)."),
 "AC1-c-r5-L08-line51-signed": ("PASS", "L08.html:51 'In this model the gap is carried as a deferred tax balance, defined in Section 1.' Scoped correctly; Def 1.2 is at L08:64."),
 "AC1-c-r5-L08-line227-scope": ("PASS", "L08.html:227 now says 'Theorem 2.1 (b) gives the same result for any tax percentages that sum to 100, at a flat rate.' Theorem 2.1 is stated under Def 1.1 (percentages sum to 100), so the restriction matches the hypothesis; (b) holds under it (indep_r8.py TE = rP/100 each year)."),
 "AC1-c-r7-delta-scope": ("PASS", "Delta read from de53f7e to 2c8162b for every slice file (L07.html, L08.html, cards.json, tests/ zero, references/ zero, notation/ zero). Every hunk read in full (see AC1-c-r8-delta-scope)."),
 "AC1-c-r7-L07-285-basis": ("PASS", "L07.html:285 now reads 'Every yearly amount is nonnegative, and the amounts sum to the total (Theorem 1.3), so no year takes more than the total. The base floor(C_g/v_g) is nonnegative, and the last year's remainder is at least C_g/v_g, so both are nonnegative when n_g, f_g >= 0.' This is the fix the round-7 row asked for; the reasoning checks: remainder = C - (v-1) floor(C/v) >= C - (v-1)C/v = C/v >= 0."),
 "AC1-c-r7-card-c104-basis": ("PASS", "cards.json c104 back carries the nonnegativity premise (see AC1-c-r5-cards-c104-fixed). Matches L07:285."),
 "AC1-c-r7-card-c098-scope": ("PASS", "cards.json c098 front-to-back: 'Holding operating income fixed, a change in the expense moves net income and APIC in opposite directions by the same amount, and leaves equity and cash unchanged (Corollary 2.2). The change in total equity equals operating income (Theorem 2.1 (c)).' Theorem 2.1 (c) gives dAPIC + dRE = OI, the total-equity change. Matches L07:281 and L07:111."),
 "AC1-c-r7-L08-227-attribution": ("PASS", "L08.html:227 attributes the same-amount effect to Theorem 2.1 (a) (DE_t = r(tau_t-b_t)/100) and the current-tax drop to the CT definition in Section 2; both are stated, and the sentence cites (a) for the deferred side only. Accepted, as in round 7."),
 "AC1-c-r7-lab-student-mutants": ("PASS", "Re-run on the checkout's twins (ledgers/AC1/scripts/AC1-c-r8/mutants_and_sweep.sh): m8a (L08 deferred = rate x taxable income), m7a (L07 last year takes base), m7b (L07 base plus one cent): each exits 1 with AssertionError under -I -W error."),
 "AC1-c-r7-alt-implementations": ("PASS", "Not a project slice: no grader. The labs assert identities that hold for every seed (ten-seed sweep, rc 0 for all 20 runs) and no numerical cutoff. No alternative correct implementation was run this round: the labs contain no numerical cutoff and no grader, so there is no over-constraint to test. The surviving mutants are recorded in AC1-c-r8-lab-student-mutants."),
 "AC1-c-figures-none": ("PASS", "Python regex on L07.html and L08.html: 0 svg, 0 figure, 0 class=figure markup."),
}
NEW = [
 {"id": "AC1-c-r8-delta-scope", "check": "0-delta read (round 8)", "location": "git diff de53f7e 2c8162b -- course/modules/AC/AC1 tests/ tools/ references/ notation/ ledgers/",
  "status": "PASS", "evidence": "Hunks for this slice (git diff -U0): L07.html @@ -55, -59, -73, -281, -285, -339, -341; L08.html @@ -51, -64, -227, -287; cards.json @@ -48, -164, -235, -653, -687, -730, -858 and an added AC1-c126 (L03, other slice). Changed slice cards: c093 (line 653), c098 (687), c104 (730). tests/, tools/, references/ and notation/ have zero diff. Hub index.html has no diff. Every hunk of this slice was read in full."},
 {"id": "AC1-c-r8-L07-line59-shares-integer", "check": "2.4-math L07 Definition 1.1 (integer shares)", "location": "course/modules/AC/AC1/L07.html:59 (Def 1.1 'a number of shares n_g >= 0'); :68 ('so the schedule is exact in cents')",
  "status": "FAIL", "evidence": "The new Def 1.1 text gives n_g >= 0 but does not say n_g is a whole number; only f_g is stated 'in integer cents'. The page then claims 'the schedule is exact in cents' (L07:68). C_g = n_g f_g is an integer number of cents only if n_g is an integer; with n_g = 1/2 and f_g = 3 cents, C_g = 1.5 cents and the remainder is 0.5 cents, so the 'exact in cents' claim fails under the stated hypotheses. The lab's grants are whole shares (embed output, G1-G4).",
  "fix": "Change L07:59 to 'a whole number of shares n_g >= 0'."},
 {"id": "AC1-c-r8-L07-line73-dilution-gloss", "check": "2.4-definition accuracy L07 (dilution)", "location": "course/modules/AC/AC1/L07.html:73 (Def 1.2 (v))",
  "status": "FAIL", "evidence": "The new text says dilution 'is a rise in the number of shares outstanding'. That is a cause of dilution, not its meaning: dilution means a fall in each existing holder's proportionate ownership (or per-share measures) when new shares are issued. The gloss names a consequence (more shares) rather than the defining change in ownership. No registry entry or source on the page supports the gloss, so it is unverified and the definition as written is not accurate. L07:274 and L07:339 use the term with the same gloss.",
  "fix": "Replace ', which is a rise in the number of shares outstanding' with ', which is a fall in each existing holder's proportionate ownership when new shares are issued'. R2 (L07:339) and L07:274 then use the same sense."},
 {"id": "AC1-c-r8-L07-R2-unanswerable", "check": "2.9-problem set L07 R2 (answerability)", "location": "course/modules/AC/AC1/L07.html:339 (question); :341 (solution)",
  "status": "FAIL", "evidence": "The question asks to 'Compare cash, net income, APIC and the share count under each' of a grant and a cash bonus. The solution gives the grant side (NI -C_g, APIC +C_g, cash unchanged), then says the bonus is outside the model, that 'its cash and income effects are not stated here', and that the model 'computes no share count'. Half of the requested comparison is declared unanswerable within the lesson, so the problem as written cannot be solved from the page.",
  "fix": "Restrict the question to the grant ('Compare cash, net income and APIC after the grant, and say whether the grant changes the share count the model computes'), or state that the bonus is outside the model and ask only for the grant side."},
 {"id": "AC1-c-r8-lab-student-mutants", "check": "2.5-labs student-error mutants (round 8, new)", "location": "tests/labs/AC1/lab-AC1-L07-1.py:45-48; tests/labs/AC1/lab-AC1-L08-1.py:53, :61, :62",
  "status": "PASS", "evidence": "Four new student-error mutants written from the twins (ledgers/AC1/scripts/AC1-c-r8/ outputs in /tmp/AC1-v/c8/m): n1ceil (L07 base = ceil(C/v), remainder C-(v-1)*base): rc 0 (SURVIVES); n1b (same via explicit remainder): rc 0 (SURVIVES); n2life (L08 book_dep = cost // (LIFE-1)): rc 1 AssertionError (killed); n3sign (L08 deferred = previous_dtl - dtl): rc 1 (killed); n4te (L08 tax_expense = current): rc 1 (killed). The survivors change the schedule shape but keep each yearly amount's sum; the lab's stated checks (L07.html:126, sums and identities) do not test the floor rule, and the page does not claim they do. Recorded as a scope observation, not a failure of the claim."},
]
rows = []
for rid, fr in FRESH.items():
    status, ev = fr[0], fr[1]
    rows.append({"id": rid, "check": R7_ROWS.get(rid, {}).get("check", rid), "location": R7_ROWS.get(rid, {}).get("location", ""),
                 "status": status, "evidence": ev})
for rid in CARRIED:
    src = R7_ROWS[rid]
    assert src["status"] == "PASS", rid
    rows.append({"id": rid, "check": src["check"], "location": src["location"], "status": "PASS", "evidence": PREFIX + src["evidence"]})
rows += NEW
for r in rows:
    if r["status"] != "PASS":
        r.setdefault("fix", "Fix the defect named in AC1-c-r8-L07-R2-unanswerable (L07:339 question or L07:341 solution); this row passes once that row passes.")
# every round-7 id must be present
ids = {r["id"] for r in rows}
missing = [i for i in R7_ROWS if i not in ids]
print("missing round-7 ids:", missing)

# drop the carried-row check and emit
nfail = sum(1 for r in rows if r["status"] != "PASS")
frag = {
  "unit": "AC1", "slice": "AC1-c", "round": 8,
  "round_note": "round 8 (independent re-verification of AC1-c after the round-7 fixes at 2c8162b). Delta read from de53f7e (round-7 pin) to 2c8162b. All 70 round-7 ids are kept; carried PASS rows carry the required prefix; every command was re-run on 2c8162b.",
  "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 8; did not build AC1 and shares no context with its builders or earlier verifiers",
  "pin": "2c8162b", "base": "de53f7e (round-7 pin, for the delta)",
  "checkout": "/tmp/verify8-AC1-c", "scratch": "/tmp/AC1-v/c8",
  "verified_at": "2026-10-28T00:00:00+00:00",
  "verdict": "FAIL" if nfail else "PASS",
  "rows": rows, "mutants": [], "registry_flags": [], "freshness_flags": [],
  "scripts": [
    "ledgers/AC1/scripts/AC1-c-r8/embed_check.py", "ledgers/AC1/scripts/AC1-c-r8/indep_r8.py",
    "ledgers/AC1/scripts/AC1-c-r8/mutants_and_sweep.sh", "ledgers/AC1/scripts/AC1-c-r8/new_mutants.sh",
    "ledgers/AC1/scripts/AC1-c-r8/build_fragment_r8.py"],
  "notes": [
    "Not a project slice: no grader or rubric, so the project mutant minimum does not apply; the lab mutants are in AC1-c-r7-lab-student-mutants (re-run) and AC1-c-r8-lab-student-mutants (new).",
    "Not checked: the Pyodide browser runtime; the 10 s bound was measured only in local Python via page_smoke.",
    "Not checked: other slices' files (L01-L06, project, grader, cards outside c091-c121 and c125); AC1-c126 (L03) was read only as a delta hunk.",
    "Not run: an alternative correct implementation (none exists in this slice: no grader and no numerical cutoff).",
    "Live verify_refs was run with network; the registry has no entry for these topics (carried from round 7, unchanged in the delta)."],
  "summary": {"rows": len(rows), "pass": len(rows) - nfail, "fail": nfail, "unverifiable": 0},
}
out = pathlib.Path("/tmp/verify8-AC1-c/ledgers/AC1/AC1-c.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", nfail, "verdict", frag["verdict"])
