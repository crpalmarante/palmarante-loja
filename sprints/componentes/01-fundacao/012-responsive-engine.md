# FiscalUI Framework

## Documento 012 — Responsive Engine

**Versão 1.0**

Este documento define o sistema responsivo do FiscalUI. Detecção de breakpoints, orientação, resize, containers queries, e adaptação de layout e componentes conforme o viewport.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Breakpoints
6. Orientação
7. Resize
8. Container Queries
9. Adaptação de Layout
10. Adaptação de Componentes
11. Estratégias Responsivas
12. Integração com CSS Core
13. Integração com EventBus
14. Integração com State Manager
15. Debugging
16. Performance
17. Testes
18. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Responsive Engine gerencia a adaptação do FiscalUI a diferentes tamanhos de tela, orientações e dispositivos. Ele detecta mudanças no viewport, notifica o sistema, e permite que layouts e componentes reajam de forma coordenada.

## 1.2 Princípios

```
1. Mobile-first — breakpoints definidos do menor para o maior
2. CSS-first — responsividade começa no CSS, o JavaScript complementa
3. Centralizado — um único lugar define e notifica breakpoints
4. Reativo — mudanças são propagadas via EventBus e State Manager
5. Container-first — componentes respondem ao container, não à viewport
```

---

# 2. Filosofia

## 2.1 CSS-first, JS-second

```js
// Responsividade começa no CSS:
// .ui-sidebar { width: 240px; }
// @container (max-width: 400px) {
//     .ui-sidebar { width: 100%; }
// }

// O JavaScript Engine apenas NOTIFICA e COMPLEMENTA
// Ele nunca substitui o CSS responsivo
```

## 2.2 Container Queries > Media Queries

```
Preferência:
1º Container Queries — componente se adapta ao espaço disponível
2º Media Queries — viewport inteiro
3º JS — lógica que CSS não pode resolver
```

## 2.3 Breakpoints como Eventos

```
Breakpoints não são apenas números — são eventos de domínio.
"Tablet" não é 768px — é "espaço suficiente para sidebar + conteúdo".
```

---

# 3. Arquitetura

## 3.1 Diagrama

```
┌──────────────────────────────────────────────┐
│            Responsive Engine                  │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Breakpoint│  │Resize    │  │Container │   │
│  │Detector  │  │Observer  │  │Observer  │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Orientation│  │  DPR    │  │  Device  │   │
│  │Detector   │  │Detector │  │ Detector │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
└──────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│              Consumidores                     │
├──────────────────────────────────────────────┤
│  via EventBus: responsive:*                   │
│  via State: state.ui.breakpoint               │
│  via CSS: @container, @media                  │
└──────────────────────────────────────────────┘
```

## 3.2 Relação com Outros Módulos

```
Responsive Engine
    │
    ├── CSS Core → variáveis CSS com breakpoints
    ├── Layout Core → layouts adaptam conforme breakpoint
    ├── EventBus → emite responsive:*
    ├── State Manager → ui.breakpoint na store
    └── Componentes → watch('ui.breakpoint') para adaptar
```

---

# 4. API Pública

## 4.1 Implementação

