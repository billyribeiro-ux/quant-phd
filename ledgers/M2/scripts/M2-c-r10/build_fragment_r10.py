import json
R9 = json.load(open('/Users/billyribeiro/.fanout/frags/B-M2-c.round9.json'))
PIN = 'e8b10b8110923bd88c3b4bd0e36e1571be3e6725'
BASE = 'b6865c7d10020e31b9858a49edf751f4b814c031'
L13 = 'course/modules/M/M2/L13.html'
L14 = 'course/modules/M/M2/L14.html'
L17 = 'course/modules/M/M2/L17.html'
CARDS = 'course/modules/M/M2/cards.json'

# Fresh rows: id -> (status, location, evidence, fix)
FRESH = {
 'M2c-gate-check-pages': ('PASS', 'tools/check_pages.py --all', "Round-10 fresh: ledgers/M2/scripts/M2-c-r10/check_pages.out 'check_pages M2: PASS', exit 0 at pin e8b10b8.", None),
 'M2c-gate-check-dag': ('PASS', 'tools/check_dag.py --all', "Round-10 fresh: ledgers/M2/scripts/M2-c-r10/check_dag.out, exit 0 (all units PASS, M2 included).", None),
 'M2c-gate-run-labs': ('PASS', 'tools/run_labs.py --unit M2', "Round-10 fresh: run_labs_M2.out 'run_labs M2: PASS (27/27)', exit 0.", None),
 'M2c-labs-twin-isolated': ('PASS', 'tests/labs/M2/lab-M2-L13-1.py .. lab-M2-L18-1.py', "Round-10 fresh: each twin run as .venv/bin/python -I -W error exits 0 (twin_L13..L18.err empty).", None),
 'M2c-gate-page-smoke': ('PASS', 'tools/page_smoke.py --unit M2 --pages L13..L18', "Round-10 fresh: page_smoke.out 'page_smoke M2: PASS', exit 0.", None),
 'M2c-gate-ruff-mypy-pytest': ('PASS', 'ruff check/format tests/labs/M2; mypy --no-incremental on L13-L18 twins; pytest tests/test_labs.py -k M2', "Round-10 fresh: ruff_check.out exit 0; ruff_format.out exit 0; mypy.out 'Success: no issues found in 6 source files'; pytest_labs_M2.out 27 passed, exit 0.", None),
 'M2c-verify-refs': ('PASS', 'tools/verify_refs.py --offline', "Round-10 fresh: verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', exit 0. Live run not performed (network).", None),
 'M2c-banned-scan': ('PASS', 'L13-L18 changed sentences and cards M2-c187, c234, c256, c258', "Round-10 fresh read of every changed sentence (git diff b6865c7..e8b10b8): L13 l.143, L14 l.66 and l.78, L17 l.250/283/297/308/335-338, and the four changed cards. No process word (builder, verifier, round, fixed, revised) and no first-person text.", None),
 'M2c-scope-words': ('PASS', 'changed sentences: L13 l.143, L14 l.66/l.78, L17 l.250-338, cards c187/c234/c256/c258', "Round-10 fresh: no new universal scope word. c234 'for every n' is supported by Example 3.4 algebra g(1/n,1/n)=(1/n^2)/(2/n^2)=1/2 for all n (numcheck_r10.out). 'provided' at L13 l.143 is the h* <= h0 proviso, already stated with the minimizer.", None),
 'M2c-notation': ('PASS', 'notation/notation.json vs L13-L18 changed symbols (w, alpha, delta, M_3, g)', "Round-10 fresh: notation.json registers only T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q and macros; w, alpha, delta and g are local per its 'about' field. L17 uses g only as the function g of Section 4 (grep: l.201, 217, 339, 389-418; no gradient g remains), and w only as the gradient in Theorem 3.1 and P2 (l.106, 111, 250, 266-268, 286, 300, 311, 338, 377). L13 M_3 defined at l.143 and P3.", None),
 'M2c-card-duplicates': ('PASS', CARDS, "Round-10 fresh: cards.json has 378 entries; python check: no duplicate ids, no duplicate fronts, no duplicate backs (case-insensitive).", None),
 'M2c-cards-L13': ('PASS', CARDS + ' lesson L13 (M2-c181..c201, c380, c381)', "Round-10 fresh: M2-c187 back (l.143 wording) re-derived: B_c'(h)=(M3/3)h-delta/h^2, zero at h*=(3delta/M3)^(1/3), B_c''>0, proviso h*<=h0 present; card statement matches L13 l.143 and P3. Other L13 cards byte-identical since b6865c7.", None),
 'M2c-cards-L15': ('PASS', CARDS + ' M2-c234 (L15, now grade T)', "Round-10 fresh: M2-c234 now grade T with no basis; g(1/n,1/n)=1/2 (Example 3.4, l.132), f(1/n,1/n)=1/(2n) (Problem E3, l.335), Lab 1 printed values n=10: g 0.500000, f 0.050000000; n=10000: f 0.000050000 (lab output l.224-229; numcheck_r10.out matches). Every cited locator exists in L15.", None),
 'M2c-cards-L17': ('PASS', CARDS + ' lesson L17 (M2-c251..c264; changed M2-c256, c258)', "Round-10 fresh: M2-c256 (hypotheses w != 0, u = w/|w|, value |w|, identity |w-(u.w)u|^2=|w|^2-(u.w)^2 verified by identity check, numcheck_r10.out) and M2-c258 ((1,1) at 45 degrees, Section 4, Assumption 1) match L17 l.106-111, l.308-311, Section 4. Other L17 cards byte-identical since b6865c7.", None),
 'M2c-L13-theorems': ('FAIL', L13 + ' l.301 (P3 statement); also l.83-85 Theorem 2.2, l.116-125 Prop 3.2, l.133-135 Corollary 4.1 (checked)', "Round-10 fresh: Theorem 2.2 statement and Taylor proof (l.83-96) re-derived, correct; Prop 3.2 statement and proof (l.110-125) correct; Corollary 4.1 bound and B'(h), B''(h), B(h*)=2sqrt(M delta) re-derived (numcheck_r10.out). l.143 now carries 'Assume f''' is continuous on [x-h0,x+h0], so that M3 is finite' (fixed). BUT P3 at l.300-301 still states 'Under the central hypotheses of Theorem 2.2 and Proposition 3.2, with M_3 = max|f'''| on [x - h_0, x + h_0], delta > 0 and M_3 > 0' with no finiteness hypothesis on f''' over [x-h0,x+h0]; Theorem 2.2 assumes continuity only on [x-h,x+h] for one h. The P3 solution uses M_3 finite. Corollary 4.1 states its finiteness hypothesis explicitly; P3 does not.", "Add to P3 (L13.html l.301) the hypothesis 'with f''' continuous on [x - h_0, x + h_0], so that M_3 is finite' as in l.143. Re-run tools/render_curriculum and build checks are not needed (page-only change)."),
 'M2c-L13-balanced-proviso': ('PASS', L13 + ' l.143 and ' + CARDS + ' M2-c187', "Round-10 fresh: l.143 proviso 'provided h* <= h_0 (otherwise the smallest value on (0, h_0] is at h_0)' present; B_c'' = M3/3 + 2delta/h^3 > 0 (numcheck_r10.out: argmin matches h* on three cases). Card M2-c187 carries the same proviso.", None),
 'M2c-L14-theorems': ('FAIL', L14 + ' l.78 (Assumption 1 sentence) and l.69-75 (Definition 2.1)', "Round-10 fresh: l.78 now reads 'assume them in its statement' with a plural subject ('The exponential and sine rules of Definition 2.1 and Proposition 3.1'); the agreement error is not fixed ('its' for two statements). Also, Definition 2.1 (l.69-75) gives the exp and sin tangent rules but its text never mentions Assumption 1 (grep 'Assumption' in L14: lines 78, 86, 96, 100, 106, 108, 115, 254, 265, 272, 356, 372, 388, 421, 430-433), so 'each such statement says so' is false for Definition 2.1. Re-verified and correct: l.66 'runs the operations of Definition 1.1 in program order' (Definition 1.1 l.~50 agrees); Example 4.1 numbers (e^2=7.389056099, f(2)=15.232760911, f'(2)=21.731770522 by product, quotient and closed form); Prop 3.1 proof; Prop 5.2 and Example 5.1 (x1bar=2+cos1=2.540302306, x2bar=1); Section 6 branch examples.", "l.78: change 'assume them in its statement' to 'assume them in their statements'; and make the Definition 2.1 claim true, e.g. add '(under Assumption 1)' to the exp and sin rules in Definition 2.1 l.73 or rewrite l.78 to say only that Proposition 3.1 and the closed forms use Assumption 1."),
 'M2c-L17-numbers': ('PASS', L17 + ' E3 l.297-300, R1 l.308-311, E2 l.290-293', "Round-10 fresh: E3 numbers re-derived: gradient angle 61.960247 deg, alpha = 0.039753 deg = 6.938e-4 rad (text 6.9e-4), alpha^2/2 = 2.407e-7 (text 2.4e-7), |w|(1-cos alpha) = 5.12e-7 (text 5e-7). R1: unit gradient (0.470084, 0.882622), max-norm rescale (0.532600, 1), value 2.410182 (text 2.4102, unrounded 2.410182), corner 2.8775826 (numcheck_r10.out). E2 truncation max 3.6e-13 bounded by 1.2e-12 in the E2 solution; rounding about 1e-10 (E2 unchanged).", None),
 'M2c-L17-theorems': ('PASS', L17 + ' Theorem 3.1 l.106, proof l.111, P2 l.266-268, Section 4 bullets l.201-217', "Round-10 fresh: Theorem 3.1 with w: u = w/|w| maximizes u.w, value |w|; proof identity |w-(u.w)u|^2 = |w|^2 - 2(u.w)^2 + (u.w)^2 = |w|^2 - (u.w)^2 re-derived; equality case w=(u.w)u=|w|u gives u=w/|w| (checked). Section 4 g(tu)=cos(theta)sin(theta) re-derived (g(0)=0 so difference quotient cos sin / t). P2 polar form correct.", None),
 'M2c-L17-g-w-rename': ('PASS', L17 + ' l.250, 286, 300, 311, 338 and remaining g uses l.201, 217, 339, 389-418', "Round-10 fresh: regex scan of L17 finds no gradient written as g; the only g uses are the function g(x,y)=xy/(x^2+y^2) of Section 4 and the quiz (l.201, 217, 339, 389, 395, 412, 418). Gradient is w at l.106, 111, 250, 266-268, 286, 300, 311, 338, 377. Round-9 FAIL (l.250/286/300/311 still g) is fixed. The E3 angle symbol alpha (l.300) replaces delta and is defined inline.", None),
}

