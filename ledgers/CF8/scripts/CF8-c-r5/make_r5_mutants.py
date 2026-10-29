import pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
subs = {
 "n01-repay-one-cent-short": ("repay = min(before - minimum, drawn)", "repay = min(before - minimum - 1, drawn) if drawn else 0"),
 "n02-liquidity-ignores-drawn": ("liquidity = cash + commitment - drawn", "liquidity = cash + commitment"),
 "n03-draw-ignores-drawn-balance": ("draw = min(need, commitment - drawn) if capped else need", "draw = min(need, commitment) if capped else need"),
 "n04-shortfall-skips-last-week": ("for row in rows]", "for row in rows[:-1]]"),
 "n05-peak-ignores-opening": ('peak = max([case["opening_drawn_cents"]] + [row["drawn_balance_cents"] for row in rows])', 'peak = max([row["drawn_balance_cents"] for row in rows])'),
}
for name, (a, b) in subs.items():
    n = src.count(a)
    if n != 1:
        print("SKIP", name, "matches", n); continue
    (out / f"{name}.py").write_text(src.replace(a, b))
    print("WROTE", name)
