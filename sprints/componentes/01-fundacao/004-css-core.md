# FiscalUI Framework

## Documento 004 — CSS Core

**Versão 1.0**

Este documento define toda a arquitetura CSS do FiscalUI Framework. Reset, normalização, utilitários, sistemas de layout, tipografia, bordas, sombras, containers, z-index e suporte a impressão.

---

# Índice

1. Introdução
2. Filosofia CSS
3. Arquitetura de Arquivos
4. Ordem de Carregamento
5. Reset CSS
6. Normalize
7. Tipografia Core
8. Utility Classes
9. Flexbox System
10. Grid System
11. Containers
12. Spacing Utilities
13. Typography Utilities
14. Color Utilities
15. Background Utilities
16. Border Utilities
17. Radius Utilities
18. Shadow Utilities
19. Opacity Utilities
20. Z-Index System
21. Display Utilities
22. Position Utilities
23. Overflow Utilities
24. Cursor Utilities
25. Pointer Events
26. User Select
27. Visibility Utilities
28. Float & Clear
29. Aspect Ratio
30. Object Fit
31. Layers System
32. CSS Custom Properties (Design Tokens)
33. Media Queries
34. Print CSS
35. Reduced Motion
36. High Contrast Mode
37. Dark Mode
38. CSS Animations Core
39. Performance CSS
40. Debugging CSS
41. Boas Práticas
42. Compatibilidade

---

# 1. Introdução

## 1.1 Propósito

O CSS Core é a fundação visual do FiscalUI. Ele estabelece o reset, a normalização, os utilitários e os sistemas de layout que todos os componentes utilizam. Nenhum componente redefine estilos básicos — eles constroem sobre o Core.

## 1.2 Abordagem

```
CSS Core → Define regras fundamentais
   │
   ├── Design Tokens → Fornecem valores
   ├── Utility Classes → Aceleram desenvolvimento
   ├── Layout Systems → Grid e Flex
   └── Component CSS → Estilos específicos
```

O CSS Core não define estilos de componentes. Ele define o solo onde os componentes são construídos.

## 1.3 Filosofia

- **Mobile First:** todo CSS base é para mobile; breakpoints adicionam
- **Performance:** seletores simples, especificidade baixa, sem `!important`
- **Consistência:** tudo referenciado por tokens, nada é valor literal
- **Manutenibilidade:** um arquivo = uma responsabilidade
- **Zero dependências:** sem pré-processadores, sem CSS-in-JS

---

# 2. Filosofia CSS

## 2.1 Princípios

### 2.1.1 Especificidade Mínima

```
❌ .ui-card .ui-card__title .ui-card__title-text { }
✅ .ui-card__title-text { }
```

Nunca aninhar seletores sem necessidade. A especificidade deve ser a mínima necessária para o seletor funcionar.

### 2.1.2 Sem !important

`!important` é proibido em todo o CSS do Framework. Se um seletor precisa de `!important` para funcionar, a especificidade está mal planejada.

### 2.1.3 Naming BEM

```
.ui-btn              → Bloco
.ui-btn__icon        → Elemento
.ui-btn--primary     → Modificador
```

### 2.1.4 Variáveis CSS para Tudo

Nenhum valor literal de cor, tamanho, espaçamento ou animação. Tudo usa `var(--token)`.

### 2.1.5 Transições GPU

Todas as animações e transições usam `transform` e `opacity`. Nunca `width`, `height`, `top`, `left`, `margin` ou `padding`.

## 2.2 Regras de Ouro

| # | Regra | Justificativa |
|---|-------|---------------|
| 1 | Um arquivo = uma responsabilidade | Manutenibilidade |
| 2 | Nada é valor literal | Consistência entre temas |
| 3 | Sem aninhamento desnecessário | Performance de renderização |
| 4 | Mobile First | Menos CSS, mais cobertura |
| 5 | Sem `!important` | Previsibilidade de cascade |
| 6 | Preferir classes a IDs | Reutilização |
| 7 | `transform` e `opacity` para animações | Performance GPU |

---

# 3. Arquitetura de Arquivos

## 3.1 Estrutura de Diretórios CSS

```
css/
├── tokens.css              ← Design Tokens (~186 tokens)
├── core.css                ← Reset, normalize, tipografia base
├── layout.css              ← Grid system, flex, containers
├── utilities.css           ← Utility classes (spacing, color, etc.)
├── components/             ← Estilos de componentes
│   ├── button.css
│   ├── card.css
│   ├── modal.css
│   ├── datagrid.css
│   └── ...
├── themes.css              ← Temas (Light, High Contrast, Glass)
├── motion.css              ← Keyframes, transições
├── icons.css               ← Classes de ícones
├── responsive.css          ← Breakpoints específicos
└── print.css               ← Estilos de impressão
```

## 3.2 Responsabilidade de Cada Arquivo

| Arquivo | Contém | NUNCA contém |
|---------|--------|--------------|
| `tokens.css` | `:root { --var: valor }` | Regras de componentes |
| `core.css` | Reset, normalize, tipografia | Cores específicas |
| `layout.css` | Grid, flex, containers | Estilos de componentes |
| `utilities.css` | Classes .flex, .text-center | Design tokens |
| `components/*.css` | Estilos BEM de componentes | Layout ou reset |
| `themes.css` | `[data-theme] {}` | Novos tokens |
| `motion.css` | `@keyframes`, transições | Cores ou layout |
| `icons.css` | `.icon`, `.icon-sm` | Estilos de botões |
| `responsive.css` | `@media` | Estilos base |
| `print.css` | `@media print` | Estilos de tela |

## 3.3 Tamanhos Estimados

| Arquivo | Tamanho (min) | Gzip |
|---------|--------------|------|
| tokens.css | 4KB | 1.2KB |
| core.css | 6KB | 1.8KB |
| layout.css | 8KB | 2.4KB |
| utilities.css | 12KB | 3.0KB |
| motion.css | 4KB | 1.0KB |
| icons.css | 3KB | 0.8KB |
| themes.css | 8KB | 2.0KB |
| **Total Core** | **~45KB** | **~12KB** |

---

# 4. Ordem de Carregamento

## 4.1 Sequência Obrigatória

A ordem de carregamento no HTML é crítica para o funcionamento correto da cascata:

```html
<!-- 1. Design Tokens (valores base) -->
<link rel="stylesheet" href="css/tokens.css">

<!-- 2. Core (reset, normalize, tipografia) -->
<link rel="stylesheet" href="css/core.css">

<!-- 3. Layout (grid, flex, containers) -->
<link rel="stylesheet" href="css/layout.css">

<!-- 4. Utilities (classes utilitárias) -->
<link rel="stylesheet" href="css/utilities.css">

<!-- 5. Motion (keyframes, transições) -->
<link rel="stylesheet" href="css/motion.css">

<!-- 6. Icons (classes de ícones) -->
<link rel="stylesheet" href="css/icons.css">

<!-- 7. Componentes (ordem alfabética recomendada) -->
<link rel="stylesheet" href="css/components/button.css">
<link rel="stylesheet" href="css/components/card.css">
<link rel="stylesheet" href="css/components/modal.css">
<!-- ... -->

<!-- 8. Temas (sobrescrita de tokens) -->
<link rel="stylesheet" href="css/themes.css">

<!-- 9. Responsivo (overrides por breakpoint) -->
<link rel="stylesheet" href="css/responsive.css">

<!-- 10. Impressão (overrides para print) -->
<link rel="stylesheet" href="css/print.css">
```

## 4.2 Por que essa Ordem?

```
tokens.css    → Define as variáveis
core.css      → Usa as variáveis
layout.css    → Usa as variáveis + core
utilities.css → Usa as variáveis + core
motion.css    → Usa as variáveis
icons.css     → Usa as variáveis
components/*  → Usa tudo acima
themes.css    → Sobrescreve variáveis (maior especificidade)
responsive.css→ Sobrescreve por breakpoint
print.css     → Sobrescreve para impressão
```

---

# 5. Reset CSS

