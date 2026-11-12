# Hook de validação local

Bloqueia o push quando as validações do projeto falham. Como não existe PR sem push, cobre também a abertura de PR. Não cobre o merge feito no GitHub.

## Instalação num projeto

1. Copie `pre-push` para `.githooks/pre-push` e `validate.sh` para `scripts/validate.sh`. Mantenha os dois executáveis (`chmod +x`).
2. Em `scripts/validate.sh`, troque os exemplos pelas validações do projeto. Use só comandos que não alteram arquivos.
3. Em `.githooks/pre-push`, ajuste `full_branches` se o branch principal ou o de integração tiver outro nome.
4. Ative com `git config core.hooksPath .githooks` e inclua esse comando no script de instalação do projeto, para clones novos.
5. Descreva o hook no README do projeto.

## Comportamento

- Push para os branches de `full_branches` ou de tags: roda `scripts/validate.sh --full`. Demais branches: `--quick`.
- Se a validação completa leva até ~3 minutos, rode tudo nos dois modos e ignore a diferença.
- Com alterações sem commit em arquivos rastreados, o push é bloqueado: a validação testaria um código diferente do enviado.
- O commit enviado precisa ser o que está em checkout.
- Uma árvore já aprovada não é validada de novo.
- Apagar um branch remoto não roda a validação.

Se o projeto já usa outro mecanismo de hooks (husky, lefthook, pre-commit…), aplique as mesmas regras nele em vez de copiar estes arquivos.
