import pathlib, sys
ref = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
def patch(old, new, count=1):
    assert ref.count(old) == 1, old
    return ref.replace(old, new)
mutants = {
 "r8n01_prints_on_quantity_one": ("Student error: CashTrade.events prints a line when the quantity is 1, a valid input the page allows, which the page's silence rule forbids.",
   ('        """One event: (settlement_day, -side * quantity * price_cents), from the holder\'s side."""\n',
    '        """One event: (settlement_day, -side * quantity * price_cents), from the holder\'s side."""\n        if self.quantity == 1:\n            print("trade")\n')),
 "r8n02_prints_on_zero_yield": ("Student error: bond_price_cents prints a line when the yield is zero, a valid input the page allows, which the page's silence rule forbids.",
   ('    y = Fraction(rate, 10_000)\n', '    y = Fraction(rate, 10_000)\n    if rate == 0:\n        print("zero yield")\n')),
 "r8n03_prints_on_settlement_day_one": ("Student error: CashTrade.events prints a line when the settlement day is 1, a valid input the page allows, which the page's silence rule forbids.",
   ('        """One event: (settlement_day, -side * quantity * price_cents), from the holder\'s side."""\n',
    '        """One event: (settlement_day, -side * quantity * price_cents), from the holder\'s side."""\n        if self.settlement_day == 1:\n            print("day one")\n')),
 "r8n04_prints_on_face_one_cent": ("Student error: Bond.events prints a line when the face is one cent, a valid input the page allows, which the page's silence rule forbids.",
   ('        """(period, amount_cents) for periods 1..periods, sorted by period, amounts from the holder\'s side."""\n',
    '        """(period, amount_cents) for periods 1..periods, sorted by period, amounts from the holder\'s side."""\n        if self.face_cents == 1:\n            print("face one")\n')),
}
for name, (doc, (old, new)) in mutants.items():
    src = patch(old, new)
    # replace module docstring? keep reference docstring, prepend mutant description as the module docstring
    lines = src.split("\n", 1)
    body = lines[1] if lines[0].startswith('"""') else src
    text = '"""' + doc + '"""\n' + src.split('"""', 2)[2] if src.startswith('"""') else '"""' + doc + '"""\n' + src
    (out / (name + ".py")).write_text(text)
    print(name)
