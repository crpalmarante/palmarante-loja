# FiscalUI Framework

## Documento 002 — Design Tokens

**Versão 1.0**

Este documento define cada variável visual do FiscalUI Framework. Nenhum valor fixo de cor, espaçamento, borda, sombra, tipografia ou animação existe em nenhum componente. Tudo é controlado por tokens.

---

# Índice

1. Introdução
2. O que são Design Tokens
3. Filosofia
4. Categorias de Tokens
5. Nomenclatura
6. Cores
7. Tipografia
8. Espaçamento
9. Bordas
10. Sombras
11. Glassmorphism
12. Opacidade
13. Z-Index
14. Motion
15. Breakpoints
16. Breakpoints por Componente
17. Tamanhos de Ícones
18. Tokens de Formulário
19. Tokens de DataGrid
20. Tokens de Tema
21. Tokens por Componente
22. Temas Oficiais
23. Como Criar um Tema
24. Boas Práticas
25. Compatibilidade
26. Ferramentas
27. Checklist de Implementação
28. Referência Rápida

---

# 1. Introdução

## 1.1 Propósito

Design Tokens são a menor unidade de configuração visual do FiscalUI. Eles existem como variáveis CSS no arquivo `css/tokens.css` e são consumidos por todos os componentes, páginas e temas do Framework.

Nenhum componente, serviço ou página define valores visuais diretamente. Toda cor, espaçamento, borda, sombra, tipografia e animação referência um token.

## 1.2 Escopo

Este documento cobre:

- Todos os tokens oficiais do FiscalUI (~200 tokens)
- Regras de nomenclatura e uso
- Integração com o Theme Engine
- Boas práticas para criação de componentes
- Guia para criação de novos temas

## 1.3 Público-Alvo

- Desenvolvedores criando ou mantendo componentes
- Designers implementando o Design System
- Equipes criando temas personalizados
- Revisores de código validando consistência visual

---

# 2. O que são Design Tokens

## 2.1 Definição

Design Tokens são pares nome-valor que representam decisões de design. Eles substituem valores literais como `#14b8a6` ou `12px` por nomes semânticos como `--color-primary` ou `--spacing-4`.

```css
/* ❌ Valor literal — proibido em componentes */
.button {
    background: #14b8a6;
    padding: 12px 22px;
    border-radius: 12px;
    font-size: 14px;
}

/* ✅ Design Tokens — obrigatório */
.button {
    background: var(--color-primary);
    padding: var(--spacing-4) var(--spacing-6);
    border-radius: var(--radius-lg);
    font-size: var(--font-size-base);
}
```

## 2.2 Por que Design Tokens?

| Benefício | Explicação |
|-----------|------------|
| Consistência | Mesma cor primária em 50 componentes |
| Manutenibilidade | Alterar um token = alterar o sistema inteiro |
| Temas | Trocar data-theme = trocar todos os tokens |
| Escalabilidade | Novos componentes seguem o mesmo padrão |
| Documentação | O token documenta a intenção do design |
| Colaboração | Designers e devs falam a mesma língua |

## 2.3 Como os Tokens Funcionam

```
tokens.css (valores padrão — tema escuro)
    │
    ├── themes.css (sobrescrita para Light, High Contrast)
    │       │
    │       └── data-theme="light" → tokens modificados
    │
    ├── component.css (consome tokens via var())
    │
    └── page.css (consome tokens via var())
```

---

# 3. Filosofia

## 3.1 Princípios

### 3.1.1 Zero valores literais

Nenhum arquivo fora de `tokens.css` ou `themes.css` pode conter um valor visual literal. Isso inclui cores hex, rgb, nomes de cor, valores de pixel, etc.

```css
/* ❌ Violação */
.card {
    border: 1px solid #e2e8f0;
}

/* ✅ Correto */
.card {
    border: var(--border-thin) solid var(--color-border);
}
```

### 3.1.2 Semântica sobre descrição

Nomes de token descrevem o **propósito**, não a aparência.

```css
/* ❌ Descritivo */
--color-teal-500: #14b8a6;

/* ✅ Semântico */
--color-primary: #14b8a6;
```

### 3.1.3 Hierarquia de tokens

```
Tokens Primitivos → Tokens Semânticos → Tokens de Componente
```

- **Primitivos:** valores brutos (`--color-teal-500: #14b8a6`)
- **Semânticos:** propósito (`--color-primary: var(--color-teal-500)`)
- **Componente:** escopo (`--btn-primary-bg: var(--color-primary)`)

### 3.1.4 Temas alteram apenas tokens semânticos

Temas nunca alteram tokens primitivos. Eles sobrescrevem apenas tokens semânticos.

```css
/* tokens.css — primitivos */
--color-teal-500: #14b8a6;
--color-teal-600: #0d9488;

/* tokens.css — semânticos (dark theme default) */
--color-primary: var(--color-teal-500);

/* themes.css — light theme */
[data-theme="light"] {
    --color-primary: var(--color-teal-600); /* mais escuro para contraste */
}
```

## 3.2 Hierarquia Completa

```
Categoria → Subcategoria → Token → Valor → Tema
```

Exemplo:

```
Categoria: Color
Subcategoria: Semantic
Token: --color-primary
Valor: var(--color-teal-500) → #14b8a6
Tema Dark: mantém
Tema Light: var(--color-teal-600) → #0d9488
Tema HC: var(--color-teal-400) → #2dd4bf
```

---

# 4. Categorias de Tokens

## 4.1 Visão Geral

