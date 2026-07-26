# FiscalUI Framework

## Documento 015 — Icon Engine

**Versão 1.0**

Este documento define o sistema de ícones do FiscalUI. Carregamento de sprites SVG, registro de ícones, cache, temas, tamanhos, e integração com componentes. Ícones são SVG inline, nunca fontes.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Sprites SVG
6. Registro de Ícones
7. Uso em Componentes
8. Tamanhos
9. Temas
10. Cache
11. Performance
12. Testes
13. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Icon Engine gerencia todos os ícones do FiscalUI. Ícones são SVG inline (sprite), nunca fontes. Isso garante resolução independente, coloração via CSS, e acessibilidade.

---

# 2. Filosofia

```
1. SVG inline > font icons (resolução, cor, acessibilidade)
2. Sprite único para produção, sprites parciais em dev
3. Tamanhos padronizados (16, 20, 24, 32, 48)
4. Cor herdada via currentColor
5. Lazy loading de sprites sob demanda
```

---

# 3. Arquitetura

```
Icon Engine
    │
    ├── Registry: Map<name, SVG content>
    ├── Sprite Manager: load, cache sprites
    ├── Icon Component: <ui-icon name="...">
    └── Render: <svg><use href="#icon-name"/></svg>
```

---

# 4. API Pública

```js
class IconEngine {
    constructor(framework = null) {
        this.framework = framework;
        this._registry = new Map();
        this._spriteCache = new Map();
        this._loading = new Set();
        this._spriteElement = null;
    }

    register(name, svgContent) {
        this._registry.set(name, svgContent);
        return this;
    }

    registerBatch(icons) {
        for (const [name, svg] of Object.entries(icons)) {
            this._registry.set(name, svg);
        }
        return this;
    }

    has(name) {
        return this._registry.has(name);
    }

    get(name) {
        return this._registry.get(name) || null;
    }

    render(name, options = {}) {
        if (!this._registry.has(name)) {
            this._log('warn', `Ícone não encontrado: ${name}`);
            return '';
        }

        const size = options.size || 24;
        const className = options.class || '';

        return `<svg class="ui-icon ${className}" width="${size}" height="${size}" aria-hidden="true" focusable="false">${this._registry.get(name)}</svg>`;
    }

    createElement(name, options = {}) {
        const html = this.render(name, options);
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        return template.content.firstChild;
    }

    loadSprite(url) {
        if (this._spriteCache.has(url)) {
            return Promise.resolve(this._spriteCache.get(url));
        }
        if (this._loading.has(url)) {
            return this._loading.get(url);
        }

        const promise = fetch(url)
            .then(res => res.text())
            .then(svg => {
                this._spriteCache.set(url, svg);
                this._loading.delete(url);
                this._injectSprite(svg);
                this._log('info', `Sprite carregado: ${url}`);
                return svg;
            })
            .catch(err => {
                this._loading.delete(url);
                this._log('error', `Erro ao carregar sprite: ${url}`, err);
                throw err;
            });

        this._loading.set(url, promise);
        return promise;
    }

    _injectSprite(svg) {
        if (this._spriteElement) {
            this._spriteElement.remove();
        }

        const div = document.createElement('div');
        div.innerHTML = svg;
        const svgEl = div.querySelector('svg');
        if (svgEl) {
            svgEl.style.display = 'none';
            svgEl.id = 'ui-icons-sprite';
            document.body.insertBefore(svgEl, document.body.firstChild);
            this._spriteElement = svgEl;
        }
    }

    get names() {
        return Array.from(this._registry.keys());
    }

    get count() {
        return this._registry.size;
    }

    destroy() {
        this._registry.clear();
        this._spriteCache.clear();
        this._loading.clear();
        if (this._spriteElement) {
            this._spriteElement.remove();
        }
    }

    _log(level, msg, err) {
        if (this.framework?.log) this.framework.log(level, `IconEngine: ${msg}`, err);
    }
}
```

## 4.1 Resumo da API

| Método | Descrição |
|--------|-----------|
| `register(name, svg)` | Registra ícone |
| `registerBatch(icons)` | Registra múltiplos |
| `has(name)` | Verifica se existe |
| `get(name)` | Obtém SVG content |
| `render(name, opts)` | Renderiza HTML string |
| `createElement(name, opts)` | Cria elemento DOM |
| `loadSprite(url)` | Carrega sprite SVG |

---

# 5. Tamanhos

```js
const iconSizes = {
    xs:  16,   // Inline com texto
    sm:  20,   // Botões pequenos
    md:  24,   // Botões padrão, itens de menu
    lg:  32,   // Títulos, cards
    xl:  48    // Empty states, avatares
};

// Uso
FiscalUI.icons.render('save', { size: 24 });
FiscalUI.icons.render('user', { size: iconSizes.md });
```

---

# 6. Uso em Componentes

```js
class UIButton extends UIComponent {
    render() {
        if (this._icon) {
            this._iconEl = FiscalUI.icons.createElement(this._icon, {
                size: 20,
                class: 'ui-btn__icon'
            });
            this.element.prepend(this._iconEl);
        }
    }
}
```

---

# 7. Testes

```js
describe('IconEngine', () => {
    let engine;

    beforeEach(() => { engine = new IconEngine(); });

    it('should register and retrieve icons', () => {
        engine.register('save', '<path d="..."/>');
        expect(engine.has('save')).toBe(true);
        expect(engine.get('save')).toBe('<path d="..."/>');
    });

    it('should render icon HTML', () => {
        engine.register('user', '<path d="M..."/>');
        const html = engine.render('user', { size: 24 });
        expect(html).toContain('ui-icon');
        expect(html).toContain('width="24"');
        expect(html).toContain('aria-hidden="true"');
    });

    it('should create DOM element', () => {
        engine.register('close', '<path d="..."/>');
        const el = engine.createElement('close', { size: 16 });
        expect(el.tagName).toBe('svg');
        expect(el.getAttribute('width')).toBe('16');
    });

    it('should warn on missing icon', () => {
        spyOn(console, 'warn');
        engine.render('nonexistent');
        expect(console.warn).toHaveBeenCalled();
    });

    it('should return list of names', () => {
        engine.register('a', ''); engine.register('b', '');
        expect(engine.names).toEqual(['a', 'b']);
    });
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Icon Engine |
