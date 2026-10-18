# PROPOSALS-L07-r7: central card fix from the round-7 verifier (row card-S7-c158)

One card in `course/modules/S/S7/cards.json` changes. Only its `back` string
changes; its id, front, grade (T) and lesson stay as they are. The old string is
copied verbatim from `cards.json` (line 1208 on integrate-r7 at 226a90d).

The new back follows the verifier's fix. "Undersized" is Proposition 5.4. The
loss of power is shown only at strong correlation, by Problem E4 at ρ = 0.95.
The ρ = 0.9 evidence is a size result under a true null, and the new wording
says so.

### S7-c158
Old:
```json
"back": "The test uses \\(V_1 + V_2\\) instead of \\(\\theta\\). Under positive correlation it is undersized and nearly powerless (no rejections in 4000 samples at \\(\\rho = 0.9\\) in the L07 Lab 4 simulation); under negative correlation it rejects a true null too often."
```
New:
```json
"back": "It uses \\(V_1 + V_2\\) instead of \\(\\theta\\). Under positive correlation it is undersized (no rejections of a true null in 4000 samples at \\(\\rho = 0.9\\), L07 Lab 4), and at strong correlation it loses its power (L07 Problem E4: about 0 against 0.61 for the paired test at \\(\\rho = 0.95\\)); under negative correlation it rejects a true null too often."
```
