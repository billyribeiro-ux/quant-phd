# quant-finance

A doctoral-track major in **finance, economics and quantitative markets**. It
takes a student from high-school algebra to the level of a top PhD program's
coursework and a defended thesis. Along the way it includes a complete Finance
degree (bachelor's level) and a Master's in Finance / Financial Engineering.

The program ships as a self-contained static HTML site with runnable labs,
autograded projects and a program-long engineering build ("Atlas").

> **Status: Phase 0 complete; Phase 1 pilot under way.** Built so far:
> - the curriculum, with its concept graph and validator
> - the verified citation registry
> - the design system, the static site and its program map
> - the vendored, hash-locked runtimes
> - the build and verification tools
>
> The first pilot module, **S7 Research Integrity & Multiple Testing**, is
> built end to end. Its 8 lessons, autograded Atlas A8 project and review
> cards are in `course/modules/S/S7/`. It is released once its independent
> verification ledger passes. See [BLUEPRINT.md §9](BLUEPRINT.md#9-build-process).

## What makes it different

- **Every claim carries an evidence grade** (T / A / B / C / D / X) and a
  citation key from a registry. Citations enter the registry only through a
  machine lookup of an authoritative record (Crossref by DOI, Open Library by
  ISBN, or the publisher's or issuer's own page), are checked against the
  source string, and are re-verified weekly in CI.
- **Every concept is taught once.** The curriculum assigns each of its 1,121
  concepts to exactly one module. The validator rejects a concept defined twice
  or used before its prerequisites, and `check_dag.py` holds every page to that.
- **Projects first.** There are 157 graded projects: one per module and one
  studio for each of the 23 parts that have one. They follow a four-rung ladder
  (worked example → completion → independent → stretch), as the
  learning-science evidence recommends.
- **Runs in the browser, verified outside it.** Every lab runs in Pyodide on
  the page and as a byte-identical twin under `pytest`. Every autograder passes
  its reference on 50 seeds, rejects the verifier's deliberately wrong
  solutions, and runs identically in the browser and locally.
- **Measured, not promised.** Every hour figure, credential size and
  career-track length is computed from the curriculum graph by
  `tools/render_curriculum.py`.

| Credential (content-equivalent) | Modules | Graded projects | Hours | Full-time years |
|---|---|---|---|---|
| Finance Degree, bachelor's level | 42 | 47 | 3,881 | 1.80 |
| Master's in Finance / Financial Engineering | 77 | 85 | 7,646 | 3.54 |
| PhD in Finance | 83 | 87 | 9,171 | 4.25 |

These are content-equivalent credentials, not accredited degrees.

## Repository map

| Path | What it is |
|---|---|
| [`BLUEPRINT.md`](BLUEPRINT.md) | Master architecture: mission, evidence standard, learning system, projects, build plan |
| [`CURRICULUM.md`](CURRICULUM.md) | The full curriculum, generated from `curriculum/*.yaml` |
| [`BUILDER_RULES.md`](BUILDER_RULES.md) / [`VERIFIER_RULES.md`](VERIFIER_RULES.md) | Binding system prompts for the agents that build and verify each module |
| `curriculum/` | Source of truth: tiers, credentials, tracks, Atlas, 134 modules, 1,121 concepts |
| `references/` | Verified citation registry, review queue, seeding report, authoritative domains |
| `notation/` | The binding notation registry (KaTeX macros and program-wide symbols) |
| `atlas/` | Frozen interface contracts for the program-long Atlas build (A8 so far) |
| `course/` | The static site: program map, concept index, review deck, released modules (S7) |
| `tools/` | Curriculum validator, registry pipeline, site builder, vendor fetcher, page/DAG/project checks, lab and grader runners, mutation tests, Chromium smoke tests |
| `tests/` | Tooling tests (each regression test names the real failure it prevents), every lab's twin, browser-module tests |

## Working on it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt

# Gates (CI runs the same)
.venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/mypy && .venv/bin/pytest
.venv/bin/python tools/render_curriculum.py      # validate the DAG and regenerate CURRICULUM.md
.venv/bin/python tools/verify_refs.py --offline  # registry integrity
.venv/bin/python tools/verify_refs.py            # live re-verification against Crossref

.venv/bin/python tools/build_site.py --check     # program map and site data are current

# Registry pipeline
.venv/bin/python tools/seed_references.py        # resolve every curriculum source against Crossref
.venv/bin/python tools/add_reference.py --doi <DOI> --source "<citation>" --used-by <UNIT>
.venv/bin/python tools/add_reference.py --list-editions --source "<book citation>"   # then --isbn
.venv/bin/python tools/add_reference.py --url <issuer or publisher page> --source "<citation>" --used-by <UNIT>

# Course site
.venv/bin/python tools/fetch_vendor.py           # download the SHA-256-locked runtime (KaTeX, D3, Pyodide, fonts)
python3 -m http.server -d course 8000             # then open http://localhost:8000
.venv/bin/python tools/check_pages.py --unit S7 && .venv/bin/python tools/check_dag.py --unit S7
.venv/bin/python tools/check_projects.py --unit S7 && .venv/bin/python tools/run_labs.py --unit S7
.venv/bin/python tools/run_graders.py --unit S7 --seeds 0-49 && .venv/bin/python tools/mutate_graders.py --unit S7
.venv/bin/python tools/page_smoke.py --unit S7   # Chromium: both themes, 360 px, labs and grader in Pyodide
```