| Categoria | Prefixo | Qtd Tokens | Arquivo |
|-----------|---------|------------|---------|
| Cores | `--color-*` | ~60 | tokens.css |
| Tipografia | `--font-*` | ~25 | tokens.css |
| Espaçamento | `--spacing-*` | ~15 | tokens.css |
| Bordas | `--border-*`, `--radius-*` | ~12 | tokens.css |
| Sombras | `--shadow-*` | ~8 | tokens.css |
| Glassmorphism | `--glass-*` | ~6 | tokens.css |
| Opacidade | `--opacity-*` | ~6 | tokens.css |
| Z-Index | `--z-*` | ~10 | tokens.css |
| Motion | `--motion-*`, `--ease-*` | ~12 | tokens.css |
| Breakpoints | `--bp-*` | ~6 | tokens.css |
| Ícones | `--icon-*` | ~6 | tokens.css |
| Formulário | `--form-*` | ~10 | tokens.css |
| DataGrid | `--grid-*` | ~10 | tokens.css |
| **Total** | | **~186** | |

## 4.2 Mapa Completo de Tokens

```
COLORS (60)
├── Brand (8)
│   ├── --color-primary, --color-primary-hover, --color-primary-active
│   ├── --color-secondary, --color-secondary-hover, --color-secondary-active
│   └── --color-accent, --color-accent-hover
│
├── Semantic (8)
│   ├── --color-success, --color-warning, --color-danger, --color-info
│   └── --color-success-bg, --color-warning-bg, --color-danger-bg, --color-info-bg
│
├── Neutral (12)
│   ├── --color-white, --color-black
│   ├── --color-gray-50, --color-gray-100, --color-gray-200, --color-gray-300
│   ├── --color-gray-400, --color-gray-500, --color-gray-600, --color-gray-700
│   ├── --color-gray-800, --color-gray-900
│
├── Surfaces (12)
│   ├── --surface-page, --surface-card, --surface-modal, --surface-sidebar
│   ├── --surface-input, --surface-tooltip, --surface-toast, --surface-glass
│   ├── --surface-hover, --surface-active, --surface-selected, --surface-disabled
│
├── Text (8)
│   ├── --text-primary, --text-secondary, --text-tertiary, --text-disabled
│   ├── --text-inverse, --text-link, --text-link-hover, --text-placeholder
│
├── Border (6)
│   ├── --color-border, --color-border-hover, --color-border-focus
│   ├── --color-border-disabled, --color-border-error, --color-border-success
│
└── Charts (6)
    ├── --chart-1 a --chart-6

TYPOGRAPHY (25)
├── Family (3)
│   ├── --font-family, --font-mono, --font-icon
│
├── Size (10)
│   ├── --font-size-xxs, --font-size-xs, --font-size-sm, --font-size-base
│   ├── --font-size-lg, --font-size-xl, --font-size-xxl, --font-size-xxxl
│   ├── --font-size-display, --font-size-hero
│
├── Weight (6)
│   ├── --font-weight-light, --font-weight-regular, --font-weight-medium
│   ├── --font-weight-semibold, --font-weight-bold, --font-weight-black
│
├── Line Height (4)
│   ├── --line-height-tight, --line-height-normal, --line-height-relaxed, --line-height-loose
│
└── Spacing (2)
    ├── --letter-spacing-tight, --letter-spacing-wide

SPACING (15)
├── --spacing-0, --spacing-1, --spacing-2, --spacing-3, --spacing-4
├── --spacing-5, --spacing-6, --spacing-7, --spacing-8, --spacing-9
├── --spacing-10, --spacing-12, --spacing-14, --spacing-16, --spacing-20

BORDERS (12)
├── Border Width (4)
│   ├── --border-none, --border-thin, --border-medium, --border-thick
│
└── Radius (8)
    ├── --radius-none, --radius-sm, --radius-md, --radius-lg
    ├── --radius-xl, --radius-2xl, --radius-rounded, --radius-pill

SHADOWS (8)
├── --shadow-xs, --shadow-sm, --shadow-md, --shadow-lg
├── --shadow-xl, --shadow-2xl, --shadow-glass, --shadow-glow

GLASS (6)
├── --glass-bg, --glass-blur, --glass-border, --glass-shadow, --glass-highlight, --glass-opacity

OPACITY (6)
├── --opacity-0, --opacity-25, --opacity-50, --opacity-75, --opacity-90, --opacity-100

Z-INDEX (10)
├── --z-base, --z-dropdown, --z-sticky, --z-fixed, --z-modal-backdrop
├── --z-modal, --z-popover, --z-toast, --z-tooltip, --z-fullscreen

MOTION (14)
├── Duration (5)
│   ├── --motion-instant, --motion-fast, --motion-normal, --motion-smooth, --motion-slow
│
├── Easing (4)
│   ├── --ease-linear, --ease-out, --ease-in-out, --ease-spring
│
└── Transition (5)
    ├── --transition-fast, --transition-normal, --transition-smooth
    ├── --transition-spring, --transition-linear

BREAKPOINTS (6)
├── --bp-xs, --bp-sm, --bp-md, --bp-lg, --bp-xl, --bp-xxl

ICONS (6)
├── --icon-xs, --icon-sm, --icon-md, --icon-lg, --icon-xl, --icon-xxl

FORM (10)
├── --form-height-sm, --form-height-md, --form-height-lg
├── --form-padding-sm, --form-padding-md, --form-padding-lg
├── --form-font-sm, --form-font-md, --form-font-lg
└── --form-label-width

DATAGRID (10)
├── --grid-row-height-sm, --grid-row-height-md, --grid-row-height-lg
├── --grid-header-bg, --grid-row-hover, --grid-row-selected
├── --grid-border, --grid-stripe-bg
├── --grid-cell-padding, --grid-font-size
```

---

# 5. Nomenclatura

## 5.1 Regras Gerais

```
--categoria-subcategoria-propriedade-estado
```

