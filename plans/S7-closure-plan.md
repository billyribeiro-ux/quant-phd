# S7 closure plan (2026-10-19)

Owner: orchestrator (Claude Code session). Executors: Claude Sonnet 5.5 agents, at most two
running at once, effort at most `xhigh`. Every claim below cites a commit, a ledger or a gate
log; nothing is estimated from memory.

## 1. Where S7 stands (evidence)

| Item | State | Evidence |
|---|---|---|
| Branch | `claude/phase0-foundations-s7-pilot` = `origin` at **8555a1b**; working tree clean | `git status -sb` |
| Gates on 8555a1b | **All pass**: ruff, format, mypy (strict), pytest, render, build_site, verify_refs (offline), fetch_data, check_pages, check_dag, check_projects, run_labs (41/41), run_graders (50/50 seeds), mutate_graders (87/87 killed), page_smoke (every page) | scratchpad `gates_int7.log`, `=== GATES PASS` |
| Benchmark gaps (benchmarks/S7.md) | **Closed:** G1 (Fed H.10/H.15 data, L05 Lab 6, L08 Lab 4), G2 and G5 (L05 §6–§7), G3 (rubric-graded memo), G4, G9 and G12 (L04), G6 (L03 §7), G7 (L01 §6), G8 (L07 MinTRL, §5). **Open:** G10, G11, G13, G14, G15 (low priority) | merge commits 8722a86, 12847fd, 7bcf0e8, 57ab53e; `grep` finds no CPCV in L08 and no Holm-optimality problem in L02 |
| Size | 8 lessons + hub + project; 41 lab twins and snippets; 176 cards; 82 registry keys used by S7 (548 in the registry); S7 = 100 h (lessons 70, project 30) | `curriculum/curriculum.json`, `cards.json`, `references/references.json` |
| Round 7 verification | 6 slices, 1,288 rows, **61 non-PASS** (60 FAIL, 1 UNVERIFIABLE). Every one has a committed fix on 8555a1b | `ledgers/S7/*.json`; fix commits 5eae7ce, fe07035, 226a90d, 92ea73f, 26ba464, d1a9d5e, 8555a1b |
| Release ledger | **Not produced.** `ledgers/S7.verification.json` needs every row PASS | `tools/ledger.py --unit S7 --check` |
| Other Phase-1 pilots | AP1 and AC2 (BLUEPRINT §9) **not started**: S7 is the only built unit | `coursekit.built_units()` |

Round-7 non-PASS rows by slice: L01-L02 7/231, L03-L04 10/270, L05-L06 8/277, L07-L08 11/226,
project 20/249, data-tooling 5/35.

## 2. Goal and definition of done

S7 ships when all of these hold on one commit of the branch, pushed:

1. Every ledger row of every slice is PASS: zero FAIL, zero UNVERIFIABLE (VERIFIER_RULES:
   fail closed).
2. `tools/ledger.py --unit S7` writes `ledgers/S7.verification.json` with verdict PASS, and
   `--check` exits 0.
3. Every CLAUDE.md gate passes on that commit (the list in §1), plus a live
   `verify_refs.py` run with 0 problems.
4. The open benchmark gaps G10, G11, G13, G14 and G15 are closed or explicitly assigned to their
   owning modules with a cross-link, and `benchmarks/S7.md` records the closure with evidence.
5. No verifier ever verified its own work. A builder never edits a ledger. The orchestrator never
   writes a ledger row.

CI on GitHub may fail for billing reasons; the local gates are the gate.

## 3. Rules every agent follows

- **Independence.** A verifier is a fresh agent that built nothing in S7. A fixer never verifies
  the rows it fixed. Round N+1 re-verifies with an agent that did not verify round N's slice.
- **One slice per verifier agent**, so no agent's context overflows; the orchestrator chains
  them, at most two at a time.
- **Frozen head while verifying.** The branch does not move during a verification wave except for
  ledger commits. Fixes and new content are built in the `integrate-r7` worktree
  (`.claude/worktrees/integrate`) and merged only after the wave and a full gate run.
- **Repo rules.** CLAUDE.md hard rules 1–5 hold: no hand-edited generated files, registry keys
  only (admitted with `add_reference.py`), the matcher is not weakened, hours are computed.
- **Network hygiene.** No email or personal data in any request. No `pkill`/`killall`: kill only
  PIDs you started.
- **Commits.** Small, frequent, each ending with the session's attribution lines; pushed with
  `git push -u origin <branch>`.

## 4. Work breakdown

### WP1: Round 8 verification (verifiers, Sonnet, `xhigh`)

