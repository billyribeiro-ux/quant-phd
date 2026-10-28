import html, re, subprocess, sys
ROOT = "/tmp/verifyB2-E1-d"
page = open(f"{ROOT}/course/modules/E/E1/project.html", encoding="utf-8").read()
labs = re.findall(r'<section class="lab[^"]*" id="(lab-E1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in labs:
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = open(f"{ROOT}/tests/labs/E1/{lab_id}.py", encoding="utf-8").read()
    twin_lines = twin.splitlines()
    page_lines = code.splitlines()
    mism = []
    for i, pl in enumerate(page_lines):
        if "___" in pl:
            continue
        if i >= len(twin_lines) or twin_lines[i] != pl:
            mism.append((i + 1, pl[:90], twin_lines[i][:90] if i < len(twin_lines) else None))
    print(lab_id, "page lines", len(page_lines), "twin lines", len(twin_lines), "line mismatches:", len(mism), mism[:3])
    run = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", f"{ROOT}/tests/labs/E1/{lab_id}.py"], capture_output=True, text=True).stdout
    print("  expected block equals run output:", run.strip() == expected.strip())
