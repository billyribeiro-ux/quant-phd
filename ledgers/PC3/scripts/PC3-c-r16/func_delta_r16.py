"""Which top-level definitions of test_project.py changed between two commits (byte comparison of each def's source).

Usage: python -I func_delta_r16.py <old.py> <new.py>
"""
import ast
import sys


def defs(path):
    src = open(path, encoding="utf-8").read()
    lines = src.splitlines()
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, (ast.FunctionDef, ast.Assign)):
            name = node.name if isinstance(node, ast.FunctionDef) else ast.unparse(node.targets[0])
            start = (node.decorator_list[0].lineno if isinstance(node, ast.FunctionDef) and node.decorator_list else node.lineno)
            out[name] = "\n".join(lines[start - 1 : node.end_lineno])
    return out


old, new = defs(sys.argv[1]), defs(sys.argv[2])
changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
print("changed or added or removed definitions:", changed)
print("unchanged definitions:", len([k for k in old if k in new and old[k] == new[k]]), "of", len(old))