Base for carry-forward: 9b6be31 (round 7's head). Head: 8555a1b.

| Wave | Agent 1 | Agent 2 | Why this order |
|---|---|---|---|
| A | project (20 round-7 failures; grader 142 checks, 87 + ≥3 new mutants, rubric form in Chromium) | L07-L08 (11; the preregistration rewrite, the grid's resampling null, sign rules) | heaviest first |
| B | L05-L06 (8; Lab 5 MTP2 proof, Lab 6 exact ties, notation) | L03-L04 (10; E4 derivation and snippet) | |
| C | L01-L02 (7; L01 §6 grades and Ville wording) | data-tooling (5; fetch_data check, `_invert`, issue ranges) | lightest last |

Each verifier reads its round-8 brief (scratchpad `round8_brief_<slice>.md`), which:
- lists the round-7 FAIL ids to re-check from scratch;
- requires `git diff 9b6be31 HEAD` on every file of the slice, a row for anything new a fix
  introduced, and recomputation rather than trust in the fix text;
- requires the slice's commands: run_labs, check_pages, check_dag, page_smoke on its pages, its
  pytest files, and for the project at least three new mutants (prefix `u`).

Output per slice: `ledgers/S7/<slice>.json`, committed by the orchestrator as it lands.

### WP2: Fix loop (fixers, Sonnet, `xhigh`, or the orchestrator for central items)

- The orchestrator triages each ledger the moment it lands: central items (registry, cards,
  curriculum, hub hours, tooling) it fixes itself; page content goes to a fixer agent with only
  the failing rows (BLUEPRINT §9, "a failure goes back to the builder with only the failing
  ledger rows").
- Fixes land in `integrate-r7`, each with `embed_labs --refresh` where a twin changed, then the
  full gate run (`gatesR2.sh`) before merging to the branch.

### WP3: Residual benchmark gaps (one builder, Sonnet, `xhigh`)

Runs in the `integrate-r7` worktree once a slot is free, verified in round 9.

| Gap | Deliverable | Where |
|---|---|---|
| G10 non-statistical false backtests | A remark naming survivorship, data errors and trading costs as false-discovery sources multiple testing cannot fix, with links forward to F1, QR1 and QR2 (the owners) | L01 canon breaks or L08 §7 |
| G11 CPCV | Name combinatorial purged cross-validation where L08 discusses CSCV's limits, with a pointer to QR2, which owns it; cite only registry keys | L08 |
| G13 knockoffs, post-selection inference | A forward pointer to F5 (owner) in L05's estimation-after-selection discussion | L05 §6 |
| G14 Holm is unimprovable | A proof problem with a full worked solution: raising any one Holm critical value admits a dependence structure with FWER > α | L02 problem set |
| G15 replicability and publication-bias models | A forward pointer to F5 beside L06's replication debate | L06 |
| Report | A "Status after the gap work" section in `benchmarks/S7.md`, mapping each gap to its commit and section; the reviewer's original text left intact | benchmarks/S7.md |
| Curriculum | S7's `core` line names the new topics (local FDR, Diebold–Mariano, simultaneous bands, k-FWER/FDX, anytime-valid inference, MinTRL) | `curriculum/01-foundations.yaml`, then render and build_site |

Concepts stay in their owning modules (BUILDER_RULES §1.10): pointers only, no definitions of
F1/F5/QR1/QR2 concepts in S7.

### WP4: Round 9 and later (verifiers, Sonnet, `xhigh`)

Targeted: every round-8 non-PASS row, every hunk changed since round 8's head, and the WP3
additions (new rows). Repeat WP2 → WP4 until a round ends with zero non-PASS rows.

### WP5: Release (orchestrator)

1. `tools/ledger.py --unit S7`, then `--check`; commit `ledgers/S7.verification.json`.
2. Live `tools/verify_refs.py` (network): 0 problems.
3. Full gate run on the release commit; push.
4. Archive the final round's ledgers under `ledgers/S7/history/`.
5. Clean up merged worktrees and the temporary `integrate-r7` branch (local); report the remote
   branch for the owner to delete if wanted.

### WP6 (next milestone, separate plan): AP1 and AC2 pilots

Out of scope here. Entry criterion: WP5 done. Each pilot follows the same build → verify →
fix loop under BUILDER_RULES and VERIFIER_RULES.

## 5. Schedule (critical path)

`WP1 wave A → B → C` (each wave ≈ 1–1.5 h) → `WP2` (in parallel with waves B–C as ledgers land)
→ `WP3` (starts when a slot frees after wave C) → `WP4 round 9` → `WP5`.

## 6. Risks and controls

| Risk | Control |
|---|---|
| Session usage limit stops agents mid-run | Agents resume with SendMessage after the reset; ledgers are written only at the end, partial work is saved in scratch folders |
| A broad `pkill` kills another agent's page_smoke | Rule in every brief; the orchestrator re-runs any gate a SIGTERM interrupted |
| Head drifts during a wave | Branch frozen during waves; fixes wait in `integrate-r7` |
| A fix passes its row but breaks a neighbour | Verifiers read every changed hunk; the full gate run precedes every merge |
| Context overflow in a Sonnet agent | One slice per agent; briefs point to files, not pasted content |
| Unverifiable claims (dates, timing, closed sources) | Rewrite as claims a reader can check, or grade and attribute them precisely |
