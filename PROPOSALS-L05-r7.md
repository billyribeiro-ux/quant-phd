# PROPOSALS-L05-r7: card changes for the round-7 fixes to L05

Round 7's verifier row `L05-L06-cards-coverage` found four numbered results in
L05 §7 without a card: Lemma 7.2, Lemma 7.3, Theorem 7.5 and Lemma 7.6. It
also named Remark 6.5 as optional. The notation fix (row `L05-notation`)
changes the one existing card that writes the harmonic number as \(C_j\).
Both changes are to `course/modules/S/S7/cards.json`, a central file, so they
are proposed here and not committed on the branch.

## 1. Edit to an existing card

### S7-c116

In its `"back"` value, as it appears in `cards.json`:

Old:

```json
"back": "Lehmann and Romano's \\(\\alpha_i = (\\lfloor \\gamma i \\rfloor + 1)\\alpha/(m + \\lfloor \\gamma i \\rfloor + 1 - i)\\), divided by \\(C_{\\lfloor \\gamma m \\rfloor + 1}\\) with \\(C_j = \\sum_{l \\le j} 1/l\\) (Theorem 7.7). Without the division they need a condition on the dependence, such as the Simes inequality for the true-null p-values.",
```

New:

```json
"back": "Lehmann and Romano's \\(\\alpha_i = (\\lfloor \\gamma i \\rfloor + 1)\\alpha/(m + \\lfloor \\gamma i \\rfloor + 1 - i)\\), divided by \\(c(\\lfloor \\gamma m \\rfloor + 1)\\) with \\(c(j) = \\sum_{l \\le j} 1/l\\), Lesson 3's constant (Theorem 7.7). Without the division they need a condition on the dependence, such as the Simes inequality for the true-null p-values.",
```

No other existing card uses \(C_j\) or Proposition 7.8's count letter. That
count is now \(D\); card S7-c117 never names it.

## 2. New cards

Append these, renumbering `S7-cNEW-n` to the next free ids (`S7-c169` to
`S7-c173`; `cards.json` currently ends at `S7-c168`). All are grade T. The
four cards on Lehmann and Romano's results cite them; Remark 6.5 is proved on
the page. Each back can be checked against the L05 text.

```json
[
 {
  "id": "S7-cNEW-1",
  "lesson": "L05",
  "front": "How is control of the false discovery exceedance related to the FDR?",
  "back": "For any procedure and \\(\\gamma \\in [0,1)\\), \\(\\FDR \\le \\gamma + (1-\\gamma)\\,\\Prob(\\FDP > \\gamma)\\), and for \\(\\gamma > 0\\), \\(\\Prob(\\FDP > \\gamma) \\le \\FDR/\\gamma\\) by Markov's inequality; at \\(\\gamma = 0\\) the exceedance is the FWER. FDR control at \\(q = 0.10\\) thus guarantees only \\(\\Prob(\\FDP > 0.2) \\le 0.5\\) (Lemma 7.2).",
  "grade": "T",
  "cite": [
   "lehmann2005generalizations"
  ]
 },
 {
  "id": "S7-cNEW-2",
  "lesson": "L05",
  "front": "State the counting bound for true-null p-values, and the single-step rule it justifies.",
  "back": "With \\(N(u) = \\#\\{i \\in I_0 : p_i \\le u\\}\\), Markov's inequality and validity give \\(\\Prob(N(u) \\ge k) \\le m_0 u/k\\) under any dependence. So rejecting every \\(H_i\\) with \\(p_i \\le k\\alpha/m\\) controls the k-FWER at \\(\\alpha\\); \\(k = 1\\) is Bonferroni (Lemma 7.3).",
  "grade": "T",
  "cite": [
   "lehmann2005generalizations"
  ]
 },
 {
  "id": "S7-cNEW-3",
  "lesson": "L05",
  "front": "With Lehmann and Romano's exceedance constants (3), where must an event \\(\\FDP > \\gamma\\) come from?",
  "back": "From some \\(l \\le \\min(\\lfloor \\gamma m \\rfloor + 1, m_0)\\) with \\(q_{(l)} \\le l\\alpha/m_0\\), the \\(q_{(l)}\\) being the ordered true-null p-values. At the first rejection \\(j\\) where the false share exceeds \\(\\gamma\\), the rejected hypothesis is the \\(l\\)-th true null with \\(l = \\lfloor \\gamma j \\rfloor + 1\\), and \\(m_0 \\le m - (j - l)\\). This holds under any dependence (Theorem 7.5).",
  "grade": "T",
  "cite": [
   "lehmann2005generalizations"
  ]
 },
 {
  "id": "S7-cNEW-4",
  "lesson": "L05",
  "front": "State the union bound for ordered p-values that generalizes Hommel's.",
  "back": "For valid p-values \\(p_1, \\dots, p_t\\), \\(M \\le t\\) and \\(0 = \\beta_0 \\le \\beta_1 \\le \\dots \\le \\beta_M \\le 1\\), under any dependence \\(\\Prob\\big(\\bigcup_{l \\le M} \\{p_{(l)} \\le \\beta_l\\}\\big) \\le t \\sum_{l=1}^{M} (\\beta_l - \\beta_{l-1})/l\\). With \\(\\beta_l = l\\alpha/t\\) and \\(M = t\\) it is Hommel's bound \\(\\alpha\\, c(t)\\) (Lemma 7.6).",
  "grade": "T",
  "cite": [
   "lehmann2005generalizations"
  ]
 },
 {
  "id": "S7-cNEW-5",
  "lesson": "L05",
  "front": "How does the limiting sup-t critical value compare with Bonferroni's?",
  "back": "If the \\(\\tau_k\\) have standard normal limits, Boole's inequality gives \\(h \\le \\Phi^{-1}(1 - \\alpha/(2K))\\), so in the limit the sup-t band is never wider than Bonferroni's. Under independence \\(h = \\Phi^{-1}\\big((1 + (1-\\alpha)^{1/K})/2\\big)\\), which is 3.016 against 3.023 at \\(K = 20\\) and \\(\\alpha = 0.05\\); beyond that small gain, the gain comes from dependence (Remark 6.5).",
  "grade": "T"
 }
]
```

## 3. Check

For the check below, all five cards went into `cards.json` temporarily as
`S7-c169` to `S7-c173`, with the S7-c116 edit applied. `check_pages.py --unit S7`
passed. The file was then restored with `git checkout`.
