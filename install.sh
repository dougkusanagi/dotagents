#!/usr/bin/env bash
# Prepara memory/ como repositório git próprio e liga os agentes via bin/sync.
set -euo pipefail

AGENTS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$AGENTS_HOME" != "$HOME/.agents" ]]; then
  echo "aviso: as regras citam ~/.agents, mas o repositório está em $AGENTS_HOME" >&2
fi

mkdir -p "$AGENTS_HOME/memory"
if [[ ! -d "$AGENTS_HOME/memory/.git" ]]; then
  git -C "$AGENTS_HOME/memory" init -q -b main
  echo "memory/: repositório git criado (adicione um remote privado para sincronizar entre máquinas)"
fi

chmod +x "$AGENTS_HOME/bin/sync"
"$AGENTS_HOME/bin/sync"