| Parte | Descrição | Exemplo |
|-------|-----------|---------|
| `categoria` | Grupo principal | `color`, `font`, `spacing` |
| `subcategoria` | Subgrupo (opcional) | `primary`, `surface`, `chart` |
| `propriedade` | O que é | `hover`, `bg`, `size` |
| `estado` | Estado (opcional) | `hover`, `active`, `disabled` |

## 5.2 Exemplos

```
--color-primary             → cor primária
--color-primary-hover       → cor primária no hover
--surface-page              → superfície da página
--text-secondary            → texto secundário
--font-size-base            → tamanho de fonte base
--spacing-4                 → espaçamento nível 4
--radius-lg                 → borda arredondada grande
--shadow-md                 → sombra média
--motion-fast               → duração rápida
--ease-out                  → easing de saída
--z-modal                   → z-index de modal
--grid-row-hover            → hover de linha no datagrid
```

## 5.3 Convenções por Categoria

| Categoria | Padrão | Exemplo |
|-----------|--------|---------|
| Cores | `--color-<nome>` | `--color-primary` |
| Superfície | `--surface-<nome>` | `--surface-card` |
| Texto | `--text-<nome>` | `--text-primary` |
| Borda | `--color-border-<estado>` | `--color-border-focus` |
| Fonte | `--font-size-<tamanho>` | `--font-size-base` |
| Espaçamento | `--spacing-<n>` | `--spacing-4` |
| Raio | `--radius-<tamanho>` | `--radius-lg` |
| Sombra | `--shadow-<tamanho>` | `--shadow-lg` |
| Z-index | `--z-<nome>` | `--z-modal` |
| Duração | `--motion-<nome>` | `--motion-fast` |
| Easing | `--ease-<nome>` | `--ease-out` |
| Breakpoint | `--bp-<nome>` | `--bp-lg` |

---

# 6. Cores

## 6.1 Paleta de Cores

### 6.1.1 Cores da Marca

```css
--color-primary: #14b8a6;
--color-primary-hover: #0d9488;
--color-primary-active: #0f766e;
--color-primary-light: #ccfbf1;
--color-primary-dark: #134e4a;

--color-secondary: #6366f1;
--color-secondary-hover: #4f46e5;
--color-secondary-active: #4338ca;
--color-secondary-light: #e0e7ff;
--color-secondary-dark: #312e81;

--color-accent: #f59e0b;
--color-accent-hover: #d97706;
--color-accent-light: #fef3c7;
--color-accent-dark: #92400e;
```

### 6.1.2 Cores Semânticas

```css
--color-success: #10b981;
--color-success-hover: #059669;
--color-success-bg: #d1fae5;
--color-success-border: #6ee7b7;

--color-warning: #f59e0b;
--color-warning-hover: #d97706;
--color-warning-bg: #fef3c7;
--color-warning-border: #fcd34d;

--color-danger: #ef4444;
--color-danger-hover: #dc2626;
--color-danger-bg: #fee2e2;
--color-danger-border: #fca5a5;

--color-info: #3b82f6;
--color-info-hover: #2563eb;
--color-info-bg: #dbeafe;
--color-info-border: #93c5fd;
```

### 6.1.3 Neutros

```css
--color-white: #ffffff;
--color-black: #000000;

--color-gray-50: #f8fafc;
--color-gray-100: #f1f5f9;
--color-gray-200: #e2e8f0;
--color-gray-300: #cbd5e1;
--color-gray-400: #94a3b8;
--color-gray-500: #64748b;
--color-gray-600: #475569;
--color-gray-700: #334155;
--color-gray-800: #1e293b;
--color-gray-900: #0f172a;
```

## 6.2 Superfícies

```css
--surface-page: var(--color-gray-900);
--surface-card: var(--color-gray-800);
--surface-modal: var(--color-gray-800);
--surface-sidebar: var(--color-gray-800);
--surface-input: var(--color-gray-700);
--surface-tooltip: var(--color-gray-600);
--surface-toast: var(--color-gray-700);
--surface-glass: rgba(255, 255, 255, 0.06);
--surface-hover: rgba(255, 255, 255, 0.08);
--surface-active: rgba(255, 255, 255, 0.12);
--surface-selected: rgba(20, 184, 166, 0.15);
--surface-disabled: rgba(255, 255, 255, 0.04);
```

## 6.3 Texto

```css
--text-primary: var(--color-gray-50);
--text-secondary: var(--color-gray-300);
--text-tertiary: var(--color-gray-400);
--text-disabled: var(--color-gray-500);
--text-inverse: var(--color-gray-900);
--text-link: var(--color-primary);
--text-link-hover: var(--color-primary-hover);
--text-placeholder: var(--color-gray-500);
```

## 6.4 Bordas

```css
--color-border: rgba(255, 255, 255, 0.12);
--color-border-hover: rgba(255, 255, 255, 0.2);
--color-border-focus: var(--color-primary);
--color-border-disabled: rgba(255, 255, 255, 0.06);
--color-border-error: var(--color-danger);
--color-border-success: var(--color-success);
```

## 6.5 Gráficos

```css
--chart-1: #14b8a6;
--chart-2: #6366f1;
--chart-3: #f59e0b;
--chart-4: #ef4444;
--chart-5: #3b82f6;
--chart-6: #8b5cf6;
```

## 6.6 Cores no Tema Light

