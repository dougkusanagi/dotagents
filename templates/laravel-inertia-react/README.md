# Seletor de tema (Laravel + Inertia + React)

Referência para o seletor Claro / Escuro / Sistema exigido em `AGENTS.md`. Copie e adapte; não crie outra versão do zero.

- `appearance-menu-control.tsx`: o widget, com as variantes `sidebar`, `panel` e `icons`. Requer o `toggle-group` do shadcn/ui e usa Phosphor.
- `use-appearance.ts`: hook que guarda a escolha em `localStorage` (ausente = Sistema), alterna a classe `dark` no `<html>`, acompanha o tema do dispositivo e sincroniza abas.

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

Remova `class="dark"` fixo do `<html>`, se existir, e use só tokens de cor (`bg-background`, `text-foreground`…) nos componentes.
