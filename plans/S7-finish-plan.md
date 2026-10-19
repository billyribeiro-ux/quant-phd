# S7 finish plan: Haiku execution to release (2026-10-19)

Supersedes the remaining work of [S7-closure-plan.md](S7-closure-plan.md) (WP4, WP5) and adds WP7. Owner:
orchestrator (Claude Code session). Executors: Claude Haiku 5.5 agents at effort `max`, at most two running at
once. Every figure below is from a commit, a ledger or a tool run in this session.

## 1. Where S7 stands

| Item | State | Evidence |
|---|---|---|
| Benchmark gaps G1–G15 | All closed or assigned to their owners with a cross-link | `benchmarks/S7.md` "Status after the gap work"; WP3 merge 3dd9a69 |
| Content and tooling fixes | Every non-PASS row of rounds 9 and 10 has a committed fix | `integrate-r7` at 7305b1d (pushed) |
| Grader | 160 checks; reference passes seeds 0–49 (slowest 8.1 s); 126 mutants in `ledgers/S7/mutants/` | `run_graders` log 2026-10-19; `mutate_graders` run in progress |
| Cards | 185 (one per misconception after c181–c185) | `course/modules/S/S7/cards.json` |
| Gates on 202ea24 | ruff, format, mypy, pytest (317), render, build_site, verify_refs offline, fetch_data, check_pages/dag/projects, run_labs 41/41 | gate log of 202ea24 |
| Ledger row ids | 1,430 rows across the latest six slice ledgers, no duplicate id | merge dry run over `ledgers/S7/history/` |

Latest verdict per slice and what it still needs:

| Slice | Latest round | Result | Next round | Pinned checkout |
|---|---|---|---|---|
| L01-L02 | 9 | 256/257 | 10 | verify12 (202ea24) |
| L03-L04 | 9 | 278/278, but L04 and its cards changed since | 10 | verify12 (202ea24) |
| L05-L06 | 10 | 299/301 | 11 | verify12 (202ea24) |
| L07-L08 | 10 | 242/243 | 11 | verify12 (202ea24) |
| project | 10 | 288/309 (17 surviving mutants, one slow test) | 11 | verify13 (integrate head once the 126-mutant run passes) |
| data-tooling | 9 | 41/42 | 10, after WP7 lands | verify14 (integrate head after WP7) |

## 2. Definition of done

S7 ships when all of these hold, with the evidence named:

1. **Every slice ledger is all PASS.** That means zero FAIL and zero UNVERIFIABLE. Each slice was verified at a pin, and for each one `git diff <pin> <release> -- <slice files>` is empty. The orchestrator records that diff check in the release commit message.
2. **The release ledger is written and current.**
   - `tools/ledger.py --unit S7` writes `ledgers/S7.verification.json` with verdict PASS.
   - `tools/ledger.py --unit S7 --check` exits 0.
3. **Every CLAUDE.md gate passes on the release commit.** That includes run_graders 50/50, mutate_graders killing every mutant, page_smoke on every page, and a live `verify_refs.py` with 0 problems.
4. **WP7 is merged and verified (data-tooling slice).** The weekly live-data job then has an issuer-sanctioned source.
5. **Independence holds.** No agent verifies a slice it built or verified before. A builder never edits a ledger. The orchestrator never writes a ledger row.

## 3. Agents and controls

