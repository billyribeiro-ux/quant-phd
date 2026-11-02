# E3 project: mutants ruled not to violate the specification

This mutant survives the project grader on seeds 0-9 (the mutant is the reference with one change: the logit log term is
computed as log(1 + exp(t)) without the stable form). It differs from the reference only for |t| above about 709, where
math.exp overflows. project.html states no numerical-stability requirement and no range for z (grep for overflow, large,
extreme and finite finds no statement about it), so the difference is outside the stated specification (architect ruling 9).
It is kept here, outside `mutants/`, so `tools/mutate_graders.py` measures only student-error mutants the specification forbids.
