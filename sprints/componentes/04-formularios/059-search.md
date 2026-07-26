# FiscalUI Framework

## Documento 059 — Search

**Nível 4 — Formulários**

**Versão 1.0**

Campo de busca dentro de formulários. Difere da Search Bar (N3) por ser um input de formulário, não um navegador de tela.

---

```js
class UIFormSearch extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.placeholder = options.placeholder || 'Buscar…';
        this.value = options.value || '';
        this.debounce = options.debounce || 0;
        this.rules = options.rules || [];
        this._timer = null;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    <span class="ui-field__prefix-icon">${FiscalUI.icons.render('search', { size: 16 })}</span>
                    <input class="ui-field__input" type="search" name="${this.name}"
                           placeholder="${this.placeholder}" value="${this.value}" autocomplete="off">
                    <button class="ui-field__clear-search" hidden aria-label="Limpar">${FiscalUI.icons.render('x', { size: 14 })}</button>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');
        this._clear = this.query('.ui-field__clear-search');

        this._input.addEventListener('input', () => {
            this.value = this._input.value;
            this._clear.hidden = !this.value;
            clearTimeout(this._timer);
            if (this.debounce) {
                this._timer = setTimeout(() => this.emit('field:change', { name: this.name, value: this.value }), this.debounce);
            } else {
                this.emit('field:change', { name: this.name, value: this.value });
            }
        });

        this._clear.addEventListener('click', () => {
            this.setValue('');
            this._input.focus();
            this.emit('field:change', { name: this.name, value: '' });
        });

        this._input.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));
    }

    value() { return this._input?.value || this.value; }
    setValue(val) { this.value = val; if (this._input) { this._input.value = val; this._clear.hidden = !val; } }
    reset() { this.setValue(''); }
    focus() { this._input?.focus(); }
}
```

```css
.ui-field__prefix-icon { padding: 0 var(--spacing-xs) 0 var(--spacing-sm); color: var(--color-text-muted); display: flex; }
.ui-field__clear-search {
    border: none; background: transparent; cursor: pointer;
    padding: 0 var(--spacing-sm); color: var(--color-text-muted); display: flex; align-items: center;
}
.ui-field__clear-search:hover { color: var(--color-text); }

/* Remove browser default search reset */
.ui-field__input[type="search"]::-webkit-search-decoration,
.ui-field__input[type="search"]::-webkit-search-cancel-button,
.ui-field__input[type="search"]::-webkit-search-results-button,
.ui-field__input[type="search"]::-webkit-search-results-decoration { display: none; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
