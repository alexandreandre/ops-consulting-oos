# Shared by the hooks: go to the repository root and find a Python interpreter.
cd "$(git rev-parse --show-toplevel)" || exit 1
PY=
for candidate in .venv/bin/python .venv/Scripts/python.exe python3 python; do
  if [ -x "$candidate" ] || command -v "$candidate" >/dev/null 2>&1; then PY=$candidate; break; fi
done
if [ -z "$PY" ]; then
  echo "✗ Confidentiality guard: Python not found, so this action is blocked. Ask Codex to set up the project." >&2
  exit 1
fi
