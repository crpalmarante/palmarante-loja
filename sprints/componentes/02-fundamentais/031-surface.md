# FiscalUI Framework

## Documento 031 — Surface

**Nível 2 — Basic Components**

**Versão 1.0**

Container de fundo com elevação variável. Usado como wrapper genérico para aplicar superfície e sombra.

---

```js
class UISurface extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.elevation = options.elevation || 0;   // 0-5
        this.padding = options.padding || 'md';
        this.border = options.border || false;
        this.radius = options.radius || 'md';
    }

    template() {
        return `
            <div class="ui-surface ui-surface--elevation-${this.elevation}
                        ui-surface--radius-${this.radius}
                        ui-surface--pad-${this.padding}
                        ${this.border ? 'ui-surface--bordered' : ''}"></div>
        `;
    }

    onInit() { this._content = this.element; }
    setContent(html) { this._content.innerHTML = html; }
    appendContent(el) { this._content.appendChild(el); }
}
```

```css
.ui-surface { background: var(--color-surface); }

.ui-surface--bordered { border: 1px solid var(--color-border); }

.ui-surface--radius-none { border-radius: 0; }
.ui-surface--radius-sm   { border-radius: var(--radius-sm); }
.ui-surface--radius-md   { border-radius: var(--radius-md); }
.ui-surface--radius-lg   { border-radius: var(--radius-lg); }

.ui-surface--pad-none { padding: 0; }
.ui-surface--pad-sm   { padding: var(--spacing-sm); }
.ui-surface--pad-md   { padding: var(--spacing-md); }
.ui-surface--pad-lg   { padding: var(--spacing-lg); }

.ui-surface--elevation-0 { box-shadow: none; }
.ui-surface--elevation-1 { box-shadow: var(--shadow-sm); }
.ui-surface--elevation-2 { box-shadow: var(--shadow-md); }
.ui-surface--elevation-3 { box-shadow: var(--shadow-lg); }
.ui-surface--elevation-4 { box-shadow: var(--shadow-xl); }
.ui-surface--elevation-5 { box-shadow: var(--shadow-2xl); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
