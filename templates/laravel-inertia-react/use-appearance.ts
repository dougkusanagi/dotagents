import { useCallback, useSyncExternalStore } from 'react';

export type Appearance = 'light' | 'dark' | 'system';

// Mantenha chave e cores em sincronia com o script de resources/views/app.blade.php (veja README.md).
const KEY = 'appearance';
const THEME_COLOR = { light: '#faf9f6', dark: '#0b0b0e' } as const;
const query = () => window.matchMedia('(prefers-color-scheme: dark)');

const listeners = new Set<() => void>();
const read = (): Appearance => {
    if (typeof window === 'undefined') return 'system';
    const stored = window.localStorage.getItem(KEY);

    return stored === 'light' || stored === 'dark' ? stored : 'system';
};

function apply(appearance: Appearance) {
    const dark = appearance === 'dark' || (appearance === 'system' && query().matches);
    document.documentElement.classList.toggle('dark', dark);
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', THEME_COLOR[dark ? 'dark' : 'light']);
}

// Revela o novo tema num círculo a partir de `origin`; sem a API ou com movimento reduzido, troca na hora.
function applyWithReveal(appearance: Appearance, origin?: { x: number; y: number }) {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!origin || reduced || !document.startViewTransition) {
        apply(appearance);
        return;
    }
    const { x, y } = origin;
    const radius = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
    document.startViewTransition(() => apply(appearance)).ready.then(() => {
        document.documentElement.animate(
            { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${radius}px at ${x}px ${y}px)`] },
            { duration: 450, easing: 'ease-out', pseudoElement: '::view-transition-new(root)' },
        );
    });
}

const subscribe = (listener: () => void) => {
    listeners.add(listener);
    const media = query();
    // Com "Automático", acompanha o sistema; em outras abas, acompanha a escolha salva.
    const onSystemChange = () => {
        apply(read());
        listener();
    };
    const onStorage = (event: StorageEvent) => {
        if (event.key !== KEY) return;
        apply(read());
        listener();
    };
    media.addEventListener('change', onSystemChange);
    window.addEventListener('storage', onStorage);

    return () => {
        listeners.delete(listener);
        media.removeEventListener('change', onSystemChange);
        window.removeEventListener('storage', onStorage);
    };
};

/** Aparência do app (claro, escuro ou automático), salva neste aparelho e aplicada na classe `dark` do <html>. */
export function useAppearance() {
    const appearance = useSyncExternalStore(subscribe, read, () => 'system' as const);
    const setAppearance = useCallback((next: Appearance, origin?: { x: number; y: number }) => {
        if (next === 'system') window.localStorage.removeItem(KEY);
        else window.localStorage.setItem(KEY, next);
        applyWithReveal(next, origin);
        listeners.forEach((listener) => listener());
    }, []);

    return [appearance, setAppearance] as const;
}
