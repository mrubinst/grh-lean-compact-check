#!/usr/bin/env python3
"""Regenerate index.html (status page, same design as grh-lean-verification) from progress text on stdin."""
import sys, re, html, datetime, os
P = sys.stdin.read()
here = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(here, 'style.css.part')).read()
def grab(k):
    m = re.search(k + r'=(\d+)', P); return int(m.group(1)) if m else 0
total, built, rok, rbad = grab('modules_total') or 794, grab('built'), grab('replay_ok'), grab('replay_bad')
sec = {}
cur = None
for line in P.splitlines():
    if line.startswith('--- '):
        cur = line[4:].split()[0]; sec[cur] = []
        if cur == 'load': sec[cur] = [line[4:]]
    elif cur: sec[cur].append(line)
stages = [l for l in sec.get('stages', []) if l.strip()]
st = ' '.join(stages)
def has(s): return s in st
failed = 'FAILED' in st
def badge(state):
    return {'ok':'<span class="badge ok">Done</span>','run':'<span class="badge wait">Running</span>',
            'wait':'<span class="badge wait">Waiting</span>','bad':'<span class="badge bad">Failed</span>'}[state]
def state(done, started, fail_key):
    if fail_key and has(fail_key): return 'bad'
    if done: return 'ok'
    return 'run' if started else 'wait'
built_disp = min(built, total)
ax = '\n'.join(sec.get('our_axioms', [])).strip()
ax_ok = has('our_axioms ok') and ax.count('[propext, Classical.choice, Quot.sound]') >= 5 and 'sorry' not in ax
rows = [
 (state(True, True, None), 'Source pinned to the authors\' release', 'Repository <a href="https://github.com/lsernau/grh-lean/tree/72fead102f663d5c7a407964a13dc0cf9d977207"><code>lsernau/grh-lean</code></a>, folder <code>grh-compact</code>, commit <code>72fead10</code> (the only commit). Same commit as the independent audits reported on Zulip.'),
 (state(True, True, None), 'The theorem statements say what they should', '<code>src/Statements.lean</code> imports only Mathlib and is identical (apart from blank lines) to the statements we checked for the original development on 20&ndash;21 Nov.'),
 (state(True, True, None), 'Static scan for unproved assumptions and kernel bypasses', 'No <code>axiom</code>, <code>sorry</code>, <code>native_decide</code>, <code>unsafe</code>, <code>implemented_by</code>, <code>@[extern]</code>, and no <code>macro</code>, <code>syntax</code>, <code>notation</code> or <code>elab</code> declarations in the project source.'),
 (state(has('cache_get ok'), has('cache_get begin'), 'cache_get FAILED'), 'Mathlib from its official cache', 'Mathlib commit <code>56a00585</code> as pinned by the project; Lean v4.35.0.'),
 (state(has('build ok'), has('build begin'), 'build FAILED'), f'Full compile of all {total} project modules', f'{built_disp:,} of {total} compiled so far.'),
 (state(ax_ok, has('axioms begin'), 'axioms FAILED'), '<code>#print axioms</code> and types of the five main theorems', 'Expected: only <code>propext</code>, <code>Classical.choice</code>, <code>Quot.sound</code>; each theorem has the type fixed in <code>Statements.lean</code>.'),
 (state(has('replay done') and rbad == 0 and rok >= total, has('replay begin'), None) if rbad == 0 else 'bad', 'Kernel replay of every module (<code>leanchecker</code>)', f'{rok:,} of {total} accepted, {rbad} rejected.'),
 (state(has('comparator_paranoid ok'), has('comparator_paranoid begin'), 'comparator_paranoid FAILED'), '<code>lake comparator --paranoid</code>: same statements, axioms, and six kernels', 'Compares the five theorems with <code>Challenge.lean</code> (the five statements with <code>sorry</code>), checks the axioms, and replays the export through Lean&rsquo;s kernel and the five external checkers bundled with Lean 4.35: <code>leanchecker-paranoid</code>, <code>lean4lean</code>, <code>nanoda</code>, <code>con-leche</code>, <code>con-ron</code>. Run with <code>--inadvisably-no-sandbox</code>: the cluster blocks the <code>bwrap</code> sandbox (AppArmor restricts unprivileged user namespaces), so this run does not have the sandbox guarantee against the project&rsquo;s own build code.'),
]
if has('comparator_paranoid ok') and ax_ok and rbad == 0 and rok >= total:
    top = '<span class="badge ok">All checks complete</span>'