## 5.1 Reset Box Model

```css
*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
```

## 5.2 Reset de Listas

```css
ul, ol {
    list-style: none;
}
```

## 5.3 Reset de Links

```css
a {
    color: inherit;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

## 5.4 Reset de Botões

```css
button {
    border: none;
    background: none;
    cursor: pointer;
    font: inherit;
    color: inherit;
    padding: 0;
}

button:focus-visible {
    outline: 2px solid var(--color-border-focus);
    outline-offset: 2px;
}
```

## 5.5 Reset de Inputs

```css
input,
textarea,
select {
    font: inherit;
    color: inherit;
    border: none;
    background: none;
    outline: none;
}

input:focus,
textarea:focus,
select:focus {
    outline: none;
}
```

## 5.6 Reset de Imagens

```css
img,
svg {
    display: block;
    max-width: 100%;
    height: auto;
}
```

## 5.7 Reset de Tabelas

```css
table {
    border-collapse: collapse;
    border-spacing: 0;
    width: 100%;
}
```

## 5.8 Reset de Fieldset

```css
fieldset {
    border: none;
    padding: 0;
    margin: 0;
}
```

## 5.9 Reset de Headings

```css
h1, h2, h3, h4, h5, h6 {
    font-size: inherit;
    font-weight: inherit;
}
```

## 5.10 Reset de Citações

```css
blockquote, q {
    quotes: none;
}
```

## 5.11 Reset de Form

```css
form {
    margin: 0;
}
```

## 5.12 Reset de HR

```css
hr {
    border: none;
    border-top: var(--border-thin) solid var(--color-border);
    margin: var(--spacing-5) 0;
}
```

## 5.13 Reset de Figure

```css
figure {
    margin: 0;
}
```

## 5.14 Reset de HTML5 Elements

```css
article, aside, details, figcaption, figure,
footer, header, hgroup, main, nav, section {
    display: block;
}
```

## 5.15 Reset de Texto

```css
p {
    margin: 0;
}

strong, b {
    font-weight: var(--font-weight-bold);
}

em, i {
    font-style: italic;
}

small {
    font-size: var(--font-size-sm);
}

mark {
    background: var(--color-warning-bg);
    color: var(--text-primary);
    padding: 0 var(--spacing-1);
    border-radius: var(--radius-sm);
}

code {
    font-family: var(--font-mono);
    font-size: var(--font-size-sm);
    background: var(--surface-hover);
    padding: var(--spacing-1) var(--spacing-2);
    border-radius: var(--radius-sm);
}

pre {
    font-family: var(--font-mono);
    font-size: var(--font-size-sm);
    background: var(--surface-card);
    padding: var(--spacing-4);
    border-radius: var(--radius-md);
    overflow-x: auto;
    white-space: pre-wrap;
}
```

## 5.16 Reset de Abbr

```css
abbr[title] {
    text-decoration: underline dotted;
    cursor: help;
}
```

---

# 6. Normalize

## 6.1 HTML Base

```css
html {
    font-size: 16px;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    text-size-adjust: 100%;
    scroll-behavior: smooth;
}

html[data-theme] {
    background: var(--surface-page);
    color: var(--text-primary);
}
```

## 6.2 Body

```css
body {
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-regular);
    line-height: var(--line-height-normal);
    color: var(--text-primary);
    background: var(--bg-gradient);
    background-attachment: fixed;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    overflow-x: hidden;
}
```

## 6.3 Root Variables Globais

```css
:root {
    /* Definido em tokens.css */
}
```

## 6.4 Selection

```css
::selection {
    background: var(--color-primary);
    color: var(--color-white);
}

::-moz-selection {
    background: var(--color-primary);
    color: var(--color-white);
}
```

## 6.5 Scrollbar

```css
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: var(--color-gray-600);
    border-radius: var(--radius-pill);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--color-gray-500);
}

/* Firefox */
* {
    scrollbar-width: thin;
    scrollbar-color: var(--color-gray-600) transparent;
}
```

## 6.6 Focus

```css
:focus {
    outline: none;
}

:focus-visible {
    outline: 2px solid var(--color-border-focus);
    outline-offset: 2px;
}

/* Remove outline para clique com mouse */
:focus:not(:focus-visible) {
    outline: none;
}
```

## 6.7 Tap Highlight (Mobile)

```css
* {
    -webkit-tap-highlight-color: transparent;
}
```

## 6.8 Print (Normalize)

```css
@media print {
    *,
    *::before,
    *::after {
        background: transparent !important;
        color: #000 !important;
        box-shadow: none !important;
        text-shadow: none !important;
    }

    body {
        font-size: 12pt;
        line-height: 1.5;
    }
}
```

---

# 7. Tipografia Core

## 7.1 Font Face (Inter)

```css
@font-face {
    font-family: 'Inter';
    src: url('../assets/fonts/Inter-Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Inter';
    src: url('../assets/fonts/Inter-Medium.woff2') format('woff2');
    font-weight: 500;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Inter';
    src: url('../assets/fonts/Inter-SemiBold.woff2') format('woff2');
    font-weight: 600;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Inter';
    src: url('../assets/fonts/Inter-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'Inter';
    src: url('../assets/fonts/Inter-Light.woff2') format('woff2');
    font-weight: 300;
    font-style: normal;
    font-display: swap;
}
```

## 7.2 Headings

```css
h1, .h1 {
    font-size: var(--font-size-display);
    font-weight: var(--font-weight-heading, var(--font-weight-semibold));
    line-height: var(--line-height-tight);
    letter-spacing: var(--letter-spacing-tight);
    margin-bottom: var(--spacing-5);
}

h2, .h2 {
    font-size: var(--font-size-xxxl);
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-tight);
    letter-spacing: var(--letter-spacing-tight);
    margin-bottom: var(--spacing-4);
}

h3, .h3 {
    font-size: var(--font-size-xxl);
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-tight);
    margin-bottom: var(--spacing-3);
}

h4, .h4 {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    margin-bottom: var(--spacing-3);
}

h5, .h5 {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    margin-bottom: var(--spacing-2);
}

h6, .h6 {
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    margin-bottom: var(--spacing-2);
    text-transform: uppercase;
    letter-spacing: var(--letter-spacing-wide);
}
```

## 7.3 Body Text

```css
body, p, .body-text {
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-regular);
    line-height: var(--line-height-normal);
}

.text-sm {
    font-size: var(--font-size-sm);
    line-height: var(--line-height-normal);
}

.text-xs {
    font-size: var(--font-size-xs);
    line-height: var(--line-height-relaxed);
}

.text-xxs {
    font-size: var(--font-size-xxs);
    line-height: var(--line-height-relaxed);
}

.text-lg {
    font-size: var(--font-size-lg);
    line-height: var(--line-height-normal);
}

.text-xl {
    font-size: var(--font-size-xl);
    line-height: var(--line-height-normal);
}

.text-xxl {
    font-size: var(--font-size-xxl);
    line-height: var(--line-height-tight);
}
```

## 7.4 Weight Utilities

```css
.font-light { font-weight: var(--font-weight-light); }
.font-regular { font-weight: var(--font-weight-regular); }
.font-medium { font-weight: var(--font-weight-medium); }
.font-semibold { font-weight: var(--font-weight-semibold); }
.font-bold { font-weight: var(--font-weight-bold); }
.font-black { font-weight: var(--font-weight-black); }
```

## 7.5 Alignment Utilities

```css
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-justify { text-align: justify; }
```

## 7.6 Transform Utilities

```css
.text-uppercase { text-transform: uppercase; }
.text-lowercase { text-transform: lowercase; }
.text-capitalize { text-transform: capitalize; }
```

## 7.7 Decoration Utilities

```css
.text-underline { text-decoration: underline; }
.text-line-through { text-decoration: line-through; }
.text-no-decoration { text-decoration: none; }
```

## 7.8 Truncate

```css
.text-truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.text-truncate-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.text-truncate-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
```

## 7.9 Word Break

```css
.text-break {
    word-break: break-word;
    overflow-wrap: break-word;
}

