# FiscalUI Framework

## Documento 003 — Theme Engine

**Versão 1.0**

Sistema completo de temas do FiscalUI. Controla toda a aparência visual através de Design Tokens. Permite múltiplos temas sem alterar um único componente.

---

# Índice

1. Introdução
2. O que é o Theme Engine
3. Filosofia
4. Arquitetura
5. Mecanismo de Troca
6. Temas Oficiais
7. Tema Dark (Padrão)
8. Tema Light
9. Tema High Contrast
10. Tema Liquid Glass
11. Tema Corporate
12. Criação de Temas
13. Registro de Temas
14. Tokens por Tema
15. Hierarquia de Temas
16. Persistência
17. Componentes e Temas
18. Temas Responsivos
19. Acessibilidade em Temas
20. Performance
21. Transições entre Temas
22. Temas por Empresa
23. Temas por Usuário
24. Tema na Tela de Login
25. Design Tokens vs Temas
26. Sobrescrita vs Criação
27. Testes de Tema
28. Debugging
29. Boas Práticas
30. Ferramentas
31. Compatibilidade
32. Roadmap

---

# 1. Introdução

## 1.1 Propósito

O Theme Engine é o coração da identidade visual do FiscalUI. Ele permite que a aparência completa do sistema seja alterada instantaneamente — sem recarregar a página, sem modificar componentes, sem tocar em HTML.

Um único atributo `data-theme` no elemento `<html>` é suficiente para transformar a interface de Dark para Light, de Light para High Contrast, ou para qualquer tema personalizado.

## 1.2 O Problema

Em sistemas ERP tradicionais, cada cliente pode exigir cores, logos e estilos próprios. Sem um sistema de temas, isso resulta em:

- CSS duplicado para cada cliente
- Componentes modificados para cada personalização
- Manutenção exponencial com o número de clientes
- Impossibilidade de o usuário escolher seu tema preferido

## 1.3 A Solução

O Theme Engine resolve isso com uma abordagem baseada exclusivamente em tokens:

```
Tema → Altera tokens → Componentes consomem tokens → Interface muda
```

O componente nunca sabe qual tema está ativo. Ele apenas usa `var(--color-primary)`. O tema define o valor de `--color-primary`. Trocar o tema = trocar o valor = trocar a cor do componente.

## 1.4 Como Funciona em Uma Linha

```js
document.documentElement.setAttribute('data-theme', 'light');
```

Isso é suficiente para alterar toda a aparência do sistema.

---

# 2. O que é o Theme Engine

## 2.1 Definição

O Theme Engine é o subsistema do FiscalUI responsável por:

1. **Definir** os tokens visuais para cada tema
2. **Aplicar** o tema ativo via `data-theme`
3. **Persistir** a preferência do usuário
4. **Notificar** componentes sobre mudanças de tema
5. **Validar** contraste e acessibilidade dos temas
6. **Gerenciar** temas registrados

## 2.2 Componentes do Theme Engine

```
┌─────────────────────────────────────────┐
│            THEME ENGINE                  │
├─────────────────────────────────────────┤
│                                         │
│  tokens.css     → Tokens padrão (Dark)  │
│  themes.css     → Temas adicionais       │
│  ThemeEngine.js → Lógica de troca       │
│  localStorage   → Preferência salva     │
│  data-theme     → Seletor no HTML       │
│                                         │
└─────────────────────────────────────────┘
```

## 2.3 O Theme Engine NÃO Faz

- Não modifica componentes
- Não gera CSS dinamicamente
- Não depende de JavaScript para funcionar (o CSS já está no HTML)
- Não recarrega a página
- Não duplica estilos

---

# 3. Filosofia

## 3.1 Princípios

### 3.1.1 O Componente Nunca Muda

Este é o princípio mais importante do Theme Engine.

```
Button → mesmo HTML → mesmo CSS → funciona em qualquer tema
```

O desenvolvedor cria o componente uma vez. O componente usa tokens. O tema define os tokens. Zero alteração no componente quando um novo tema é criado.

### 3.1.2 Temas Fornecem Apenas Valores

Temas contêm exclusivamente valores de tokens. Nunca comportamento, nunca estilos de componente, nunca HTML.

```css
/* ✅ Certo — Tema só tem tokens */
[data-theme="light"] {
    --surface-page: #f8fafc;
    --text-primary: #0f172a;
}

/* ❌ Errado — Tema não deve ter estilos de componente */
[data-theme="light"] .ui-btn {
    box-shadow: none; /* Isso pertence ao componente */
}
```

### 3.1.3 Troca Instantânea

A troca de tema é síncrona e instantânea (sub 1ms). Apenas uma atribuição de atributo DOM. O CSS já está carregado — apenas os valores mudam.

### 3.1.4 Tema Escuro é o Padrão

O tema escuro (Dark) é o tema padrão do FiscalUI. Ele está definido em `:root` no `tokens.css`. Todos os outros temas sobrescrevem esses valores.

### 3.1.5 Qualquer Tema Funciona em Qualquer Componente

Se um novo tema for criado e não sobrescrever um token específico, o componente simplesmente usará o valor do tema padrão (Dark). Isso significa que criar um tema parcial é seguro — componentes não quebram.

---

# 4. Arquitetura

## 4.1 Visão Geral

```
┌──────────────────────────────────────────────────────────┐
│                    THEME ENGINE                           │
│                                                          │
│  tokens.css                                               │
│  :root { --color-primary: #14b8a6; }     ← Tema padrão  │
│                                                          │
│  themes.css                                               │
│  [data-theme="light"]        { ... }    ← Tema Light    │
│  [data-theme="high-contrast"]{ ... }    ← Tema HC       │
│  [data-theme="glass"]        { ... }    ← Liquid Glass  │
│                                                          │
│  ThemeEngine.js                                           │
│  setTheme(name)                       ← Troca tema      │
│  getTheme()                           ← Tema atual      │
│  getAvailableThemes()                 ← Lista temas     │
│  register(name, config)               ← Novo tema       │
│                                                          │
│  HTML                                                     │
│  <html data-theme="light">            ← Tema ativo      │
│                                                          │
│  localStorage                                              │
│  fiscalui_theme: "light"              ← Preferência     │
└──────────────────────────────────────────────────────────┘
```

