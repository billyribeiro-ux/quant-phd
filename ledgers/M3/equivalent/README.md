# M3 project: mutants ruled not to violate the specification

These three mutants survive the project grader on seeds 0-49. Independent verifiers (rounds 6, 11, 15) ruled each a
non-violation: project.html states no stop criterion for the projection loop (line 660) and fixes only the returned
matrix's properties, which these variants still satisfy within the stated tolerances. They are kept here, outside
`mutants/`, so `tools/mutate_graders.py` measures only student-error mutants the specification forbids.

- `r6d_m04_projection_stops_on_gap_only.py`: `projection_repair` stops when the gap alone is at most `tol`, ignoring the step.
- `r11d_m02_projection_stops_on_step_only.py`: `projection_repair` stops when the step alone is at most `tol`, ignoring the gap.
- `r15d_m03_projection_repair_never_stops_early.py`: `projection_repair` never stops early; its stop test ends in `and False`,
  so every call runs the full `max_iter` budget. Its only change from `grader/reference.py` is that stop test and the
  first docstring line.
