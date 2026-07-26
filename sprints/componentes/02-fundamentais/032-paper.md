# FiscalUI Framework

## Documento 032 — Paper

**Nível 2 — Basic Components**

**Versão 1.0**

Container para destacar conteúdo do fundo. Similar ao Surface, mas com fundo branco puro e borda sutil. Ideal para formulários e leitura.

---

```js
class UIPaper extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.padding = options.padding || 'lg';
        this.elevation = options.elevation || 0;
    }

    template() {
        return `<div class="ui-paper ui-paper--pad-${this.padding} ui-surface--elevation-${this.elevation}"></div>`;
    }

    onInit() { this._content = this.element; }
    setContent(html) { this._content.innerHTML = html; }
}
```

```css
.ui-paper {
    background: #fff;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
}

.ui-paper--pad-none { padding: 0; }
.ui-paper--pad-sm   { padding: var(--spacing-md); }
.ui-paper--pad-md   { padding: var(--spacing-lg); }
.ui-paper--pad-lg   { padding: var(--spacing-xl); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
