# Seletor de tema (Laravel + Inertia + React)

Referência para o seletor Claro / Escuro / Sistema exigido nas regras globais (`global.md`). Copie e adapte; não crie outra versão do zero.

- `appearance-menu-control.tsx`: o widget, com as variantes `sidebar`, `panel` e `icons`. Requer o `toggle-group` do shadcn/ui e usa Phosphor.
- `use-appearance.ts`: hook que revela o novo tema num círculo a partir do botão clicado, guarda a escolha em `localStorage` (ausente = Sistema), alterna a classe `dark` no `<html>`, acompanha o tema do dispositivo e sincroniza abas.

Para evitar o flash do tema errado, aplique a escolha antes da primeira pintura em `resources/views/app.blade.php`, dentro do `<head>`, com a mesma chave e as mesmas cores do hook:

```html
<meta name="theme-color" content="#0b0b0e">
<script>
    (function () {
        var stored = null;
        try { stored = localStorage.getItem('appearance'); } catch (e) {}
        var dark = stored === 'dark' || (stored !== 'light' && matchMedia('(prefers-color-scheme: dark)').matches);
        document.documentElement.classList.toggle('dark', dark);
        document.querySelector('meta[name="theme-color"]').setAttribute('content', dark ? '#0b0b0e' : '#faf9f6');
    })();
</script>
```

Para a animação de troca de tema (círculo a partir do botão), desative a transição padrão no `resources/css/app.css`:

```css
::view-transition-old(root),
::view-transition-new(root) {
    animation: none;
    mix-blend-mode: normal;
}
```

Sem suporte à View Transitions API ou com `prefers-reduced-motion`, o tema troca sem animação.

Remova `class="dark"` fixo do `<html>`, se existir, e use só tokens de cor (`bg-background`, `text-foreground`…) nos componentes.

Posicione o widget conforme o layout:

- Barra lateral: `variant="sidebar"` no rodapé, acima do usuário.
- Celular: `variant="panel"` no painel da conta, sem aumentar a navegação inferior.
- Só menu horizontal: `variant="icons"` no cabeçalho desktop; no celular, use o painel da conta.