notes_carry = {
 # carried rows: id -> (files, evidence override or None)
}

rows = []
for r in R9['rows']:
    rid = r['id']
    if rid in FRESH:
        status, loc, ev, fix = FRESH[rid]
        row = {'id': rid, 'check': r['check'], 'location': loc, 'status': status, 'evidence': ev}
        if status != 'PASS':
            row['fix'] = fix
        rows.append(row)
        continue
    if r['status'] != 'PASS':
        raise SystemExit(f'unhandled round-9 non-PASS row {rid}')
    old = r['evidence']
    ev = ("Carried from round 9 (cited subject byte-identical between b6865c7 and e8b10b8; the round-10 delta touches only "
          "L13.html l.143, L14.html l.66 and l.78, L17.html l.250, 283, 297, 308, 335-338 and cards M2-c187, c234, c256, c258): " + old)
    rows.append({'id': rid, 'check': r['check'], 'location': r['location'], 'status': 'PASS', 'evidence': ev})

# add a new row for the L14 Assumption-1 claim: keep as separate FAIL row
rows.append({
 'id': 'M2c-L14-assumption1-claim',
 'check': '2.4-mathematics',
 'location': L14 + ' l.69-75 (Definition 2.1) vs l.78 (Assumption 1 paragraph)',
 'status': 'FAIL',
 'evidence': "Round-10 fresh: l.78 says the exp and sine rules of Definition 2.1 'assume them in its statement' and that 'each such statement says so'. Definition 2.1 l.69-75 contains the rules exp(a+b eps)=e^a+b e^a eps and sin(a+b eps)=sin a+b cos a eps and does not mention Assumption 1 (see the grep list in M2c-L14-theorems). The claim is false for Definition 2.1.",
 'fix': "Add '(under Assumption 1)' to the exp and sin rules of Definition 2.1 (l.73) and make l.78 say 'Proposition 3.1 assumes them in its statement, and Definition 2.1 uses them' with correct agreement.",
})

