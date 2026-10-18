# PROPOSALS-L05: central edits for benchmark gaps G2 and G5

This file lists every change to shared files that the L05 work on branch
`worktree-agent-a288e181d4f5eb635` needs. None of these edits is committed on
the branch. The gates were run with all of them applied temporarily and then
reverted (section 7). Apply them centrally in the order below.

The L05 page itself is committed on the branch:

- **§6, "From StepM to simultaneous bands":**
  - Definitions 6.1, 6.2 and 6.6;
  - Theorem 6.3;
  - Proposition 6.4;
  - Remark 6.5;
  - Lab 4.
- **§7, "Tolerating a few false claims: the k-FWER and FDP exceedance":**
  - Definitions 7.1 and 7.9;
  - Lemmas 7.2, 7.3 and 7.6;
  - Theorems 7.4, 7.5, 7.7 and 7.10;
  - Proposition 7.8;
  - Lab 5.
- **Problems:** M4, P4 and R4 are new. R3 is rewritten.
- **Sections 8–13:** renumbered from 6–11.

## 1. References: admit by DOI

All seven were admitted in the worktree with exactly these commands. Each
printed the key shown. The citation strings use the print year, which is what
`verify_refs.py` checks against `print_year`.

| Key | DOI | Print year (Crossref `published-print`) |
|---|---|---|
| `lehmann2005generalizations` | 10.1214/009053605000000084 | 2005 |
| `romano2007control` | 10.1214/009053606000001622 | 2007 |
| `romano2007formalized` | 10.1017/s0266466608080171 | 2008 (online 2007) |
| `laan2004augmentation` | 10.2202/1544-6115.1042 | 2004 |
| `benjamini2005false` | 10.1198/016214504000001907 | 2005 |
| `olea2018simultaneous` | 10.1002/jae.2656 | 2019 (online 2018) |
| `andrews2023inference` | 10.1093/qje/qjad043 | 2024 (online 2023) |

```bash
.venv/bin/python tools/add_reference.py --doi 10.1214/009053605000000084 --source "Lehmann & Romano (2005), 'Generalizations of the Familywise Error Rate', Annals of Statistics 33(3)" --used-by S7
.venv/bin/python tools/add_reference.py --doi 10.1214/009053606000001622 --source "Romano & Wolf (2007), 'Control of Generalized Error Rates in Multiple Testing', Annals of Statistics 35(4)" --used-by S7
.venv/bin/python tools/add_reference.py --doi 10.1017/s0266466608080171 --source "Romano, Shaikh & Wolf (2008), 'Formalized Data Snooping Based on Generalized Error Rates', Econometric Theory 24" --used-by S7
.venv/bin/python tools/add_reference.py --doi 10.2202/1544-6115.1042 --source "van der Laan, Dudoit & Pollard (2004), 'Augmentation Procedures for Control of the Generalized Family-Wise Error Rate and Tail Probabilities for the Proportion of False Positives', Statistical Applications in Genetics and Molecular Biology 3(1)" --used-by S7
.venv/bin/python tools/add_reference.py --doi 10.1198/016214504000001907 --source "Benjamini & Yekutieli (2005), 'False Discovery Rate–Adjusted Multiple Confidence Intervals for Selected Parameters', JASA 100(469)" --used-by S7
.venv/bin/python tools/add_reference.py --doi 10.1002/jae.2656 --source "Montiel Olea & Plagborg-Møller (2019), 'Simultaneous Confidence Bands: Theory, Implementation, and an Application to SVARs', Journal of Applied Econometrics 34(1)" --used-by S7
.venv/bin/python tools/add_reference.py --doi 10.1093/qje/qjad043 --source "Andrews, Kitagawa & McCloskey (2024), 'Inference on Winners', QJE 139(1)" --used-by S7
```

The Romano, Shaikh and Wolf string carries no issue number. Crossref records
the issue as `02`. The matcher compares the leading number literally, so
`"24(2)"` is rejected (`{'issue': ('2', '02')}`). I did not change
`tools/refs/match.py` to get around this, per CLAUDE.md rule 4.

A follow-up, if wanted: make `norm_issue` strip leading zeros, with a test in
`tests/test_refs.py`. The string could then read `24(2)`.

**What was read.**

