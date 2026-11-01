#!/usr/bin/env bash
# Atalho: sincroniza as regras e memórias (o mesmo que dotagents-sync).
exec "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/bin/sync" "$@"
