# FiscalUI Framework

## Documento 110 — Blank Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout vazio mínimo, sem sidebar ou navbar. Apenas conteúdo centralizado com padding opcional.

---

```js
class BlankLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.content = options.content || '';
        this.padding = options.padding !== false;
        this.centered = options.centered || false;
        this.maxWidth = options.maxWidth || '';
    }

    template() {
        return `
            <div class="ui-layout-blank ${this.padding ? 'ui-layout-blank--pad' : ''} ${this.centered ? 'ui-layout-blank--centered' : ''}"
                 ${this.maxWidth ? `style="max-width: ${typeof this.maxWidth === 'number' ? this.maxWidth + 'px' : this.maxWidth}"` : ''}>
                ${this.content || '<div class="ui-layout-blank__placeholder">Conteúdo</div>'}
            </div>
        `;
    }

    onInit() {
        this._content = this.element;
    }

    setContent(html) { this._content.innerHTML = html; }
}
```

```css
.ui-layout-blank { min-height: 100vh; }
.ui-layout-blank--pad { padding: var(--spacing-lg); }
.ui-layout-blank--centered { display: flex; flex-direction: column; align-items: center; margin: 0 auto; }
.ui-layout-blank__placeholder { text-align: center; color: var(--color-text-muted); padding: var(--spacing-xl); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
