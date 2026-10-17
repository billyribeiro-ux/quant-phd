"""Every inline lab on every built page runs locally and matches its page (tools/run_labs.py)."""

from __future__ import annotations

import pytest

from coursekit import Lab, built_units, labs_in, load_page
from run_labs import check_lab


def all_labs() -> list[Lab]:
    found: list[Lab] = []
    for u in built_units():
        for path in u.pages():
            found.extend(labs_in(load_page(path)))
    return found


@pytest.mark.parametrize("lab", all_labs(), ids=lambda lab: lab.id)
def test_lab_runs_and_matches_its_page(lab: Lab) -> None:
    problems = check_lab(lab)
    assert not problems, "\n".join(problems)
