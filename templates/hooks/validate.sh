#!/usr/bin/env bash
#
# Validações locais exigidas antes de push, PR ou merge. Não altera arquivos.
# Uso: scripts/validate.sh [--full|--quick]
#
# --full  (padrão) toda a validação; exigida nos branches principal e de integração.
# --quick só o que é rápido; use quando a validação completa passa de ~3 minutos.

set -uo pipefail

cd "$(git rev-parse --show-toplevel)"

mode="${1:---full}"
mode="${mode#--}"
started_at="$(date +%s)"
log_directory="$(mktemp -d)"
trap 'rm -rf "$log_directory"' EXIT

names=()
pids=()

# Roda uma validação em paralelo. O comando não pode alterar arquivos
# (use o modo de checagem do formatador, não o de correção).
run_check() {
    local name="$1"
    shift
    "$@" >"$log_directory/$name.log" 2>&1 &
    names+=("$name")
    pids+=("$!")
}

# Adapte ao projeto. Exemplos:
#   run_check formato bun run format:check
#   run_check lint bun run lint:check
#   run_check tipos bun run types:check
#   if [[ "$mode" == full ]]; then
#       run_check testes bun test
#   fi

if [[ "${#pids[@]}" == 0 ]]; then
    echo 'Nenhuma validação configurada em scripts/validate.sh.' >&2
    exit 1
fi

status=0

for index in "${!pids[@]}"; do
    if wait "${pids[$index]}"; then
        printf 'ok      %s\n' "${names[$index]}"
    else
        status=1
        printf 'FALHOU  %s\n' "${names[$index]}"
        tail -n 40 "$log_directory/${names[$index]}.log" | sed 's/^/        /'
    fi
done

printf 'Validação local (%s): %s segundos.\n' "$mode" "$(($(date +%s) - started_at))"

# Registra a árvore validada para o pre-push não repetir a mesma validação.
# A validação completa também vale como rápida.
if [[ "$status" == 0 && -z "$(git status --porcelain --untracked-files=no)" ]]; then
    tree="$(git rev-parse 'HEAD^{tree}')"
    echo "$tree" >"$(git rev-parse --git-dir)/validated-tree-$mode"
    [[ "$mode" == full ]] && echo "$tree" >"$(git rev-parse --git-dir)/validated-tree-quick"
fi

exit "$status"
