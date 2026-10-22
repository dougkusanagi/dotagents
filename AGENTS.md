# Instruções do repositório dotagents

- As regras globais compartilhadas ficam em `global.md`. Este `AGENTS.md` contém apenas instruções de manutenção deste repositório e não deve entrar nos arquivos globais gerados.
- Ao receber um pedido para inserir ou editar uma regra global, redija-a em `global.md`, na seção adequada. Use os princípios de clareza do ASD-STE100, adaptados ao português, sem exigir conformidade estrita: prefira frases curtas, verbos diretos e termos consistentes. Explicite o comportamento esperado e suas condições. Preserve a intenção, os requisitos e as exceções do pedido; use exemplos quando ajudarem a eliminar ambiguidades. Revise as regras relacionadas para evitar duplicações e contradições, sem alterar requisitos fora do escopo do pedido.
- Após alterar regras globais ou a sincronização, execute `bash tests/test.sh` e `dotagents-sync`. Não edite diretamente os arquivos globais gerados.
- Para mudanças perceptíveis ao usuário, crie um fragmento em `changelog/unreleased/` com o tipo e uma linha em português. Use Conventional Commits quando houver pedido de commit.
