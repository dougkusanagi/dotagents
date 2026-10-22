#!/usr/bin/env bash
set -euo pipefail
REPO="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
source "$REPO/bin/paths"
command_path="$HOME/.local/bin/dotagents-sync"
if [[ -e "$command_path" && ! -L "$command_path" ]]; then
  echo "erro: arquivo existente: $command_path" >&2
  exit 1
fi
mkdir -p "$DOTAGENTS_DATA/memory" "$DOTAGENTS_CONFIG" "$DOTAGENTS_STATE" "$HOME/.local/bin"
if [[ ! -e "$DOTAGENTS_DATA/memory/.git" ]]; then
  git -C "$DOTAGENTS_DATA/memory" init -q -b main
fi
ln -sfn "$REPO/bin/sync" "$command_path"
# Hooks versionados: sincronizam os agentes após commit e após pull/merge.
if [[ -d "$REPO/.git" ]]; then git -C "$REPO" config core.hooksPath hooks; fi
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) echo 'aviso: adicione ~/.local/bin ao PATH para usar dotagents-sync' >&2 ;;
esac
"$command_path"
