# Known issues

Deferred rows, listed with their ledger ids so that nothing is hidden (FINAL-ARCHITECT-RULINGS, ruling 26 and ruling 29).

## E3, slice e (verifier round 14: `/Users/billyribeiro/.fanout/frags/D-E3-e.round14.json`)

LOW, forward-premise orderings (architect ruling 29). Each is a use of a result or object before the page states it. No arithmetic or proof step is affected.

| Ledger id | Location | Premise used before it appears | Status |
|---|---|---|---|
| E3e-r14-L03-forward-premise | `course/modules/E/E3/L03.html` (Definition 1.3 near line 90; Example 1.5 near line 107) | Definition 1.3 cites Proposition 2.7 (stated near line 173); Example 1.5 cites Proposition 1.7 (stated near line 116) | open, LOW |
| E3e-r14-L07-forward-premise | `course/modules/E/E3/L07.html` (Remark 1.6, near line 101) | Remark 1.6 uses lotteries A and B, which Example 2.1 defines near lines 109 to 110 | open, LOW |
| E3e-r14-L08-forward-gamble | `course/modules/E/E3/L08.html` (near lines 85, 90, 113, 132, 138) | The Section 4 gamble (wealth 110000 or 95000 cents, from 100000) is used in Example 1.4, the Section 2 opening, Remark 2.3, Example 2.5 and Section 3; it is defined near line 432 | open, LOW |

Deferred to the notation slice (ruling 29 renames; not done in slice e):

| Ledger id | Location | Conflict | Status |
|---|---|---|---|
| E3e-r14-notation-v | `L01.html` (near line 148), `L02.html` (near line 149), `L03.html` (near line 134) vs `L06.html` (near lines 61 to 62) and L07, L08 | `v` is an affine transform of a Bernoulli utility in L01 to L03 and the prospect value function from L06 on | deferred to notation slice |
| E3e-r14-notation-eps | `L05.html` (near line 107) vs `L02.html` (near lines 164 to 209) | `\varepsilon` is the EIS in L05 and the scale of the wealth lottery in L02 | deferred to notation slice |

Additional symbol collisions found by the whole-page scan of slice e, not in the round-14 ledger. Recorded here for the notation slice; not renamed in slice e:

- `\eta`: the L03 affine constant (Proposition 2.7) and the L07 weighting exponent (Example 1.4, `\omega_\eta`, lab `ETA`).
- `W`: the L02 wealth lottery (Example 1.5, lab) and the L06 prospect value (Definition 1.3 and Remark 2.4).
- `a`: the affine constant in L01 to L02 (Propositions 3.1, 3.3 and 2.2) and the Epstein–Zin exponent `a = 1 - 1/\psi` in L05 and L08.
- `\tau`: the L01 mixture weight (Definition 2.1; ruling 29 renames it) and the L08 alpha-MEU weight (Definition 1.2).

## Rubric calibration: blind scores within one level of the official scores (rulings 15, 23, 26)

A dedicated scorer read only the stripped exemplar text. Differences from the official scores, all one level, accepted by the architect:

| Unit | Exemplar | Criterion (blind vs official) |
|---|---|---|
| CS2 | B | C1, C2, C3 (3 vs 4 each; closing-sentence citation of hypotheses, unnamed identities, variance conversion not carried through) |
| FC2 | B | C2 (3 vs 4; net amounts given, the gap to zero never stated as such) |
| M5 | A | C2, C6 (1 vs 2 each) |
| M5 | B | C2, C4, C5 (3 vs 4 each) |
| E1 | A | C2 (1 vs 2), C5 (2 vs 1) |
| E3 | A, B | C1 depends on counting example lotteries rather than pairs (ruling 29 and the E3 rubric wording); the C1 levels do not partition a memo that has a count and a unit but no loss reason and no example |

## Notation and wording left as notes (LOW)

- M2: the difference quotient is the plain `Q(h)` in L04 to L06 and the cards; the registered `\mathbb{Q}` does not occur in M2 and is a different symbol.
- E4 project: grader gap checks at the boundary use an absolute tolerance of 1e-8 where the page states 1e-14; no mutant depends on it (ruling 25, verifier round 21 notes N4 and N10).
- BK4: mutant r15c (a float floor equal to the integer quotient for every list that fits in memory) stays in `ledgers/BK4/equivalent/`; the page says no float appears.
- Rubric exemplar B of BK4: its recommendation uses a defaulter margin of 111074 cents against the 50000 of its waterfall paragraph; the memo says so itself and the descriptors do not address consistency.

## Registry and data gaps (unchanged, still open)

- SEC reuse statement unread; the AC filers are SIMULATED.
- Beneish constants rest on one secondary page.
- Dechow (1995) author count: registry 2, curriculum 3.
- Pending registry correction for `kao2025estimated`.
- AP1 has five unverifiable paper rows.
- The `grader/reference.py` files are tracked in the repository; excluding them from deployment is a deploy-time item for the owner (ruling 4).
- Friedman (1963): the registry lists Friedman only; the curriculum source string says Friedman and Schwartz. Bernanke (1983) and Kindleberger and Aliber are not in the registry (LX1).
