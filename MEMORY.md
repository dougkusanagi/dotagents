# Memória do projeto

Fatos operacionais duráveis que o código não mostra. Uma linha por fato, até 30 linhas. Regras ficam em `AGENTS.md` e `global.md`.

- Commits que alteram `global.md` exigem `DOTAGENTS_ALLOW_RULES=1`; o hook `pre-commit` bloqueia os demais.
