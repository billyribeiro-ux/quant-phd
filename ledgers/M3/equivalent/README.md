# M3 project: mutants ruled not to violate the specification

These three mutants survive the project grader on seeds 0-49. Independent verifiers (rounds 6, 11, 15) ruled each a
non-violation: project.html states no stop criterion for the projection loop (line 660) and fixes only the returned
matrix's properties, which these variants still satisfy within the stated tolerances. They are kept here, outside
`mutants/`, so `tools/mutate_graders.py` measures only student-error mutants the specification forbids.
