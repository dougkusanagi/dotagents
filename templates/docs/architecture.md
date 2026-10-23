# Arquitetura

Visão geral em poucas frases: o que o sistema faz e seus limites.

```mermaid
flowchart LR
  usuario[Usuário] --> app[Aplicação]
  app --> db[(Banco de dados)]
```

## Componentes

- Aplicação: responsabilidade principal.
- Banco de dados: o que guarda.

## Decisões

Veja `docs/adr/`.
