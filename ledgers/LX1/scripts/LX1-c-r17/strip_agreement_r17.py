"""Round-17 verifier: the agreement check was removed from the Lab 3 twin (700bf33f). Mutants written against the
older twin still carry it, so their kills could come from a check the page no longer claims. This script writes a
copy of each mutant with the agreement check and its printed line removed, so that each mutant's kill can be
attributed to its own error. Usage: python -I strip_agreement_r17.py <out_dir> <mutant.py>...
"""
import pathlib
import re
import sys

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
CHECK = re.compile(r"\n[ \t]*if abs\(100 \* \(.*?statistics\.stdev\(.*?\n[ \t]*raise ValueError\([^\n]*\n", re.S)
PRINT = re.compile(r'\n[ \t]*print\("two-pass and statistics\.stdev agree[^\n]*')
IMPORT = re.compile(r"\nimport statistics[^\n]*")
AGREE = re.compile(r"\nAGREEMENT = [^\n]*")
for name in sys.argv[2:]:
    src = pathlib.Path(name).read_text(encoding="utf-8")
    new = PRINT.sub("", CHECK.sub("\n", src))
    new = IMPORT.sub("", AGREE.sub("", new))
    (out / pathlib.Path(name).name).write_text(new, encoding="utf-8")
    print(f"{pathlib.Path(name).name}: check_removed={src != new} statistics_left={'statistics.stdev' in new}")