- **Read in full:** Lehmann–Romano (2005), from arXiv math/0507420, the IMS
  reprint of the published article; and Romano–Wolf (2007), from arXiv
  0710.2258, likewise. Every locator on those two papers was checked against
  the text: Theorems 2.1–2.3, 3.1–3.3, Lemma 3.1, Remark 2.1, Eqs. (12),
  (26), (27) and (34); Algorithms 2.1, 2.2 and 4.1, Eqs. (19)–(21),
  Theorems 3.3 and 4.1, Remarks 3.2–3.3 and Section 5.
- **Abstract only (OpenAlex, no email sent):** the other five. The full texts
  were closed or blocked by bot protection. Every claim on them is attributed
  to the abstract, with `data-locator="Abstract"`. BY (2005) is used only
  through two verbatim quotations and a description of its procedure.

## 2. Curriculum: the S7 entry in `curriculum/01-foundations.yaml`

```diff
       - id: S7
         title: "Research Integrity & Multiple Testing"
         tier: M
-        hours: 80
+        hours: 83
         prereqs: [S1, S2, S3]
@@ introduces
           romano-wolf-stepdown: "Romano–Wolf StepM procedure"
+          simultaneous-confidence-band: "Simultaneous confidence band (bootstrap sup-t band)"
+          false-coverage-statement-rate: "False coverage-statement rate (FCR)"
+          k-familywise-error-rate: "k-familywise error rate (k-FWER)"
+          false-discovery-exceedance: "False discovery exceedance, P(FDP > γ)"
           t-stat-hurdle: "Multiple-testing t-statistic hurdle"
@@ uses
           - t-statistic
+          - confidence-interval
+          - coverage-probability
           - bootstrap
@@ sources (append after Gelman & Loken)
+          - "Lehmann & Romano (2005), 'Generalizations of the Familywise Error Rate', Annals of Statistics 33(3)"
+          - "Romano & Wolf (2007), 'Control of Generalized Error Rates in Multiple Testing', Annals of Statistics 35(4)"
+          - "Romano, Shaikh & Wolf (2008), 'Formalized Data Snooping Based on Generalized Error Rates', Econometric Theory 24"
+          - "van der Laan, Dudoit & Pollard (2004), 'Augmentation Procedures for Control of the Generalized Family-Wise Error Rate and Tail Probabilities for the Proportion of False Positives', Statistical Applications in Genetics and Molecular Biology 3(1)"
+          - "Benjamini & Yekutieli (2005), 'False Discovery Rate–Adjusted Multiple Confidence Intervals for Selected Parameters', JASA 100(469)"
+          - "Montiel Olea & Plagborg-Møller (2019), 'Simultaneous Confidence Bands: Theory, Implementation, and an Application to SVARs', Journal of Applied Econometrics 34(1)"
+          - "Andrews, Kitagawa & McCloskey (2024), 'Inference on Winners', QJE 139(1)"
```

**Concepts.** L05 defines the four new concepts with `<dfn data-concept>`:

- `simultaneous-confidence-band` in Definition 6.1;
- `false-coverage-statement-rate` in Definition 6.6;
- `k-familywise-error-rate` and `false-discovery-exceedance` in Definition 7.1.

It links `confidence-interval` and `coverage-probability`, both of which S1
introduces and S7 already reaches through its prerequisites.

**Hours: L05 goes from 7 to 10, so S7 goes from 80 to 83.** L05 gains:

- two sections, with 4 definitions, 4 theorems, 3 lemmas, 2 propositions and
  a remark, every one with a full proof;
- two labs;
- three new problems (M4, P4, R4) and one rewritten (R3);
- two misconceptions and three quiz items.

At the pace of the existing lessons, §6 and §7 take about 1¼ h and 1¾ h, and
the new problems about 1 h, less the time of the replaced R3. L05 stays inside
the 6–12 h band. The project's share is 24/83 = 29%, inside 10–40%.

`render_curriculum.py` then reports the following. These are copied from its
output with the edits applied; none was typed.

- Total design hours: 13,695 → **13,698**. Concepts: 1,121 → **1,125**.
- Master's in Finance / Financial Engineering: 7,646 → **7,649** h.
  PhD in Finance: 9,171 → **9,174** h.
- Financial Econometrics core: 290 → **293**. Tier M: 5,770 → **5,773** h.
- Master's-Equivalent: 11,135 → **11,138** (5.16 FTE years).
- Doctoral Candidate: 12,495 → **12,498** (5.78 → **5.79**).
- Doctoral: 13,695 → **13,698** (6.34).
- Quantitative Researcher: 4,056 → **4,059**. Quant Developer: 3,756 →
  **3,759**. Research doctorate path: 5,626 → **5,629** (2.60 → **2.61**).