```css
[data-theme="light"] {
    --color-primary: #0d9488;
    --color-primary-hover: #0f766e;
    --color-primary-active: #115e59;

    --surface-page: var(--color-gray-50);
    --surface-card: #ffffff;
    --surface-modal: #ffffff;
    --surface-sidebar: #ffffff;

    --text-primary: var(--color-gray-900);
    --text-secondary: var(--color-gray-600);
    --text-tertiary: var(--color-gray-400);
    --text-disabled: var(--color-gray-300);

    --color-border: rgba(0, 0, 0, 0.1);
    --color-border-hover: rgba(0, 0, 0, 0.16);
    --color-border-focus: var(--color-primary);

    --surface-glass: rgba(255, 255, 255, 0.7);
    --surface-hover: rgba(0, 0, 0, 0.04);
    --surface-active: rgba(0, 0, 0, 0.08);
    --surface-selected: rgba(13, 148, 136, 0.12);
}
```

## 6.7 Cores no Tema High Contrast

```css
[data-theme="high-contrast"] {
    --color-primary: #2dd4bf;
    --color-primary-hover: #5eead4;
    --color-primary-active: #99f6e4;

    --surface-page: #000000;
    --surface-card: #0a0a0a;
    --surface-modal: #0a0a0a;
    --surface-sidebar: #0a0a0a;
    --surface-input: #1a1a1a;

    --text-primary: #ffffff;
    --text-secondary: #e0e0e0;
    --text-tertiary: #b0b0b0;

    --color-border: #ffffff;
    --color-border-hover: #cccccc;
    --color-border-focus: #2dd4bf;

    --shadow-xs: 0 1px 2px rgba(255, 255, 255, 0.2);
    --shadow-sm: 0 2px 4px rgba(255, 255, 255, 0.2);
    --shadow-md: 0 4px 8px rgba(255, 255, 255, 0.2);
}
```

---

# 7. Tipografia

## 7.1 Família

```css
--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
--font-icon: 'Inter', sans-serif; /* Para ícones inline */
```

### 7.1.1 Font Stack (Fallback Progressivo)

```
Inter (woff2, self-hosted) → -apple-system (macOS) →
BlinkMacSystemFont (Chrome macOS) → Segoe UI (Windows) →
sans-serif (fallback genérico)
```

## 7.2 Escala Tipográfica

```css
--font-size-hero: 3rem;       /* 48px — Título de página principal */
--font-size-display: 2.25rem; /* 36px — Display */
--font-size-xxxl: 1.875rem;   /* 30px — Título de seção */
--font-size-xxl: 1.5rem;      /* 24px — Título de card */
--font-size-xl: 1.25rem;      /* 20px — Subtítulo */
--font-size-lg: 1.125rem;     /* 18px — Corpo grande */
--font-size-base: 1rem;       /* 16px — Corpo padrão */
--font-size-sm: 0.875rem;     /* 14px — Corpo pequeno, label */
--font-size-xs: 0.75rem;      /* 12px — Caption, badge */
--font-size-xxs: 0.625rem;    /* 10px — Tag, metacaption */
```

### 7.2.1 Hierarchy Semântica

```css
/* Títulos */
--font-size-h1: var(--font-size-display);
--font-size-h2: var(--font-size-xxxl);
--font-size-h3: var(--font-size-xxl);
--font-size-h4: var(--font-size-xl);
--font-size-h5: var(--font-size-lg);
--font-size-h6: var(--font-size-base);

/* Corpo */
--font-size-body: var(--font-size-base);
--font-size-body-sm: var(--font-size-sm);
--font-size-caption: var(--font-size-xs);

/* Botões */
--font-size-btn-sm: var(--font-size-sm);
--font-size-btn-md: var(--font-size-base);
--font-size-btn-lg: var(--font-size-lg);

/* Formulários */
--font-size-label: var(--font-size-sm);
--font-size-input: var(--font-size-base);
--font-size-helper: var(--font-size-xs);
```

## 7.3 Pesos

```css
--font-weight-light: 300;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
--font-weight-black: 900;
```

### 7.3.1 Uso Semântico

```css
--font-weight-heading: var(--font-weight-semibold);
--font-weight-body: var(--font-weight-regular);
--font-weight-label: var(--font-weight-medium);
--font-weight-btn: var(--font-weight-medium);
--font-weight-strong: var(--font-weight-bold);
```

## 7.4 Altura de Linha

```css
--line-height-tight: 1.15;    /* Títulos grandes */
--line-height-normal: 1.4;    /* Corpo padrão */
--line-height-relaxed: 1.6;   /* Texto longo */
--line-height-loose: 1.8;     /* Artigo, documentação */
```

### 7.4.1 Uso Semântico

```css
--line-height-heading: var(--line-height-tight);
--line-height-body: var(--line-height-normal);
--line-height-label: var(--line-height-normal);
--line-height-caption: var(--line-height-relaxed);
```

## 7.5 Espaçamento de Letras

```css
--letter-spacing-tight: -0.025em;  /* Títulos */
--letter-spacing-wide: 0.05em;     /* Uppercase, label */
--letter-spacing-normal: 0;        /* Corpo */
```

---

# 8. Espaçamento

## 8.1 Escala

A escala de espaçamento do FiscalUI é baseada em uma progressão de 4px (base) com alguns incrementos de 8px para valores maiores.

```css
--spacing-0:  0px;       /* 0 */
--spacing-1:  2px;       /* 2px — micro */
--spacing-2:  4px;       /* 4px — mini */
--spacing-3:  8px;       /* 8px — pequeno */
--spacing-4:  12px;      /* 12px — base */
--spacing-5:  16px;      /* 16px — médio */
--spacing-6:  20px;      /* 20px — grande */
--spacing-7:  24px;      /* 24px — extra */
--spacing-8:  32px;      /* 32px — seção */
--spacing-9:  40px;      /* 40px — seção grande */
--spacing-10: 48px;      /* 48px — container */
--spacing-12: 64px;      /* 64px — página */
--spacing-14: 80px;      /* 80px — página grande */
--spacing-16: 96px;      /* 96px — hero */
--spacing-20: 128px;     /* 128px — seção hero */
```

