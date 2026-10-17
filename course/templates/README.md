# Page templates

Skeletons for builder agents (BUILDER_RULES §4). Copy a template into the unit's
output directory and replace every `{{SLOT}}`. The tools never read this folder:
a template is correct when the page built from it passes `check_pages.py`,
`check_dag.py`, `check_projects.py`, `run_labs.py`, `run_graders.py` and
`page_smoke.py`. Module S7 (`course/modules/S/S7/`) is the reference instance of
every template here and is the first thing to read before building a unit.

| Template | Becomes | Contract |
|---|---|---|
| `hub.html` | `modules/<PART>/<ID>/index.html` | objectives, prerequisites, placement diagnostic, lesson map, ladder, hours split |
| `lesson.html` | `modules/<PART>/<ID>/Lnn.html` | BUILDER_RULES §4.2 section order and minimum counts |
| `project.html` | `modules/<PART>/<ID>/project.html` | four-rung ladder, specification, time budget, grader or rubric, reading list |
| `studio.html` | `studios/<STUDIO-ID>/index.html` | rung 3 at Part scale: deliverable, reuse map, rubric and exemplars |

Paths: a module page sits three levels below `course/`, so its `data-root` is
`../../../`; a studio page sits two levels down and uses `../../`.