## 4.2 Fluxo de Carregamento

```
1. HTML carrega tokens.css
   → :root define tokens padrão (Dark)
   → Todos os componentes funcionam imediatamente

2. HTML carrega themes.css
   → Regras adicionais para Light, HC, Glass
   → Nenhum seletor ativo ainda (data-theme não definido)

3. ThemeEngine.js é carregado
   → Lê localStorage → fiscalui_theme
   → Se existir: aplica tema salvo
   → Se não existir: mantém Dark (padrão)

4. Aplicação inicia
   → Tema está definido e visível
```

## 4.3 Diagrama de Dependências

```
tokens.css (base)
    │
    └── themes.css (sobrescreve tokens)
            │
            └── ThemeEngine.js (aplica data-theme)
                    │
                    ├── localStorage (persiste)
                    ├── EventBus (notifica)
                    └── StateManager (sincroniza estado)
```

## 4.4 Arquivos do Sistema de Temas

| Arquivo | Função | Ordem de Carga |
|---------|--------|----------------|
| `css/tokens.css` | Tokens padrão (Dark) | 1º |
| `css/themes.css` | Temas adicionais | 2º |
| `js/theme/ThemeEngine.js` | Lógica de gerenciamento | 3º |

---

# 5. Mecanismo de Troca

## 5.1 Troca via Atributo HTML

O mecanismo mais simples e direto:

```js
// Trocar para tema Light
document.documentElement.setAttribute('data-theme', 'light');

// Trocar para High Contrast
document.documentElement.setAttribute('data-theme', 'high-contrast');

// Voltar para Dark (padrão)
document.documentElement.setAttribute('data-theme', 'dark');
// OU
document.documentElement.removeAttribute('data-theme');
```

## 5.2 Troca via ThemeEngine

```js
// FiscalUI.ThemeEngine API
FiscalUI.theme.setTheme('light');

// Com persistência automática
FiscalUI.theme.setTheme('light', { persist: true });

// Alternar entre temas (toggle)
FiscalUI.theme.toggleTheme();
// Dark → Light → High Contrast → Dark
```

## 5.3 Alternador de Tema (UI)

```html
<div class="theme-switcher" role="radiogroup" aria-label="Tema">
    <button class="theme-option" data-theme="dark" aria-label="Tema escuro">
        <svg class="icon icon-md"><use href="#icon-moon"/></svg>
    </button>
    <button class="theme-option" data-theme="light" aria-label="Tema claro">
        <svg class="icon icon-md"><use href="#icon-sun"/></svg>
    </button>
    <button class="theme-option" data-theme="high-contrast" aria-label="Alto contraste">
        <svg class="icon icon-md"><use href="#icon-eye"/></svg>
    </button>
</div>
```

```js
document.querySelectorAll('.theme-option').forEach(btn => {
    btn.addEventListener('click', () => {
        FiscalUI.theme.setTheme(btn.dataset.theme);
    });
});
```

## 5.4 Ciclo de Troca

```
Usuário clica em "Light"
    │
    ▼
ThemeEngine.setTheme('light')
    │
    ├── Evento: theme:before-change
    │       └── Componentes podem se preparar
    │
    ├── document.documentElement.setAttribute('data-theme', 'light')
    │       └── CSS aplica novos valores instantaneamente
    │
    ├── localStorage.setItem('fiscalui_theme', 'light')
    │
    ├── StateManager.set('theme', 'light')
    │
    └── Evento: theme:change
            └── Componentes reagem (se necessário)
```

## 5.5 Troca via Teclado

Atalho padrão: `Ctrl+Shift+T` — alterna entre temas.

```js
FiscalUI.shortcuts.register('ctrl+shift+t', () => {
    FiscalUI.theme.toggleTheme();
});
```

---

# 6. Temas Oficiais

## 6.1 Catálogo de Temas

| # | Tema | data-theme | Ambiente ideal |
|---|------|-----------|----------------|
| 1 | Dark | `dark` | Uso contínuo, ambiente com pouca luz |
| 2 | Light | `light` | Escritórios, ambientes claros |
| 3 | High Contrast | `high-contrast` | Acessibilidade, baixa visão |
| 4 | Liquid Glass | `glass` | Demonstrações, modo premium |
| 5 | Corporate | `corporate` | Clientes com identidade visual própria |

## 6.2 Temas por Versão

| Versão | Temas Disponíveis |
|--------|------------------|
| 1.0 | Dark, Light, High Contrast |
| 1.1 | + Liquid Glass |
| 1.2 | + Corporate (customizável) |

## 6.3 Registro de Temas no Framework

```js
// Temas oficiais (já registrados)
FiscalUI.theme.register('dark', {
    name: 'Escuro',
    icon: 'icon-moon',
    description: 'Tema escuro padrão'
});

FiscalUI.theme.register('light', {
    name: 'Claro',
    icon: 'icon-sun',
    description: 'Tema claro para ambientes iluminados'
});

FiscalUI.theme.register('high-contrast', {
    name: 'Alto Contraste',
    icon: 'icon-eye',
    description: 'Tema de acessibilidade com contraste máximo'
});

// Obter lista de temas
const themes = FiscalUI.theme.getAvailableThemes();
// [
//   { id: 'dark', name: 'Escuro', icon: 'icon-moon', active: true },
//   { id: 'light', name: 'Claro', icon: 'icon-sun', active: false },
//   { id: 'high-contrast', name: 'Alto Contraste', icon: 'icon-eye', active: false }
// ]
```

---

# 7. Tema Dark (Padrão)

## 7.1 Visão Geral

O tema Dark é o tema padrão do FiscalUI. É o tema definido em `:root` no arquivo `css/tokens.css`. Todos os outros temas são variações deste.

## 7.2 Filosofia do Tema Escuro

