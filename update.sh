#!/bin/bash
# Pull progress from cpu160 and regenerate README.md (private status page). Pushes only on change.
cd "$(dirname "$0")"
P=$(ssh -o BatchMode=yes -o ConnectTimeout=20 -J mrubinst@biglinux.math.uwaterloo.ca mrubinst@cpu160 '/u/mrubinst/grhc/progress.sh; echo "--- axioms"; cat /u/mrubinst/grhc/axioms.out 2>/dev/null | head -20; echo "--- our_axioms"; cat /u/mrubinst/grhc/our_axioms.out 2>/dev/null | head -30; echo "--- buildtime"; grep -E "Elapsed|Maximum resident" /u/mrubinst/grhc/build.time 2>/dev/null; true') || exit 0
NOW=$(date -u +"%Y-%m-%d %H:%M UTC")
{
echo "# GRH Lean check: compact edition (private)"
echo
echo "Independent build and check of **lsernau/grh-lean**, folder \`grh-compact\`, commit \`72fead102f663d5c7a407964a13dc0cf9d977207\` (25 Nov 2026), on our own hardware (UWaterloo cpu160, local disk). Lean v4.35.0, Mathlib \`56a00585\` as pinned by the project. This page reports only our own runs."
echo
echo "Last updated: $NOW"
echo
echo "## Plan"
echo "1. \`lake exe cache get\` (Mathlib oleans from the Mathlib cache)"
echo "2. \`lake build\` of all project modules"
echo "3. \`#print axioms\` for the five theorems (project script and our own file), and \`#check\` of their types against \`Statements.lean\`"
echo "4. Kernel replay of every project module with \`leanchecker\`"
echo "5. (later) export and independent checker"
echo
echo "## Current state"
echo '```'
echo "$P"
echo '```'
echo
echo "## Statements"
echo "\`src/Statements.lean\` (imports only Mathlib) is identical, apart from blank lines, to the one in the original Alpöge–Claude development we checked on 20–21 Nov 2026."
} > README.md
git add -A; git diff --cached --quiet || { git commit -qm "status $NOW"; git push -q origin HEAD:main 2>/dev/null; }
grep -q "pipeline finished" <<<"$P" && echo FINISHED
exit 0
