"""Builds ledgers/CF1/CF1-a.json (round 11) from the round 10 fragment plus round 11 re-verification results."""
import json, re, sys, pathlib
PREV = pathlib.Path('/tmp/fanout-frags/CF1-a.round10.json')
ROOT = pathlib.Path(sys.argv[1])
prev = json.loads(PREV.read_text())
CARRY = 'Carried from round 10 ({files} byte-identical since the previous pin):'
DIR = 'course/modules/CF/CF1/'

def files_of(loc):
    out = []
    for tok in re.findall(r'[\w./-]+\.(?:html|py|json|yaml)', loc):
        if tok.startswith(('tests/', 'course/', 'notation/', 'ledgers/', 'tools/', 'references/')):
            out.append(tok)
        elif tok.startswith('lab-CF1'):
            out.append('tests/labs/CF1/' + tok)
        elif tok in ('L01.html', 'L02.html', 'L03.html', 'L05.html', 'index.html', 'cards.json'):
            out.append(DIR + tok)
        else:
            out.append(tok)
    return ', '.join(dict.fromkeys(out)) or 'the cited files'

# Rows whose cited subject changed between af08ad1 and 91946cf, or that were FAIL in round 10: re-verified now.
OVR = {
 'CF1-a-L01-read-full': ('PASS', 'Round 11 read of L01.html lines 1-570 in full (1-200, 200-390, 390-570), every line; the changed lines 111, 322, 338 and 438 were checked against the proof, Proposition 3.1 (limit C_0), Lab 1 output (lines 289-313) and Corollary 4.2. No line left unread.'),
 'CF1-a-L02-read-full': ('PASS', 'Round 11 read of L02.html lines 1-522 in full (1-29 head, 30-179, 180-349, 350-522), every line; the changed lines 280 and 508 were checked against the lab twin (lines 162-252 of L02.html; tests/labs/CF1/lab-CF1-L02-1.py) and against AC1 concept definitions (course/concepts.html entries accrual-accounting, balance-sheet, depreciation-and-amortization point to AC1 L01, L02, L03 definitions).'),
 'CF1-a-L01-misconception-and-quiz': ('PASS', 'L01.html lines 331-341 (line 338 changed; now conditioned on a negative date-0 outlay, and the Lab 1 Part A figures 7,000.00 at 0.00 and -46.94 at 0.20 match the printed Lab 1 output, lines 289-295); quiz lines 477-550 re-read and every answer key matches the text (item 3 answer "tends to the period-0 flow"; item 8 "negative, at -83.33"; item 10 Corollary 4.2).'),
 'CF1-a-L01-remark32-conventional': ('PASS', 'L01.html line 111 (Remark 3.2, changed): "If the date-0 flow is negative, the limit C_0 is negative, so a project with a positive NPV at a low rate has a negative NPV at some higher rate." Valid: Proposition 3.1 gives NPV(r) to C_0 < 0 as r grows, and NPV(low) > 0 with continuity gives a sign change; the sentence is conditional on C_0 < 0 and on the conventional stream of the Remark. "date-0" first appears here and is tied to C_0 in the same sentence (see CF1-a-r11-date0-term).'),
 'CF1-a-L01-misc2-conventional-referent': ('PASS', 'L01.html line 338 (Section 7 misconception 2, changed): "Proposition 3.1 says that for a conventional stream with a negative date-0 outlay, such as the Lab 1, Part A project, the NPV falls as the rate rises ...". The Lab 1 Part A project has flows -1,000,000 cents at period 0 (L01.html line 235), so C_0 < 0 holds; the Proposition states no sign condition, so the restriction is a narrowing, not an error.'),
 'CF1-a-L01-misc2-positive-needs-C0': ('PASS', 'L01.html line 338 (changed): the sign change is now stated only for a conventional stream with a negative date-0 outlay (C_0 < 0). With that premise, the limit NPV(r) to C_0 in Proposition 3.1 (L01.html line 99) and continuity give the change of sign that the sentence asserts. The printed values 7,000.00 at 0.00 and -46.94 at 0.20 are the Lab 1 Part A output (L01.html lines 291, 295). Card CF1-c012 carries the same condition.'),
 'CF1-a-L01-canon-line322-scope': ('PASS', 'L01.html line 322 (changed): "Proposition 3.1 shows that the NPV falls as r rises, so with a negative date-0 outlay the decision can change with r. In Lab 1, Part A, the NPV is 1,211.49 dollars at 0.15 and -46.94 dollars at 0.20." Both numbers equal the printed output (L01.html lines 294, 295); the decision changes because the NPV is positive at 0.15 and negative at 0.20; the "can" is existence, shown by that case.'),
 'CF1-a-L01-line323-one-rate': ('PASS', 'L01.html line 323 is byte-identical to round 10 (not in the af08ad1..91946cf hunks); carried.'),
 'CF1-a-L01-num-R2-E1-E3': ('PASS', 'L01.html line 438 (R2 solution, changed): NPV per dollar with outlays 100 and 1,000 and NPVs 50 and 120 gives 0.50 and 0.12, computed here; "Corollary 4.2 supports ranking by NPV under Assumption 4.0" matches Corollary 4.2 (L01.html line 138: the larger NPV leaves more cash today under Assumption 4.0). E1 (line 407) and E3 (line 421) are byte-identical and re-read: E1 values 7,000.00, 4,635.81, 2,744.72, 1,211.49, -46.94 match the printed output lines 291-295.'),
 'CF1-a-L02-line280-accrual': ('PASS', 'L02.html line 280 (changed): "The lab takes revenue and cash cost as its inputs and does not start from net income." Lab 2 twin generates revenue_cents and cost_cents (tests/labs/CF1/lab-CF1-L02-1.py lines 197-201) and computes EBITDA = revenue - cost (line 216); no net income variable exists in the twin (grep). The accrual sentence before it is unchanged.'),
 'CF1-a-L02-references-scope': ('PASS', 'L02.html line 508 (changed): "The quantities this lesson computes include EBITDA and EBIT (Section 2), operating cash flow (Definition 2.1) and net working capital (Definition 3.1), each defined in its text." Each named quantity is defined in its text: EBITDA_t and EBIT_t at L02.html line 87, OCF_t in Definition 2.1 (line 91), NWC_t in Definition 3.1 (line 123). "include" is not an exhaustive list, so no completeness claim is made. "The net present value it discounts is defined in Lesson 1 (Definition 1.1)" matches L01.html line 59 (dfn id def-net-present-value).'),
 'CF1-a-L02-citations': ('PASS', 'L02.html lines 508-509: "This lesson cites no registry source." grep -c data-cite on L02.html returns 0 (run in round 11); the only link is to Lesson 1 Definition 1.1 and the concept pages. Line 509 is the reference list shell, unchanged.'),
 'CF1-a-scope-words': ('PASS', 'Changed sentences in this round re-scanned for only, all, always, as much as, same, drives, offsets, raises: L01 lines 111, 322, 338, 438 and L02 lines 280, 508 contain "same" (L01 338: "for the same project", matches Lab 1 Part A) and "each" / "include" (L02 508, non-exhaustive, see CF1-a-L02-references-scope). No universal scope word without a computation behind it. Index line 151 (ladder, unchanged) re-scanned: no scope word that overreaches.'),
 'CF1-a-cards-L01-L02': ('PASS', 'course/modules/CF/CF1/cards.json: card CF1-c012 (changed) now reads "For a conventional stream with a negative date-0 outlay (C_0 < 0), NPV falls strictly as the rate rises and tends to C_0 (Proposition 3.1), so a positive NPV at one rate can be negative at a higher one." This matches L01.html line 338 and line 111. Other cards CF1-c001 to c032, c089 and c090 re-read against their lessons: each number (3,452.62; -83.33; 7,000.00; -46.94; 534.24; -1,465.76; -130.50; 2,000.00; 750.00; 10 per cent; 1/12) appears in its lesson (L01.html 68, 338, 407, 421, 458-464, 483; L02.html 153-157, 161, 272, 292, 296, 300, 397, 473). Card CF1-c005 matches Proposition 3.1 (L01.html line 99).'),
 'CF1-a-hub-L05-card': ('PASS', 'index.html line 142 (changed): "Payback and What Firms Actually Use ... and why this lesson states no finding from the registered source on firm use." L05.html line 52 ("the evidence section quotes no passage from the registered paper and states no finding about use"), line 233 ("This lesson states no finding from it. It quotes no passage from that paper ...") and line 450 ("no passage locator has been confirmed, so this lesson states no practice finding") give the why. Title matches L05.html line 36 h1.'),
 'CF1-a-hub-lesson-map': ('PASS', 'index.html lines 136-143 (lines 139, 140, 142 changed): L01 card title = L01.html line 35 h1; L02 = L02.html line 35; L03 "Inflation and Real Cash Flows" = L03.html line 35 h1 (round 10 mismatch resolved); L04 = L04.html line 35; L05 "Payback and What Firms Actually Use" = L05.html line 36 (round 10 punctuation mismatch resolved); L06 = L06.html line 36. Card hours "8 h" match data-hours in each page header.'),
 'CF1-a-mutants': ('PASS', 'Round 11: all 58 lab mutant files under ledgers/CF1/mutants/CF1-a-r7..r11 re-run against the twins under python -I -W error (ledgers/CF1/scripts/CF1-a-r11/run_mut.py; output in ledgers/CF1/scripts/CF1-a-r11/mutants_all.txt): 56 killed, 2 survived (r9_m07_no_tax_credit.py and n05_l02_identity_check_stubbed_true.py, both out of scope, see CF1-a-r11-survivors). Three new round 11 mutants killed (m02-n04, m02-n06, m02-n07).'),
 'CF1-a-notation': ('PASS', 'notation/notation.json lists 8 symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); none is used in CF1 L01 or L02. The changed lines use C_0, C_t, NPV, r, tau, D_t, R_t, K_t, NWC_t, which carry no registered meaning. Changed lines use only KaTeX built-ins and \\mathrm, not an unregistered custom macro (L01.html 111, 322, 338, 438; L02.html 280, 508).'),
 'CF1-a-L02-dag-concepts': ('PASS', 'L02.html lines 22-60 and 280 (line 280 changed: the accrual-accounting link is unchanged in the anchor and href). check_dag CF1: PASS (ledgers/CF1/scripts/CF1-a-r11 gate run, /tmp/cf1-v/a-r11/check_dag.txt). Concepts accrual-accounting, balance-sheet and depreciation-and-amortization are defined once in AC1 (AC1/L01.html line 82, AC1/L02.html line 64, AC1/L03.html line 62; concept index course/concepts.html lines 101-106 link to them).'),
 'CF1-a-L01-banned-process': ('PASS', 'Round 11 grep over L01.html, L02.html and index.html for roughly, about <digit>, historically, typically, usually, generally, ellipsis, TODO, TBD, lorem, clearly, obviously, verifier, round <n>, REQUEST, unit report: no hits in learner text except the verb "builds" (L02.html line 153, index.html line 33, L02 meta line 7), which describes the module and lab, not the build process; BUILDER_RULES 1.2-1.3 do not ban it. Output in /tmp/cf1-v/a-r11/banned.txt.'),
 'CF1-a-gate-check-pages': ('PASS', 'Round 11 re-run: tools/check_pages.py --unit CF1 -> "check_pages CF1: PASS", rc 0 (/tmp/cf1-v/a-r11/check_pages.txt).'),
 'CF1-a-gate-check-dag': ('PASS', 'Round 11 re-run: tools/check_dag.py --all -> "check_dag CF1: PASS", "check_dag AP1: PASS", rc 0 (/tmp/cf1-v/a-r11/check_dag.txt).'),
 'CF1-a-gate-run-labs': ('PASS', 'Round 11 re-run: tools/run_labs.py --unit CF1 -> "run_labs CF1: PASS (9/9)", rc 0 (/tmp/cf1-v/a-r11/run_labs.txt).'),
 'CF1-a-gate-page-smoke': ('PASS', 'Round 11 re-run: tools/page_smoke.py --unit CF1 --pages index L01 L02 -> index, L01, L02 PASS; "page_smoke CF1: PASS", rc 0 (/tmp/cf1-v/a-r11/smoke.txt).'),
 'CF1-a-gate-lint-types': ('PASS', 'Round 11 re-run: ruff check tests/labs/CF1 and ruff format --check -> "9 files already formatted", rc 0; mypy --no-incremental tests/labs/CF1 -> "Success: no issues found in 9 source files", rc 0 (/tmp/cf1-v/a-r11/ruff.txt, mypy.txt).'),
 'CF1-a-gate-pytest': ('PASS', 'Round 11 re-run: pytest -q tests/test_labs.py tests/test_page_checks.py tests/test_refs.py -> all dots, rc 0 (/tmp/cf1-v/a-r11/pytest.txt).'),
 'CF1-a-cite-verify-refs': ('PASS', 'Round 11 re-run: tools/verify_refs.py --offline -> "offline integrity: 560 entries, 0 problems", rc 0; tools/verify_refs.py --unit CF1 (live) -> "live re-verification of CF1: 2 of 560 entries, 0 problems", rc 0 (/tmp/cf1-v/a-r11/vr_offline.txt, vr_live.txt).'),
}
NEW = [
 {'id': 'CF1-a-r11-changed-numbers', 'check': 'every number in the changed sentences recomputed', 'location': 'L01.html lines 111, 322, 338, 438; L02.html lines 280, 300, 508; cards.json CF1-c012', 'status': 'PASS',
  'evidence': 'ledgers/CF1/scripts/CF1-a-r11/recompute.py run with python -I (/tmp/cf1-v/a-r11/recompute.py): WC PV at 8% of -690, 10, 0, 680 at periods 1-4 = -130.4952 (page: -130.50, L02.html line 300); 100[1.08^-3 - 1.08^-1] = -13.2094 (R2); NPV at 8% of the L02 flows 534.24 and with the 2,000 sunk charge -1,465.76 (L02.html lines 157, 270); P3 values 30 and 20 at r=0, 7.44 and 9.09 at 0.10, 10.77 at r*=1/12 (L01.html line 396). Lab 1 Part A values 7,000.00, -46.94, 1,211.49 are the printed output of the twin (run). Ratio 13.2094/100 = 0.132 (L02.html line 397).'},
 {'id': 'CF1-a-r11-lab-expected-vs-twin', 'check': 'page expected block and page code equal the twin', 'location': 'L01.html lines 178-313; L02.html lines 162-271; tests/labs/CF1/lab-CF1-L01-1.py, lab-CF1-L02-1.py', 'status': 'PASS',
  'evidence': 'ledgers/CF1/scripts/CF1-a-r11/expcheck.py (python -I): for L01 and L02 the pre.expected text equals the twin stdout under python -I -W error, and the page code block equals the twin file (True, True for both). tests/labs/CF1 has 0 changed files since af08ad1 (git diff --name-only).'},
 {'id': 'CF1-a-r11-alt-implementations', 'check': 'two correct alternative NPV implementations (Horner form) print the same output', 'location': 'tests/labs/CF1/lab-CF1-L01-1.py npv_dollars; tests/labs/CF1/lab-CF1-L02-1.py npv_dollars', 'status': 'PASS',
  'evidence': 'ledgers/CF1/scripts/CF1-a-r11/alt_l01_horner.py and alt_l02_horner.py (backward recursion acc = acc/(1+r) + C_t) run under python -I -W error: output identical to the twin output (diff empty), so the printed expected blocks do not depend on the summation order.'},
 {'id': 'CF1-a-r11-check-liveness', 'check': 'the printed True checks in the L02 lab can fail', 'location': 'tests/labs/CF1/lab-CF1-L02-1.py lines 220-226; L02.html line 272', 'status': 'PASS',
  'evidence': 'ledgers/CF1/mutants/CF1-a-r11/n04 (shield check compares with EBITDA times tax) and n07 (identity check drops the shield term): both killed (printed True becomes False; ledgers/CF1/scripts/CF1-a-r11/mutants_all.txt, n07.txt). The shield-check and identity-check claims of L02.html line 272 can therefore be falsified by the printed output.'},
 {'id': 'CF1-a-r11-survivors', 'check': 'the two surviving mutants are out of scope', 'location': 'ledgers/CF1/mutants/CF1-a-r11/n05_l02_identity_check_stubbed_true.py; ledgers/CF1/mutants/CF1-a-r9/r9_m07_no_tax_credit.py; L02.html lines 87, 116, 272', 'status': 'PASS',
  'evidence': 'n05 replaces the identity check by identity_ok = True: printed output is unchanged, so only a code reading (not the printed expected block) reveals it. r9_m07 floors the tax at zero: output unchanged because EBIT is positive in every year of the seed (L02 twin output lines 258-261). L02.html line 116 says the lab "does not test any firm\'s tax position", and no page sentence states that the printed output exercises negative taxable income. The mutants violate the code, not a stated output behaviour, so they are recorded here and not in the mutants list (equivalent for the printed output).'},
 {'id': 'CF1-a-r11-date0-term', 'check': 'the term date-0 is understood before use', 'location': 'L01.html line 111 (first use), lines 220, 275, 306, 338', 'status': 'PASS',
  'evidence': 'grep -n date-0 L01.html: first use is line 111, where "the date-0 flow" is tied to C_0 in the same sentence; Section 1 (line 55) fixes flows at period ends and period 0. The term is a synonym of period 0, not a new concept. No definition is needed beyond that.'},
]
NEW_MUT = [
 {'id': 'm02-n04', 'file': 'ledgers/CF1/mutants/CF1-a-r11/n04_l02_shield_check_uses_ebitda.py', 'description': 'L02 lab: shield check compares the operating-cash-flow difference with EBITDA times the tax rate instead of depreciation times the tax rate (new, round 11)', 'killed_by': 'round 11 run_mut.py: printed shield line becomes False (killed)'},
 {'id': 'm02-n06', 'file': 'ledgers/CF1/mutants/CF1-a-r11/n06_l01_years_drawn_with_randrange.py', 'description': 'L01 lab: Part B project lengths drawn with randrange(1, 15) instead of randint(1, 15) (new, round 11)', 'killed_by': 'round 11 run_mut.py: stdout differs from twin (killed)'},
 {'id': 'm02-n07', 'file': 'ledgers/CF1/mutants/CF1-a-r11/n07_l02_identity_check_drops_shield_term.py', 'description': 'L02 lab: identity check drops the tau times D term (new, round 11)', 'killed_by': 'round 11 run_mut.py: printed identity line becomes False (killed)'},
]
GATES_NEW_IDS = set()
rows = []
for r in prev['rows']:
    if r['id'] in OVR:
        st, ev = OVR[r['id']]
        rows.append({'id': r['id'], 'check': r['check'], 'location': r['location'], 'status': st, 'evidence': ev})
    elif r['status'] == 'PASS':
        rows.append({'id': r['id'], 'check': r['check'], 'location': r['location'], 'status': 'PASS',
                     'evidence': CARRY.format(files=files_of(r['location'])) + ' ' + r['evidence']})
    else:
        raise SystemExit('unhandled non-PASS row ' + r['id'])