- **Fundo escuro** (`#0f172a` — slate-900) para reduzir fadiga visual em uso prolongado
- **Elementos em vidro** (glassmorphism) para criar profundidade sem usar cores vibrantes
- **Destaque em teal** (`#14b8a6`) para ações primárias
- **Gradiente sutil** no fundo para evitar tela chapada
- **Bordas translúcidas** (`rgba(255,255,255,0.12)`) em vez de bordas sólidas

## 7.3 Tokens do Tema Dark

```css
:root {
    /* === CORES DA MARCA === */
    --color-primary: #14b8a6;
    --color-primary-hover: #0d9488;
    --color-primary-active: #0f766e;
    --color-primary-light: #ccfbf1;
    --color-primary-dark: #134e4a;

    --color-secondary: #6366f1;
    --color-secondary-hover: #4f46e5;
    --color-secondary-active: #4338ca;

    --color-accent: #f59e0b;
    --color-accent-hover: #d97706;

    /* === CORES SEMÂNTICAS === */
    --color-success: #10b981;
    --color-success-hover: #059669;
    --color-success-bg: rgba(16, 185, 129, 0.15);
    --color-success-border: rgba(16, 185, 129, 0.4);

    --color-warning: #f59e0b;
    --color-warning-hover: #d97706;
    --color-warning-bg: rgba(245, 158, 11, 0.15);
    --color-warning-border: rgba(245, 158, 11, 0.4);

    --color-danger: #ef4444;
    --color-danger-hover: #dc2626;
    --color-danger-bg: rgba(239, 68, 68, 0.15);
    --color-danger-border: rgba(239, 68, 68, 0.4);

    --color-info: #3b82f6;
    --color-info-hover: #2563eb;
    --color-info-bg: rgba(59, 130, 246, 0.15);
    --color-info-border: rgba(59, 130, 246, 0.4);

    /* === SUPERFÍCIES === */
    --surface-page: #0f172a;
    --surface-card: #1e293b;
    --surface-modal: #1e293b;
    --surface-sidebar: #1e293b;
    --surface-input: #334155;
    --surface-tooltip: #475569;
    --surface-toast: #334155;
    --surface-glass: rgba(255, 255, 255, 0.06);

    --surface-hover: rgba(255, 255, 255, 0.08);
    --surface-active: rgba(255, 255, 255, 0.12);
    --surface-selected: rgba(20, 184, 166, 0.15);
    --surface-disabled: rgba(255, 255, 255, 0.04);

    /* === TEXTO === */
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-tertiary: #94a3b8;
    --text-disabled: #64748b;
    --text-inverse: #0f172a;
    --text-link: #14b8a6;
    --text-link-hover: #0d9488;
    --text-placeholder: #64748b;

    /* === BORDAS === */
    --color-border: rgba(255, 255, 255, 0.12);
    --color-border-hover: rgba(255, 255, 255, 0.2);
    --color-border-focus: #14b8a6;
    --color-border-disabled: rgba(255, 255, 255, 0.06);
    --color-border-error: #ef4444;
    --color-border-success: #10b981;

    /* === SOMBRAS === */
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.35);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.45);
    --shadow-xl: 0 12px 40px rgba(0, 0, 0, 0.5);
    --shadow-2xl: 0 24px 64px rgba(0, 0, 0, 0.6);
    --shadow-glass: 0 4px 24px rgba(20, 184, 166, 0.08);
    --shadow-glow: 0 0 30px rgba(20, 184, 166, 0.12);

    /* === VIDRO === */
    --glass-bg: rgba(255, 255, 255, 0.06);
    --glass-blur: blur(12px);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    --glass-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.1);
    --glass-opacity: 0.85;

    /* === GRADIENTE DE FUNDO === */
    --bg-gradient: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #0f172a 100%
    );
}
```

## 7.4 Aparência Característica

- Fundo gradiente escuro com leve variação de slate
- Cards e painéis com efeito glass (translúcidos com backdrop-filter)
- Botões primários em teal com hover mais escuro
- Texto principal em branco suave (`#f8fafc`)
- Bordas sutis e translúcidas
- Sombras profundas e difusas

---

# 8. Tema Light

## 8.1 Visão Geral

O tema Light é a versão clara do FiscalUI. Projetado para ambientes com muita luz natural ou iluminação intensa, onde o tema escuro reduz o contraste percebido.

## 8.2 Diferenças do Dark

```
Dark                           → Light
────                           ─────
Fundo: #0f172a (slate-900)     → Fundo: #f8fafc (slate-50)
Card: #1e293b (slate-800)      → Card: #ffffff (white)
Texto: #f8fafc (slate-50)      → Texto: #0f172a (slate-900)
Borda: rgba(255,255,255,0.12)  → Borda: rgba(0,0,0,0.12)
Sombra: preto 35%              → Sombra: preto 8%
Vidro: rgba(255,255,255,0.06)  → Vidro: rgba(255,255,255,0.7)
```

## 8.3 Tokens do Tema Light

