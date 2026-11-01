# Memória do projeto

Fatos operacionais duráveis que o código não mostra. Uma linha por fato, até 30 linhas. Regras ficam em `AGENTS.md` e `global.md`.

- No `global.md`, escreva `<dotagents>` para citar o caminho deste repositório; o sync o troca pelo caminho real, e `~/.local/share/dotagents/memory` pelo diretório efetivo das memórias.
- Windows (Git Bash): sem `flock` e, sem Modo Desenvolvedor/admin, `ln -s` falha; o sync usa lock por diretório e copia os arquivos (reconhecidos pelo cabeçalho "Gerado por"). Os `.cmd` usam o Git Bash, nunca o `bash.exe` do WSL. `tests/test.sh` roda lá com `uv run python`.
