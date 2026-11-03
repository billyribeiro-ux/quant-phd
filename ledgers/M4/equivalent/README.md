# M4 project: mutants ruled not to violate the specification

`m17_student_t_second_seed.py` draws the Student-t family from `seed + 1` while the Gaussian family draws from `seed`. It
survives the project grader on seeds 0-49, so `tools/mutate_graders.py` reports it as SURVIVED. It is kept here, outside
`mutants/`, because it is a conforming implementation, not a student error the specification forbids.

Proof that it does not violate the specification:

1. The module contract (project.html, Rung 3 · Specification, Context) requires only that every run is reproducible from
   its seed. `m17` is deterministic in its seed: for each seed the Student-t losses are a fixed function of that seed.
2. Conventions item 5 (project.html, Conventions) states that the source of the Student-t family's normals and the order
   of its draws are not fixed. It fixes only the Gaussian stream, `random.Random(seed).gauss(0.0, 1.0)`, in position
   order. `m17` changes only the Student-t source (it reads its normals from `random.Random(seed + 1)`), so it violates
   no sentence of the page.
3. Measured: `m17` passes every check of `grader/test_project.py` on every seed from 0 to 49 (round-2 verifier run,
   `signt_m17_collect_seeds.out`; the suite collects 138 checks, and one is skipped on instances with nu of 3 or 4). The suite has no property that observes the Student-t source, so the survival is
   expected.
4. The page sentences that tie the two families to one seed are not in the contract. The Lab 1 code docstring ("from the
   same seed") describes the lab's own simulator, whose printed losses are not a contract for `tail_risk.py`. Item 5
   leaves the Student-t source open, so a conforming module need not reproduce the lab's numbers.

Design note (owner's choice): the alternative to this ruling is to freeze the Student-t source in item 5 and add a
grader test that observes it. Freezing the source alone would not make it observable in a conforming module: the order
of the Student-t normals and chi-square variables within that stream would also have to be fixed, and the page
leaves that order open. The page as revised leaves both open.