```css
[data-theme="light"] {
    /* === CORES DA MARCA === */
    --color-primary: #0d9488;
    --color-primary-hover: #0f766e;
    --color-primary-active: #115e59;
    --color-primary-light: #ccfbf1;
    --color-primary-dark: #134e4a;

    --color-secondary: #4f46e5;
    --color-secondary-hover: #4338ca;

    --color-accent: #d97706;
    --color-accent-hover: #b45309;

    /* === CORES SEMÂNTICAS === */
    --color-success: #059669;
    --color-success-hover: #047857;
    --color-success-bg: #d1fae5;
    --color-success-border: #6ee7b7;

    --color-warning: #d97706;
    --color-warning-hover: #b45309;
    --color-warning-bg: #fef3c7;
    --color-warning-border: #fcd34d;

    --color-danger: #dc2626;
    --color-danger-hover: #b91c1c;
    --color-danger-bg: #fee2e2;
    --color-danger-border: #fca5a5;

    --color-info: #2563eb;
    --color-info-hover: #1d4ed8;
    --color-info-bg: #dbeafe;
    --color-info-border: #93c5fd;

    /* === SUPERFÍCIES === */
    --surface-page: #f8fafc;
    --surface-card: #ffffff;
    --surface-modal: #ffffff;
    --surface-sidebar: #ffffff;
    --surface-input: #ffffff;
    --surface-tooltip: #1e293b;
    --surface-toast: #ffffff;
    --surface-glass: rgba(255, 255, 255, 0.7);

    --surface-hover: rgba(0, 0, 0, 0.04);
    --surface-active: rgba(0, 0, 0, 0.08);
    --surface-selected: rgba(13, 148, 136, 0.12);
    --surface-disabled: rgba(0, 0, 0, 0.02);

    /* === TEXTO === */
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-tertiary: #94a3b8;
    --text-disabled: #cbd5e1;
    --text-inverse: #ffffff;
    --text-link: #0d9488;
    --text-link-hover: #0f766e;
    --text-placeholder: #94a3b8;

    /* === BORDAS === */
    --color-border: rgba(0, 0, 0, 0.1);
    --color-border-hover: rgba(0, 0, 0, 0.16);
    --color-border-focus: #0d9488;
    --color-border-disabled: rgba(0, 0, 0, 0.06);
    --color-border-error: #dc2626;
    --color-border-success: #059669;

    /* === SOMBRAS === */
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 12px 40px rgba(0, 0, 0, 0.12);
    --shadow-2xl: 0 24px 64px rgba(0, 0, 0, 0.15);
    --shadow-glass: 0 4px 24px rgba(13, 148, 136, 0.08);
    --shadow-glow: 0 0 30px rgba(13, 148, 136, 0.1);

    /* === VIDRO === */
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-blur: blur(12px);
    --glass-border: rgba(255, 255, 255, 0.2);
    --glass-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
    --glass-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.9);

    /* === GRADIENTE === */
    --bg-gradient: linear-gradient(
        135deg,
        #f8fafc 0%,
        #f1f5f9 50%,
        #e2e8f0 100%
    );
}
```

## 8.4 Aparência Característica

- Fundo claro com gradiente sutil em tons de cinza
- Cards brancos com sombra suave
- Botões primários em teal escuro (`#0d9488`) para contraste
- Texto principal em slate-900 (quase preto)
- Bordas sutis em cinza claro

---

# 9. Tema High Contrast

## 9.1 Visão Geral

O tema High Contrast foi projetado para usuários com baixa visão ou para ambientes onde o contraste máximo é necessário (projetores, telas externas, monitores com baixa qualidade). Ele atende aos requisitos WCAG 2.2 AAA para contraste.

## 9.2 Diretrizes de Acessibilidade

```
Texto normal:     contraste ≥ 7:1 (WCAG AAA)
Texto grande:     contraste ≥ 4.5:1 (WCAG AAA)
Componentes UI:   contraste ≥ 3:1 (WCAG AA)
Foco:             outline 3px sólido
Bordas:           sempre visíveis (nunca translúcidas)
```

## 9.3 Tokens do Tema High Contrast

```css
[data-theme="high-contrast"] {
    /* === CORES === */
    --color-primary: #2dd4bf;
    --color-primary-hover: #5eead4;
    --color-primary-active: #99f6e4;
    --color-primary-light: #ccfbf1;
    --color-primary-dark: #134e4a;

    --color-secondary: #a78bfa;
    --color-secondary-hover: #c4b5fd;

    --color-accent: #fbbf24;
    --color-accent-hover: #fcd34d;

    --color-success: #34d399;
    --color-success-hover: #6ee7b7;
    --color-success-bg: #065f46;
    --color-success-border: #34d399;

    --color-warning: #fbbf24;
    --color-warning-hover: #fcd34d;
    --color-warning-bg: #78350f;
    --color-warning-border: #fbbf24;

    --color-danger: #f87171;
    --color-danger-hover: #fca5a5;
    --color-danger-bg: #7f1d1d;
    --color-danger-border: #f87171;

    --color-info: #60a5fa;
    --color-info-hover: #93c5fd;
    --color-info-bg: #1e3a5f;
    --color-info-border: #60a5fa;

    /* === SUPERFÍCIES === */
    --surface-page: #000000;
    --surface-card: #0a0a0a;
    --surface-modal: #0a0a0a;
    --surface-sidebar: #0a0a0a;
    --surface-input: #1a1a1a;
    --surface-tooltip: #1a1a1a;
    --surface-toast: #1a1a1a;
    --surface-glass: rgba(255, 255, 255, 0.1);

    --surface-hover: #1a1a1a;
    --surface-active: #2a2a2a;
    --surface-selected: rgba(45, 212, 191, 0.2);
    --surface-disabled: #0a0a0a;

    /* === TEXTO === */
    --text-primary: #ffffff;
    --text-secondary: #e0e0e0;
    --text-tertiary: #cccccc;
    --text-disabled: #888888;
    --text-inverse: #000000;
    --text-link: #2dd4bf;
    --text-link-hover: #5eead4;
    --text-placeholder: #888888;

    /* === BORDAS === */
    --border-thin: 2px;
    --border-medium: 3px;

    --color-border: #ffffff;
    --color-border-hover: #cccccc;
    --color-border-focus: #2dd4bf;
    --color-border-disabled: #555555;
    --color-border-error: #f87171;
    --color-border-success: #34d399;

    /* === SOMBRAS === */
    --shadow-xs: 0 1px 2px rgba(255, 255, 255, 0.2);
    --shadow-sm: 0 2px 4px rgba(255, 255, 255, 0.25);
    --shadow-md: 0 4px 8px rgba(255, 255, 255, 0.3);
    --shadow-lg: 0 8px 16px rgba(255, 255, 255, 0.35);
    --shadow-xl: 0 12px 24px rgba(255, 255, 255, 0.4);
    --shadow-2xl: 0 24px 48px rgba(255, 255, 255, 0.5);

    /* === VIDRO === */
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-blur: blur(4px); /* Reduzido para performance e clareza */
    --glass-border: rgba(255, 255, 255, 0.3);
    --glass-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
    --glass-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.2);

    /* === GRADIENTE === */
    --bg-gradient: #000000; /* Sem gradiente — fundo sólido para contraste */
}
```

## 9.4 Aparência Característica