## 3. The S7 hub, `course/modules/S/S7/index.html`

These are exact replacements. Each old string occurs once.

| Old | New |
|---|---|
| `the probability of backtest overfitting. 80 hours, ending in Atlas milestone A8.` | `… 83 hours, ending in Atlas milestone A8.` |
| `data-hours-lessons="56" data-hours-project="24"` | `data-hours-lessons="59" data-hours-project="24"` |
| `Tier M (master's) · 80 hours ·` | `Tier M (master's) · 83 hours ·` |
| `aria-label="56 lesson hours and 24 project hours"` | `aria-label="59 lesson hours and 24 project hours"` |
| `style="width:70%"` … `style="width:30%"` (the hours-split bar) | `style="width:71%"` … `style="width:29%"` |
| `56 h lessons · 24 h project (30%)` | `59 h lessons · 24 h project (29%)` |
| `Eight lessons of seven study hours each. Every lesson has graded claims, runnable labs, a twelve-problem set with worked solutions …` | `Eight lessons: seven of seven study hours and L05 of ten. Every lesson has graded claims, runnable labs, a problem set of at least twelve problems with worked solutions …` (L05 now has 15 problems) |
| L05 card: `<span class="card-kicker">L05 · 7 h</span>` … `<span class="card-body">Step-down bootstrap testing, studentization, and why strategies must be resampled jointly.</span>` | `L05 · 10 h` … `Step-down bootstrap testing, studentization, why strategies must be resampled jointly, simultaneous bands from the same draws, and control of the k-FWER and of false discovery exceedance.` |

## 4. New cards for `course/modules/S/S7/cards.json`

Append these, renumbering `S7-cNEW-n` to the next free `S7-cNNN` ids; the
branch base ends at `S7-c108`. For the gate run they went in temporarily as
`S7-c901` to `S7-c912`, and `check_pages` passed.

Card S7-cNEW-4 uses `basis` exactly as the key-results row has it. Every
other non-T card has a `cite`. Each back can be checked against the L05 text.

