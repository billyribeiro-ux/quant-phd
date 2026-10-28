import ast, sys
def funcs(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef,)):
            seg = ast.get_source_segment(src, node)
            # include decorators in segment
            if node.decorator_list:
                start = node.decorator_list[0].lineno
                seg = "\n".join(src.splitlines()[start-1:node.end_lineno])
            out[node.name] = (seg, node.lineno)
    return out
old = funcs(sys.argv[1]); new = funcs(sys.argv[2])
names = sys.argv[3:]
for n in names:
    if n not in old or n not in new:
        print(n, "MISSING", n in old, n in new); continue
    print(f"{n}: identical={old[n][0]==new[n][0]} old_line={old[n][1]} new_line={new[n][1]}")
print("all top-level functions:", len(old), len(new), "changed:", sorted(k for k in old if k in new and old[k][0]!=new[k][0]), "removed:", sorted(set(old)-set(new)), "added:", sorted(set(new)-set(old)))