- Fundo preto sólido (sem gradiente)
- Cards cinza muito escuro com bordas brancas
- Botões primários em teal claro com alto contraste
- Texto branco puro, nunca cinza
- Bordas grossas (2px mínimo) sempre visíveis
- Sombras claras (branco/translúcido) em vez de sombras escuras
- Efeito glass reduzido (blur mínimo)

---

# 10. Tema Liquid Glass

## 10.1 Visão Geral

O tema Liquid Glass é uma variação premium do tema escuro. Ele adiciona efeitos de vidro líquido com reflexos animados, brilhos sutis e uma estética mais sofisticada. Ideal para demonstrações e dashboards executivos.

## 10.2 Tokens do Tema Liquid Glass

```css
[data-theme="glass"] {
    /* Herda todos os tokens do tema Dark */
    /* E sobrescreve: */

    --surface-card: rgba(255, 255, 255, 0.04);
    --surface-glass: rgba(255, 255, 255, 0.08);
    --glass-blur: blur(20px);
    --glass-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.15);

    --shadow-glass: 0 8px 32px rgba(20, 184, 166, 0.12);
    --shadow-glow: 0 0 40px rgba(20, 184, 166, 0.15);

    --bg-gradient: linear-gradient(
        135deg,
        #0a0f1e 0%,
        #12202e 25%,
        #0d1f2d 50%,
        #0f172a 75%,
        #0a0f1e 100%
    );
}
```

## 10.3 Efeito Glass Premium

```css
/* Aplicado a cards e painéis no tema Glass */
.glass-panel.glass-premium {
    position: relative;
    background: var(--glass-bg);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid var(--glass-border);
    box-shadow: var(--glass-shadow);
    overflow: hidden;
}

.glass-panel.glass-premium::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(
        circle at 30% 20%,
        rgba(20, 184, 166, 0.06) 0%,
        transparent 60%
    );
    pointer-events: none;
    animation: glassGlow 8s ease-in-out infinite alternate;
}

@keyframes glassGlow {
    0% {
        transform: translate(0, 0);
        opacity: 0.5;
    }
    50% {
        transform: translate(5%, 3%);
        opacity: 1;
    }
    100% {
        transform: translate(-3%, -2%);
        opacity: 0.6;
    }
}
```

## 10.4 Quando Usar

- Telas de demonstração e apresentação
- Dashboard executivo
- Tela de login (primeira impressão)
- Modo premium/configurável por usuário

---

# 11. Tema Corporate

## 11.1 Visão Geral

O tema Corporate permite que cada empresa/cliente tenha sua própria identidade visual sem modificar o Framework. As cores primárias, logotipo e estilo são definidos por tema.

## 11.2 Estrutura

```css
/* themes/corporate/client-abc.css */
[data-theme="corporate-abc"] {
    --color-primary: #1e40af;
    --color-primary-hover: #1e3a8a;
    --color-primary-active: #172554;
    --color-primary-light: #dbeafe;

    --color-secondary: #dc2626;
    --color-secondary-hover: #b91c1c;

    --surface-page: #f8fafc;
    --surface-card: #ffffff;
    --surface-sidebar: #1e293b;

    --text-primary: #0f172a;
    --text-secondary: #475569;

    --bg-gradient: linear-gradient(135deg, #eff6ff, #dbeafe);
}
```

## 11.3 Registro

```js
FiscalUI.theme.register('corporate-abc', {
    name: 'ABC Corp',
    icon: 'icon-building',
    description: 'Tema personalizado ABC Corporation',
    company: 'ABC Corp'
});
```

---

# 12. Criação de Temas

## 12.1 Guia Passo a Passo

### Passo 1: Definir os Tokens

Crie um seletor `[data-theme="nome-tema"]` com os tokens que deseja alterar:

```css
[data-theme="amazon"] {
    --color-primary: #ff9900;
    --color-primary-hover: #e88b00;
    --color-primary-active: #cc7a00;
    --surface-page: #f0f0f0;
    --surface-card: #ffffff;
    --text-primary: #111111;
    --text-secondary: #444444;
    --bg-gradient: linear-gradient(135deg, #f0f0f0, #e0e0e0);
}
```

### Passo 2: Adicionar ao themes.css

Adicione o bloco ao final do arquivo `css/themes.css`. O CSS já está carregado no HTML — nenhuma alteração no HTML é necessária.

### Passo 3: Registrar no Framework

```js
FiscalUI.theme.register('amazon', {
    name: 'Amazon Style',
    icon: 'icon-sun',
    description: 'Tema inspirado na Amazon'
});
```

### Passo 4: Aplicar

```js
FiscalUI.theme.setTheme('amazon');
```

## 12.2 Regras para Criação de Temas

### Regra 1: Sobrescreva apenas tokens semânticos

```css
/* ✅ Certo — sobrescreve token semântico */
[data-theme="meu-tema"] {
    --color-primary: #ff0000;
}

/* ❌ Errado — não sobrescreva tokens primitivos */
[data-theme="meu-tema"] {
    --color-red-500: #ff0000;
}
```

### Regra 2: Nunca crie tokens novos em um tema

```css
/* ❌ Errado — token novo que só existe neste tema */
[data-theme="meu-tema"] {
    --color-custom-header: #123456;
}

/* ✅ Certo — use tokens existentes */
[data-theme="meu-tema"] {
    --surface-page: #123456;
}
```

### Regra 3: Todo token não sobrescrito herda do tema Dark

Se você criar um tema com apenas 3 tokens, os outros 180+ tokens continuarão com os valores do tema Dark. Isso é seguro e intencional.

### Regra 4: Garanta contraste mínimo

```
Texto normal (≤18px):   contraste ≥ 4.5:1
Texto grande (>18px):   contraste ≥ 3:1
Componentes:            não depender apenas de cor para transmitir informação
```

### Regra 5: Teste em todos os componentes

Antes de disponibilizar um tema, teste-o em todos os componentes do Framework. Um tema pode ter contraste adequado no texto mas falhar em bordas de input ou hover de botão.

---

# 13. Registro de Temas

## 13.1 ThemeEngine API