## 8.2 Uso Semântico

```css
--space-inset-sm: var(--spacing-3);   /* 8px — padding interno pequeno */
--space-inset-md: var(--spacing-4);   /* 12px — padding interno padrão */
--space-inset-lg: var(--spacing-6);   /* 20px — padding interno grande */
--space-stack-sm: var(--spacing-3);   /* 8px — margem inferior pequena */
--space-stack-md: var(--spacing-5);   /* 16px — margem inferior padrão */
--space-stack-lg: var(--spacing-8);   /* 32px — margem inferior grande */
--space-inline-sm: var(--spacing-2);  /* 4px — gap horizontal pequeno */
--space-inline-md: var(--spacing-3);  /* 8px — gap horizontal padrão */
--space-inline-lg: var(--spacing-5);  /* 16px — gap horizontal grande */
--space-section: var(--spacing-10);   /* 48px — separação de seções */
```

## 8.3 Tokens Legado (Compatibilidade)

```css
/* Tokens legado mantidos para compatibilidade */
--space-0: var(--spacing-0);
--space-1: var(--spacing-1);
--space-2: var(--spacing-2);
--space-3: var(--spacing-3);
--space-4: var(--spacing-4);
--space-5: var(--spacing-5);
--space-6: var(--spacing-6);
--space-8: var(--spacing-7);
--space-10: var(--spacing-8);
--space-12: var(--spacing-9);
--space-16: var(--spacing-10);
--space-20: var(--spacing-12);
--space-24: var(--spacing-14);
```

---

# 9. Bordas

## 9.1 Largura

```css
--border-none: 0px;
--border-thin: 1px;
--border-medium: 2px;
--border-thick: 4px;
```

## 9.2 Raio (Border Radius)

```css
--radius-none: 0px;            /* 0 — sem arredondamento */
--radius-sm: 4px;              /* 4px — sutil */
--radius-md: 8px;              /* 8px — padrão */
--radius-lg: 12px;             /* 12px — card, modal */
--radius-xl: 16px;             /* 16px — drawer, painel */
--radius-2xl: 24px;            /* 24px — destaque */
--radius-rounded: 9999px;      /* círculo/pílula — avatar, badge */
--radius-pill: 9999px;         /* pílula — chip, tag */
```

## 9.3 Uso Semântico

```css
--radius-card: var(--radius-lg);
--radius-btn: var(--radius-md);
--radius-input: var(--radius-md);
--radius-modal: var(--radius-xl);
--radius-badge: var(--radius-rounded);
--radius-chip: var(--radius-pill);
```

---

# 10. Sombras

## 10.1 Escala de Sombras

```css
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.35);
--shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.45);
--shadow-xl: 0 12px 40px rgba(0, 0, 0, 0.5);
--shadow-2xl: 0 24px 64px rgba(0, 0, 0, 0.6);
--shadow-glass: 0 4px 24px rgba(20, 184, 166, 0.08);
--shadow-glow: 0 0 30px rgba(20, 184, 166, 0.12);
```

## 10.2 Uso Semântico

```css
--shadow-card: var(--shadow-sm);
--shadow-modal: var(--shadow-lg);
--shadow-dropdown: var(--shadow-md);
--shadow-toast: var(--shadow-md);
--shadow-btn: var(--shadow-xs);
--shadow-btn-hover: var(--shadow-sm);
--shadow-tooltip: var(--shadow-md);
--shadow-drawer: var(--shadow-xl);
```

---

# 11. Glassmorphism

## 11.1 Tokens de Vidro

```css
--glass-bg: rgba(255, 255, 255, 0.06);
--glass-blur: blur(12px);
--glass-border: rgba(255, 255, 255, 0.08);
--glass-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
--glass-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.1);
--glass-opacity: 0.85;
```

## 11.2 Aplicação

```css
.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: var(--border-thin) solid var(--glass-border);
    box-shadow: var(--shadow-glass);
}

.glass-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: var(--glass-highlight);
}
```

---

# 12. Opacidade

```css
--opacity-0: 0;
--opacity-25: 0.25;
--opacity-50: 0.5;
--opacity-75: 0.75;
--opacity-90: 0.9;
--opacity-100: 1;
```

### Uso Semântico

```css
--opacity-disabled: var(--opacity-50);
--opacity-overlay: var(--opacity-50);
--opacity-glass: var(--opacity-90);
--opacity-hover: var(--opacity-75);
```

---

# 13. Z-Index

## 13.1 Escala

```css
--z-base: 0;
--z-dropdown: 100;
--z-sticky: 200;
--z-fixed: 300;
--z-modal-backdrop: 400;
--z-modal: 500;
--z-popover: 600;
--z-toast: 700;
--z-tooltip: 800;
--z-fullscreen: 900;
```

## 13.2 Regras

1. Nunca usar `z-index` value literais. Sempre usar tokens.
2. A escala deixa espaços intencionais (50, 150, 250) para variações.
3. Nenhum componente define z-index sem usar um token desta escala.

```css
/* ❌ Ruim */
.modal { z-index: 99999; }

/* ✅ Correto */
.modal { z-index: var(--z-modal); }
```

---

# 14. Motion

## 14.1 Durações

```css
--motion-instant: 100ms;    /* Microfeedback */
--motion-fast: 150ms;       /* Hover, focus, clique */
--motion-normal: 250ms;     /* Transições padrão */
--motion-smooth: 350ms;     /* Modal, drawer, toast */
--motion-slow: 500ms;       /* KPI, entrada de tela */
```

## 14.2 Easing

```css
--ease-linear: cubic-bezier(0, 0, 1, 1);
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
```

## 14.3 Transições Compostas