.text-nowrap {
    white-space: nowrap;
}

.text-pre {
    white-space: pre-wrap;
}
```

## 7.10 Color Utilities

```css
.text-primary { color: var(--text-primary); }
.text-secondary { color: var(--text-secondary); }
.text-tertiary { color: var(--text-tertiary); }
.text-disabled { color: var(--text-disabled); }
.text-inverse { color: var(--text-inverse); }
.text-link { color: var(--text-link); }

.text-success { color: var(--color-success); }
.text-warning { color: var(--color-warning); }
.text-danger { color: var(--color-danger); }
.text-info { color: var(--color-info); }
```

---

# 8. Utility Classes

## 8.1 Display

```css
.d-none { display: none; }
.d-inline { display: inline; }
.d-inline-block { display: inline-block; }
.d-block { display: block; }
.d-flex { display: flex; }
.d-inline-flex { display: inline-flex; }
.d-grid { display: grid; }
.d-inline-grid { display: inline-grid; }
.d-table { display: table; }
.d-table-cell { display: table-cell; }
.d-table-row { display: table-row; }
```

## 8.2 Display Responsivo

```css
/* XS */
.d-xs-none { display: none; }
.d-xs-block { display: block; }
.d-xs-flex { display: flex; }

/* SM+ */
@media (min-width: 576px) {
    .d-sm-none { display: none; }
    .d-sm-block { display: block; }
    .d-sm-flex { display: flex; }
}

/* MD+ */
@media (min-width: 768px) {
    .d-md-none { display: none; }
    .d-md-block { display: block; }
    .d-md-flex { display: flex; }
}

/* LG+ */
@media (min-width: 1024px) {
    .d-lg-none { display: none; }
    .d-lg-block { display: block; }
    .d-lg-flex { display: flex; }
}
```

## 8.3 Flex Direction

```css
.flex-row { flex-direction: row; }
.flex-row-reverse { flex-direction: row-reverse; }
.flex-column { flex-direction: column; }
.flex-column-reverse { flex-direction: column-reverse; }
```

## 8.4 Flex Wrap

```css
.flex-wrap { flex-wrap: wrap; }
.flex-nowrap { flex-wrap: nowrap; }
.flex-wrap-reverse { flex-wrap: wrap-reverse; }
```

## 8.5 Justify Content

```css
.justify-start { justify-content: flex-start; }
.justify-end { justify-content: flex-end; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }
.justify-evenly { justify-content: space-evenly; }
```

## 8.6 Align Items

```css
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.items-center { align-items: center; }
.items-baseline { align-items: baseline; }
.items-stretch { align-items: stretch; }
```

## 8.7 Align Self

```css
.self-start { align-self: flex-start; }
.self-end { align-self: flex-end; }
.self-center { align-self: center; }
.self-stretch { align-self: stretch; }
```

## 8.8 Align Content

```css
.content-start { align-content: flex-start; }
.content-end { align-content: flex-end; }
.content-center { align-content: center; }
.content-between { align-content: space-between; }
.content-around { align-content: space-around; }
.content-stretch { align-content: stretch; }
```

## 8.9 Flex

```css
.flex-1 { flex: 1; }
.flex-auto { flex: 1 1 auto; }
.flex-initial { flex: 0 1 auto; }
.flex-none { flex: none; }
```

## 8.10 Gap

```css
.gap-0 { gap: 0; }
.gap-1 { gap: var(--spacing-1); }
.gap-2 { gap: var(--spacing-2); }
.gap-3 { gap: var(--spacing-3); }
.gap-4 { gap: var(--spacing-4); }
.gap-5 { gap: var(--spacing-5); }
.gap-6 { gap: var(--spacing-6); }
.gap-7 { gap: var(--spacing-7); }
.gap-8 { gap: var(--spacing-8); }
.gap-9 { gap: var(--spacing-9); }
.gap-10 { gap: var(--spacing-10); }

.gap-x-1 { column-gap: var(--spacing-1); }
.gap-x-2 { column-gap: var(--spacing-2); }
.gap-x-3 { column-gap: var(--spacing-3); }
.gap-x-4 { column-gap: var(--spacing-4); }
.gap-x-5 { column-gap: var(--spacing-5); }

.gap-y-1 { row-gap: var(--spacing-1); }
.gap-y-2 { row-gap: var(--spacing-2); }
.gap-y-3 { row-gap: var(--spacing-3); }
.gap-y-4 { row-gap: var(--spacing-4); }
.gap-y-5 { row-gap: var(--spacing-5); }
```

## 8.11 Order

```css
.order-first { order: -1; }
.order-last { order: 999; }
.order-0 { order: 0; }
.order-1 { order: 1; }
.order-2 { order: 2; }
.order-3 { order: 3; }
```

---

# 9. Flexbox System

## 9.1 Container Flex

```css
.flex-container {
    display: flex;
}

.flex-container--row {
    flex-direction: row;
}

.flex-container--column {
    flex-direction: column;
}

.flex-container--wrap {
    flex-wrap: wrap;
}

