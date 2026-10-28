# dotagents

Regras globais e memórias em Markdown compartilhadas entre Claude Code, Codex, OpenCode e Gemini CLI. Só um índice estável entra no contexto; cada memória é lida sob demanda.

## Instalação e atualização

Clone em qualquer pasta, fora de `~/.agents`:

```bash
git clone https://github.com/dougkusanagi/dotagents ~/dev/dotagents
~/dev/dotagents/install.sh
```

Requer Bash, Git, ferramentas GNU (`readlink -f`, `mktemp`) e `flock`. O instalador cria o repositório git das memórias e `~/.local/bin/dotagents-sync`, um link para `bin/sync`, e ativa os hooks de `hooks/`. Adicione `~/.local/bin` ao PATH se avisado.

Para atualizar: `git -C ~/dev/dotagents pull --ff-only && dotagents-sync`.

A versão do projeto fica em `VERSION` e muda a cada entrega. Mudanças relevantes são registradas em `changelog/unreleased/` e consolidadas em `changelog/X.Y.Z.md` na nova versão. Este projeto não cria tags de versão.

## Testes

```bash
bash tests/test.sh
```

Requer Python 3 apenas para os testes. Os testes de integração usam um HOME temporário e não alteram a instalação ativa.

## Layout

- Repositório: regras globais em `global.md`, instruções de manutenção em `AGENTS.md`, scripts e documentação; nenhum dado pessoal.
- Memórias: `${DOTAGENTS_DATA}/memory`, padrão `~/.local/share/dotagents/memory`.
- Regras pessoais: `${DOTAGENTS_CONFIG}/local.md`, padrão `~/.config/dotagents/local.md`.
- Estado: `${DOTAGENTS_STATE}`, padrão `~/.local/state/dotagents`, com `AGENTS.md`, `CLAUDE.md` e `external/`.
- Skills de outras ferramentas: `~/.agents/skills`, nunca gerenciado pelo dotagents.

As variáveis `DOTAGENTS_*` indicam diretórios do aplicativo. Quando vazias ou ausentes, usam respectivamente `XDG_DATA_HOME`, `XDG_CONFIG_HOME` e `XDG_STATE_HOME`, com `/dotagents`. XDG vazio ou relativo usa o padrão em HOME; DOTAGENTS relativo é erro. Use os mesmos valores na instalação e em todas as sincronizações, exportando-os no ambiente se personalizados.

## Sincronização

Edite `global.md` para alterar as regras globais compartilhadas; o `AGENTS.md` deste repositório orienta sua manutenção e não é sincronizado. O hook `pre-commit` recusa commits que alteram `global.md` sem `DOTAGENTS_ALLOW_RULES=1`, para que agentes não mudem regras sem pedido. Os hooks `post-commit` e `post-merge` rodam o sync após cada commit e merge. Os arquivos gerados continuam com os nomes `AGENTS.md` e `CLAUDE.md`.

Rode `dotagents-sync` após editar regras, memórias ou `local.md`. Ele preserva blocos `<!-- nome:begin -->` … `<!-- nome:end -->` em `external/nome.md`, inclusive quando outra ferramenta substitui um link por arquivo comum. Arquivos comuns são preservados em backups únicos `.bak-<data>-XXXX` antes de substituir por links.

Codex (`~/.codex/AGENTS.md`), OpenCode (`${XDG_CONFIG_HOME:-~/.config}/opencode/AGENTS.md`) e Gemini (`~/.gemini/GEMINI.md`) apontam para o estado `AGENTS.md`. Claude (`~/.claude/CLAUDE.md`) aponta para `CLAUDE.md`, sem blocos externos, pois já recebe o lerd por MCP. Só são ligados agentes cujo diretório existe.

A instalação e cada sync descobrem também perfis em `~/.codex_*` e `~/.codex-*` que contenham `config.toml` ou `auth.json`, como `~/.codex_mkt` e `~/.codex_douglas`. Arquivos de instruções existentes são preservados em backup; credenciais e configurações não são alteradas.

Quando `CODEX_HOME` está definido com um caminho absoluto, o sync também configura o `AGENTS.md` desse perfil, inclusive fora desses nomes: `CODEX_HOME="/outro/perfil" dotagents-sync`. Abra uma nova sessão do agente após atualizar as regras.

O índice usa caminhos absolutos, ordem `LC_ALL=C sort` e aviso acima de `INDEX_CAP` (padrão 30), sem truncar memórias. Os arquivos gerados informam o caminho efetivo das memórias. Execuções simultâneas são serializadas por lock.

## Memórias e regras pessoais

Crie um `.md` por memória:

```markdown
---
description: Testes com Pest
applies_to: [php]
---

Prefira Pest nos projetos que já o utilizam.
```

`description` ocupa uma linha; `applies_to` é opcional. O parser aceita campos simples, não YAML completo. `local.md` entra após o índice.

O sync faz commit local automático das alterações das memórias; nunca push. Configure a identidade Git para permitir commits. Um remote privado é opcional:

```bash
git -C ~/.local/share/dotagents/memory remote add origin git@github.com:usuario/agents-memory.git
```

## Migração do layout antigo

Primeiro rode os testes (veja “Testes”). Antes de aplicar na instalação ativa, revise `git status`, inventarie inclusive arquivos ignorados em `~/.agents`, escolha um destino inexistente e registre os links atuais para recuperação. Preserve backups existentes dos agentes.

Com estes scripts já presentes no clone antigo:

```bash
~/.agents/bin/migrate "$HOME/dev/dotagents"
```

O migrador recusa destinos existentes e arquivos desconhecidos. Preserva `.git` do clone e das memórias, remotes, alterações locais e `skills/` no mesmo lugar. Copia o estado antigo antes de mover o código, migra memórias e `local.md`, instala o comando e refaz links. Só apaga `build/` antigo após sucesso. Não cria remote de memórias nem faz push.

Se houver interrupção, não repita às cegas: confira origem e destinos. O código estará na origem ou no destino, memórias/configuração nos respectivos caminhos e o `build/` antigo permanece se a instalação falhar. Corrija a causa e rode `<REPO>/install.sh`; para desfazer, restaure os diretórios e links inventariados, sem sobrescrever dados novos.

## Remoção

Remova apenas links que apontem para dotagents e restaure os backups desejados. Memórias, configuração e estado são preservados até remoção explícita. Para retirar um bloco externo, remova também suas ocorrências nos arquivos globais/gerados antes de apagar `external/<nome>.md` e sincronizar, evitando sua recaptura.