```js
// Registro
FiscalUI.theme.register('dark', {
    name: 'Escuro',
    icon: 'icon-moon',
    description: 'Tema escuro padrão'
});

// Aplicar
FiscalUI.theme.setTheme('light');
FiscalUI.theme.setTheme('light', { persist: true });

// Consultar
FiscalUI.theme.getTheme();              // 'light'
FiscalUI.theme.getAvailableThemes();    // [{ id, name, icon, active }]
FiscalUI.theme.isDark();                // false
FiscalUI.theme.isLight();               // true
FiscalUI.theme.isHighContrast();        // false

// Alternar
FiscalUI.theme.toggleTheme();           // Dark → Light → HC → Dark

// Eventos
FiscalUI.events.on('theme:change', (payload) => {
    console.log(`Tema alterado: ${payload.theme}`);
});

FiscalUI.events.on('theme:before-change', (payload) => {
    // Preparação antes da troca
});
```

## 13.2 Configuração de Tema

```js
// Opções de registro
FiscalUI.theme.register('corporate', {
    name: 'Corporate',
    icon: 'icon-building',
    description: 'Tema corporativo',
    dark: false,              // É um tema escuro?
    highContrast: false,      // É alto contraste?
    company: null,            // Empresa associada (opcional)
    version: '1.0',           // Versão do tema
    author: 'FiscalUI Team',  // Autor
    tags: ['light', 'blue']   // Tags para filtro
});
```

## 13.3 Persistência Automática

```js
// Ao setar com persist:true, salva no localStorage
FiscalUI.theme.setTheme('light', { persist: true });

// Na inicialização, restaura automaticamente
// ThemeEngine.init() → localStorage.getItem('fiscalui_theme')
```

---

# 14. Tokens por Tema

## 14.1 Tokens que SEMPRE devem ser sobrescritos

Para um tema ser visualmente coerente, estes tokens devem ser sobrescritos:

| Categoria | Tokens |
|-----------|--------|
| Primary | `--color-primary`, `--color-primary-hover`, `--color-primary-active` |
| Surfaces | `--surface-page`, `--surface-card`, `--surface-input` |
| Text | `--text-primary`, `--text-secondary`, `--text-disabled` |
| Border | `--color-border`, `--color-border-focus` |
| Background | `--bg-gradient` |

## 14.2 Tokens que PODEM ser mantidos (herdar Dark)

| Categoria | Motivo |
|-----------|--------|
| Shadow | Sombras funcionam bem em qualquer tema |
| Z-index | Não depende de cor |
| Spacing | Espaçamento é universal |
| Font | Tipografia não muda entre temas |
| Radius | Bordas arredondadas são universais |
| Motion | Animações não mudam entre temas |

## 14.3 Mapa de Sobrescrita por Tema

| Categoria | Dark | Light | HC | Glass | Corporate |
|-----------|------|-------|----|-------|-----------|
| Primary | Teal | Teal escuro | Teal claro | Teal | Personalizado |
| Surfaces | Escuras | Claras | Pretas | Vidro | Personalizado |
| Text | Branco | Preto | Branco | Branco | Personalizado |
| Borders | Translúcida | Translúcida | Sólida branca | Translúcida | Personalizado |
| Shadows | Escura | Suave | Clara | Glow | Suave |
| Glass | Padrão | Claro | Mínimo | Premium | Padrão |
| Gradient | Sim | Sim | Não | Sim | Sim |

---

# 15. Hierarquia de Temas

## 15.1 Como o CSS Resolve

```
:root                         → Tema Dark (padrão)
  [data-theme="light"]        → Tema Light
  [data-theme="high-contrast"] → Tema High Contrast
```

A resolução CSS segue a especificidade: `[data-theme="light"]` tem maior especificidade que `:root`. Quando o `data-theme` é alterado, o seletor correspondente entra em vigor.

## 15.2 Hierarquia de Fallback

```
Tema específico (se existir)
    ↓
Tema Light / HC / Glass (se aplicável)
    ↓
Tema Dark (:root) — sempre disponível
```

Se um token não for encontrado no tema ativo, o CSS procura no `:root`. Isso significa que temas podem ser parciais.

---

# 16. Persistência

## 16.1 localStorage

```js
// Salvar
localStorage.setItem('fiscalui_theme', 'light');

// Restaurar
const savedTheme = localStorage.getItem('fiscalui_theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Remover
localStorage.removeItem('fiscalui_theme');
```

## 16.2 Persistência por Usuário (via Backend)

Para ambientes multi-usuário, a preferência de tema pode ser salva no perfil do usuário no backend:

```js
// Ao mudar tema
FiscalUI.theme.setTheme('light');

// Salvar no backend
FiscalUI.http.put('/user/preferences', {
    theme: 'light'
});

// Ao carregar a aplicação
const prefs = await FiscalUI.http.get('/user/preferences');
if (prefs.theme) {
    FiscalUI.theme.setTheme(prefs.theme);
}
```

---

# 17. Componentes e Temas

## 17.1 Como Componentes Consomem Temas

Componentes nunca sabem qual tema está ativo. Eles apenas consomem tokens:

```js
class Button extends ComponentBase {
    get styles() {
        return {
            backgroundColor: 'var(--color-primary)',
            color: 'var(--text-inverse)',
            border: `var(--border-thin) solid var(--color-border)`
        };
    }
}
```

## 17.2 Reagindo a Mudanças de Tema

Alguns componentes precisam reagir a mudanças de tema (por exemplo, gráficos que usam cores em canvas):

```js
class ChartWidget extends ComponentBase {
    init() {
        // Escuta mudanças de tema
        this.on('theme:change', (payload) => {
            this.colors = this.getThemeColors();
            this.render();
        });
    }

    getThemeColors() {
        const style = getComputedStyle(document.documentElement);
        return {
            primary: style.getPropertyValue('--color-primary').trim(),
            success: style.getPropertyValue('--color-success').trim(),
            danger: style.getPropertyValue('--color-danger').trim()
        };
    }
}
```

---

# 18. Temas Responsivos

## 18.1 Tema por Breakpoint

Em alguns casos, pode ser desejável que o tema mude conforme o dispositivo:

```css
/* Mobile → Light */
@media (max-width: 767px) {
    html:not([data-theme]) {
        /* Mantém Dark em desktop, Light em mobile */
    }
}
```

## 18.2 Tema Automático (Sistema)

```js
// Detectar preferência do sistema
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

if (prefersDark.matches) {
    FiscalUI.theme.setTheme('dark');
} else {
    FiscalUI.theme.setTheme('light');
}

// Escutar mudanças
prefersDark.addEventListener('change', (e) => {
    FiscalUI.theme.setTheme(e.matches ? 'dark' : 'light');
});
```

---

# 19. Acessibilidade em Temas

## 19.1 Contraste Mínimo

| Elemento | Contraste Mínimo | Padrão WCAG |
|----------|-----------------|-------------|
| Texto normal (< 18px) | 4.5:1 | AA |
| Texto grande (≥ 18px) | 3:1 | AA |
| Texto (High Contrast) | 7:1 | AAA |
| Componentes UI | 3:1 | AA |
| Foco visível | 3:1 | AA |

## 19.2 Verificação Automática

```js
FiscalUI.theme.validateContrast = function(themeId) {
    const el = document.documentElement;
    el.setAttribute('data-theme', themeId);

    const style = getComputedStyle(el);
    const bg = style.getPropertyValue('--surface-page').trim();
    const text = style.getPropertyValue('--text-primary').trim();

    // Calcular contraste (implementação simplificada)
    const ratio = getContrastRatio(bg, text);
    console.log(`Tema ${themeId}: contraste ${ratio.toFixed(2)}:1`);

    return ratio >= 4.5;
};
```

## 19.3 Modo Forçado (OS)

O tema High Contrast respeita automaticamente o modo de alto contraste do sistema operacional:

```css
@media (forced-colors: active) {
    .ui-btn {
        border: 2px solid ButtonText;
    }
}
```

---

# 20. Performance

## 20.1 Impacto da Troca de Tema

A troca de tema é uma operação O(1):

```js
// Custa ~0.1ms — apenas uma atribuição de atributo
document.documentElement.setAttribute('data-theme', 'light');
```

O navegador então reavalia todas as regras CSS com `var()`. Isso é extremamente rápido (sub-ms para centenas de variáveis).

## 20.2 Reflow

A troca de tema **não causa reflow** se apenas cores e sombras mudam. Propriedades que causam reflow (width, height, padding, margin) não são alteradas por temas.

## 20.3 Aceleração

```css
/* Transição suave entre temas */
:root {
    transition: background-color var(--transition-smooth),
                color var(--transition-smooth);
}

[data-theme] {
    transition: background-color var(--transition-smooth),
                color var(--transition-smooth);
}
```

> ⚠️ Nota: transition em todas as propriedades pode causar flicker. Aplicar com cautela.

---

# 21. Transições entre Temas

## 21.1 Transição Suave (Opcional)

```css
/* Aplicar transição nos elementos principais */
body,
.surface-page,
.ui-card,
.ui-btn,
.ui-input {
    transition: background-color var(--transition-smooth),
                color var(--transition-smooth),
                border-color var(--transition-smooth),
                box-shadow var(--transition-smooth);
}
```

## 21.2 Quando Usar

- Transições tornam a troca mais agradável visualmente
- Mas podem causar flicker se muitos elementos forem animados
- Recomendado: aplicar apenas em elementos principais (body, cards, botões)

## 21.3 Tema com Transição CSS

```css
/* Tema "fade" */
[data-theme] {
    animation: themeFade 0.3s ease-out;
}

@keyframes themeFade {
    0% { opacity: 0.8; }
    100% { opacity: 1; }
}
```

---

# 22. Temas por Empresa

## 22.1 Múltiplos Temas por Cliente

Em sistemas ERP multi-empresa, cada empresa pode ter seu próprio tema:

```js
// Ao selecionar empresa
FiscalUI.events.on('company:change', (payload) => {
    const theme = `corporate-${payload.companyId}`;
    if (FiscalUI.theme.isRegistered(theme)) {
        FiscalUI.theme.setTheme(theme);
    }
});
```

## 22.2 CSS por Empresa

```css
/* Cliente A — Cores azuis */
[data-theme="client-001"] {
    --color-primary: #1e40af;
    --color-primary-hover: #1e3a8a;
}

/* Cliente B — Cores verdes */
[data-theme="client-002"] {
    --color-primary: #047857;
    --color-primary-hover: #065f46;
}
```

## 22.3 Logotipo por Empresa

```js
FiscalUI.theme.register('client-001', {
    name: 'Cliente ABC',
    icon: 'icon-building',
    logo: 'assets/img/logos/abc.svg',  // Logotipo personalizado
    company: 'ABC Ltda'
});
```

---

# 23. Temas por Usuário

## 23.1 Preferência Individual

Cada usuário pode escolher seu tema preferido, independentemente do tema da empresa:

```js
// Prioridade: Tema do usuário > Tema da empresa > Tema padrão
const userTheme = FiscalUI.auth.user?.preferences?.theme;
const companyTheme = companyConfig?.theme;
const defaultTheme = 'dark';

FiscalUI.theme.setTheme(userTheme || companyTheme || defaultTheme);
```

---

# 24. Tema na Tela de Login

## 24.1 Seletor de Tema no Login

Para permitir que usuários com necessidades de acessibilidade escolham o tema antes de logar:

```html
<div class="login-theme-selector">
    <label>Theme:</label>
    <select id="login-theme">
        <option value="dark">Dark</option>
        <option value="light">Light</option>
        <option value="high-contrast">High Contrast</option>
    </select>
</div>
```

```js
document.getElementById('login-theme').addEventListener('change', (e) => {
    FiscalUI.theme.setTheme(e.target.value);
});
```

---

# 25. Design Tokens vs Temas

## 25.1 Separação de Responsabilidades

```
Design Tokens (tokens.css)     Temas (themes.css)
─────────────────────          ───────────────
Define o que existe            Define os valores
Categoria dos tokens           Valores específicos
Valores padrão (Dark)          Sobrescritas para Light/HC
Primitivos (--color-teal-500)  Semânticos (--color-primary)
```

