import ast, sys
def norm(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:] or [ast.Pass()]
        if isinstance(node, ast.Raise) and node.exc is not None and isinstance(node.exc, ast.Call):
            node.exc.args = []
    return ast.dump(tree, include_attributes=False)
a = norm("/tmp/verify-ap1-r10-m/course/modules/AP/AP1/grader/reference.py")
b = norm("/tmp/verify-ap1-r10-m/ledgers/AP1/equivalent/m48_generic_value_error_messages.py")
print("AST EQUAL" if a == b else "AST DIFFERENT", len(a))
