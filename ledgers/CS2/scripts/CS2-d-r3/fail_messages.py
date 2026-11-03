"""List every pytest.fail / must_raise / must_accept message in the CS2 grader and flag any that contains a digit
or an f-string placeholder (a possible printed expected value). Usage: python -I fail_messages.py <suite path>"""

import ast
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        fn = ast.unparse(node.func)
        if fn in ("pytest.fail", "must_raise", "must_accept", "refuse_or_correct"):
            msg_nodes = []
            if fn == "pytest.fail":
                msg_nodes = node.args[:1]
            elif fn in ("must_raise", "must_accept"):
                msg_nodes = node.args[1:2]
            else:
                msg_nodes = node.args[2:3]
            for m in msg_nodes:
                text = ast.unparse(m)
                flag = "DIGIT" if re.search(r"\d", text) else ""
                fstr = "FSTR" if isinstance(m, ast.JoinedStr) else ""
                print(f"L{node.lineno} {fn} {flag} {fstr} :: {text[:170]}")