.flex-container--center {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

## 9.2 Flex Item

```css
.flex-item--grow {
    flex: 1;
}

.flex-item--shrink {
    flex: 0 1 auto;
}

.flex-item--fixed {
    flex: none;
}
```

## 9.3 Flex Grid

```css
/* Grid flexível que se adapta ao conteúdo */
.flex-grid {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-5);
}

.flex-grid__item {
    flex: 1 1 280px; /* Mínimo 280px, cresce para ocupar */
    min-width: 0;
}

.flex-grid--2 {
    --flex-grid-min: calc(50% - var(--spacing-5));
}

.flex-grid--3 {
    --flex-grid-min: calc(33.333% - var(--spacing-5));
}

.flex-grid--4 {
    --flex-grid-min: calc(25% - var(--spacing-5));
}
```

## 9.4 Flex Table

```css
/* Layout tipo tabela com flex */
.flex-table {
    display: flex;
    flex-direction: column;
}

.flex-table__row {
    display: flex;
    align-items: center;
    border-bottom: var(--border-thin) solid var(--color-border);
}

.flex-table__cell {
    flex: 1;
    padding: var(--spacing-3) var(--spacing-4);
}

.flex-table__cell--fixed {
    flex: none;
    width: 120px;
}
```

---

# 10. Grid System

## 10.1 Grid Container

```css
.grid {
    display: grid;
    gap: var(--spacing-5);
}

.grid--no-gap {
    gap: 0;
}

.grid--compact {
    gap: var(--spacing-3);
}

.grid--loose {
    gap: var(--spacing-8);
}
```

## 10.2 Grid Columns

```css
.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
.grid-cols-5 { grid-template-columns: repeat(5, 1fr); }
.grid-cols-6 { grid-template-columns: repeat(6, 1fr); }
.grid-cols-7 { grid-template-columns: repeat(7, 1fr); }
.grid-cols-8 { grid-template-columns: repeat(8, 1fr); }
.grid-cols-9 { grid-template-columns: repeat(9, 1fr); }
.grid-cols-10 { grid-template-columns: repeat(10, 1fr); }
.grid-cols-11 { grid-template-columns: repeat(11, 1fr); }
.grid-cols-12 { grid-template-columns: repeat(12, 1fr); }
```

## 10.3 Grid Column Span

```css
.col-span-1 { grid-column: span 1; }
.col-span-2 { grid-column: span 2; }
.col-span-3 { grid-column: span 3; }
.col-span-4 { grid-column: span 4; }
.col-span-5 { grid-column: span 5; }
.col-span-6 { grid-column: span 6; }
.col-span-7 { grid-column: span 7; }
.col-span-8 { grid-column: span 8; }
.col-span-9 { grid-column: span 9; }
.col-span-10 { grid-column: span 10; }
.col-span-11 { grid-column: span 11; }
.col-span-12 { grid-column: span 12; }

.col-span-full { grid-column: 1 / -1; }
```

## 10.4 Grid Row Span

```css
.row-span-1 { grid-row: span 1; }
.row-span-2 { grid-row: span 2; }
.row-span-3 { grid-row: span 3; }
.row-span-4 { grid-row: span 4; }
```

## 10.5 Grid Auto Flow

```css
.grid-flow-row { grid-auto-flow: row; }
.grid-flow-col { grid-auto-flow: column; }
.grid-flow-dense { grid-auto-flow: dense; }
.grid-flow-row-dense { grid-auto-flow: row dense; }
.grid-flow-col-dense { grid-auto-flow: column dense; }
```

## 10.6 Grid Auto Columns/Rows

```css
.grid-auto-cols-min { grid-auto-columns: min-content; }
.grid-auto-cols-max { grid-auto-columns: max-content; }
.grid-auto-cols-fr { grid-auto-columns: 1fr; }

.grid-auto-rows-min { grid-auto-rows: min-content; }
.grid-auto-rows-max { grid-auto-rows: max-content; }
.grid-auto-rows-fr { grid-auto-rows: 1fr; }
```

## 10.7 Grid Responsivo

```css
/* Mobile padrão: 1 coluna */
.grid {
    grid-template-columns: 1fr;
}

/* SM+ */
@media (min-width: 576px) {
    .grid-sm-2 { grid-template-columns: repeat(2, 1fr); }
    .grid-sm-3 { grid-template-columns: repeat(3, 1fr); }
}

/* MD+ */
@media (min-width: 768px) {
    .grid-md-2 { grid-template-columns: repeat(2, 1fr); }
    .grid-md-3 { grid-template-columns: repeat(3, 1fr); }
    .grid-md-4 { grid-template-columns: repeat(4, 1fr); }
}

/* LG+ */
@media (min-width: 1024px) {
    .grid-lg-2 { grid-template-columns: repeat(2, 1fr); }
    .grid-lg-3 { grid-template-columns: repeat(3, 1fr); }
    .grid-lg-4 { grid-template-columns: repeat(4, 1fr); }
    .grid-lg-6 { grid-template-columns: repeat(6, 1fr); }
    .grid-lg-12 { grid-template-columns: repeat(12, 1fr); }
}
```

## 10.8 Grid Areas

```css
.grid-areas {
    display: grid;
    gap: var(--spacing-5);
}

.grid-areas--sidebar {
    grid-template-areas:
        "sidebar header"
        "sidebar content"
        "sidebar footer";
    grid-template-columns: 260px 1fr;
    grid-template-rows: auto 1fr auto;
}

.grid-areas--dashboard {
    grid-template-areas:
        "header header header"
        "kpi1 kpi2 kpi3"
        "chart1 chart2 chart2"
        "table table table";
    grid-template-columns: repeat(3, 1fr);
}

.area-header { grid-area: header; }
.area-sidebar { grid-area: sidebar; }
.area-content { grid-area: content; }
.area-footer { grid-area: footer; }
.area-kpi1 { grid-area: kpi1; }
.area-kpi2 { grid-area: kpi2; }
.area-kpi3 { grid-area: kpi3; }
.area-chart1 { grid-area: chart1; }
.area-chart2 { grid-area: chart2; }
.area-table { grid-area: table; }
```

## 10.9 Grid Auto-fill

```css
/* Grid que se adapta automaticamente */
.grid-auto {
    display: grid;
    gap: var(--spacing-5);
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.grid-auto--sm {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
}

.grid-auto--lg {
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
}

.grid-auto--cards {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}

.grid-auto--launchpad {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
}
```

## 10.10 Grid Alignment

```css
/* Justify Items */
.justify-items-start { justify-items: start; }
.justify-items-end { justify-items: end; }
.justify-items-center { justify-items: center; }
.justify-items-stretch { justify-items: stretch; }

/* Align Items */
.align-items-start { align-items: start; }
.align-items-end { align-items: end; }
.align-items-center { align-items: center; }
.align-items-stretch { align-items: stretch; }

/* Place Items */
.place-items-center {
    place-items: center;
}

/* Justify Content */
.justify-content-start { justify-content: start; }
.justify-content-end { justify-content: end; }
.justify-content-center { justify-content: center; }
.justify-content-between { justify-content: space-between; }
.justify-content-around { justify-content: space-around; }
.justify-content-evenly { justify-content: space-evenly; }

/* Align Content */
.align-content-start { align-content: start; }
.align-content-end { align-content: end; }
.align-content-center { align-content: center; }
.align-content-between { align-content: space-between; }
.align-content-around { align-content: space-around; }
.align-content-stretch { align-content: stretch; }
```

---

# 11. Containers

## 11.1 Container Padrão

```css
.container {
    width: 100%;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--spacing-5);
    padding-right: var(--spacing-5);
}
```

## 11.2 Container Fluid

```css
.container-fluid {
    width: 100%;
    padding-left: var(--spacing-5);
    padding-right: var(--spacing-5);
}
```

## 11.3 Container Compact

```css
.container-compact {
    width: 100%;
    max-width: 480px;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--spacing-5);
    padding-right: var(--spacing-5);
}
```

## 11.4 Container Narrow

```css
.container-narrow {
    width: 100%;
    max-width: 720px;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--spacing-5);
    padding-right: var(--spacing-5);
}
```

## 11.5 Container Wide

```css
.container-wide {
    width: 100%;
    max-width: 1440px;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--spacing-5);
    padding-right: var(--spacing-5);
}
```

## 11.6 Container Full

```css
.container-full {
    width: 100%;
    max-width: 100%;
}
```

## 11.7 Container Responsivo

```css
.container {
    width: 100%;
    padding-left: var(--spacing-4);
    padding-right: var(--spacing-4);
}

@media (min-width: 576px) {
    .container {
        max-width: 540px;
        padding-left: var(--spacing-5);
        padding-right: var(--spacing-5);
    }
}

@media (min-width: 768px) {
    .container {
        max-width: 720px;
    }
}

@media (min-width: 1024px) {
    .container {
        max-width: 960px;
    }
}

@media (min-width: 1280px) {
    .container {
        max-width: 1140px;
    }
}

@media (min-width: 1536px) {
    .container {
        max-width: 1320px;
    }
}
```

## 11.8 Section Container

```css
.section {
    padding-top: var(--spacing-10);
    padding-bottom: var(--spacing-10);
}

.section--sm {
    padding-top: var(--spacing-5);
    padding-bottom: var(--spacing-5);
}

.section--lg {
    padding-top: var(--spacing-14);
    padding-bottom: var(--spacing-14);
}

.section--xl {
    padding-top: var(--spacing-16);
    padding-bottom: var(--spacing-16);
}
```

---

# 12. Spacing Utilities

## 12.1 Padding

```css
.p-0 { padding: 0; }
.p-1 { padding: var(--spacing-1); }
.p-2 { padding: var(--spacing-2); }
.p-3 { padding: var(--spacing-3); }
.p-4 { padding: var(--spacing-4); }
.p-5 { padding: var(--spacing-5); }
.p-6 { padding: var(--spacing-6); }
.p-7 { padding: var(--spacing-7); }
.p-8 { padding: var(--spacing-8); }
.p-9 { padding: var(--spacing-9); }
.p-10 { padding: var(--spacing-10); }

.pt-0 { padding-top: 0; }
.pt-1 { padding-top: var(--spacing-1); }
.pt-2 { padding-top: var(--spacing-2); }
.pt-3 { padding-top: var(--spacing-3); }
.pt-4 { padding-top: var(--spacing-4); }
.pt-5 { padding-top: var(--spacing-5); }
.pt-6 { padding-top: var(--spacing-6); }
.pt-7 { padding-top: var(--spacing-7); }
.pt-8 { padding-top: var(--spacing-8); }

.pb-0 { padding-bottom: 0; }
.pb-1 { padding-bottom: var(--spacing-1); }
.pb-2 { padding-bottom: var(--spacing-2); }
.pb-3 { padding-bottom: var(--spacing-3); }
.pb-4 { padding-bottom: var(--spacing-4); }
.pb-5 { padding-bottom: var(--spacing-5); }
.pb-6 { padding-bottom: var(--spacing-6); }
.pb-7 { padding-bottom: var(--spacing-7); }
.pb-8 { padding-bottom: var(--spacing-8); }

.pl-0 { padding-left: 0; }
.pl-1 { padding-left: var(--spacing-1); }
.pl-2 { padding-left: var(--spacing-2); }
.pl-3 { padding-left: var(--spacing-3); }
.pl-4 { padding-left: var(--spacing-4); }
.pl-5 { padding-left: var(--spacing-5); }
.pl-6 { padding-left: var(--spacing-6); }

.pr-0 { padding-right: 0; }
.pr-1 { padding-right: var(--spacing-1); }
.pr-2 { padding-right: var(--spacing-2); }
.pr-3 { padding-right: var(--spacing-3); }
.pr-4 { padding-right: var(--spacing-4); }
.pr-5 { padding-right: var(--spacing-5); }
.pr-6 { padding-right: var(--spacing-6); }

.px-0 { padding-left: 0; padding-right: 0; }
.px-1 { padding-left: var(--spacing-1); padding-right: var(--spacing-1); }
.px-2 { padding-left: var(--spacing-2); padding-right: var(--spacing-2); }
.px-3 { padding-left: var(--spacing-3); padding-right: var(--spacing-3); }
.px-4 { padding-left: var(--spacing-4); padding-right: var(--spacing-4); }
.px-5 { padding-left: var(--spacing-5); padding-right: var(--spacing-5); }
.px-6 { padding-left: var(--spacing-6); padding-right: var(--spacing-6); }

.py-0 { padding-top: 0; padding-bottom: 0; }
.py-1 { padding-top: var(--spacing-1); padding-bottom: var(--spacing-1); }
.py-2 { padding-top: var(--spacing-2); padding-bottom: var(--spacing-2); }
.py-3 { padding-top: var(--spacing-3); padding-bottom: var(--spacing-3); }
.py-4 { padding-top: var(--spacing-4); padding-bottom: var(--spacing-4); }
.py-5 { padding-top: var(--spacing-5); padding-bottom: var(--spacing-5); }
.py-6 { padding-top: var(--spacing-6); padding-bottom: var(--spacing-6); }
.py-7 { padding-top: var(--spacing-7); padding-bottom: var(--spacing-7); }
.py-8 { padding-top: var(--spacing-8); padding-bottom: var(--spacing-8); }
```

## 12.2 Margin

```css
.m-0 { margin: 0; }
.m-1 { margin: var(--spacing-1); }
.m-2 { margin: var(--spacing-2); }
.m-3 { margin: var(--spacing-3); }
.m-4 { margin: var(--spacing-4); }
.m-5 { margin: var(--spacing-5); }
.m-6 { margin: var(--spacing-6); }
.m-7 { margin: var(--spacing-7); }
.m-8 { margin: var(--spacing-8); }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: var(--spacing-1); }
.mt-2 { margin-top: var(--spacing-2); }
.mt-3 { margin-top: var(--spacing-3); }
.mt-4 { margin-top: var(--spacing-4); }
.mt-5 { margin-top: var(--spacing-5); }
.mt-6 { margin-top: var(--spacing-6); }
.mt-7 { margin-top: var(--spacing-7); }
.mt-8 { margin-top: var(--spacing-8); }
.mt-auto { margin-top: auto; }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: var(--spacing-1); }
.mb-2 { margin-bottom: var(--spacing-2); }
.mb-3 { margin-bottom: var(--spacing-3); }
.mb-4 { margin-bottom: var(--spacing-4); }
.mb-5 { margin-bottom: var(--spacing-5); }
.mb-6 { margin-bottom: var(--spacing-6); }
.mb-7 { margin-bottom: var(--spacing-7); }
.mb-8 { margin-bottom: var(--spacing-8); }
.mb-auto { margin-bottom: auto; }

.ml-0 { margin-left: 0; }
.ml-1 { margin-left: var(--spacing-1); }
.ml-2 { margin-left: var(--spacing-2); }
.ml-3 { margin-left: var(--spacing-3); }
.ml-4 { margin-left: var(--spacing-4); }
.ml-5 { margin-left: var(--spacing-5); }
.ml-auto { margin-left: auto; }

.mr-0 { margin-right: 0; }
.mr-1 { margin-right: var(--spacing-1); }
.mr-2 { margin-right: var(--spacing-2); }
.mr-3 { margin-right: var(--spacing-3); }
.mr-4 { margin-right: var(--spacing-4); }
.mr-5 { margin-right: var(--spacing-5); }
.mr-auto { margin-right: auto; }

.mx-0 { margin-left: 0; margin-right: 0; }
.mx-1 { margin-left: var(--spacing-1); margin-right: var(--spacing-1); }
.mx-2 { margin-left: var(--spacing-2); margin-right: var(--spacing-2); }
.mx-3 { margin-left: var(--spacing-3); margin-right: var(--spacing-3); }
.mx-4 { margin-left: var(--spacing-4); margin-right: var(--spacing-4); }
.mx-5 { margin-left: var(--spacing-5); margin-right: var(--spacing-5); }
.mx-auto { margin-left: auto; margin-right: auto; }

.my-0 { margin-top: 0; margin-bottom: 0; }
.my-1 { margin-top: var(--spacing-1); margin-bottom: var(--spacing-1); }
.my-2 { margin-top: var(--spacing-2); margin-bottom: var(--spacing-2); }
.my-3 { margin-top: var(--spacing-3); margin-bottom: var(--spacing-3); }
.my-4 { margin-top: var(--spacing-4); margin-bottom: var(--spacing-4); }
.my-5 { margin-top: var(--spacing-5); margin-bottom: var(--spacing-5); }
.my-auto { margin-top: auto; margin-bottom: auto; }
```

## 12.3 Width

```css
.w-full { width: 100%; }
.w-auto { width: auto; }
.w-25 { width: 25%; }
.w-33 { width: 33.333%; }
.w-50 { width: 50%; }
.w-66 { width: 66.666%; }
.w-75 { width: 75%; }

.w-screen { width: 100vw; }
.w-min { width: min-content; }
.w-max { width: max-content; }
.w-fit { width: fit-content; }
```

## 12.4 Max Width

```css
.max-w-none { max-width: none; }
.max-w-xs { max-width: 320px; }
.max-w-sm { max-width: 480px; }
.max-w-md { max-width: 640px; }
.max-w-lg { max-width: 768px; }
.max-w-xl { max-width: 1024px; }
.max-w-2xl { max-width: 1280px; }
.max-w-full { max-width: 100%; }
```

## 12.5 Height

```css
.h-full { height: 100%; }
.h-auto { height: auto; }
.h-screen { height: 100vh; }
.h-min { height: min-content; }
.h-max { height: max-content; }
```

## 12.6 Min Height

```css
.min-h-0 { min-height: 0; }
.min-h-screen { min-height: 100vh; }
.min-h-full { min-height: 100%; }
```

---

# 13. Background Utilities

```css
/* Background color */
.bg-primary { background: var(--color-primary); }
.bg-primary-light { background: var(--color-primary-light); }
.bg-secondary { background: var(--color-secondary); }
.bg-secondary-light { background: var(--color-secondary-light); }
.bg-success { background: var(--color-success); }
.bg-success-bg { background: var(--color-success-bg); }
.bg-warning { background: var(--color-warning); }
.bg-warning-bg { background: var(--color-warning-bg); }
.bg-danger { background: var(--color-danger); }
.bg-danger-bg { background: var(--color-danger-bg); }
.bg-info { background: var(--color-info); }
.bg-info-bg { background: var(--color-info-bg); }

.bg-page { background: var(--surface-page); }
.bg-card { background: var(--surface-card); }
.bg-modal { background: var(--surface-modal); }
.bg-input { background: var(--surface-input); }

.bg-transparent { background: transparent; }
.bg-white { background: var(--color-white); }
.bg-black { background: var(--color-black); }
.bg-current { background: currentColor; }

.bg-none { background: none; }

.bg-gradient {
    background: var(--bg-gradient);
}

/* Background size */
.bg-cover { background-size: cover; }
.bg-contain { background-size: contain; }

/* Background position */
.bg-center { background-position: center; }
.bg-top { background-position: top; }
.bg-bottom { background-position: bottom; }
.bg-left { background-position: left; }
.bg-right { background-position: right; }

/* Background repeat */
.bg-no-repeat { background-repeat: no-repeat; }
.bg-repeat { background-repeat: repeat; }
.bg-repeat-x { background-repeat: repeat-x; }
.bg-repeat-y { background-repeat: repeat-y; }

/* Background attachment */
.bg-fixed { background-attachment: fixed; }
.bg-scroll { background-attachment: scroll; }
```

---

# 14. Border Utilities

```css
/* Border */
.border { border: var(--border-thin) solid var(--color-border); }
.border-0 { border: none; }
.border-2 { border: var(--border-medium) solid var(--color-border); }
.border-4 { border: var(--border-thick) solid var(--color-border); }

.border-t { border-top: var(--border-thin) solid var(--color-border); }
.border-b { border-bottom: var(--border-thin) solid var(--color-border); }
.border-l { border-left: var(--border-thin) solid var(--color-border); }
.border-r { border-right: var(--border-thin) solid var(--color-border); }

.border-t-0 { border-top: none; }
.border-b-0 { border-bottom: none; }
.border-l-0 { border-left: none; }
.border-r-0 { border-right: none; }

/* Border color */
.border-primary { border-color: var(--color-primary); }
.border-success { border-color: var(--color-success); }
.border-warning { border-color: var(--color-warning); }
.border-danger { border-color: var(--color-danger); }
.border-info { border-color: var(--color-info); }
.border-transparent { border-color: transparent; }
```

---

# 15. Radius Utilities

```css
.rounded-none { border-radius: var(--radius-none); }
.rounded-sm { border-radius: var(--radius-sm); }
.rounded-md { border-radius: var(--radius-md); }
.rounded-lg { border-radius: var(--radius-lg); }
.rounded-xl { border-radius: var(--radius-xl); }
.rounded-2xl { border-radius: var(--radius-2xl); }
.rounded-full { border-radius: var(--radius-rounded); }
.rounded-pill { border-radius: var(--radius-pill); }

.rounded-t-none { border-top-left-radius: 0; border-top-right-radius: 0; }
.rounded-b-none { border-bottom-left-radius: 0; border-bottom-right-radius: 0; }
.rounded-l-none { border-top-left-radius: 0; border-bottom-left-radius: 0; }
.rounded-r-none { border-top-right-radius: 0; border-bottom-right-radius: 0; }
```

---

# 16. Shadow Utilities

```css
.shadow-none { box-shadow: none; }
.shadow-xs { box-shadow: var(--shadow-xs); }
.shadow-sm { box-shadow: var(--shadow-sm); }
.shadow-md { box-shadow: var(--shadow-md); }
.shadow-lg { box-shadow: var(--shadow-lg); }
.shadow-xl { box-shadow: var(--shadow-xl); }
.shadow-2xl { box-shadow: var(--shadow-2xl); }
.shadow-glass { box-shadow: var(--shadow-glass); }
.shadow-glow { box-shadow: var(--shadow-glow); }

.shadow-card { box-shadow: var(--shadow-card); }
.shadow-modal { box-shadow: var(--shadow-modal); }
.shadow-dropdown { box-shadow: var(--shadow-dropdown); }
.shadow-toast { box-shadow: var(--shadow-toast); }
```

---

# 17. Opacity Utilities

```css
.opacity-0 { opacity: var(--opacity-0); }
.opacity-25 { opacity: var(--opacity-25); }
.opacity-50 { opacity: var(--opacity-50); }
.opacity-75 { opacity: var(--opacity-75); }
.opacity-90 { opacity: var(--opacity-90); }
.opacity-100 { opacity: var(--opacity-100); }
```

---

# 18. Z-Index System

## 18.1 Core Z-Index

```css
.z-base { z-index: var(--z-base); }
.z-dropdown { z-index: var(--z-dropdown); }
.z-sticky { z-index: var(--z-sticky); }
.z-fixed { z-index: var(--z-fixed); }
.z-modal-backdrop { z-index: var(--z-modal-backdrop); }
.z-modal { z-index: var(--z-modal); }
.z-popover { z-index: var(--z-popover); }
.z-toast { z-index: var(--z-toast); }
.z-tooltip { z-index: var(--z-tooltip); }
.z-fullscreen { z-index: var(--z-fullscreen); }
```

## 18.2 Valores dos Tokens

```css
:root {
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
}
```

## 18.3 Regras de Uso Z-Index

1. Nunca usar `z-index` com valor literal
2. Usar tokens exclusivamente
3. Deixar espaços entre os níveis (50, 150, 250) para variações
4. Nenhum componente pode definir z-index sem usar token

---

# 19. Display Utilities

```css
.d-none { display: none; }
.d-inline { display: inline; }
.d-inline-block { display: inline-block; }
.d-block { display: block; }
.d-flex { display: flex; }
.d-inline-flex { display: inline-flex; }
.d-grid { display: grid; }
.d-inline-grid { display: inline-grid; }
.d-table { display: table; }
.d-table-cell { display: table-cell; }
.d-table-row { display: table-row; }
.d-contents { display: contents; }
.d-hidden { display: none; }
```

### Visible/Hidden

```css
.visible { visibility: visible; }
.invisible { visibility: hidden; }
```

---

# 20. Position Utilities

```css
.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }
.sticky { position: sticky; }
.static { position: static; }

/* Inset (top, right, bottom, left) */
.inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
.inset-x-0 { left: 0; right: 0; }
.inset-y-0 { top: 0; bottom: 0; }
.top-0 { top: 0; }
.right-0 { right: 0; }
.bottom-0 { bottom: 0; }
.left-0 { left: 0; }

.top-auto { top: auto; }
.right-auto { right: auto; }
.bottom-auto { bottom: auto; }
.left-auto { left: auto; }
```

---

# 21. Overflow Utilities

```css
.overflow-auto { overflow: auto; }
.overflow-hidden { overflow: hidden; }
.overflow-visible { overflow: visible; }
.overflow-scroll { overflow: scroll; }
.overflow-x-auto { overflow-x: auto; }
.overflow-y-auto { overflow-y: auto; }
.overflow-x-hidden { overflow-x: hidden; }
.overflow-y-hidden { overflow-y: hidden; }
.overflow-x-scroll { overflow-x: scroll; }
.overflow-y-scroll { overflow-y: scroll; }
```

---

# 22. Cursor Utilities

```css
.cursor-auto { cursor: auto; }
.cursor-default { cursor: default; }
.cursor-pointer { cursor: pointer; }
.cursor-wait { cursor: wait; }
.cursor-text { cursor: text; }
.cursor-move { cursor: move; }
.cursor-not-allowed { cursor: not-allowed; }
.cursor-grab { cursor: grab; }
.cursor-grabbing { cursor: grabbing; }
.cursor-zoom-in { cursor: zoom-in; }
.cursor-zoom-out { cursor: zoom-out; }
```

---

# 23. Pointer Events

```css
.pointer-events-none { pointer-events: none; }
.pointer-events-auto { pointer-events: auto; }
```

---

# 24. User Select

```css
.select-none { user-select: none; }
.select-text { user-select: text; }
.select-all { user-select: all; }
.select-auto { user-select: auto; }
```

---

# 25. Visibility Utilities

```css
.visible { visibility: visible; }
.invisible { visibility: hidden; }
.collapse { visibility: collapse; }
```

---

# 26. Float & Clear

```css
.float-right { float: right; }
.float-left { float: left; }
.float-none { float: none; }

.clearfix::after {
    content: '';
    display: table;
    clear: both;
}

.clear-left { clear: left; }
.clear-right { clear: right; }
.clear-both { clear: both; }
```

---

# 27. Aspect Ratio

```css
.aspect-square { aspect-ratio: 1 / 1; }
.aspect-video { aspect-ratio: 16 / 9; }
.aspect-portrait { aspect-ratio: 3 / 4; }
.aspect-wide { aspect-ratio: 21 / 9; }
.aspect-auto { aspect-ratio: auto; }
```

---

# 28. Object Fit

```css
.object-contain { object-fit: contain; }
.object-cover { object-fit: cover; }
.object-fill { object-fit: fill; }
.object-none { object-fit: none; }
.object-scale-down { object-fit: scale-down; }
```

---

# 29. Layers System

## 29.1 Contextos de Empilhamento

O FiscalUI gerencia contextos de empilhamento através de classes específicas para cada camada da interface.

```css
/* Layer: App */
.layer-app {
    position: relative;
    z-index: var(--z-base);
}

/* Layer: Sidebar */
.layer-sidebar {
    position: fixed;
    z-index: var(--z-fixed);
}

/* Layer: Topbar */
.layer-topbar {
    position: sticky;
    top: 0;
    z-index: var(--z-sticky);
}

/* Layer: Modal Backdrop */
.layer-modal-backdrop {
    position: fixed;
    z-index: var(--z-modal-backdrop);
}

/* Layer: Modal */
.layer-modal {
    position: fixed;
    z-index: var(--z-modal);
}

/* Layer: Toast */
.layer-toast {
    position: fixed;
    z-index: var(--z-toast);
}

/* Layer: Tooltip */
.layer-tooltip {
    position: fixed;
    z-index: var(--z-tooltip);
}

/* Layer: Fullscreen */
.layer-fullscreen {
    position: fixed;
    z-index: var(--z-fullscreen);
}
```

## 29.2 Mapa de Camadas

```
Layer      Elementos                   Z-index
─────      ─────────                   ──────
Base       App, conteúdo               0
Sidebar    Sidebar fixa                300
Topbar     Topbar sticky               200
Dropdown   Menus, autocomplete         100
Modal      Modal + backdrop            400-500
Popover    Popover, context menu       600
Toast      Toast, notificações         700
Tooltip    Tooltip, dicas              800
Fullscreen Tela cheia, loading         900
```

---

# 30. CSS Custom Properties (Design Tokens)

## 30.1 Categoria: Colors

```css
:root {
    /* Brand */
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

    /* Semantic */
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

    /* Neutral */
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
}
```

## 30.2 Categoria: Typography

```css
:root {
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

    --font-size-hero: 3rem;
    --font-size-display: 2.25rem;
    --font-size-xxxl: 1.875rem;
    --font-size-xxl: 1.5rem;
    --font-size-xl: 1.25rem;
    --font-size-lg: 1.125rem;
    --font-size-base: 1rem;
    --font-size-sm: 0.875rem;
    --font-size-xs: 0.75rem;
    --font-size-xxs: 0.625rem;

    --font-weight-light: 300;
    --font-weight-regular: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    --font-weight-black: 900;

    --line-height-tight: 1.15;
    --line-height-normal: 1.4;
    --line-height-relaxed: 1.6;
    --line-height-loose: 1.8;

    --letter-spacing-tight: -0.025em;
    --letter-spacing-wide: 0.05em;
}
```

## 30.3 Categoria: Spacing

```css
:root {
    --spacing-0: 0px;
    --spacing-1: 2px;
    --spacing-2: 4px;
    --spacing-3: 8px;
    --spacing-4: 12px;
    --spacing-5: 16px;
    --spacing-6: 20px;
    --spacing-7: 24px;
    --spacing-8: 32px;
    --spacing-9: 40px;
    --spacing-10: 48px;
    --spacing-12: 64px;
    --spacing-14: 80px;
    --spacing-16: 96px;
    --spacing-20: 128px;

    /* Aliases (compatibilidade) */
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
}
```

## 30.4 Categoria: Border & Radius

```css
:root {
    --border-none: 0px;
    --border-thin: 1px;
    --border-medium: 2px;
    --border-thick: 4px;

    --radius-none: 0px;
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-2xl: 24px;
    --radius-rounded: 9999px;
    --radius-pill: 9999px;
}
```

## 30.5 Categoria: Shadows

```css
:root {
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.35);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.45);
    --shadow-xl: 0 12px 40px rgba(0, 0, 0, 0.5);
    --shadow-2xl: 0 24px 64px rgba(0, 0, 0, 0.6);
    --shadow-glass: 0 4px 24px rgba(20, 184, 166, 0.08);
    --shadow-glow: 0 0 30px rgba(20, 184, 166, 0.12);
}
```

## 30.6 Categoria: Z-Index

```css
:root {
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
}
```

## 30.7 Categoria: Opacity

```css
:root {
    --opacity-0: 0;
    --opacity-25: 0.25;
    --opacity-50: 0.5;
    --opacity-75: 0.75;
    --opacity-90: 0.9;
    --opacity-100: 1;
}
```

## 30.8 Categoria: Motion

```css
:root {
    --motion-instant: 100ms;
    --motion-fast: 150ms;
    --motion-normal: 250ms;
    --motion-smooth: 350ms;
    --motion-slow: 500ms;

    --ease-linear: cubic-bezier(0, 0, 1, 1);
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

    --transition-fast: var(--motion-fast) var(--ease-out);
    --transition-normal: var(--motion-normal) var(--ease-out);
    --transition-smooth: var(--motion-smooth) var(--ease-out);
    --transition-spring: var(--motion-smooth) var(--ease-spring);
}
```

## 30.9 Categoria: Breakpoints

```css
:root {
    --bp-xs: 0px;
    --bp-sm: 576px;
    --bp-md: 768px;
    --bp-lg: 1024px;
    --bp-xl: 1440px;
    --bp-xxl: 1920px;
}
```

---

# 31. Media Queries

## 31.1 Breakpoints Oficiais

```css
/* XS: 0-575px (smartphone) — padrão mobile first */
/* SM: 576-767px (smartphone grande) */
@media (min-width: 576px) { }

/* MD: 768-1023px (tablet) */
@media (min-width: 768px) { }

/* LG: 1024-1439px (notebook) */
@media (min-width: 1024px) { }

/* XL: 1440-1919px (desktop) */
@media (min-width: 1440px) { }

/* XXL: 1920px+ (ultrawide) */
@media (min-width: 1920px) { }
```

## 31.2 Range Queries

```css
/* Apenas mobile (XS + SM) */
@media (max-width: 767px) { }

/* Apenas tablet (MD) */
@media (min-width: 768px) and (max-width: 1023px) { }

/* Apenas desktop (LG + XL + XXL) */
@media (min-width: 1024px) { }

/* Apenas notebook (LG) */
@media (min-width: 1024px) and (max-width: 1439px) { }

/* Apenas desktop grande (XL) */
@media (min-width: 1440px) and (max-width: 1919px) { }

/* Apenas ultrawide (XXL) */
@media (min-width: 1920px) { }
```

## 31.3 Feature Queries

```css
/* Prefers color scheme */
@media (prefers-color-scheme: dark) { }
@media (prefers-color-scheme: light) { }

/* Prefers reduced motion */
@media (prefers-reduced-motion: reduce) { }
@media (prefers-reduced-motion: no-preference) { }

/* Prefers contrast */
@media (prefers-contrast: more) { }
@media (prefers-contrast: less) { }

/* Forced colors (Windows High Contrast) */
@media (forced-colors: active) { }

/* Pointer */
@media (pointer: coarse) { }       /* Touch */
@media (pointer: fine) { }         /* Mouse */
@media (hover: hover) { }          /* Hover disponível */
@media (hover: none) { }           /* Touch, sem hover */

/* Orientation */
@media (orientation: portrait) { }
@media (orientation: landscape) { }

/* Resolution */
@media (min-resolution: 192dpi) { }   /* Retina */

/* Supports */
@supports (display: grid) { }
@supports (backdrop-filter: blur(1px)) { }
@supports not (display: grid) { }
```

---

# 32. Print CSS

## 32.1 Estilos de Impressão

```css
@media print {
    /* Reset geral */
    *,
    *::before,
    *::after {
        background: transparent !important;
        color: #000 !important;
        box-shadow: none !important;
        text-shadow: none !important;
        border-color: #000 !important;
    }

    /* Esconder elementos de UI */
    .no-print,
    .sidebar,
    .topbar,
    .toast-container,
    .modal-backdrop,
    .modal,
    .tooltip,
    .dropdown,
    .context-menu,
    .theme-switcher,
    .btn,
    button:not(.print-btn),
    .toolbar,
    .status-bar,
    nav,
    footer {
        display: none !important;
    }

    /* Mostrar apenas conteúdo */
    .print-only {
        display: block !important;
    }

    /* Ajustes de página */
    body {
        font-size: 12pt;
        line-height: 1.5;
        color: #000;
        background: #fff !important;
    }

    h1 { font-size: 24pt; }
    h2 { font-size: 18pt; }
    h3 { font-size: 14pt; }

    /* Links */
    a {
        text-decoration: underline;
    }

    a[href]::after {
        content: " (" attr(href) ")";
        font-size: 0.8em;
        font-weight: normal;
    }

    a[href^="#"]::after,
    a[href^="javascript"]::after {
        content: "";
    }

    /* Tabelas */
    table {
        border-collapse: collapse;
        width: 100%;
    }

    th, td {
        border: 1px solid #000;
        padding: 8px 12px;
    }

    th {
        background: #f0f0f0 !important;
        font-weight: bold;
    }

    /* Page breaks */
    .page-break {
        page-break-before: always;
    }

    .page-break-after {
        page-break-after: always;
    }

    .avoid-break {
        page-break-inside: avoid;
    }

    /* @page */
    @page {
        margin: 2cm;
        size: A4;
    }

    @page :first {
        margin-top: 3cm;
    }
}
```

## 32.2 Utility Classes para Print

```css
.print-only {
    display: none;
}

@media print {
    .print-only {
        display: block !important;
    }

    .print\:d-none {
        display: none !important;
    }
}
```

---

# 33. Reduced Motion

## 33.1 Respeitando Preferências do Usuário

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* Toggle manual via classe */
.reduced-motion *,
.reduced-motion *::before,
.reduced-motion *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
}
```

## 33.2 Animações Condicionais

```css
/* Animação só executa se o usuário permitir */
@media (prefers-reduced-motion: no-preference) {
    .card:hover {
        transform: translateY(-2px);
        transition: transform var(--transition-normal);
    }

    .fade-in {
        animation: fadeIn var(--motion-smooth) var(--ease-out);
    }
}
```

---

# 34. High Contrast Mode

## 34.1 Forced Colors (Windows)

```css
@media (forced-colors: active) {
    .ui-btn {
        border: 2px solid ButtonText;
    }

    .ui-btn--primary {
        background: Highlight;
        color: HighlightText;
    }

    .ui-card {
        border: 2px solid ButtonText;
    }

    .ui-input {
        border: 2px solid ButtonText;
    }

    .icon {
        color: ButtonText;
    }
}
```

## 34.2 High Contrast Manual

```css
/* Quando o tema high-contrast estiver ativo */
[data-theme="high-contrast"] {
    .ui-btn {
        border: 2px solid currentColor;
    }

    .ui-card {
        border: 2px solid var(--color-border);
    }
}
```

---

# 35. Performance CSS

## 35.1 Seletores Eficientes

```css
/* ❌ Ineficiente */
html body div.container ul li a { }

