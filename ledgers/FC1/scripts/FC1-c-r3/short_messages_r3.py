"""Round-3 (verifier D3): list assert messages of five words or fewer in test_project.py. Usage: short_messages_r3.py <file>."""
import ast
import sys

src = open(sys.argv[1], encoding="utf-8").read()
tree = ast.parse(src)
short = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assert) and node.msg is not None:
        text = ast.get_source_segment(src, node.msg) or ""
        if len(text.split()) <= 5:
            short.append((node.lineno, text))
print("asserts with a message:", sum(1 for n in ast.walk(tree) if isinstance(n, ast.Assert) and n.msg is not None))
print("messages of five words or fewer:", len(short))
for line, text in short:
    print(" line", line, text)