elif has('pipeline finished') and ax_ok and rbad == 0 and rok >= total:
    top = '<span class="badge wait">Compile, axioms and kernel replay complete; paranoid multi-kernel check running</span>'
elif failed or rbad:
    top = '<span class="badge bad">A step failed; see the log</span>'
else:
    top = '<span class="badge wait">In progress</span>'
pct = 0
if has('build begin'): pct = 10 + 60*built_disp/total
if has('build ok'): pct = 70
if has('replay begin'): pct = 75 + 25*rok/total
if has('pipeline finished'): pct = 80
if has('comparator_paranoid begin'): pct = 85
if has('comparator finished'): pct = 100
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
log = ''.join(f'<li><time>{html.escape(l[:10]+" "+l[11:16])} UTC</time>{html.escape(l[21:])}</li>\n' for l in reversed(stages) if len(l) > 21)
trs = ''.join(f'<tr><td>{badge(s)}</td><td><div class="what">{w}</div><div class="how">{d}</div></td></tr>\n' for s, w, d in rows)
axblock = f'<pre>{html.escape(ax)}</pre>' if ax else '<p>Not yet run.</p>'
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Short GRH Lean Check</title>
<style>
{css}
</style>
</head>
<body>
<main>
<h1>An independent check of the short Lean proof of RH and GRH</h1>
<p class="sub">Checking the compact edition (about 76,000 lines) of the shortened Lean 4 proof posted by Luke Sernau with colleagues at Anthropic and Claude on 25 November 2026, a rewriting of the Alp&ouml;ge&ndash;Claude development. Last updated {now}.</p>
<p class="sub"><a href="https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/">&larr; Michael Rubinstein's page on the Alp&ouml;ge/Claude proof</a> &middot; <a href="https://mrubinst.github.io/grh-lean-verification/">our check of the original 17-million-line development</a> &middot; <a href="https://github.com/mrubinst/grh-lean-compact-check">GitHub repository</a> (scripts and the source of this page)</p>
<div class="box status">
  {top}
  <div>
    <strong>Where things stand.</strong> {built_disp:,} of {total} modules compiled; kernel replay {rok:,} accepted, {rbad} rejected.
    <div class="bar" aria-label="progress"><span style="width:{pct:.0f}%"></span></div>
    <div style="font-size:.9rem;color:var(--muted)">Server load on cpu160: {html.escape(' '.join(sec.get('load', ['?'])))}. This page reloads every 5 minutes and is regenerated every 10.</div>
  </div>
</div>
<h2>Checklist</h2>
<table class="steps">
{trs}</table>
<h2>Axiom check output</h2>
{axblock}
<h2>Paranoid multi-kernel check (latest lines)</h2>
<pre>{html.escape(chr(10).join(sec.get('comparator', [])).strip() or 'Not yet run.')}</pre>
<h2>How we are building it</h2>
<p>One server (cpu160, University of Waterloo), local disk, <code>lake build</code> at slightly lowered priority because the machine is shared. The open-file limit is raised to the hard limit (the first attempt failed while unpacking the Mathlib cache with the default limit of 1024). Kernel replay runs <code>lake env leanchecker</code> on each of the project's modules, 48 at a time. Every result on this page comes from our own runs.</p>
<h2>What a successful check will and won't mean</h2>
<p>If the compile succeeds, the axioms are only the standard three, and the kernel accepts every module, then the five theorems are proved, assuming the Lean kernel is sound and Mathlib's definitions of &zeta; and of Dirichlet L-functions mean what they are supposed to. It says nothing about whether the shortened proof is the clearest one, or how its arguments compare with the original; we are studying that separately.</p>
<h2>Log</h2>
<ul class="log">
{log}</ul>
<footer>The checks are run by Claude Code (an AI agent) on the account owner's university compute allocation. Source of this page: <a href="https://github.com/mrubinst/grh-lean-compact-check">github.com/mrubinst/grh-lean-compact-check</a>.</footer>
</main>
</body>
</html>
'''
open(os.path.join(here, 'index.html'), 'w').write(page)