/* ✅ Eficiente */
.nav-link { }
```

## 35.2 Propriedades GPU

```css
/* GPU aceleradas (não causam reflow) */
transform
opacity
filter
will-change

/* Causam reflow (evitar em animações) */
width, height, top, left, right, bottom
padding, margin, border
font-size, line-height
display, position, float
```

## 35.3 Regras de Performance

```
1. Use transform + opacity para animações
2. Evite seletores universais (*) em contexto amplo
3. Prefira classes a seletores de elemento
4. Especificidade mínima necessária
5. Evite !important (quebra cascade natural)
6. Use contain: layout style paint para isolamento
7. Evite @import (use <link>)
8. Evite expressions, filters complexos
9. use will-change com moderação
```

---

# 36. Debugging CSS

## 36.1 Utility Classes de Debug

```css
/* Destacar elementos para debug */
.debug {
    outline: 2px solid red !important;
}

.debug * {
    outline: 1px solid rgba(255, 0, 0, 0.3) !important;
}

/* Mostrar medidas */
.debug-sizes::after {
    content: attr(class);
    position: absolute;
    top: 0;
    right: 0;
    background: red;
    color: white;
    font-size: 10px;
    padding: 2px 4px;
    z-index: 9999;
}
```

## 36.2 Breakpoint Indicator

```css
/* Mostrar breakpoint atual no canto da tela */
.debug-breakpoint::after {
    position: fixed;
    bottom: 4px;
    right: 4px;
    padding: 4px 8px;
    background: var(--color-primary);
    color: var(--text-inverse);
    font-size: 12px;
    z-index: 9999;
    border-radius: var(--radius-sm);
}

