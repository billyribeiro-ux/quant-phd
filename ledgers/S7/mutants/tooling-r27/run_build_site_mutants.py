"""Re-create the 10 build_site.py mutants (P01-P11 family) from their round-23 descriptions and run their killers.

Run from a scratch copy of the repository: python -I run_build_site_mutants.py <repo copy root> <this checkout's venv python>.
Each mutant is one exact text replacement in tools/build_site.py; the killer is the test named in the ledger.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = sys.argv[2]
ORIG = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
RX = '_TEX_INLINE_MATH = re.compile(r"\\$(\\S|\\S[^$]*\\S)\\$")'
PLAIN_RETURN = "    return _TEX_INLINE_MATH.sub(r\"\\1\", title)"
FULL_TITLE = 'title = title_case(plain_title(entry["title"])).rstrip(".")'
MUTANTS = {
    "P01-no-hugging-rule": (RX, '_TEX_INLINE_MATH = re.compile(r"\\$([^$]*)\\$")'),
    "P02-single-character-math-not-matched": (RX, '_TEX_INLINE_MATH = re.compile(r"\\$(\\S[^$]*\\S)\\$")'),
    "P03-greedy-body": (RX, '_TEX_INLINE_MATH = re.compile(r"\\$(\\S|\\S.*\\S)\\$")'),
    "P05-word-characters-only-at-delimiters": (RX, '_TEX_INLINE_MATH = re.compile(r"\\$(\\w|\\w[^$]*\\w)\\$")'),
    "P06-two-character-math-not-matched": (RX, '_TEX_INLINE_MATH = re.compile(r"\\$(\\S|\\S[^$]+\\S)\\$")'),
    "P07-only-first-span-replaced": (PLAIN_RETURN, '    return _TEX_INLINE_MATH.sub(r"\\1", title, count=1)'),
    "P08-math-body-dropped-with-delimiters": (PLAIN_RETURN, '    return _TEX_INLINE_MATH.sub("", title)'),
    "P09-replacement-keeps-delimiters": (PLAIN_RETURN, '    return _TEX_INLINE_MATH.sub(r"$\\1$", title)'),
    "P10-full-cite-skips-plain-title": (FULL_TITLE, 'title = title_case(entry["title"]).rstrip(".")'),
    "P11-plain-title-after-title-case": (FULL_TITLE, 'title = plain_title(title_case(entry["title"])).rstrip(".")'),
}
KILLERS = {
    "P01-no-hugging-rule": "tests/test_build_site.py::test_tex_inline_math_in_a_title_is_shown_as_plain_text[prices-kept]",
    "P02-single-character-math-not-matched": "tests/test_build_site.py::test_tex_inline_math_in_a_title_is_shown_as_plain_text[tex-inline-math]",
    "P03-greedy-body": "tests/test_build_site.py::test_tex_math_spans_of_any_length_and_content_are_shown_as_plain_text[several-multi-character-spans]",
    "P05-word-characters-only-at-delimiters": "tests/test_build_site.py::test_tex_math_spans_of_any_length_and_content_are_shown_as_plain_text[math-that-is-not-word-characters]",
    "P06-two-character-math-not-matched": "tests/test_build_site.py::test_tex_math_spans_of_any_length_and_content_are_shown_as_plain_text[several-multi-character-spans]",
    "P07-only-first-span-replaced": "tests/test_build_site.py::test_tex_inline_math_in_a_title_is_shown_as_plain_text[two-spans]",
    "P08-math-body-dropped-with-delimiters": "tests/test_build_site.py::test_tex_inline_math_in_a_title_is_shown_as_plain_text[tex-inline-math]",
    "P09-replacement-keeps-delimiters": "tests/test_build_site.py::test_tex_inline_math_in_a_title_is_shown_as_plain_text[tex-inline-math]",
    "P10-full-cite-skips-plain-title": "tests/test_build_site.py::test_tex_inline_math_in_a_title_is_shown_as_plain_text[tex-inline-math]",
    "P11-plain-title-after-title-case": "tests/test_build_site.py::test_a_shouting_title_is_recased_after_its_math_is_made_plain",
}
target = ROOT / "tools/build_site.py"
for name, (old, new) in MUTANTS.items():
    assert ORIG.count(old) == 1, (name, ORIG.count(old))
    target.write_text(ORIG.replace(old, new), encoding="utf-8")
    import shutil
    for cache in ROOT.rglob("__pycache__"):
        shutil.rmtree(cache)
    r = subprocess.run([PY, "-B", "-m", "pytest", "-p", "no:cacheprovider", "-o", "addopts=", "-q", KILLERS[name]],
                       cwd=ROOT, capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin", "HOME": "/tmp"})
    status = "KILLED" if r.returncode != 0 else "SURVIVED"
    print(f"{name}: {status} ({r.stdout.strip().splitlines()[-1]})")
target.write_text(ORIG, encoding="utf-8")