```json
[
 {
  "id": "S7-cNEW-1",
  "lesson": "L05",
  "front": "Define a simultaneous confidence band for \\(K\\) mean differentials at level \\(1-\\alpha\\).",
  "back": "Random intervals \\(C_1, \\dots, C_K\\) computed from the data with \\(\\Prob(\\mu_k \\in C_k \\text{ for every } k) \\ge 1-\\alpha\\); it is asymptotically valid if the \\(\\liminf\\) of that probability is at least \\(1-\\alpha\\). The pointwise coverage \\(\\Prob(\\mu_k \\in C_k)\\) of one interval is a statement about that strategy alone (Definition 6.1).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-2",
  "lesson": "L05",
  "front": "How is the bootstrap sup-t band built from StepM's joint draws, and what does it guarantee?",
  "back": "\\(c^{\\pm}_\\alpha\\) is the \\(\\lceil (1-\\alpha)B \\rceil\\)-th smallest of the \\(B\\) maxima \\(\\max_k |t^{\\ast}_{b,k}|\\) over all \\(K\\) strategies, and \\(C_k = \\bar d_k \\pm c^{\\pm}_\\alpha s_k/\\sqrt{T}\\). If the bootstrap is consistent for the distribution of \\(\\max_k |\\tau_k|\\), whose limit is continuous and strictly increasing at its \\((1-\\alpha)\\)-quantile, the simultaneous coverage tends to \\(1-\\alpha\\) (Definition 6.2, Theorem 6.3).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-3",
  "lesson": "L05",
  "front": "When does the sup-t band exclude zero for strategy \\(k\\), and how does that relate to StepM's rejections?",
  "back": "Exactly when \\(|t_k| > c^{\\pm}_\\alpha\\): the two-sided single-step max-\\(|t|\\) test. Since \\(c_\\alpha(\\{1, \\dots, K\\}) \\le c^{\\pm}_\\alpha\\), every strategy whose interval lies above zero is rejected at StepM's first step, and StepM can reject strategies whose interval contains zero (Proposition 6.4).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-4",
  "lesson": "L05",
  "front": "In Lab 4's simulated 20-strategy book, how did the pointwise, Bonferroni and sup-t 95% bands compare?",
  "back": "Pointwise intervals covered all twenty together in 45.5% of studies at correlation 0.3 and 84.8% at 0.9. Bonferroni (critical value 3.023) and sup-t held at both; sup-t was about as wide as Bonferroni at 0.3 (3.031) and 17% narrower at 0.9 (2.508).",
  "grade": "C",
  "basis": "Lab 4 (simulation)"
 },
 {
  "id": "S7-cNEW-5",
  "lesson": "L05",
  "front": "Define the false coverage-statement rate, and state Benjamini and Yekutieli's adjustment for selected intervals.",
  "back": "\\(\\mathrm{FCR} = \\E[V_{\\mathrm{CI}}/\\max(R,1)]\\), with \\(R\\) the number of selected parameters and \\(V_{\\mathrm{CI}}\\) the number of their intervals that miss. Benjamini and Yekutieli build each selected interval at marginal level \\(1 - Rq/K\\): \\(q\\) divided by the number of parameters considered and multiplied by the number selected (Definition 6.6).",
  "grade": "T",
  "cite": [
   "benjamini2005false"
  ]
 },
 {
  "id": "S7-cNEW-6",
  "lesson": "L05",
  "front": "Define the k-FWER and the false discovery exceedance.",
  "back": "The k-FWER is \\(\\Prob(V \\ge k)\\), the probability of \\(k\\) or more false rejections; \\(k = 1\\) is the FWER. The exceedance at \\(\\gamma\\) is \\(\\Prob(\\FDP > \\gamma)\\) with \\(\\FDP = V/\\max(R,1)\\) (Definition 7.1).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-7",
  "lesson": "L05",
  "front": "State Lehmann and Romano's step-down constants for the k-FWER and what they guarantee.",
  "back": "\\(\\alpha_i = k\\alpha/m\\) for \\(i \\le k\\) and \\(k\\alpha/(m + k - i)\\) for \\(i > k\\); the step-down rejects \\(H_{(1)}, \\dots, H_{(r)}\\) while \\(p_{(i)} \\le \\alpha_i\\). It controls the k-FWER at \\(\\alpha\\) under any dependence and is Holm's procedure at \\(k = 1\\) (Theorem 7.4).",
  "grade": "T",
  "cite": [
   "lehmann2005generalizations"
  ]
 },
 {
  "id": "S7-cNEW-8",
  "lesson": "L05",
  "front": "Which step-down constants control \\(\\Prob(\\FDP > \\gamma) \\le \\alpha\\) under any dependence?",
  "back": "Lehmann and Romano's \\(\\alpha_i = (\\lfloor \\gamma i \\rfloor + 1)\\alpha/(m + \\lfloor \\gamma i \\rfloor + 1 - i)\\), divided by \\(C_{\\lfloor \\gamma m \\rfloor + 1}\\) with \\(C_j = \\sum_{l \\le j} 1/l\\) (Theorem 7.7). Without the division they need a condition on the dependence, such as the Simes inequality for the true-null p-values.",
  "grade": "T",
  "cite": [
   "lehmann2005generalizations"
  ]
 },
 {
  "id": "S7-cNEW-9",
  "lesson": "L05",
  "front": "How does augmentation turn a procedure that controls the FWER into one that controls \\(\\Prob(\\FDP > \\gamma)\\)?",
  "back": "Add the \\(\\lfloor \\gamma R_0/(1-\\gamma) \\rfloor\\) most significant remaining hypotheses to its \\(R_0\\) rejections. If the original procedure makes no false rejection, the FDP is then at most \\(\\gamma\\), so \\(\\Prob(\\FDP > \\gamma) \\le \\alpha\\) (Proposition 7.8).",
  "grade": "T",
  "cite": [
   "laan2004augmentation"
  ]
 },
 {
  "id": "S7-cNEW-10",
  "lesson": "L05",
  "front": "How does k-StepM choose its critical value at step \\(j\\), and why?",
  "back": "\\(d_j = \\max\\{c^{(k)}_\\alpha(A_j \\cup I) : I \\subseteq R_{j-1}, |I| \\le k-1\\}\\), where \\(c^{(k)}_\\alpha\\) is the bootstrap quantile of the \\(k\\)-th largest \\(t^{\\ast}\\). Up to \\(k-1\\) rejected strategies are let back in because earlier false rejections may already have removed true hypotheses from the active set (Definition 7.9, Theorem 7.10).",
  "grade": "T",
  "cite": [
   "romano2007control"
  ]
 },
 {
  "id": "S7-cNEW-11",
  "lesson": "L05",
  "front": "What is the coverage of the conventional 95% interval for the best of 20 independent null strategies?",
  "back": "\\(0.975^{20} - 0.025^{20} = 0.603\\): it covers only when the largest t-statistic lies within \\(\\pm 1.96\\). The winner's interval from the sup-t band keeps coverage of at least \\(1-\\alpha\\) asymptotically, whatever rule picked it (Problem R4).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-12",
  "lesson": "L05",
  "front": "Do twenty 95% confidence intervals give 95% confidence that all twenty contain the truth?",
  "back": "No. Each covers its own mean 95% of the time; all twenty cover together with probability \\(\\Prob(\\max_k |\\tau_k| \\le 1.960)\\), far lower unless the strategies move together. A joint statement needs a simultaneous band, such as Bonferroni's or the sup-t band (Definition 6.1).",
  "grade": "T"
 }
]
```