```css
--transition-fast: var(--motion-fast) var(--ease-out);
--transition-normal: var(--motion-normal) var(--ease-out);
--transition-smooth: var(--motion-smooth) var(--ease-out);
--transition-spring: var(--motion-smooth) var(--ease-spring);
--transition-linear: var(--motion-normal) var(--ease-linear);
```

## 14.4 Aplicação

```css
/* ❌ Ruim */
.card {
    transition: all 300ms ease-in-out;
}

/* ✅ Correto */
.card {
    transition: transform var(--transition-normal),
                box-shadow var(--transition-normal),
                opacity var(--transition-normal);
}
```

---

# 15. Breakpoints

## 15.1 Escala

```css
--bp-xs: 0px;
--bp-sm: 576px;
--bp-md: 768px;
--bp-lg: 1024px;
--bp-xl: 1440px;
--bp-xxl: 1920px;
```

## 15.2 Uso em Media Queries

```css
/* Mobile First — sempre min-width */
@media (min-width: 576px) { /* SM+ */ }
@media (min-width: 768px) { /* MD+ */ }
@media (min-width: 1024px) { /* LG+ */ }
@media (min-width: 1440px) { /* XL+ */ }
@media (min-width: 1920px) { /* XXL */ }

/* Apenas mobile */
@media (max-width: 575px) { /* XS only */ }
@media (max-width: 767px) { /* XS + SM */ }
```

## 15.3 Resolução de Nomes

| Nome | Largura | Dispositivo típico |
|------|---------|-------------------|
| XS | 0–575px | Smartphone |
| SM | 576–767px | Smartphone grande |
| MD | 768–1023px | Tablet |
| LG | 1024–1439px | Notebook |
| XL | 1440–1919px | Desktop |
| XXL | 1920px+ | Ultra-wide |

---

# 16. Tamanhos de Ícones

```css
--icon-xs: 16px;
--icon-sm: 20px;
--icon-md: 24px;
--icon-lg: 32px;
--icon-xl: 48px;
--icon-xxl: 64px;
```

---

# 17. Tokens de Formulário

```css
/* Alturas */
--form-height-sm: 32px;
--form-height-md: 40px;
--form-height-lg: 48px;

/* Padding */
--form-padding-sm: var(--spacing-2) var(--spacing-3);
--form-padding-md: var(--spacing-3) var(--spacing-4);
--form-padding-lg: var(--spacing-4) var(--spacing-5);

/* Fonte */
--form-font-sm: var(--font-size-sm);
--form-font-md: var(--font-size-base);
--form-font-lg: var(--font-size-lg);

/* Label */
--form-label-width: 140px;
--form-label-color: var(--text-secondary);
--form-label-font: var(--font-size-sm);
--form-label-weight: var(--font-weight-medium);
```

---

# 18. Tokens de DataGrid

```css
/* Altura de linha */
--grid-row-height-sm: 36px;
--grid-row-height-md: 44px;
--grid-row-height-lg: 52px;

/* Cores */
--grid-header-bg: var(--surface-card);
--grid-header-color: var(--text-secondary);
--grid-header-font: var(--font-size-sm);

--grid-row-hover: var(--surface-hover);
--grid-row-selected: var(--surface-selected);
--grid-row-color: var(--text-primary);

--grid-border: var(--color-border);
--grid-stripe-bg: rgba(255, 255, 255, 0.02);

/* Célula */
--grid-cell-padding: var(--spacing-3) var(--spacing-4);
--grid-font-size: var(--font-size-sm);
```

---

# 19. Tokens por Componente

## 19.1 Button

```css
--btn-height-sm: 32px;
--btn-height-md: 40px;
--btn-height-lg: 48px;
--btn-font-sm: var(--font-size-sm);
--btn-font-md: var(--font-size-base);
--btn-font-lg: var(--font-size-lg);
--btn-radius: var(--radius-md);
--btn-padding-sm: var(--spacing-3) var(--spacing-4);
--btn-padding-md: var(--spacing-4) var(--spacing-6);
--btn-padding-lg: var(--spacing-5) var(--spacing-8);
--btn-primary-bg: var(--color-primary);
--btn-primary-color: var(--color-white);
--btn-primary-hover: var(--color-primary-hover);
--btn-outline-border: var(--color-primary);
--btn-outline-color: var(--color-primary);
--btn-ghost-hover: var(--surface-hover);
--btn-danger-bg: var(--color-danger);
--btn-danger-color: var(--color-white);
```

## 19.2 Card

```css
--card-bg: var(--surface-card);
--card-border: var(--color-border);
--card-radius: var(--radius-lg);
--card-shadow: var(--shadow-card);
--card-padding: var(--spacing-6);
--card-header-padding: var(--spacing-5) var(--spacing-6);
--card-footer-padding: var(--spacing-4) var(--spacing-6);
```

## 19.3 Modal

```css
--modal-bg: var(--surface-modal);
--modal-radius: var(--radius-xl);
--modal-shadow: var(--shadow-modal);
--modal-padding: var(--spacing-7);
--modal-header-padding: var(--spacing-5) var(--spacing-7);
--modal-footer-padding: var(--spacing-4) var(--spacing-7);
--modal-overlay-bg: rgba(0, 0, 0, 0.6);
--modal-width-sm: 400px;
--modal-width-md: 560px;
--modal-width-lg: 720px;
--modal-width-xl: 960px;
--modal-width-full: calc(100vw - 64px);
```

## 19.4 Toast

```css
--toast-radius: var(--radius-md);
--toast-shadow: var(--shadow-toast);
--toast-padding: var(--spacing-4) var(--spacing-5);
--toast-success-bg: var(--color-success);
--toast-error-bg: var(--color-danger);
--toast-warning-bg: var(--color-warning);
--toast-info-bg: var(--color-info);
```

