# FiscalUI Framework

## Documento 033 — Container

**Nível 2 — Basic Components**

**Versão 1.0**

Container de largura máxima controlada. Centraliza o conteúdo horizontalmente com breakpoints responsivos.

---

```js
class UIContainer extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.size = options.size || 'lg';         // sm, md, lg, xl, fluid
        this.padding = options.padding || true;
    }

    template() {
        return `<div class="ui-container ui-container--${this.size} ${this.padding ? 'ui-container--pad' : ''}"></div>`;
    }

    onInit() { this._content = this.element; }
    setContent(html) { this._content.innerHTML = html; }
    appendContent(el) { this._content.appendChild(el); }
}
```

```css
.ui-container {
    width: 100%;
    margin: 0 auto;
}

.ui-container--pad { padding-left: var(--spacing-md); padding-right: var(--spacing-md); }
.ui-container--sm  { max-width: 640px; }
.ui-container--md  { max-width: 768px; }
.ui-container--lg  { max-width: 1024px; }
.ui-container--xl  { max-width: 1280px; }
.ui-container--fluid { max-width: 100%; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
