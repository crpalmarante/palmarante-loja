# FiscalUI Framework

## Documento 017 — Build System

**Versão 1.0**

Este documento define o sistema de build do FiscalUI. Estrutura de diretórios, task runners, processamento de CSS/JS, otimizações, e deploy. O build system é baseado em ferramentas nativas (npm scripts), sem frameworks de build pesados.

---

# Índice

1. Introdução
2. Estrutura de Diretórios
3. Pipeline de Build
4. CSS Build
5. JavaScript Build
6. Otimizações
7. Ambiente Dev vs Produção
8. Temas
9. Sprites de Ícones
10. Testes
11. Lint
12. Deploy

---

# 1. Introdução

## 1.1 Propósito

O Build System transforma o código fonte do FiscalUI em artefatos otimizados para produção. Ele processa CSS, JavaScript, sprites, temas, e gera bundles mínimos para cada ambiente.

---

# 2. Estrutura de Diretórios

```
fiscalui/
├── src/
│   ├── css/
│   │   ├── core/           # Reset, normalize, utilities
│   │   ├── components/     # CSS de cada componente
│   │   ├── themes/         # Temas oficials
│   │   └── fiscalui.css    # Entry point
│   ├── js/
│   │   ├── core/           # Core JS (EventBus, State, Router)
│   │   ├── components/     # JS de cada componente
│   │   ├── services/       # Serviços
│   │   └── fiscalui.js     # Entry point
│   ├── icons/              # SVGs individuais
│   └── fiscalui.scss       # (opcional) Versão SCSS
├── dist/
│   ├── css/
│   ├── js/
│   └── icons/
├── sprints/                # Documentação RFC
├── package.json
└── fiscalui.json           # Configuração de build
```

---

# 3. Pipeline de Build

```
src/css/*.css     → PostCSS (autoprefixer, minify) → dist/css/fiscalui.min.css
src/js/*.js       → Babel (opcional) + Minify → dist/js/fiscalui.min.js
src/icons/*.svg   → SVG Sprite → dist/icons/sprite.svg
src/css/themes/*  → PostCSS → dist/css/themes/*.css
```

---

# 4. Scripts npm

```json
{
    "scripts": {
        "dev":       "npm run build && node scripts/dev-server.js",
        "build":     "npm run build:css && npm run build:js && npm run build:icons",
        "build:css": "postcss src/css/fiscalui.css -o dist/css/fiscalui.min.css",
        "build:js":  "terser src/js/fiscalui.js -o dist/js/fiscalui.min.js",
        "build:icons": "svg-sprite --symbol --symbol-dest dist/icons src/icons/*.svg",
        "build:themes": "postcss src/css/themes/*.css --dir dist/css/themes",
        "lint":      "npm run lint:css && npm run lint:js",
        "lint:css":  "stylelint src/css/**/*.css",
        "lint:js":   "eslint src/js/**/*.js",
        "test":      "karma start karma.conf.js",
        "watch":     "chokidar 'src/**/*' -c 'npm run build'"
    }
}
```

---

# 5. CSS Build

## 5.1 PostCSS

```js
// postcss.config.js
module.exports = {
    plugins: [
        require('autoprefixer'),
        require('cssnano')({
            preset: ['default', { discardComments: { removeAll: true } }]
        })
    ]
};
```

## 5.2 Entrada

```css
/* src/css/fiscalui.css */

/* Core */
@import './core/reset.css';
@import './core/variables.css';
@import './core/utilities.css';

/* Layout */
@import './core/layout.css';

/* Componentes */
@import './components/button.css';
@import './components/modal.css';
@import './components/datagrid.css';
/* ... */
```

---

# 6. JavaScript Build

## 6.1 Entrada

```js
// src/js/fiscalui.js
import { EventBus } from './core/event-bus.js';
import { StateManager } from './core/state-manager.js';
import { Router } from './core/router.js';
import { ComponentBase } from './core/component-base.js';

window.FiscalUI = {
    version: '1.0.0',
    events: new EventBus(),
    state: new StateManager(),
    router: new Router(),
    component: ComponentBase
};
```

## 6.2 Minificação

```json
{
    "scripts": {
        "build:js": "terser src/js/fiscalui.js --compress --mangle -o dist/js/fiscalui.min.js"
    }
}
```

---

# 7. Otimizações

```
CSS:
  - Autoprefixer: compatibilidade跨 browser
  - cssnano: minificação (remove comentários, whitespace)
  - PurgeCSS (opcional): remove CSS não utilizado

JS:
  - Terser: minificação + mangling
  - Tree shaking (se usar ES modules)
  - Dead code elimination

Ícones:
  - Sprite único: 1 request em vez de N
  - SVGO: otimização de SVGs (remove metadata, viewbox padronizado)
```

---

# 8. Temas

```json
{
    "scripts": {
        "build:themes": "postcss src/css/themes/*.css --dir dist/css/themes"
    }
}
```

```css
/* src/css/themes/light.css */
:root {
    --color-primary: #1a73e8;
    /* ... */
}

/* src/css/themes/dark.css */
:root {
    --color-primary: #8ab4f8;
    /* ... */
}
```

---

# 9. Testes

```json
{
    "scripts": {
        "test": "karma start karma.conf.js",
        "test:watch": "karma start karma.conf.js --auto-watch --no-single-run",
        "test:coverage": "karma start karma.conf.js --coverage"
    }
}
```

---

# 10. Lint

```json
{
    "scripts": {
        "lint": "npm run lint:css && npm run lint:js",
        "lint:css": "stylelint src/css/**/*.css",
        "lint:js": "eslint src/js/**/*.js",
        "lint:fix": "npm run lint:css -- --fix && npm run lint:js -- --fix"
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Build System |
