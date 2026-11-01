#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash -n bin/sync bin/migrate bin/paths install.sh sync.sh hooks/pre-commit
bash tests/pre-commit.sh
# No Windows, python3 pode ser só um atalho da Microsoft Store: confira se roda de fato.
if python3 -c '' 2>/dev/null; then py=(python3)
elif python -c '' 2>/dev/null; then py=(python)
elif command -v uv >/dev/null 2>&1; then py=(uv run python)
else echo "erro: Python 3 não encontrado" >&2; exit 1; fi
export PYTHONUTF8=1
if command -v cygpath >/dev/null 2>&1; then export DOTAGENTS_TEST_BASH="$(cygpath -w "$BASH")"; fi
"${py[@]}" tests/integration.py