```js
class ResponsiveEngine {
    constructor(framework = null) {
        this.framework = framework;
        this._breakpoints = new Map();
        this._current = null;
        this._previous = null;
        this._orientation = null;
        this._dpr = window.devicePixelRatio || 1;
        this._width = 0;
        this._height = 0;
        this._resizeThrottle = 150;
        this._resizeTimer = null;
        this._containerObservers = new Map();
        this._enabled = true;
    }

    // ─── Breakpoints ────────────────────────────────────────

    defineBreakpoint(name, query) {
        if (this._breakpoints.has(name)) {
            this._log('warn', `Breakpoint "${name}" já definido — substituindo`);
        }

        const mql = window.matchMedia(query);
        this._breakpoints.set(name, { name, query, mql });

        // Listener para quando o breakpoint mudar
        mql.addEventListener('change', (event) => {
            if (event.matches) {
                this._onBreakpointEnter(name);
            } else {
                this._onBreakpointLeave(name);
            }
        });

        this._log('info', `Breakpoint definido: ${name} (${query})`);
        return this;
    }

    defineBreakpoints(breakpoints) {
        for (const [name, query] of Object.entries(breakpoints)) {
            this.defineBreakpoint(name, query);
        }
        return this;
    }

    _onBreakpointEnter(name) {
        this._previous = this._current;

        if (this._current !== name) {
            this._current = name;

            this._log('debug', `Breakpoint: ${name}`);

            this._emitEvent('responsive:breakpoint', {
                breakpoint: name,
                width: this._width,
                height: this._height
            });

            this._updateState({ breakpoint: name });
        }
    }

    _onBreakpointLeave(name) {
        // O breakpoint ativo agora é o maior que ainda match
        this._determineActiveBreakpoint();
    }

    _determineActiveBreakpoint() {
        // Itera breakpoints do maior para o menor
        const sorted = Array.from(this._breakpoints.entries())
            .sort((a, b) => this._breakpointWeight(b[0]) - this._breakpointWeight(a[0]));

        for (const [name, bp] of sorted) {
            if (bp.mql.matches) {
                if (this._current !== name) {
                    this._previous = this._current;
                    this._current = name;
                    this._emitEvent('responsive:breakpoint', {
                        breakpoint: name,
                        width: this._width,
                        height: this._height
                    });
                    this._updateState({ breakpoint: name });
                }
                return;
            }
        }
    }

    // ─── Resize ─────────────────────────────────────────────

    start() {
        window.addEventListener('resize', this._onResize.bind(this), { passive: true });
        this._updateDimensions();
        this._determineActiveBreakpoint();
        this._log('info', 'Responsive Engine iniciado');
        return this;
    }

    stop() {
        window.removeEventListener('resize', this._onResize);
        if (this._resizeTimer) {
            clearTimeout(this._resizeTimer);
            this._resizeTimer = null;
        }
        return this;
    }

    _onResize() {
        if (this._resizeTimer) return;

        this._resizeTimer = setTimeout(() => {
            this._resizeTimer = null;
            this._updateDimensions();
            this._determineActiveBreakpoint();

            this._emitEvent('responsive:resize', {
                width: this._width,
                height: this._height,
                breakpoint: this._current
            });

            this._updateState({
                width: this._width,
                height: this._height
            });
        }, this._resizeThrottle);
    }

    // ─── Orientação ─────────────────────────────────────────

    startOrientation() {
        if (screen?.orientation) {
            screen.orientation.addEventListener('change', this._onOrientationChange.bind(this));
        } else {
            // Fallback para resize
            window.addEventListener('resize', this._onOrientationChange.bind(this));
        }

        this._orientation = this._getOrientation();
        return this;
    }

    _onOrientationChange() {
        const newOrientation = this._getOrientation();
        if (newOrientation !== this._orientation) {
            this._previousOrientation = this._orientation;
            this._orientation = newOrientation;

            this._emitEvent('responsive:orientation', {
                orientation: this._orientation,
                previous: this._previousOrientation
            });

            this._updateState({ orientation: this._orientation });
        }
    }

    // ─── Container Queries ──────────────────────────────────

    observeContainer(element, callback, options = {}) {
        if (!element || typeof callback !== 'function') {
            this._log('error', 'observeContainer: element e callback obrigatórios');
            return () => {};
        }

        const observer = new ResizeObserver((entries) => {
            for (const entry of entries) {
                const { width, height } = entry.contentBoxSize?.[0] || entry.contentRect;
                callback({
                    width: Math.round(width),
                    height: Math.round(height),
                    breakpoint: this._classifyContainerSize(width)
                }, entry);
            }
        });

        observer.observe(element, options);
        this._containerObservers.set(element, observer);

        // Retorna unobserve
        return () => {
            observer.disconnect();
            this._containerObservers.delete(element);
        };
    }

    unobserveContainer(element) {
        if (this._containerObservers.has(element)) {
            this._containerObservers.get(element).disconnect();
            this._containerObservers.delete(element);
        }
    }

    // ─── Getters ────────────────────────────────────────────

    get breakpoint() {
        return this._current;
    }

    get isMobile() {
        return this._current === 'xs' || this._current === 'sm';
    }

    get isTablet() {
        return this._current === 'md';
    }

    get isDesktop() {
        return this._current === 'lg' || this._current === 'xl' || this._current === 'xxl';
    }

    get orientation() {
        return this._orientation;
    }

    get isPortrait() {
        return this._orientation === 'portrait';
    }

    get isLandscape() {
        return this._orientation === 'landscape';
    }

    get dimensions() {
        return { width: this._width, height: this._height };
    }

    get dpr() {
        return this._dpr;
    }

    // ─── Utilitários ────────────────────────────────────────

    isBreakpoint(name) {
        return this._current === name;
    }

    isBreakpointOrAbove(name) {
        return this._breakpointWeight(this._current) >= this._breakpointWeight(name);
    }

    isBreakpointOrBelow(name) {
        return this._breakpointWeight(this._current) <= this._breakpointWeight(name);
    }

    isBetween(min, max) {
        const current = this._breakpointWeight(this._current);
        return current >= this._breakpointWeight(min) && current <= this._breakpointWeight(max);
    }

    // ─── Destruição ─────────────────────────────────────────

    destroy() {
        this.stop();
        this.stopOrientation();

        for (const [, observer] of this._containerObservers) {
            observer.disconnect();
        }
        this._containerObservers.clear();

        this._breakpoints.clear();
        this._current = null;
        this._previous = null;
    }

    // ─── Internos ───────────────────────────────────────────

    _updateDimensions() {
        this._width = window.innerWidth;
        this._height = window.innerHeight;
    }

    _getOrientation() {
        if (screen?.orientation?.type) {
            return screen.orientation.type.startsWith('portrait') ? 'portrait' : 'landscape';
        }
        return window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
    }

    _classifyContainerSize(width) {
        if (width < 576) return 'xs';
        if (width < 768) return 'sm';
        if (width < 992) return 'md';
        if (width < 1200) return 'lg';
        return 'xl';
    }

    _breakpointWeight(name) {
        const order = ['xs', 'sm', 'md', 'lg', 'xl', 'xxl'];
        const idx = order.indexOf(name);
        return idx >= 0 ? idx : -1;
    }

    _emitEvent(event, data) {
        if (this.framework && this.framework.events) {
            this.framework.events.emit(event, { source: 'ResponsiveEngine', ...data });
        }
    }

    _updateState(data) {
        if (this.framework && this.framework.state) {
            this.framework.state.dispatch({
                type: 'responsive/update',
                payload: data
            });
        }
    }

    _log(level, message, error = null) {
        if (this.framework && this.framework.log) {
            this.framework.log(level, `ResponsiveEngine: ${message}`, error);
        } else if (level === 'error') {
            console.error(`[ResponsiveEngine] ${message}`, error || '');
        } else if (level === 'warn') {
            console.warn(`[ResponsiveEngine] ${message}`);
        } else if (level === 'debug' && this.framework?.config?.debug) {
            console.log(`[ResponsiveEngine] ${message}`);
        }
    }
}
```