rows += NEW
mutants = [dict(m) for m in prev['mutants']] + NEW_MUT
for m in mutants:
    m['killed_by'] = m.get('killed_by') or 'round 10 run_mut.py: killed'
frag = {
 'unit': 'CF1', 'slice': 'CF1-a', 'round': 11,
 'verifier': 'independent Haiku verifier, round 11, slice CF1-a (hub index.html, L01, L02 and their lab twins); did not build CF1 and shares no context with the builders',
 'pin': '91946cf',
 'base': 'af08ad1 (round 10 pin). Delta in this slice (git diff af08ad1 91946cf): index.html lines 140 (L03 title) and 142 (L05 card); L01.html lines 111, 322, 338, 438; L02.html lines 280, 508; cards.json entry CF1-c012. Lab twins tests/labs/CF1/* unchanged; L03, L05, L06, project and grader changes are outside this slice.',
 'previous_fragment': '/tmp/fanout-frags/CF1-a.round10.json (context only; PASS rows carried only where the cited subject is byte-identical since af08ad1; changed subjects re-verified)',
 'checkout': '/tmp/verify11-CF1-a', 'scratch': '/tmp/cf1-v/a-r11',
 'verified_at': '2026-10-28T06:30:00+00:00',
 'verdict': 'PASS',
 'registry_flags': [], 'freshness_flags': [],
 'mutants': mutants,
 'notes': prev['notes'][:0] + [
  'Round 11 PASS. The four round 10 FAIL rows about L01 and L02 full reads, the line 338 sign-change inference, the L02 line 508 references sentence and scope words, the card CF1-c012 and the hub L05 card are re-verified and PASS (see their evidence).',
  'Full reads: L01.html 1-570 and L02.html 1-522 read line by line in this round. index.html lines 1-175 read in this round; no hub line is quoted without a locator.',
  'Hub titles: the round 10 observations (L03 card title and L05 card title differing from the h1) are resolved in the delta: index.html line 140 and 142 now equal L03.html line 35 and L05.html line 36.',
  'Mutants: 58 lab mutant files re-run (CF1-a-r7..r11 folders); 56 killed. Survivors r9_m07 and n05 are out of scope (see CF1-a-r11-survivors). Three new round 11 mutants killed (m02-n04, m02-n06, m02-n07). Alternative correct implementations: two Horner-form NPV variants print the same output.',
  'Not checked: no external source was read (no registry key is cited in L01 or L02; the hub reading list is rendered from the registry, graham2001theory). No learner trial. Hours not re-judged (architect ruling); lesson hours 8 + 8 match the hub split. Lab timings beyond page_smoke were not re-measured. Project, grader and L03 to L06 changes are out of this slice.'],
 'summary': None,
 'rows': rows,
}
n = len(rows); p = sum(1 for r in rows if r['status'] == 'PASS')
frag['summary'] = f'Slice CF1-a round 11 (pin 91946cf, delta from af08ad1): {"PASS" if p == n else "FAIL"}. {p} of {n} rows PASS. All gates re-run PASS. The round 10 FAIL rows are re-verified and PASS (full reads of L01 and L02 completed; line 338 and card CF1-c012 now carry the C_0 < 0 premise; L02 line 508 names the EBITDA, OCF, NWC and NPV sources; hub L05 card matches L05). Mutants: 58 lab files re-run, 56 killed, 2 out-of-scope survivors recorded; 3 new mutants killed; 2 alternative correct NPV implementations print the same output.'
out = ROOT / 'ledgers/CF1/CF1-a.json'
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + '\n')
print('rows', n, 'pass', p, 'mutants', len(mutants))
