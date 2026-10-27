import json, re, subprocess, collections, sys
R = '/tmp/verify-s7-r1-p'
BASE = '5e5da87'
old = json.load(open('/tmp/ap1-r5/s7p/project_release.json'))
rows = old['rows']
_cache = {}
def changed(p):
    if p not in _cache:
        r = subprocess.run(['git', '-C', R, 'diff', '--quiet', BASE, 'HEAD', '--', p])
        _cache[p] = r.returncode != 0
    return _cache[p]
S7 = 'course/modules/S/S7/'
BN = {
 'project.html': S7+'project.html', 'index.html': S7+'index.html', 'cards.json': S7+'cards.json',
 'reference.py': S7+'grader/reference.py', 'test_project.py': S7+'grader/test_project.py', 'instance.py': S7+'grader/instance.py', 'starter.py': S7+'grader/starter.py',
 'A8.contract.md': 'atlas/A8.contract.md', 'rubric.js': 'course/assets/js/rubric.js', 'grader.js': 'course/assets/js/grader.js', 'site.js': 'course/assets/js/site.js',
 'quiz.js': 'course/assets/js/quiz.js', 'store.js': 'course/assets/js/store.js', 'print.css': 'course/assets/css/print.css', 'course.css': 'course/assets/css/course.css',
 'MANIFEST.json': 'course/assets/data/market/MANIFEST.json', 'data_sources.yaml': 'tools/data_sources.yaml', 'page_smoke.py': 'tools/page_smoke.py',
 'references.json': 'references/references.json', 'notation.json': 'notation/notation.json', 'glossary.json': 'course/assets/data/glossary.json',
 'program.json': 'course/assets/data/program.json', 'curriculum.json': 'curriculum/curriculum.json', 'test_memo_exemplars.py': 'tests/test_memo_exemplars.py',
 'test_labs.py': 'tests/test_labs.py', 'test_page_checks.py': 'tests/test_page_checks.py', 'test_docs_figures.py': 'tests/test_docs_figures.py',
 'test_figure_kernels.py': 'tests/test_figure_kernels.py', 'test_run_labs.py': 'tests/test_run_labs.py', 'test_fetch_data.py': 'tests/test_fetch_data.py',
 'test_js.py': 'tests/test_js.py', 'rubric.test.mjs': 'tests/js/rubric.test.mjs', 'BLUEPRINT.md': 'BLUEPRINT.md', 'README.md': 'README.md',
 'VERIFIER_RULES.md': 'VERIFIER_RULES.md', 'BUILDER_RULES.md': 'BUILDER_RULES.md', 'CURRICULUM.md': 'CURRICULUM.md', 'S7.md': 'benchmarks/S7.md',
 'LOCK.json': 'course/assets/vendor/LOCK.json', 'vendor_spec.yaml': 'tools/vendor_spec.yaml', 'requirements-dev.txt': 'requirements-dev.txt',
 'pyproject.toml': 'pyproject.toml', 'fetch_data.py': 'tools/fetch_data.py', 'run_labs.py': 'tools/run_labs.py', 'run_graders.py': 'tools/run_graders.py',
 'mutate_graders.py': 'tools/mutate_graders.py', 'verify_refs.py': 'tools/verify_refs.py', 'check_pages.py': 'tools/check_pages.py', 'check_dag.py': 'tools/check_dag.py',
 'check_projects.py': 'tools/check_projects.py', 'build_site.py': 'tools/build_site.py', 'ledger.py': 'tools/ledger.py',
}
for n in range(1, 9):
    BN[f'L0{n}.html'] = S7+f'L0{n}.html'
TOK = re.compile(r"(?:[A-Za-z0-9_\-.\[\]]+/)*[A-Za-z0-9_\-.]+\.(?:html|py|js|json|yaml|md|mjs|css|txt|toml|csv|mjs|sh)")
DIRS = {'atlas/': 'atlas', 'tests/labs/S7/': 'tests/labs/S7', 'grader/': S7+'grader', 'ledgers/S7/mutants/': 'ledgers/S7/mutants', 'course/assets/data/market/': 'course/assets/data/market'}
def paths_of(loc):
    out = []
    for t in TOK.findall(loc):
        pass
    for m in re.finditer(r"(?:[A-Za-z0-9_\-.]+/)*[A-Za-z0-9_\-.]+\.(?:html|py|js|json|yaml|md|mjs|css|txt|toml|csv|sh)", loc):
        t = m.group(0).lstrip('./')
        if '/' in t:
            if t.startswith('../'): t = t[3:]
            out.append(t)
        elif t in BN:
            out.append(BN[t])
    for k, v in DIRS.items():
        if k in loc: out.append(v)
    for kw in ['S7/', 'project.html']:
        pass
    return sorted(set(out))
if __name__ == '__main__':
    need = []
    for r in rows:
        ps = paths_of(r['location'])
        ch = [p for p in ps if changed(p)]
        r['_paths'] = ps; r['_changed'] = ch
        if ch or not ps:
            need.append(r)
    print('rows', len(rows), 'need-explicit', len(need))
    c = collections.Counter()
    for r in need:
        c[tuple(r['_changed']) or ('NOPATH',)] += 1
    for k, v in c.most_common(): print(v, k)
    print('--- sample no-path rows:', [r['id'] for r in need if not r['_paths']][:80])