## 4.2 Resumo da API

| Método | Descrição |
|--------|-----------|
| `defineBreakpoint(name, query)` | Define um breakpoint |
| `defineBreakpoints(breakpoints)` | Define múltiplos breakpoints |
| `start()` | Inicia observação de resize |
| `stop()` | Para observação de resize |
| `startOrientation()` | Inicia observação de orientação |
| `observeContainer(element, cb)` | Observa tamanho de container |
| `unobserveContainer(element)` | Para observação de container |
| `isBreakpoint(name)` | Verifica breakpoint atual |
| `isBreakpointOrAbove(name)` | Breakpoint atual >= nome |
| `isBreakpointOrBelow(name)` | Breakpoint atual <= nome |
| `isBetween(min, max)` | Breakpoint entre min e max |
| `destroy()` | Remove tudo |

### Getters

| Getter | Descrição |
|--------|-----------|
| `breakpoint` | Breakpoint atual (xs, sm, md, lg, xl, xxl) |
| `isMobile` | xs ou sm |
| `isTablet` | md |
| `isDesktop` | lg, xl ou xxl |
| `orientation` | portrait ou landscape |
| `isPortrait` | true se portrait |
| `isLandscape` | true se landscape |
| `dimensions` | { width, height } |
| `dpr` | devicePixelRatio |

