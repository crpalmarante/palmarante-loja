# Changelog — Sprint 01

## Adicionado

- `index4.html` — HTML semântico com `#app`, `#sidebar`, `#main`, `#header`,
  `#breadcrumb`, `#workspace`, `#footer`
- `css/fonts.css` — `@font-face` para Inter (Regular 400, Medium 500, Bold 700)
- `css/variaveis.css` — Todas as variáveis CSS do design system
- `css/reset.css` — Reset global com scrollbar customizada
- `css/layout.css` — Grid principal, sidebar fixa, header sticky, workspace flex,
  footer, sidebar collapsed, container, flex/grid utilitários
- `css/icons.css` — Classe `.icon` com tamanhos 16, 20, 24, 32
- `css/style.css` — Estilos do menu na sidebar (brand, item, submenu, section)
- `js/app.js` — ES Module: carrega sprite SVG, fetch menu.json, renderiza sidebar
- `assets/fonts/Inter-Regular.ttf`
- `assets/fonts/Inter-Medium.ttf`
- `assets/fonts/Inter-Bold.ttf`
- `assets/data/menu.json` — 7 módulos principais + submenus de Faturamento e RH
- `img/icons.svg` — 27 ícones (dashboard, users, box, cart, dollar, file-text, etc.)

## Alterado

- `css/variaveis.css` — `--font-family` alterado para `"Inter", "Segoe UI", Arial, sans-serif`

## Removido

- `frontend/` — Estrutura movida para `css/` e `js/` na raiz

## Observações

- Zero dependências externas (sem Google Fonts, sem CDN, sem frameworks)
- Menu 100% data-driven via `menu.json`
- Ícones via SVG sprite — sem PNG, sem font-icons
- Sidebar fixa + header sticky — sem JS para altura
