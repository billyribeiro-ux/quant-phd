# E3 open items (Builder F: cards)

Scope: `course/modules/E/E3/cards.json`, re-synced against L01 to L08 as they stand on 2026-10-28. Items are for the
orchestrator and the lesson owners. Nothing here is learner text.

## 1. Lesson text defects found while checking cards (owners to fix; cards follow the proposition, not the defect)

1. `L02.html`, Assumption A4 (strict concavity) reads `u(y) < 0`. Proposition 1.3(b) and its text need `u''(y) < 0`
   (the assumption's own sentence names strict concavity). E3-c023 states the `u''` condition.
2. `L03.html` line 82 (Definition 1.3 note) cites "Proposition 2.5", which does not exist in L03. The invariance it
   describes is Proposition 2.7 (E3-c039 cites 2.7).
3. `L03.html` line 82 cites "Proposition 1.6" for the Arrow–Pratt measures, and line 99 (Example 1.5) says the concavity
   of u_2 is shown by "Proposition 1.6". L03 has no Proposition 1.6; the measures are Proposition 1.7 and Definition 1.6.
   (Line 75 and the Proposition 2.6 proof cite Lesson M1, Proposition 1.6(b); those are external and correct.)
4. Symbol clash between lessons: L05 writes `a := 1 - 1/psi` (Definition 1.1), L08 Definition 3.1 writes `rho = 1 - 1/psi`.
   The plan's notation note asks for one symbol across the unit. Cards quote the formula, not the symbol.

## 2. Card decisions

- Ids E3-c001 to E3-c158 kept, in order. E3-c159 added (L06, grade D, cite `kahneman1979prospect`, the lesson's own D claim).
- Changed text: E3-c011 (states A1), E3-c040 (names A2), E3-c048 and E3-c146 (state positive outcomes), E3-c050 (wording),
  E3-c094 (window stated as 0.999 c1 to 1.001 c1), E3-c097 (year removed: the lesson does not print it), E3-c128 (the lesson
  says "ten" utilities and "power functions and step functions"; the five-and-five split is in the code only),
  E3-c135 (Problem R2 result, grade T on its solution), E3-c146.
- Removed: none.
- Project page: no cards. The plan (section 3 and section 13) asks for cards from L01 to L08 only.

## 3. Requests

- DATA_REQUESTS: none (no real data; all labs are exact or SIMULATED as stated in the lessons).
- REFERENCE_REQUESTS: none new. The five curriculum keys are cited only at work level (D or C with title-only locators).
- GLOSSARY_REQUESTS: none raised by cards.
- CONTRACT_CHANGE_REQUESTS: none.