---

# 5. Breakpoints

## 5.1 Breakpoints Padrão

```js
FiscalUI.responsive.defineBreakpoints({
    xs:  '(max-width: 575px)',
    sm:  '(min-width: 576px) and (max-width: 767px)',
    md:  '(min-width: 768px) and (max-width: 991px)',
    lg:  '(min-width: 992px) and (max-width: 1199px)',
    xl:  '(min-width: 1200px) and (max-width: 1399px)',
    xxl: '(min-width: 1400px)'
});
```

## 5.2 Mapa de Breakpoints

| Nome | Largura | Dispositivo Típico |
|------|---------|--------------------|
| xs | < 576px | Smartphones pequenos |
| sm | 576px — 767px | Smartphones grandes |
| md | 768px — 991px | Tablets |
| lg | 992px — 1199px | Desktops pequenos |
| xl | 1200px — 1399px | Desktops |
| xxl | ≥ 1400px | Desktops grandes / TV |

## 5.3 Breakpoints Customizados

```js
// Aplicação pode sobrescrever
FiscalUI.responsive.defineBreakpoints({
    phone:  '(max-width: 480px)',
    tablet: '(min-width: 481px) and (max-width: 1024px)',
    desktop: '(min-width: 1025px)'
});
```

---

# 6. Orientação

## 6.1 Detecção

```js
FiscalUI.responsive.startOrientation();

// Getter
const orientation = FiscalUI.responsive.orientation;
// 'portrait' ou 'landscape'

const isPortrait = FiscalUI.responsive.isPortrait;
const isLandscape = FiscalUI.responsive.isLandscape;
```

## 6.2 Evento

```js
FiscalUI.events.on('responsive:orientation', ({ orientation, previous }) => {
    if (orientation === 'portrait') {
        layoutStackVertically();
    } else {
        layoutStackHorizontally();
    }
});
```

---

# 7. Resize

## 7.1 Observação

```js
FiscalUI.responsive.start();

// Dimensões atuais
const { width, height } = FiscalUI.responsive.dimensions;
```

## 7.2 Throttle

```js
// Resize é throttled (padrão: 150ms)
// Durante resize contínuo, apenas o último evento é disparado

FiscalUI.events.on('responsive:resize', ({ width, height, breakpoint }) => {
    // Disparado apenas após usuário parar de redimensionar
    updateLayout(width, height);
});
```

---

# 8. Container Queries

## 8.1 Observação JS

```js
const unobserve = FiscalUI.responsive.observeContainer(
    document.getElementById('sidebar'),
    ({ width, height, breakpoint }) => {
        console.log(`Sidebar: ${width}x${height} (${breakpoint})`);

        if (breakpoint === 'xs') {
            sidebar.collapse();
        } else {
            sidebar.expand();
        }
    }
);

// Para de observar
unobserve();
```

## 8.2 No CSS

```css
/* Container query complementar */
.sidebar {
    container-type: inline-size;
    container-name: sidebar;
}

@container sidebar (max-width: 300px) {
    .sidebar__menu {
        display: none;
    }
    .sidebar__toggle {
        display: block;
    }
}

@container sidebar (min-width: 301px) {
    .sidebar__menu {
        display: block;
    }
    .sidebar__toggle {
        display: none;
    }
}
```

---

# 9. Adaptação de Layout

## 9.1 Layout Core + Responsive

```js
// O layout se adapta automaticamente ao breakpoint
FiscalUI.events.on('responsive:breakpoint', ({ breakpoint }) => {
    switch (breakpoint) {
        case 'xs':
        case 'sm':
            // Mobile: sidebar oculta, conteúdo full width
            FiscalUI.layout.sidebar.hide();
            FiscalUI.layout.topbar.compact();
            break;

        case 'md':
        case 'lg':
            // Tablet: sidebar icones, topbar normal
            FiscalUI.layout.sidebar.iconMode();
            FiscalUI.layout.topbar.normal();
            break;

        case 'xl':
        case 'xxl':
            // Desktop: tudo expandido
            FiscalUI.layout.sidebar.show();
            FiscalUI.layout.topbar.extended();
            break;
    }
});
```