## 25.2 Regra de Ouro

**Nunca misturar.** Tokens são a definição. Temas são a instanciação.

---

# 26. Sobrescrita vs Criação

## 26.1 Quando Sobrescrever

Você sobrescreve um token quando:

- O novo valor é uma variação do original (ex: mesma cor, tom diferente)
- O token já existe e é semanticamente equivalente
- O token será usado pelos mesmos componentes

## 26.2 Quando Criar

Você cria um token novo quando:

- Nenhum token existente representa o conceito visual desejado
- Um componente específico precisa de um valor que não se aplica a outros componentes
- Há necessidade de granularidade adicional (ex: múltiplos tons de uma cor)

## 26.3 Processo de Criação de Novo Token

1. Verificar se já existe um token semelhante
2. Propor o novo token em `tokens.css` (valor padrão)
3. Atualizar todos os temas em `themes.css`
4. Atualizar este documento
5. Atualizar componentes que devem usar o novo token

---

# 27. Testes de Tema

## 27.1 Checklist de Teste para Cada Tema

```
☐ Todos os botões funcionam (primary, secondary, outline, ghost, danger)
☐ Todos os tamanhos de botão funcionam (sm, md, lg)
☐ Input fields têm contraste adequado
☐ Modais são legíveis
☐ Toast notifications são legíveis
☐ Sidebar menus são legíveis
☐ DataGrid linhas são distinguíveis
☐ Cards têm sombra adequada
☐ Tooltips são legíveis
☐ Foco visível em todos os elementos interativos
☐ Ícones têm contraste adequado
☐ High Contrast: bordas visíveis em todos os elementos
☐ Gradiente de fundo não interfere na legibilidade
```

## 27.2 Teste Automatizado de Contraste

```js
describe('Theme contrast', () => {
    const themes = ['dark', 'light', 'high-contrast'];

    themes.forEach(theme => {
        it(`should have sufficient contrast for ${theme}`, () => {
            document.documentElement.setAttribute('data-theme', theme);
            const style = getComputedStyle(document.body);
            const bg = style.backgroundColor;
            const text = style.color;
            const ratio = getContrastRatio(bg, text);
            expect(ratio).toBeGreaterThanOrEqual(4.5);
        });
    });
});
```

## 27.3 Teste Visual (Screenshots)

Recomenda-se usar ferramentas de screenshot comparison (Percy, Chromatic) para detectar regressões visuais em cada tema.

---

# 28. Debugging

## 28.1 Console

```js
// Ver tema atual
FiscalUI.theme.getTheme();     // "light"

// Ver temas disponíveis
FiscalUI.theme.getAvailableThemes();

// Verificar se tema está registrado
FiscalUI.theme.isRegistered('corporate-x');

// Forçar tema
FiscalUI.theme.setTheme('light', { persist: false });
```

## 28.2 DevTools

```css
/* No DevTools Console, inspecionar tokens */
getComputedStyle(document.documentElement)
    .getPropertyValue('--color-primary');
// → "#0d9488"
```

## 28.3 Problemas Comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| Tema não aplica | data-theme incorreto | Verificar spelling do nome do tema |
| Cores erradas | Token não sobrescrito | Adicionar token ao tema |
| Contraste baixo | Tema novo não testado | Usar ferramenta de contraste |
| Tema não persiste | localStorage desabilitado | Usar fallback sessionStorage |
| Transição lenta | Transition em muitas props | Limitar a opacity e cores |

---

# 29. Boas Práticas

## 29.1 Para Desenvolvedores

1. **Nunca** usar `data-theme` em elementos que não sejam `<html>`
2. **Sempre** testar novo componente em todos os temas oficiais
3. **Nunca** criar token novo sem necessidade real
4. **Sempre** documentar tokens novos neste documento
5. **Preferir** sobrescrita a criação de novos tokens
6. **Usar** `var(--token, fallback)` com fallback para segurança

## 29.2 Para Designers

1. **Sempre** especificar tokens, nunca valores absolutos
2. **Criar** variações de tema testando contraste
3. **Documentar** decisões de cor com os tokens correspondentes
4. **Verificar** todos os modos (hover, focus, active, disabled) em cada tema

## 29.3 Para Gestores

1. **Manter** o `tokens.css` como documento de referência de identidade visual
2. **Revisar** mudanças de tokens em code review
3. **Testar** novos temas com usuários reais antes de disponibilizar
4. **Documentar** temas corporativos para referência do cliente

---

# 30. Ferramentas

## 30.1 Stylelint

```json
{
    "rules": {
        "color-no-hex": true,
        "declaration-property-value-allowed-list": {
            "/color/": ["/var\\(--/"],
            "/background/": ["/var\\(--/"],
            "/border/": ["/var\\(--/"]
        }
    }
}
```

## 30.2 Visualizador de Temas

Página que exibe todos os temas disponíveis para comparação visual lado a lado:

```
sprints/tools/theme-viewer.html
```

---

# 31. Compatibilidade

## 31.1 Browsers

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS Variables | 49+ | 31+ | 9.1+ | 15+ |
| `data-*` selectors | All | All | All | All |
| `backdrop-filter` | 76+ | 103+ | 9+ | 17+ |
| `prefers-color-scheme` | 76+ | 67+ | 12.1+ | 79+ |
| `forced-colors` | 89+ | 89+ | 15+ | 89+ |

## 31.2 Polyfills

Nenhum polyfill é necessário. O FiscalUI não suporta IE11.

---

# 32. Roadmap

## Versão 1.0
- [x] Dark, Light, High Contrast
- [x] ThemeEngine.js
- [x] Persistência localStorage
- [ ] Tema Liquid Glass
- [ ] Seletor de tema na tela de login

## Versão 1.1
- [ ] Temas por empresa
- [ ] Temas por usuário
- [ ] Tema automático (prefers-color-scheme)

## Versão 1.2
- [ ] Editor visual de temas
- [ ] Marketplace de temas
- [ ] Tema Corporate (customizável)
- [ ] Preview de tema ao vivo

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — 32 seções, 4 temas oficiais |
