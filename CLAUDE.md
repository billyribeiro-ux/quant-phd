# CLAUDE.md — agent instructions for this repo

## Read first

| Doc | When |
|---|---|
| [BLUEPRINT.md](BLUEPRINT.md) | Always. It defines the architecture, the evidence standard and the build process |
| [BUILDER_RULES.md](BUILDER_RULES.md) | Before building any module, studio, lesson or project. It is a binding contract |
| [VERIFIER_RULES.md](VERIFIER_RULES.md) | Before verifying any unit. A verifier is never the agent that built the unit |
| [references/SEED_REPORT.md](references/SEED_REPORT.md) | Before citing anything: what is verified, and what is still in review |

## Hard rules

1. **Never hand-edit generated files.** `CURRICULUM.md` and
   `curriculum/curriculum.json` come from `tools/render_curriculum.py`.
   `references/references.json`, `review_queue.json`, `corrections.json` and
   `SEED_REPORT.md` come from the registry tools. Edit the sources
   (`curriculum/*.yaml`, `references/extra_sources.yaml`,
   `references/doi_hints.yaml`) and regenerate.
2. **Cite only registry keys.** A source that is not in
   `references/references.json` cannot be cited. Admit it with
   `tools/add_reference.py`, which rejects a DOI that does not match its
   citation string. Never type bibliographic data from memory.
3. **A DOI hint is a hypothesis.** `references/doi_hints.yaml` only adds a
   candidate. The record must still pass the identity rules in
   `tools/refs/match.py`.
4. **Do not weaken the matcher to clear the review queue.** Each rule in
   `tools/refs/match.py` exists because it caught a real false positive, and
   `tests/test_refs.py` names each one. Change a rule only with a test that
   shows the new behaviour is right.
5. **Hours and credential sizes are computed.** Never type them into
   documentation without re-running `render_curriculum.py` and copying its
   output.

## Gates (all must pass before committing; CI runs the same)

```bash
.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/mypy                                   # strict
.venv/bin/pytest
.venv/bin/python tools/render_curriculum.py && git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json
.venv/bin/python tools/verify_refs.py --offline  # add the live run after changing references
```

## Conventions

- Python 3.12+, fully typed (mypy strict), formatted by ruff at line length 120.
  Pin every dependency in `requirements*.txt`.
- The Crossref client sends no personal data. Do not add an email address to
  its User-Agent or parameters.
- Tooling tests must be offline. Any network behaviour is exercised by the
  tools themselves and by the scheduled CI job.