## 9.2 Estratégias por Breakpoint

```
Breakpoint | Sidebar | Topbar | Content   | DataGrid
-----------|---------|--------|-----------|---------
xs         | oculta  | compact| full width| card view
sm         | oculta  | compact| full width| card view
md         | ícones  | normal | padding   | table compact
lg         | expand  | normal | padding   | table
xl         | expand  | normal | max-width | table + detalhe
xxl        | expand  | extended| max-width| table + detalhe
```

---

# 10. Adaptação de Componentes

## 10.1 Componentes Responsivos

```js
class DataGrid extends UIComponent {
    init() {
        // Adapta ao breakpoint atual
        this.responsive = FiscalUI.responsive;
        this._adaptToBreakpoint(this.responsive.breakpoint);

        // Escuta mudanças
        this._unsub = FiscalUI.events.on('responsive:breakpoint', (data) => {
            this._adaptToBreakpoint(data.breakpoint);
        });
    }

    _adaptToBreakpoint(bp) {
        switch (bp) {
            case 'xs':
            case 'sm':
                this.viewMode = 'cards';      // Cards em vez de tabela
                this.columns = ['chave', 'valor', 'status'];
                break;
            case 'md':
                this.viewMode = 'table';
                this.columns = ['chave', 'emissor', 'valor', 'status'];
                this.compact = true;
                break;
            case 'lg':
            case 'xl':
            case 'xxl':
                this.viewMode = 'table';
                this.columns = ['chave', 'emissor', 'valor', 'data', 'status', 'acoes'];
                this.compact = false;
                break;
        }
        this.render();
    }

    destroy() {
        if (this._unsub) this._unsub();
    }
}
```

## 10.2 Componente com Container Query

```js
class CardGrid extends UIComponent {
    init() {
        this._unobserve = FiscalUI.responsive.observeContainer(
            this.element,
            ({ width, breakpoint }) => {
                // Ajusta número de colunas conforme largura do container
                const columns = breakpoint === 'xs' ? 1
                    : breakpoint === 'sm' ? 2
                    : breakpoint === 'md' ? 3
                    : 4;

                this.element.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
            }
        );
    }

    destroy() {
        if (this._unobserve) this._unobserve();
    }
}
```

---

# 11. Estratégias Responsivas

## 11.1 Mobile First

```js
// CSS: mobile é o padrão, breakpoints adicionam
.ui-data-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

@container (min-width: 600px) {
    .ui-data-grid {
        display: table;
    }
}
```

## 11.2 Progressive Enhancement

```js
// Funcionalidades adicionais em telas maiores
if (FiscalUI.responsive.isDesktop) {
    // Atalhos de teclado
    this.enableKeyboardShortcuts();

    // Drag and drop
    this.enableDragAndDrop();

    // Tooltips ricos
    this.enableRichTooltips();
}
```

## 11.3 Degradação Graciosa

```js
// Funcionalidades reduzidas em telas menores
if (FiscalUI.responsive.isMobile) {
    // Sem drag-and-drop
    this.disableDragAndDrop();

    // Accordion em vez de abas
    this.useAccordionLayout();

    // Inputs maiores (touch target)
    this.inputs.classList.add('ui-input--touch');
}
```

---

# 12. Integração com CSS Core

## 12.1 Variáveis CSS

```css
:root {
    --bp-xs: 575px;
    --bp-sm: 576px;
    --bp-md: 768px;
    --bp-lg: 992px;
    --bp-xl: 1200px;
    --bp-xxl: 1400px;
}
```

## 12.2 Classes Utilitárias

```css
/* Exibir/ocultar por breakpoint */
.ui-show--xs { display: block; }
.ui-hide--xs { display: none; }

@media (min-width: 576px) {
    .ui-show--sm { display: block; }
    .ui-hide--sm { display: none; }
}

@media (min-width: 768px) {
    .ui-show--md { display: block; }
    .ui-hide--md { display: none; }
}

@media (min-width: 992px) {
    .ui-show--lg { display: block; }
    .ui-hide--lg { display: none; }
}

@media (min-width: 1200px) {
    .ui-show--xl { display: block; }
    .ui-hide--xl { display: none; }
}
```