frag = {
 'unit': 'M2', 'slice': 'c', 'round': 10,
 'verifier': 'Haiku 5.5 independent verifier (B10)',
 'pin': PIN,
 'base': BASE + ' (round-9 pin; round-9 fragment /Users/billyribeiro/.fanout/frags/B-M2-c.round9.json used as context and for carried rows)',
 'checkout': '/Users/billyribeiro/.fanout/wt/verifyB10-M2-c',
 'scratch': '/Users/billyribeiro/.fanout/wt/verifyB10-M2-c/ledgers/M2/scripts/M2-c-r10',
 'verified_at': '2026-10-29',
 'verdict': 'FAIL',
 'rows': rows,
 'mutants': [],
 'registry_flags': [],
 'freshness_flags': [],
 'notes': ("Slice L13-L18 and six lab twins. No project grader in the slice, so no mutation test (ruling); check_projects --all run (PASS, AP1 and all units). "
           "Round-10 delta on slice paths (git diff b6865c7..e8b10b8): L13.html l.143 (finiteness sentence added), L14.html l.66 ('forward mode ... program order') and l.78 (verb changed), "
           "L17.html l.250, 283, 297, 308, 335-338 (gradient g renamed w; alpha for the angle at l.297-300), cards M2-c187, c234, c256, c258, plus cards outside the slice (M2-c388 new, c003, c064, c163, c180, c299, c315, c326, c347) which are not in slice c. "
           "Not re-read line by line this round: the unchanged hunks of L13-L18 (carried by byte-identity of the cited subjects, per the round rule); L15, L16 and L18 HTML are unchanged since b6865c7. "
           "Not run: verify_refs live (network), render_curriculum (no curriculum yaml in the delta), build_site --check (run, PASS, but the fragment does not carry it as a row), browser beyond page_smoke, five alternative implementations (no grader)."),
 'summary': ("Slice c, round 10: %d rows. Round-9 FAILs: M2c-L17-g-w-rename now PASS (fixed); M2c-cards-L15 now PASS (c234 regraded T with its basis in the lesson); "
             "M2c-L13-theorems still FAIL (P3 l.301 omits the finiteness hypothesis that l.143 now gives); M2c-L14-theorems still FAIL (l.78 'its statement' agreement, and Definition 2.1 does not say it uses Assumption 1). "
             "New FAIL M2c-L14-assumption1-claim (same defect as the second half of M2c-L14-theorems, split out for a precise fix)." ) % len(rows),
}
json.dump(frag, open('ledgers/M2/M2-c.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(rows), 'non-PASS', [r['id'] for r in rows if r['status'] != 'PASS'])
