# Phase 2 architect rulings (binding for the modules built after the first 20)

These confirm, with the changes below, the sections titled "Architect decisions (PROPOSED ...)" that the architect's
assistants appended to the plans of P0.1, P0.2, S0, CS1, CS3 and FI1, and the Atlas contracts A1, A2, A3 and A5. Where this
file and a proposal differ, this file wins. All rulings of plans/FINAL-ARCHITECT-RULINGS.md (1-41) continue to apply.

1. **P0.1 and P0.2 hours.** Both modules are 16 h (P0.1: lessons 12 h plus a 4 h project; P0.2 follows its own plan's split
   under the same total). The yaml edit and regeneration (render_curriculum, build_site, the BLUEPRINT and README figures,
   tests/test_docs_figures.py) are done once, for both modules, in one commit.
2. **S0.** Prerequisites become [CS1, M4] (the Q-Q reference needs the normal distribution and the quantile function; S1 already
   lists M4). The data-quality function takes an in-memory dataset (A3 contract), not a CS3 store, following A15. The
   Anscombe table is not typed from memory: the lab uses a constructed SIMULATED set labelled as not Anscombe's data until a
   builder can read a cleared source. The placement bar is 0.8 (the AC2 value). Lessons 8+7+6+8+6 = 35 h, project 15 h.
3. **CS1.** Labs and graders use Python 3.14 (the Pyodide runtime is 314.0.7); the curriculum text "3.13" is changed with the
   hours edit in one regeneration. Nine lessons. Timing is a deterministic count, never a clock value. pandas stays a pending
   concept until a Pyodide wheel is confirmed. atlas/A1.contract.md is accepted as drafted.
4. **CS3.** The store lab runs in Python with a pure-Python as-of reference; SQL is shown as "not run". Local engine: sqlite3
   everywhere in labs and graders (no DuckDB pin is needed); DuckDB appears in prose only. Tick size 0.01 for fixtures. Eight
   lessons of 8 h plus a 16 h project. "Parquet snapshot" in L08 becomes a CSV example. atlas/A2.contract.md is accepted;
   QR1's DuckDB lab follows the same rule when it is planned.
5. **FI1.** Contract atlas/A5.contract.md is accepted; L06 uses a SIMULATED curve with an honest-pending note; the GSW parameter
   test is honest-pending; no DATA_REQUEST is raised. The Svensson registry title spacing ("1992 - 1994" versus "1992-1994") is
   cosmetic and the registry record stands. Lessons 8 x 9 h plus an 18 h project. NumPy only.
6. **Registry requests.** No agent runs tools/add_reference.py. Each request listed in the six plans is run by the architect
   after the issuer page is read; until then the module cites nothing from it. Requests whose title cannot be identified from
   evidence are withdrawn.
7. **Sequence.** Build order follows the prerequisite order: P0.1, P0.2, S0, CS1, CS3, FI1 first (they block almost everything),
   then the modules whose prerequisites are built.