## 12.3 Grid Responsivo

```css
.ui-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
}

@media (min-width: 768px) {
    .ui-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 992px) {
    .ui-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (min-width: 1200px) {
    .ui-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

---

# 13. Integração com EventBus

## 13.1 Eventos

```js
'responsive:breakpoint'       // Breakpoint mudou (xs → sm → md → lg → xl → xxl)
'responsive:orientation'      // Orientação mudou (portrait ↔ landscape)
'responsive:resize'           // Viewport redimensionou (throttled)
```

## 13.2 Payload

```js
// responsive:breakpoint
{
    source: 'ResponsiveEngine',
    breakpoint: 'md',
    width: 800,
    height: 600
}

// responsive:orientation
{
    source: 'ResponsiveEngine',
    orientation: 'portrait',
    previous: 'landscape'
}

// responsive:resize
{
    source: 'ResponsiveEngine',
    width: 1024,
    height: 768,
    breakpoint: 'lg'
}
```

---

# 14. Integração com State Manager

## 14.1 Slice na Store

```js
// Automaticamente mantido:
{
    ui: {
        breakpoint: 'lg',
        orientation: 'landscape',
        width: 1200,
        height: 800
    }
}
```

## 14.2 Ações

```js
'responsive/update'   // Atualiza estado responsivo
```

## 14.3 Componente Lendo

```js
class Dashboard extends UIComponent {
    init() {
        this.watch('ui', (ui) => {
            if (ui.breakpoint === 'xs') {
                this.layout = 'single-column';
            } else {
                this.layout = 'multi-column';
            }
            this.render();
        });
    }
}
```

---

# 15. Debugging

## 15.1 Modo Debug

```js
FiscalUI.config.debug = true;

// Logs:
// [ResponsiveEngine] Breakpoint definido: xs ((max-width: 575px))
// [ResponsiveEngine] Breakpoint: lg
// [ResponsiveEngine] Resize: 1200x800
```

## 15.2 Indicador Visual

```js
// Opcional: exibe breakpoint atual no canto da tela
if (FiscalUI.config.debug) {
    const indicator = document.createElement('div');
    indicator.id = 'ui-breakpoint-indicator';
    indicator.style.cssText = 'position:fixed;bottom:0;right:0;padding:4px 8px;background:#333;color:#fff;font-size:12px;z-index:9999;';

    FiscalUI.events.on('responsive:breakpoint', ({ breakpoint }) => {
        indicator.textContent = `${breakpoint} (${window.innerWidth}px)`;
    });

    document.body.appendChild(indicator);
}
```

---

# 16. Performance

## 16.1 Métricas

| Operação | Performance |
|----------|-------------|
| `defineBreakpoint()` | < 0.1ms |
| `start()` | < 0.5ms |
| Resize (throttled) | ~150ms entre execuções |
| Container observer | Nativo (ResizeObserver) |
| `isBreakpoint()` | < 0.001ms |

## 16.2 Otimizações

```js
// 1. Throttle de resize evita execução excessiva
✅ Padrão: 150ms

// 2. ResizeObserver é nativo e performático
✅ use observeContainer() em vez de poll de tamanho

// 3. matchMedia é otimizado pelo browser
✅ use matchMedia em vez de window.innerWidth em loops

