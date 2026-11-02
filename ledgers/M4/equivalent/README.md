# M4 project: mutants ruled not to violate the specification

`m17_student_t_second_seed.py` draws the Student-t family from `seed + 1` while the Gaussian family draws from `seed`. It
survives the project grader on seeds 0-49, so `tools/mutate_graders.py` reports it as SURVIVED. It is kept here, outside
`mutants/`, because it is a conforming implementation, not a student error the specification forbids.

Proof that it does not violate the specification:

1. The module contract (project.html, Rung 3 · Specification, Context) requires only that every run is reproducible from
   its seed. `m17` is deterministic in its seed: for each seed the Student-t losses are a fixed function of that seed.
2. Conventions item 5 leaves the order and the source of the Student-t family's draws open. The suite's properties hold
   for any generator that is seeded and yields the stated distributions, so a different stream for one family cannot
   fail a stated property.
3. Measured: `m17` passes all 138 checks of `grader/test_project.py` on every seed from 0 to 49 (run in this round).
4. The only page sentence that ties the two families to one seed is the Lab 1 code docstring ("from the same seed"),
   which describes the lab's own simulator. That simulator's output (for example the Lab 1 printed losses) is not
   a contract for `tail_risk.py`: the module's order of draws is not fixed, so a conforming module does not reproduce
   the lab's numbers. The docstring therefore does not bind the module.

Architect note: if the page should require a shared seed between the families, Conventions item 5 must freeze the
Student-t draw order. Alternative 4 draws its chi-square variable from the Gaussian stream and would then need replacing.
