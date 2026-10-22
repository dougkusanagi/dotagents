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
    const setAppearance = useCallback((next: Appearance) => {
        if (next === 'system') window.localStorage.removeItem(KEY);
        else window.localStorage.setItem(KEY, next);
        apply(next);
        listeners.forEach((listener) => listener());
    }, []);

    return [appearance, setAppearance] as const;
}