// 4. Desative observers quando componentes são destruídos
✅ sempre chame unobserveContainer() ou o retorno
```

---

# 17. Testes

## 17.1 Teste Unitário

```js
describe('ResponsiveEngine', () => {
    let engine;

    beforeEach(() => {
        engine = new ResponsiveEngine();
    });

    afterEach(() => {
        engine.destroy();
    });

    it('should define breakpoints', () => {
        engine.defineBreakpoints({
            xs: '(max-width: 575px)',
            lg: '(min-width: 992px)'
        });

        expect(engine._breakpoints.has('xs')).toBe(true);
        expect(engine._breakpoints.has('lg')).toBe(true);
    });

    it('should detect current breakpoint on start', () => {
        engine.defineBreakpoints({
            xs: '(max-width: 575px)',
            lg: '(min-width: 992px)'
        });

        // Simula viewport largo
        spyOnProperty(window, 'innerWidth', 'get').and.returnValue(1200);
        engine.start();

        expect(engine.breakpoint).toBe('lg');
    });

    it('should detect orientation', () => {
        engine.startOrientation();

        spyOnProperty(window, 'innerHeight', 'get').and.returnValue(800);
        spyOnProperty(window, 'innerWidth', 'get').and.returnValue(400);

        const orientation = engine._getOrientation();
        expect(orientation).toBe('portrait');
    });

    it('should emit events on breakpoint change', () => {
        const events = [];
        engine.framework = {
            events: {
                emit: (event, data) => events.push({ event, data })
            },
            config: { debug: false }
        };

        engine.defineBreakpoints({
            xs: '(max-width: 575px)',
            lg: '(min-width: 992px)'
        });

        // Simula match do breakpoint lg
        engine._breakpoints.get('lg').mql = { matches: true };
        engine._breakpoints.get('xs').mql = { matches: false };

        engine._determineActiveBreakpoint();

        expect(events.length).toBe(1);
        expect(events[0].event).toBe('responsive:breakpoint');
        expect(events[0].data.breakpoint).toBe('lg');
    });

    it('should update state on breakpoint change', () => {
        const dispatched = [];
        engine.framework = {
            state: {
                dispatch: (action) => dispatched.push(action)
            },
            events: {
                emit: () => {}
            },
            config: { debug: false }
        };

        engine.defineBreakpoints({
            lg: '(min-width: 992px)'
        });

        engine._breakpoints.get('lg').mql = { matches: true };
        engine._determineActiveBreakpoint();

        expect(dispatched.length).toBe(1);
        expect(dispatched[0].type).toBe('responsive/update');
    });

    it('should provide helper getters', () => {
        engine._current = 'xs';
        expect(engine.isMobile).toBe(true);
        expect(engine.isTablet).toBe(false);
        expect(engine.isDesktop).toBe(false);

        engine._current = 'md';
        expect(engine.isMobile).toBe(false);
        expect(engine.isTablet).toBe(true);
        expect(engine.isDesktop).toBe(false);

        engine._current = 'xl';
        expect(engine.isMobile).toBe(false);
        expect(engine.isTablet).toBe(false);
        expect(engine.isDesktop).toBe(true);
    });

    it('should compare breakpoints', () => {
        engine._current = 'md';

        expect(engine.isBreakpoint('md')).toBe(true);
        expect(engine.isBreakpoint('lg')).toBe(false);

        expect(engine.isBreakpointOrAbove('sm')).toBe(true);
        expect(engine.isBreakpointOrAbove('lg')).toBe(false);

        expect(engine.isBreakpointOrBelow('lg')).toBe(true);
        expect(engine.isBreakpointOrBelow('sm')).toBe(false);

        expect(engine.isBetween('sm', 'lg')).toBe(true);
        expect(engine.isBetween('lg', 'xl')).toBe(false);
    });
});
```

---

# 18. Boas Práticas

## 18.1 Regras de Ouro

```
1. NUNCA use JS para o que CSS pode fazer — responsividade começa no CSS
2. SEMPRE defina breakpoints antes de iniciar o engine
3. NUNCA coloque lógica de breakpoint dentro de loops (requestAnimationFrame)
4. SEMPRE use container queries para componentes reutilizáveis
5. NUNCA confie em user agent para detectar dispositivo — use viewport
6. SEMPRE destrua observers quando componentes morrerem
7. NUNCA use breakpoints mágicos (números soltos) — sempre nomeie
8. SEMPRE teste em múltiplos tamanhos de tela
9. NUNCA bloqueie funcionalidades por dispositivo — use capacidade
10. SEMPRE pense mobile-first
```

## 18.2 Checklist

```
☐ Breakpoints definidos e nomeados
☐ Engine.start() chamado na inicialização
☐ Layout adapta a cada breakpoint
☐ Componentes críticos são responsivos
☐ Container queries usadas para componentes reutilizáveis
☐ Observers destruídos no destroy() dos componentes
☐ Estado responsivo na store (ui.breakpoint)
☐ Testes de breakpoint e orientação
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Responsive Engine completo |
