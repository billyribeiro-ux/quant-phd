#!/bin/bash
# Round-4 independent grep checks for FC2 L04-L06: twin imports, network, hub hours, twin docstring lines.
# Run from the checkout root: ledgers/FC2/scripts/FC2-b-r4/misc_ind_r4.sh
echo "== twin imports / randomness / network / file IO"
grep -n "^import\|^from\|random\|socket\|urllib\|http\|open(\|__name__" tests/labs/FC2/lab-FC2-L04-1.py tests/labs/FC2/lab-FC2-L05-1.py tests/labs/FC2/lab-FC2-L06-1.py
echo "== hub hour cards (index.html)"
grep -o 'data-hours-lessons="[0-9]*" data-hours-project="[0-9]*"' course/modules/FC/FC2/index.html
grep -o 'card-kicker">L0[4-6] · [0-9] h' course/modules/FC/FC2/index.html
echo "== lesson data-hours and eyebrows"
grep -o 'data-hours="[0-9]*"' course/modules/FC/FC2/L04.html course/modules/FC/FC2/L05.html course/modules/FC/FC2/L06.html
grep -o 'eyebrow">FC2 · Lesson [0-9] of 8 · [0-9] study hours' course/modules/FC/FC2/L04.html course/modules/FC/FC2/L05.html course/modules/FC/FC2/L06.html
echo "== L06 twin docstring claim about printed cents (lines 3-6)"
sed -n 3,6p tests/labs/FC2/lab-FC2-L06-1.py
echo "== L06 printed output lines that show prices in currency units (no cents suffix)"
grep -n "stock at expiry\|payoff after an up move\|payoff at expiry\|value after an up move" course/modules/FC/FC2/L06.html