## 5. Regenerate after applying §1–§4

```bash
.venv/bin/python tools/render_curriculum.py   # CURRICULUM.md, curriculum/curriculum.json
.venv/bin/python tools/build_site.py          # course/assets/data/*, course/index.html, course/concepts.html
```

`build_site.py` picks up the four concepts in `glossary.json` and
`concepts.html`, and the seven short citations in
`course/assets/data/references.json`.

## 6. Other central items

- **A8, rung 4 (suggestion only).** The A8 contract, grader and project are
  unchanged. The stretch rung could add
  `sup_t_band(differentials, alpha, n_boot, mean_block, seed) -> (lower, upper, critical_value)`.
  - It should reuse the joint stationary-bootstrap draws of the StepM
    function.
  - Its natural tests are:
    - `critical_value >= StepM's first-step critical value` on the same
      draws (Proposition 6.4(b));
    - `0 not in [lower_k, upper_k]` exactly when `|t_k| > critical_value`
      (Proposition 6.4(a)).
- **`benchmarks/S7.md`.** G2 and G5 can be marked closed in L05 §6–§7. Two
  qualifications:
  - The band lab does not show the sup-t band narrower than Bonferroni at
    Lab 1's correlation of 0.3: 3.031 against 3.023. At correlation 0.9 it is
    17% narrower. Remark 6.5 and the lab's interpretation explain why, and
    the page reports this as it is.
  - FDX is proved under arbitrary dependence (Theorems 7.5, 7.7, Lemma 7.6,
    Proposition 7.8). Lehmann–Romano's uncorrected constants (3) are stated
    with their published conditions (their Theorems 3.1–3.2), not proved on
    the page.
- **Notation.** No `notation.json` change is needed. The new symbols are
  local to L05:
  - \(c^{\pm}_\alpha\), \(c^{(k)}_\alpha\) and \(\max^{(k)}\);
  - \(C_j\), which is Lesson 3's \(c(j)\);
  - \(\gamma\) as the FDP bound, which is not registered and differs from the
    registered \(\gamma_3\) and \(\gamma_4\).
- **Concept owner.** L03 §8's canon break says that "none of this lesson's
  procedures" controls the exceedance. That is still true, and L05 §7 now
  supplies the tool. L03 could add a forward link, but it is not required.

## 7. How the gates were run

Every edit in §1–§4 was applied to the worktree, then `render_curriculum.py`
and `build_site.py` were run. The gates were then run. Afterwards
`references/references.json`, the S7 curriculum entry, `CURRICULUM.md`,
`curriculum/curriculum.json`, `course/assets/data/*`, `course/index.html`,
`course/concepts.html`, the hub and `cards.json` were restored with
`git checkout`.

The branch already had main (727ed58) merged in. Results with the edits
applied:

| Gate | Result |
|---|---|
| `ruff check .` and `ruff format --check .` | pass |
| `mypy` (strict) | no issues in 64 source files |
| `pytest` | 163 passed |
| `render_curriculum.py`, then `build_site.py --check` | site data current |
| `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all` | PASS |
| `run_labs.py --unit S7` | PASS (33/33) |
| `verify_refs.py --offline` | 522 entries, 0 problems |
| `page_smoke.py --unit S7 --pages L05`, with labs and the figure sweep | PASS |

Pyodide lab times in the `page_smoke` run, all under the 10 s limit:

| Lab | Time |
|---|---|
| L05-1 | 2.3 s |
| L05-2 | 4.4 s |
| L05-3 | 0.3 s |
| L05-4 | 2.8 s |
| L05-5 | 0.7 s |

`run_graders.py` and `mutate_graders.py` were not run. No grader file changed.

**Without these edits, the branch fails two gates:**

- `check_pages` fails because L05 declares 10 h and the hub still says 56
  lesson hours.
- `check_dag` fails because S7 does not yet introduce the four new concepts.