@media (min-width: 0px) {
    .debug-breakpoint::after { content: "XS"; }
}

@media (min-width: 576px) {
    .debug-breakpoint::after { content: "SM"; }
}

@media (min-width: 768px) {
    .debug-breakpoint::after { content: "MD"; }
}

@media (min-width: 1024px) {
    .debug-breakpoint::after { content: "LG"; }
}

@media (min-width: 1440px) {
    .debug-breakpoint::after { content: "XL"; }
}

@media (min-width: 1920px) {
    .debug-breakpoint::after { content: "XXL"; }
}
```

---

# 37. Boas Práticas

## 37.1 Código Limpo

```css
/* ✅ Organizado */
.button { }
.button__icon { }
.button__label { }
.button--primary { }
.button--disabled { }

/* ❌ Desorganizado */
div .button .icon { }
button.primary.btn { }
```

## 37.2 Propriedades na Ordem Correta

```css
.element {
    /* Positioning */
    position: absolute;
    top: 0;
    right: 0;
    z-index: var(--z-dropdown);

    /* Display & Box Model */
    display: flex;
    align-items: center;
    width: 100%;
    height: 40px;
    padding: var(--spacing-3);
    margin: var(--spacing-2);

    /* Typography */
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    text-align: center;
    color: var(--text-primary);

    /* Visual */
    background: var(--surface-card);
    border: var(--border-thin) solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);

    /* Misc */
    cursor: pointer;
    transition: transform var(--transition-fast);
}
```

## 37.3 Evitar Propriedades Redundantes

```css
/* ❌ Redundante */
.button {
    display: block;
    width: 100%;
}

