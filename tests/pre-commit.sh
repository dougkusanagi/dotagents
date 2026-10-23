#!/usr/bin/env bash
# O hook pre-commit bloqueia global.md sem DOTAGENTS_ALLOW_RULES=1 e libera os demais arquivos.
set -euo pipefail
hook="$(cd "$(dirname "$0")/.." && pwd)/hooks/pre-commit"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
git -C "$tmp" init -q
cd "$tmp"
echo x > MEMORY.md; git add MEMORY.md
DOTAGENTS_ALLOW_RULES= "$hook"
echo x > global.md; git add global.md
if DOTAGENTS_ALLOW_RULES= "$hook" 2>/dev/null; then echo "falha: global.md não foi bloqueado" >&2; exit 1; fi
DOTAGENTS_ALLOW_RULES=1 "$hook"
