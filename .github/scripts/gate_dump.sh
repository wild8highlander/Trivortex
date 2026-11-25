#!/usr/bin/env bash
# Dump a failed pytest gate's diagnostics to every channel readable without
# signing in to GitHub: the public job summary ($GITHUB_STEP_SUMMARY) and
# ::error:: workflow commands (they become annotations, which the job page
# serves server-side). The raw Actions log itself is behind a sign-in wall,
# so a reference-value failure must land here, fully localized (traceback,
# versions, platform), without a second run.
set -u

log="$1"
label="$2"

env_block="$(python -V 2>&1
uname -mr
ldd --version 2>/dev/null | head -n 1
python - <<'PY'
import sys

print("executable:", sys.executable)
try:
    import numpy

    print("numpy:", numpy.__version__)
except Exception as exc:  # pragma: no cover - diagnostics only
    print("numpy import FAILED:", exc)
PY
pip freeze 2>/dev/null | grep -Ei '^(numpy|scipy|mpmath|pytest)==')"

# ── channel 1: the public job summary ───────────────────────────────────────
{
  echo "### Gate failed: ${label}"
  echo
  echo '```text'
  if [ -f "${log}" ]; then
    tail -n 200 "${log}"
  else
    echo "(log file ${log} not found)"
  fi
  echo '```'
  echo
  echo '```text'
  printf '%s\n' "${env_block}"
  echo '```'
} >> "${GITHUB_STEP_SUMMARY:-/dev/null}"

# ── channel 2: ::error:: annotations (server-rendered on the job page) ──────
# GitHub caps each annotation at ~1 KiB and the count per step, so the tail
# of the log is split into line-aligned chunks of ~700 characters.
chunk="${env_block}"
count=0
if [ -f "${log}" ]; then
  while IFS= read -r line; do
    cand="${chunk}
${line}"
    if [ "${#cand}" -gt 700 ]; then
      count=$((count + 1))
      [ "${count}" -gt 9 ] && break
      msg="${chunk//'%'/'%25'}"
      msg="${msg//$'\r'/'%0D'}"
      msg="${msg//$'\n'/'%0A'}"
      echo "::error title=CI gate failed: ${label}::${msg}"
      chunk="${line}"
    else
      chunk="${cand}"
    fi
  done < "${log}"
fi
if [ -n "${chunk}" ] && [ "${count}" -le 9 ]; then
  count=$((count + 1))
  [ "${count}" -gt 9 ] && exit 0
  msg="${chunk//'%'/'%25'}"
  msg="${msg//$'\r'/'%0D'}"
  msg="${msg//$'\n'/'%0A'}"
  echo "::error title=CI gate failed: ${label}::${msg}"
fi
