import os, sys, re
src_dir, out_dir = sys.argv[1], sys.argv[2]
FUNC = '''def sales_price_by_product(products: tuple[Product, ...]) -> dict[str, int]:
    """Sales price variance of each product, (p_a,i - p_b,i) * q_a,i, in cents, keyed by product name."""
    return {p.name: (p.price_actual - p.price_budget) * p.units_actual for p in products}


'''
LOOP = '''    for name, value in sales_price_by_product(PRODUCTS).items():
        print(f"sales_price_variance_{name} {value}")
'''
report = []
for root, _, files in os.walk(src_dir):
    for f in files:
        if not f.endswith('.py'):
            continue
        p = os.path.join(root, f)
        t = open(p, encoding='utf-8').read()
        if 'AC4 L06' not in t[:200]:
            continue
        n_def = t.count('\ndef decompose(')
        n_pr = len(re.findall(r"\n    print\(f\"sales_price_variance \{result\['sales_price'\]\}\"\)\n", t))
        if n_def != 1 or n_pr != 1:
            report.append(f"ANCHOR {f} def={n_def} print={n_pr}")
            continue
        t = t.replace('\ndef decompose(', '\n' + FUNC + 'def decompose(', 1)
        t = re.sub(r"(\n    print\(f\"sales_price_variance \{result\['sales_price'\]\}\"\)\n)", lambda m: m.group(1) + LOOP, t, count=1)
        rel = os.path.relpath(p, src_dir).replace(os.sep, '__')
        open(os.path.join(out_dir, rel), 'w', encoding='utf-8').write(t)
        report.append(f"OK {rel}")
print("\n".join(report))
