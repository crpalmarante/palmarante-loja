# Sprint 01 — Fundação da Interface

## Objetivo

Estabelecer a base estrutural do frontend: HTML semântico, sistema de CSS modular,
tipografia auto-hospedada, sprite de ícones SVG e navegação data-driven.

## Estrutura

```
index4.html
├── css/
│   ├── fonts.css       @font-face da Inter (Regular, Medium, Bold)
│   ├── variaveis.css   Cores, fontes, espaçamento, sombras, z-index, breakpoints
│   ├── reset.css       Reset global, scrollbar, seleção
│   ├── layout.css      Grid principal: app, sidebar, main, header, breadcrumb,
│   │                   workspace, footer, collapsed, container, flex, grid utils
│   ├── icons.css       Classe base .icon e variações de tamanho (.icon-16, .icon-20, etc.)
│   └── style.css       Componentes: sidebar brand, menu-item, submenu
├── js/
│   └── app.js          Carrega sprite SVG, fetch do menu.json, renderiza sidebar
└── assets/
    ├── fonts/           Inter-Regular.ttf, Inter-Medium.ttf, Inter-Bold.ttf
    └── data/
        └── menu.json    Estrutura completa de navegação do ERP
```

## Como executar

```bash
cd palmarante-loja
python3 server.py
# Acesse http://localhost:8080/index4.html
```

## Decisões

| Decisão | Motivo |
|---------|--------|
| CSS modular (6 arquivos) | Separação clara de responsabilidades |
| Inter self-hosted | Zero dependência externa (sem Google Fonts) |
| SVG sprite | Escalável, rápido, sem CDN |
| Menu via JSON | Navegação vira dado — alterações sem tocar em HTML |
| Sidebar fixa + margin-left | Performance, sem JS para altura |
| Header sticky | Sempre visível durante scroll do workspace |
| ES Modules | Zero globais, código preparado para crescimento |
| Sem frameworks | React, Vue, Bootstrap, Tailwind — nada disso |

## Artefatos

- `index4.html` — Página principal
- `css/*.css` — 6 arquivos CSS
- `js/app.js` — Entry point ES Module
- `assets/fonts/Inter-*.ttf` — Fonte Inter
- `assets/data/menu.json` — Definição do menu
- `img/icons.svg` — 27 ícones SVG