## 19.5 Sidebar

```css
--sidebar-width: 260px;
--sidebar-collapsed: 64px;
--sidebar-bg: var(--surface-sidebar);
--sidebar-border: var(--color-border);
--sidebar-item-height: 44px;
--sidebar-item-hover: var(--surface-hover);
--sidebar-item-active: var(--surface-selected);
--sidebar-icon-size: var(--icon-md);
--sidebar-font: var(--font-size-sm);
```

## 19.6 Tooltip

```css
--tooltip-bg: var(--surface-tooltip);
--tooltip-color: var(--text-primary);
--tooltip-font: var(--font-size-xs);
--tooltip-radius: var(--radius-sm);
--tooltip-padding: var(--spacing-2) var(--spacing-3);
--tooltip-shadow: var(--shadow-tooltip);
--tooltip-arrow-size: 6px;
```

---

# 20. Temas Oficiais

## 20.1 Tema Dark (Padrão)

```css
:root,
[data-theme="dark"] {
    /* Cores */
    --color-primary: #14b8a6;
    --color-primary-hover: #0d9488;
    --color-primary-active: #0f766e;
    --color-secondary: #6366f1;
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    --color-info: #3b82f6;

    /* Superfícies */
    --surface-page: var(--color-gray-900);
    --surface-card: var(--color-gray-800);
    --surface-modal: var(--color-gray-800);
    --surface-sidebar: var(--color-gray-800);
    --surface-input: var(--color-gray-700);

    /* Texto */
    --text-primary: var(--color-gray-50);
    --text-secondary: var(--color-gray-300);
    --text-disabled: var(--color-gray-500);

    /* Bordas */
    --color-border: rgba(255, 255, 255, 0.12);

    /* Vidro */
    --glass-bg: rgba(255, 255, 255, 0.06);
    --glass-blur: blur(12px);

    /* Gradiente de fundo */
    --bg-gradient: linear-gradient(135deg, #0f172a, #1e293b, #0f172a);
}
```

## 20.2 Tema Light

```css
[data-theme="light"] {
    /* Cores */
    --color-primary: #0d9488;
    --color-primary-hover: #0f766e;
    --color-secondary: #4f46e5;
    --color-success: #059669;
    --color-warning: #d97706;
    --color-danger: #dc2626;
    --color-info: #2563eb;

    /* Superfícies */
    --surface-page: var(--color-gray-50);
    --surface-card: #ffffff;
    --surface-modal: #ffffff;
    --surface-sidebar: #ffffff;
    --surface-input: #ffffff;

    /* Texto */
    --text-primary: var(--color-gray-900);
    --text-secondary: var(--color-gray-600);
    --text-disabled: var(--color-gray-300);

    /* Bordas */
    --color-border: rgba(0, 0, 0, 0.12);
    --color-border-hover: rgba(0, 0, 0, 0.2);

    /* Vidro */
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-blur: blur(12px);

    /* Gradiente */
    --bg-gradient: linear-gradient(135deg, #f0f4f8, #e2e8f0, #cbd5e1);

    /* Sombras (mais suaves no light) */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.1);
}
```

## 20.3 Tema High Contrast

```css
[data-theme="high-contrast"] {
    --color-primary: #2dd4bf;
    --color-primary-hover: #5eead4;
    --color-success: #34d399;
    --color-warning: #fbbf24;
    --color-danger: #f87171;
    --color-info: #60a5fa;

    --surface-page: #000000;
    --surface-card: #0a0a0a;
    --surface-modal: #0a0a0a;
    --surface-sidebar: #0a0a0a;
    --surface-input: #1a1a1a;

    --text-primary: #ffffff;
    --text-secondary: #e0e0e0;
    --text-disabled: #888888;

    --color-border: #ffffff;
    --color-border-focus: #2dd4bf;

    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-blur: blur(4px);

    --bg-gradient: #000000;

    --border-thin: 2px; /* Dobrado para contraste */
    --border-medium: 3px;

    --shadow-sm: 0 1px 2px rgba(255, 255, 255, 0.2);
    --shadow-md: 0 2px 4px rgba(255, 255, 255, 0.3);
    --shadow-lg: 0 4px 8px rgba(255, 255, 255, 0.4);
}
```

---

# 21. Como Criar um Tema

## 21.1 Estrutura de um Tema

Todo tema no FiscalUI é um bloco `[data-theme="nome-do-tema"]` no arquivo `css/themes.css` que sobrescreve tokens.

```css
[data-theme="corporate"] {
    --color-primary: #1e40af;
    --color-primary-hover: #1e3a8a;
    --color-primary-active: #172554;

    --surface-page: #f8fafc;
    --surface-card: #ffffff;
    --surface-sidebar: #1e293b;

    --text-primary: #0f172a;
    --text-secondary: #475569;

    --color-border: #e2e8f0;

    --bg-gradient: linear-gradient(135deg, #f1f5f9, #e2e8f0);
}
```

## 21.2 Regras para Criação de Temas

1. **Nunca criar tokens novos em um tema.** Temas apenas sobrescrevem tokens existentes.
2. **Nunca alterar tokens primitivos.** Altere apenas tokens semânticos.
3. **Todo token deve ter valor em todo tema.** Se um token não for sobrescrito, ele herdará o valor do tema escuro (padrão).
4. **Contraste mínimo 4.5:1** para texto normal, 3:1 para texto grande.
5. **Testar em todos os componentes** antes de disponibilizar o tema.

## 21.3 Registro do Tema

```js
// Registrar o tema no Framework
FiscalUI.theme.register('corporate', {
    name: 'Corporate',
    icon: 'icon-building',
    description: 'Tema corporativo azul'
});

// Aplicar
FiscalUI.setTheme('corporate');
```

---

