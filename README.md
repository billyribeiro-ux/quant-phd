# quant-finance

A doctoral-track major in **finance, economics and quantitative markets**. It
takes a student from high-school algebra to the level of a top PhD program's
coursework and a defended thesis. Along the way it includes a complete Finance
degree (bachelor's level) and a Master's in Finance / Financial Engineering.

The program ships as a self-contained static HTML site with runnable labs,
autograded projects and a program-long engineering build ("Atlas").

> **Status: Phase 0 (foundations) in progress.** Built so far:
> - the curriculum and its validator
> - the verified citation registry (403 works)
> - pinned, integrity-checked runtimes
> - the design system
> - the program map
> - a reference lesson whose Python lab runs in the browser
> - a browser smoke test
>
> Next come the lesson, project and studio templates, the grader harness, and
> spaced retrieval. See [BLUEPRINT.md §9](BLUEPRINT.md#9-build-process).

## What makes it different

- **Every claim carries an evidence grade** (T / A / B / C / D / X) and a
  citation key from a registry. Citations enter the registry only through a
  Crossref DOI lookup, are checked against the source string, and are
  re-verified weekly in CI.
- **Projects first.** There are 157 graded projects: one per module and one
  studio per part. They follow a four-rung ladder (worked example → completion
  → independent → stretch), as the learning-science evidence recommends.
- **Measured, not promised.** Every hour figure, credential size and
  career-track length is computed from the curriculum graph by
  `tools/render_curriculum.py`.

| Credential (content-equivalent) | Modules | Graded projects | Hours | Full-time years |
|---|---|---|---|---|
| Finance Degree, bachelor's level | 42 | 47 | 3,881 | 1.80 |
| Master's in Finance / Financial Engineering | 76 | 84 | 7,546 | 3.49 |
| PhD in Finance | 83 | 87 | 9,171 | 4.25 |

These are content-equivalent credentials, not accredited degrees.

## Repository map

| Path | What it is |
|---|---|
| [`BLUEPRINT.md`](BLUEPRINT.md) | Master architecture: mission, evidence standard, learning system, projects, build plan |
| [`CURRICULUM.md`](CURRICULUM.md) | The full curriculum, generated from `curriculum/*.yaml` |
| [`BUILDER_RULES.md`](BUILDER_RULES.md) / [`VERIFIER_RULES.md`](VERIFIER_RULES.md) | Binding system prompts for the agents that build and verify each module |
| `curriculum/` | Source of truth: tiers, credentials, tracks, Atlas, 134 modules |
| `references/` | Verified citation registry, review queue, seeding report |
| `tools/` | Validators, the registry pipeline, and (later) build and verification tools |
| `tests/` | Tooling tests; each regression test names the real failure it prevents |

## Working on it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt

# Gates (CI runs the same)
.venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/mypy && .venv/bin/pytest
.venv/bin/python tools/render_curriculum.py      # validate the DAG and regenerate CURRICULUM.md
.venv/bin/python tools/verify_refs.py --offline  # registry integrity
.venv/bin/python tools/verify_refs.py            # live re-verification against Crossref

# Site: fetch runtimes once, publish data, preview, and smoke-test in Chromium
.venv/bin/python tools/vendor.py install          # pinned + sha512-verified, from the npm registry
.venv/bin/python tools/build_site.py
python3 -m http.server -d course 8000            # open http://localhost:8000
.venv/bin/python tools/page_smoke.py             # needs: python -m playwright install chromium

# Registry pipeline
.venv/bin/python tools/seed_references.py        # resolve every curriculum source against Crossref
.venv/bin/python tools/add_reference.py --doi <DOI> --source "<citation>" --used-by <UNIT>
```