/* ✅ Suficiente */
.button {
    display: block;
}
```

---

# 38. Compatibilidade

## 38.1 Browsers Suportados

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS Grid | 57+ | 52+ | 10.1+ | 16+ |
| Flexbox | 29+ | 28+ | 9+ | 12+ |
| CSS Variables | 49+ | 31+ | 9.1+ | 15+ |
| `backdrop-filter` | 76+ | 103+ | 9+ | 17+ |
| `aspect-ratio` | 88+ | 87+ | 15+ | 88+ |
| `gap` for flex | 84+ | 63+ | 14.1+ | 84+ |
| `:focus-visible` | 86+ | 85+ | 15.4+ | 86+ |
| `@supports` | 28+ | 22+ | 9+ | 12+ |
| `display: contents` | 65+ | 60+ | 11.1+ | 79+ |
| `prefers-reduced-motion` | 74+ | 63+ | 10.1+ | 79+ |
| `prefers-color-scheme` | 76+ | 67+ | 12.1+ | 79+ |
| `forced-colors` | 89+ | 89+ | 15+ | 89+ |

## 38.2 Não Suportado

- Internet Explorer 11 (deliberado)
- Safari < 11 (sem suporte a CSS Variables)
- Chrome < 49 (muito antigo, < 0.1% de mercado)

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — 42 seções, CSS Core completo |