# 22. Boas Práticas

## 22.1 Para Desenvolvedores de Componentes

```css
/* ✅ Sempre usar tokens */
.component {
    color: var(--text-primary);
    background: var(--surface-card);
    padding: var(--spacing-4);
    border: var(--border-thin) solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--transition-normal);
}

/* ❌ Nunca usar valores literais */
.component {
    color: #f8fafc;
    background: #1e293b;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.35);
    transition: box-shadow 250ms ease-out;
}
```

## 22.2 Para Designers

Use a tabela de tokens como referência ao especificar novos componentes. Nunca especifique cores hex — especifique tokens.

```
❌ "Botão primário: background #14b8a6, hover #0d9488"
✅ "Botão primário: background --color-primary, hover --color-primary-hover"
```

## 22.3 Para Revisores de Código

Checklist de revisão visual:

- [ ] `color` usa `--text-*` e não valor literal
- [ ] `background` usa `--surface-*`, `--color-*` ou `--glass-*`
- [ ] `padding`, `margin`, `gap` usam `--spacing-*`
- [ ] `border-radius` usa `--radius-*`
- [ ] `box-shadow` usa `--shadow-*`
- [ ] `transition` usa `--transition-*` ou `--motion-*` + `--ease-*`
- [ ] `z-index` usa `--z-*`
- [ ] `opacity` usa `--opacity-*`
- [ ] Nenhum `#hex`, `rgb()`, `hsl()` ou valor em px para os casos acima

## 22.4 Para Gestores de Projeto

- Incluir verificação de tokens no code review (automático via Stylelint)
- Manter o arquivo `tokens.css` como referência única de identidade visual
- Alterações de identidade visual envolvem apenas alterar `tokens.css` e `themes.css`
- Toda personalização de cliente/empresa deve ser um novo tema, nunca alteração de componente

---

# 23. Compatibilidade

## 23.1 Browsers

CSS Custom Properties (Design Tokens) são suportados em:

| Browser | Versão mínima |
|---------|--------------|
| Chrome | 49+ |
| Firefox | 31+ |
| Safari | 9.1+ |
| Edge | 15+ |
| Opera | 36+ |
| Samsung Internet | 5+ |

**Não suportado:** IE11 (deliberado — o FiscalUI não tem suporte a IE11).

## 23.2 Fallback para Tokens Indisponíveis

Em situações onde o CSS precisa funcionar mesmo sem tokens (raro), usar fallback:

```css
.button {
    color: var(--text-primary, #f8fafc);
    background: var(--color-primary, #14b8a6);
}
```

## 23.3 Feature Query

Para ambientes que não suportam CSS Variables, usar @supports:

```css
@supports (--custom: property) {
    .button {
        color: var(--text-primary);
    }
}

@supports not (--custom: property) {
    .button {
        color: #f8fafc; /* Fallback */
    }
}
```

---

# 24. Ferramentas

## 24.1 Stylelint Config

```json
{
    "plugins": ["stylelint-declaration-strict-value"],
    "rules": {
        "declaration-strict-value/declaration-strict-value": [
            ["color", "background", "background-color",
             "border", "border-color", "border-radius",
             "box-shadow", "padding", "margin", "gap",
             "font-size", "font-family", "font-weight",
             "line-height", "z-index", "opacity",
             "transition", "animation"],
            {
                "ignoreValues": ["transparent", "inherit", "initial", "unset", "currentColor"],
                "expandShorthand": true
            }
        ]
    }
}
```

## 24.2 Visualizador de Tokens

Uma página HTML que exibe todos os tokens visualmente para referência de designers e desenvolvedores:

```
sprints/tools/tokens-viewer.html
```

---

# 25. Checklist de Implementação

- [ ] `tokens.css` criado com ~186 tokens oficiais
- [ ] `themes.css` criado com Dark, Light, High Contrast
- [ ] Nenhum valor literal existe em arquivos de componente
- [ ] Stylelint configurado para validar uso de tokens
- [ ] Página de visualização de tokens criada
- [ ] Todos os componentes existentes revisados e migrados para tokens
- [ ] Novos componentes só aprovados com uso correto de tokens

---

# 26. Referência Rápida

## 26.1 Tokens Mais Usados

| Token | Valor (dark) | Uso |
|-------|-------------|-----|
| `--color-primary` | `#14b8a6` | Background de botão primário |
| `--text-primary` | `#f8fafc` | Cor de texto principal |
| `--text-secondary` | `#cbd5e1` | Cor de texto secundário |
| `--surface-page` | `#0f172a` | Fundo da página |
| `--surface-card` | `#1e293b` | Fundo de card |
| `--color-border` | `rgba(255,255,255,0.12)` | Borda padrão |
| `--spacing-4` | `12px` | Padding padrão |
| `--radius-md` | `8px` | Border radius padrão |
| `--shadow-sm` | `0 2px 4px rgba(0,0,0,0.35)` | Sombra de card |
| `--font-size-base` | `16px` | Tamanho de fonte base |
| `--transition-normal` | `250ms ease-out` | Transição padrão |
| `--z-modal` | `500` | Z-index de modal |

## 26.2 Mapa Rápido — Categoria → Token

```
Cor       → --color-*
Superfície → --surface-*
Texto     → --text-*
Borda     → --color-border-*
Fonte     → --font-*
Espaço    → --spacing-*
Raio      → --radius-*
Sombra    → --shadow-*
Vidro     → --glass-*
Opacidade → --opacity-*
Z-index   → --z-*
Duração   → --motion-*
Easing    → --ease-*
Transição → --transition-*
Breakpoint → --bp-*
Ícone     → --icon-*
Form      → --form-*
Grid      → --grid-*
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — ~186 tokens documentados, 26 seções |
