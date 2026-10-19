# dotagents

Regras globais e uma memória em markdown simples, compartilhadas entre Claude Code, Codex, OpenCode e Gemini CLI, sem inflar o contexto base.

- **Regras** ([AGENTS.md](AGENTS.md)): curtas, curadas à mão, carregadas em toda sessão.
- **Memória** (`memory/`): um arquivo por preferência ou correção que você der aos agentes. Só um índice de uma linha por memória entra no contexto (teto de 30); o conteúdo é lido sob demanda.
- **Arquivos gerados** (`build/AGENTS.md` e `build/CLAUDE.md`) juntam tudo, e os arquivos globais de cada agente viram links para eles.

## Instalação

Com `~/.agents` vazio ou inexistente:

```bash
git clone https://github.com/dougkusanagi/dotagents ~/.agents && ~/.agents/install.sh
```

Se `~/.agents` já existir (por exemplo, com `skills/`):

```bash
cd ~/.agents && git init -b main && git remote add origin https://github.com/dougkusanagi/dotagents && git pull origin main && ./install.sh
```

O `install.sh` cria `memory/` como repositório git próprio e roda o `bin/sync`, que:

1. faz backup (`.bak-<data>`) de arquivos globais existentes que não sejam links;
2. preserva blocos `<!-- nome:begin -->` … `<!-- nome:end -->` escritos por outras ferramentas (como o lerd), copiando-os para `build/external/`;
3. gera `build/AGENTS.md` e liga a ele `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md` e `~/.gemini/GEMINI.md`; gera `build/CLAUDE.md`, igual mas sem os blocos externos (o Claude Code já recebe as instruções dos servidores MCP, como o lerd), e liga `~/.claude/CLAUDE.md` a ele. Só liga agentes cujo diretório existe;
4. commita mudanças em `memory/`.

Rode `~/.agents/bin/sync` de novo sempre que editar regras ou memórias (os agentes fazem isso sozinhos ao salvar uma memória). Para atualizar as regras: `git -C ~/.agents pull && ~/.agents/bin/sync`.

## Memórias

Os agentes salvam memórias quando você corrige algo ou expressa uma preferência durável que vale para todos os projetos. Formato:

```markdown
---
description: Testes com Pest, não PHPUnit
applies_to: [php]
---

Usar Pest em projetos PHP novos e nos que já o usam.
Por quê: sintaxe mais curta e plugins de browser testing.
```

Cada arquivo vira uma linha no índice: `- [php] Testes com Pest, não PHPUnit (memory/pest.md)`. A ordem é estável (sem datas) para aproveitar o cache de prompt.

Para sincronizar entre máquinas, crie um repositório **privado** e ligue-o a `memory/`:

```bash
git -C ~/.agents/memory remote add origin git@github.com:<usuario>/agents-memory.git && git -C ~/.agents/memory push -u origin main
```

O `sync` só commita; o push é sempre seu.

## Regras pessoais

Regras que você não quer publicar vão em `~/.agents/local.md` (ignorado pelo git) e entram no arquivo gerado logo após o índice.

## Desinstalar

Remova os links e restaure os backups, se quiser:

```bash
rm ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.config/opencode/AGENTS.md ~/.gemini/GEMINI.md
```

Um bloco externo que não deve mais aparecer (ferramenta removida) sai apagando `build/external/<nome>.md` e rodando o `sync`.
