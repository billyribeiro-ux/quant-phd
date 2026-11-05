"""Round-12 notation tally: macros and single-letter symbols in LX2 math vs notation/notation.json."""
import re, json
ROOT = '/Users/billyribeiro/.fanout/wt/verifyE12-LX2-d/'
n = json.load(open(ROOT + 'notation/notation.json', encoding='utf-8'))
macros = set(n['macros'])
used_macros, letters = set(), {}
for L in ['L01', 'L02', 'L03', 'L04', 'project', 'index']:
    t = open(ROOT + f'course/modules/LX/LX2/{L}.html', encoding='utf-8').read()
    for mth in re.finditer(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', t, re.S):
        s = mth.group(1) or mth.group(2) or ''
        used_macros |= {m for m in re.findall(r'\\[A-Za-z]+', s) if m in macros}
        s2 = re.sub(r'\\[A-Za-z]+', '', s)
        for m in re.finditer(r'(?<![A-Za-z])([A-Za-z])(?![A-Za-z])', s2):
            letters.setdefault(m.group(1), set()).add(L)
registered_symbols = ['T', 'Phi', 'gamma_3', 'gamma_4', 'R^*', 'R^{e*}', 'R_f', 'Q']
print('registered macros used in LX2 math:', sorted(used_macros))
print('single letters used (lesson: letters):', {k: sorted(v) for k, v in sorted(letters.items())})
print('registered program-wide symbols used as letters:', [s for s in ['T', 'Q', 'R', 'G'] if s in letters and s in ('T', 'Q')])
