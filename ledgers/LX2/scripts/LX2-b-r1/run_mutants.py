# Runs each standing LX2 lab mutant (no new mutants) under python -I -W error and compares stdout with the twin's expected output.
import glob, os, subprocess, sys
OUT = 'ledgers/LX2/scripts/LX2-b-r1/out'
exp = {'L03': open(f'{OUT}/twin_L03.out', encoding='utf-8').read(), 'L04': open(f'{OUT}/twin_L04.out', encoding='utf-8').read()}
groups = {'L03': ['r2_alt_l03_own_order_by_arrival', 'r2_l03_bid_sort_wrong_key', 'r2_l03_drop_trader_cancel_term',
                  'r2_l03_one_fill_per_execution', 'r3_l03_ask_first_cancel_order', 'r3_l03_draw_before_own_check'],
          'L04': ['r2_l04_strict_band', 'r2_l04_truncate_not_round', 'r3_l04_partD_error_sign_flipped',
                  'mut-lab2-bias-mean-abs', 'mut-lab2-bias-sign-flip', 'mut-lab2-hit-over-8', 'mut-lab2-strict-band',
                  'mut-lab2-truncated-hit-rate']}
for twin, names in groups.items():
    for n in names:
        path = f'ledgers/LX2/mutants/{n}.py'
        if not os.path.exists(path):
            print(n, 'MISSING'); continue
        p = subprocess.run([sys.executable, '-I', '-W', 'error', path], capture_output=True, text=True, timeout=120)
        same = p.stdout == exp[twin] and p.returncode == 0
        diff_line = ''
        if not same:
            a = exp[twin].splitlines(); b = p.stdout.splitlines()
            for x, y in zip(a, b):
                if x != y:
                    diff_line = f'expected: {x[:90]!r} | got: {y[:90]!r}'; break
            if not diff_line and len(a) != len(b):
                diff_line = f'line counts {len(a)} vs {len(b)}; exit {p.returncode}; stderr: {p.stderr.strip()[-120:]!r}'
        print(f'{n} [{twin}] exit={p.returncode} {"SURVIVES" if same else "KILLED"} {diff_line}')
