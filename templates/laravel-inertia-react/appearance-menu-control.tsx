import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'; // shadcn/ui: `bunx shadcn add toggle-group`
import { useAppearance, type Appearance } from '@/hooks/use-appearance';
import { cn } from '@/lib/utils';
import { useRef } from 'react';
import { MonitorIcon, MoonIcon, SunIcon } from '@phosphor-icons/react'; // sem Phosphor, troque por Sun, Moon e Monitor da biblioteca de ícones do projeto

const options: { value: Appearance; label: string; icon: typeof SunIcon }[] = [
    { value: 'light', label: 'Claro', icon: SunIcon },
    { value: 'dark', label: 'Escuro', icon: MoonIcon },
    { value: 'system', label: 'Sistema', icon: MonitorIcon },
];

/**
 * Alternador de tema.
 * - `sidebar` (padrão): rodapé da barra lateral. Só a opção ativa mostra o nome, com animação de largura;
 *   com a barra recolhida (`collapsible="icon"`), os ícones se empilham.
 * - `panel`: o mesmo controle, mais alto (44px), para o painel da conta no celular.
 * - `icons`: versão minimalista, só ícones, para menus horizontais no desktop.
 */
export function AppearanceMenuControl({ variant = 'sidebar' }: { variant?: 'sidebar' | 'panel' | 'icons' }) {
    const [appearance, setAppearance] = useAppearance();
    const panel = variant === 'panel';
    const icons = variant === 'icons';
    // Origem da animação: o ponto do clique ou, pelo teclado, o centro do botão focado.
    const pointer = useRef<{ x: number; y: number } | undefined>(undefined);
    const origin = () => {
        if (pointer.current) return pointer.current;
        const rect = document.activeElement?.getBoundingClientRect();
        return rect && { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
    };

    return (
        <ToggleGroup
            type="single"
            value={appearance}
            onPointerDown={(event) => (pointer.current = { x: event.clientX, y: event.clientY })}
            onKeyDown={() => (pointer.current = undefined)}
            onValueChange={(value) => value && setAppearance(value as Appearance, origin())}
            aria-label="Tema"
            className={cn(
                'bg-muted gap-0.5 rounded-xl p-1',
                icons ? 'w-fit' : 'w-full',
                variant === 'sidebar' &&
                    'group-data-[collapsible=icon]:flex-col group-data-[collapsible=icon]:rounded-lg group-data-[collapsible=icon]:p-0.5',
            )}
        >
            {options.map((option) => {
                const active = option.value === appearance;

                return (
                    <ToggleGroupItem
                        key={option.value}
                        value={option.value}
                        aria-label={option.label}
                        title={option.label}
                        className={cn(
                            'text-muted-foreground hover:text-foreground min-w-0 rounded-lg px-2 text-xs font-medium transition-[flex-grow,background-color,color] duration-200 hover:bg-transparent',
                            'data-[state=on]:bg-background data-[state=on]:text-foreground data-[state=on]:ring-border data-[state=on]:shadow-sm data-[state=on]:ring-1',
                            icons
                                ? 'size-8 flex-none p-0'
                                : 'h-8 flex-1 group-data-[collapsible=icon]:size-7 group-data-[collapsible=icon]:flex-none group-data-[collapsible=icon]:p-0 data-[state=on]:flex-[2.4]',
                            panel && 'h-11 text-sm',
                        )}
                    >
                        {/* `text-brand`: troque pelo token de destaque do projeto (ex.: `text-primary`). */}
                        <option.icon aria-hidden className={cn('shrink-0', panel ? 'size-5' : 'size-4', active && 'text-brand')} />
                        <span className={cn('truncate', !icons && active ? 'group-data-[collapsible=icon]:sr-only' : 'sr-only')}>{option.label}</span>
                    </ToggleGroupItem>
                );
            })}
        </ToggleGroup>
    );
}