- **Model and effort:** Haiku 5.5 at effort `max`, as the owner asked.
- **Concurrency:** at most two agents at once, as the owner ordered. The host has 4 cores, and Pyodide labs must finish in 10 s. At load 8.5 a lab reached 10.5 s, so more agents would fail page_smoke on timing alone.
- **Two agents already running:** the Sonnet verifiers of L01-L02 and L03-L04 round 10 were 12 and 7 minutes in. They are stopped and re-run as Haiku verifiers with fresh briefs.
- **The Haiku risk and its controls.** A smaller verifier is likelier to pass an error it did not re-derive. Four controls apply:
  1. **Targeted rounds.** The remaining rounds are diff-scoped, and each brief names the exact FAIL rows and changed hunks.
  2. **A procedural preamble.** Every brief starts with `haiku_preamble.md` (scratchpad). It sets the order of work and the evidence standard: what was run and what was observed, never "looks right". A check the agent cannot complete is UNVERIFIABLE, and UNVERIFIABLE is a FAIL.
  3. **Orchestrator audit.** Before a ledger is accepted, the orchestrator:
     - runs `validate()` on it;
     - confirms that every re-checked row carries concrete evidence;
     - replicates at least three of its PASS claims (one number, one derivation, one command).

     A ledger that fails audit is discarded, and a fresh Haiku verifier redoes the slice.
  4. **Model-independent gates.** The tests, the mutants, page_smoke and the 50-seed grader run decide what they cover, whatever the verifier.
- **Rules carried over:**
  - no email or personal data in any request;
  - no pkill or killall;
  - commits end with the session's attribution lines;
  - generated files are produced only by their tools;
  - citations are registry keys only.

## 4. Work packages

### WP4b: verification to zero failures (Haiku verifiers)

| Wave | Slot 1 | Slot 2 |
|---|---|---|
| 1 | L01-L02 round 10 (verify12) | WP7 builder (own worktree) |
| 2 | L03-L04 round 10 (verify12) | L05-L06 round 11 (verify12) |
| 3 | L07-L08 round 11 (verify12) | project round 11 (verify13) |
| 4 | data-tooling round 10 (verify14, after WP7 merges) | first re-round, if any slice failed |
| 5+ | re-rounds until every slice is all PASS | |

WP7 goes into wave 1 because data-tooling waits for it, which puts it on the critical path.

The fix loop runs while the waves go on, with no agent:
- the orchestrator fixes each FAIL on `integrate-r7`, with `embed_labs --refresh` where a lab twin changed;
- then fast gates and pytest;
- then a new pin for the slice's next round.

### WP7: replace the Federal Reserve Data Download Program source (Haiku builder)

The round-9 data-tooling verifier reports that the program retires from the week of 2026-11-09. `tools/data_sources.yaml` already notes the retirement. The committed snapshots keep the labs safe; the weekly `fetch_data.py --fetch` job breaks.

The builder:
1. Establishes the retirement notice and the issuer's replacement path for H.10 and H.15 from the Federal Reserve's own pages, quoting them.
2. Prefers a Board-issued source. FRED is acceptable only if its terms permit redistribution of these series, quoted as BLUEPRINT §5.3 requires.
3. Changes `tools/fetch_data.py`, `tools/data_sources.yaml` and the offline tests to use that source. `MANIFEST.json` is regenerated by the tool, never by hand.
4. Proves the three CSV snapshots are byte-identical when rebuilt from the new source. If any cell differs, it stops and reports: lab numbers depend on those snapshots.
5. Runs every gate, commits in its worktree, and does not merge.

The orchestrator merges WP7 into `integrate-r7` after review and a gate run. The data-tooling round 10 then verifies the migration together with round 9's fixes.

### WP5: release (orchestrator)

1. Merge `integrate-r7` into `claude/phase0-foundations-s7-pilot` after the full gate run, including page_smoke on every page. The run happens with no verifier running, so lab timings are clean.
2. Move the final slice ledgers into `ledgers/S7/`, then run `tools/ledger.py --unit S7` and `--check`, and commit `ledgers/S7.verification.json`.
3. Run the live `tools/verify_refs.py` and get 0 problems. If an Open Library redirect fails transiently again, re-run it and record both runs.
4. Push. Then remove the merged worktrees (verify9–14, integrate, the WP7 worktree) and delete the local `integrate-r7`. Report the remote branches the owner may delete.

## 5. Out of scope

WP6, the AP1 and AC2 pilots, is the next milestone (BLUEPRINT §9). It gets its own plan once S7 ships. Building two units to S7's standard is a build → verify → fix programme of its own, not a finishing task.
