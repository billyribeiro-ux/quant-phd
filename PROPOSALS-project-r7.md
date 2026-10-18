# PROPOSALS-project-r7: central edits after the round-7 fixes to the memo

The branch fixes the eight project rows of round 7 in `project.html`,
`rubric.js`, `store.js`, `L08.html` and the tests (see the commit message).
Two things need central action.

## 1. Card S7-c167 in `course/modules/S/S7/cards.json`

Its back repeats the PBO reading the verifier failed. Exact replacement (the
old string occurs once):

| Old | New |
|---|---|
| `and PBO 0.733 with 16 blocks: what an uninformative selection produces. It is not a 73% chance of losing money.` | `and PBO 0.733 with 16 blocks: consistent with a selection that carries no information, whose expected PBO is one half. It is not a 73% chance of losing money.` |

No other card quotes the rubric, the exemplars or the old phrasing.

## 2. A shared line in `project.html` (merge note)

The rubric now has **seven** criteria. C7, brief compliance, holds the
brief's form requirements, so the bar stays "level 3 or above on every
criterion". The grading-mode entry of the specification says so in the
sentence "Both modes apply …: … against the seven criteria of the memo rubric
…". That sentence sits on the same physical line (the `<dd>` after
`<dt>Grading mode</dt>`) as the check-count sentence, which the coordinator is
editing centrally. On this branch only the words "six criteria" changed to
"seven criteria" on that line; the check-count sentence and the grader panel
are untouched. When the two edits meet, keep the coordinator's check-count
sentence and this branch's "seven criteria".
