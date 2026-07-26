# FiscalUI Framework

## Documento 072 — AutoComplete

**Nível 4 — Formulários**

**Versão 1.0**

Input com sugestões automáticas à medida que o usuário digita. Busca local ou remota.

---

```js
class UIAutoComplete extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.placeholder = options.placeholder || '';
        this.source = options.source || [];
        this.minChars = options.minChars || 2;
        this.debounce = options.debounce || 300;
        this.maxResults = options.maxResults || 10;
        this.rules = options.rules || [];
        this._open = false;
        this._timer = null;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-autocomplete">
                    <div class="ui-field__input-wrapper">
                        <input class="ui-field__input ui-autocomplete__input" type="text"
                               name="${this.name}" placeholder="${this.placeholder}"
                               value="${this.value}" autocomplete="off">
                        <span class="ui-autocomplete__loader" hidden>${FiscalUI.icons.render('loader', { size: 16 })}</span>
                    </div>
                    <div class="ui-autocomplete__dropdown" hidden></div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-autocomplete__input');
        this._dropdown = this.query('.ui-autocomplete__dropdown');
        this._loader = this.query('.ui-autocomplete__loader');

        this._input.addEventListener('input', () => {
            this.value = this._input.value;
            clearTimeout(this._timer);
            if (this._input.value.length >= this.minChars) {
                this._timer = setTimeout(() => this._search(), this.debounce);
            } else {
                this.close();
            }
            this.emit('field:change', { name: this.name, value: this.value });
        });

        this._input.addEventListener('blur', () => {
            setTimeout(() => this.close(), 200);
            this.emit('field:blur', { name: this.name });
        });

        this._input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.close();
            if (e.key === 'ArrowDown') { e.preventDefault(); this._next(); }
            if (e.key === 'ArrowUp') { e.preventDefault(); this._prev(); }
            if (e.key === 'Enter' && this._open) { e.preventDefault(); this._selectActive(); }
        });

        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });
    }

    async _search() {
        const q = this._input.value;
        let results;
        if (typeof this.source === 'function') {
            this._loader.hidden = false;
            try { results = await this.source(q); } catch { results = []; }
            this._loader.hidden = true;
        } else {
            results = this.source.filter(s => s.toLowerCase().includes(q.toLowerCase()));
        }
        results = results.slice(0, this.maxResults);
        if (!results.length) { this.close(); return; }
        this._showResults(results);
    }

    _showResults(results) {
        this._dropdown.innerHTML = results.map((r, i) =>
            `<div class="ui-autocomplete__item ${i === 0 ? 'ui-autocomplete__item--active' : ''}" data-value="${r}">${r}</div>`
        ).join('');
        this._dropdown.hidden = false;
        this._open = true;
        this._activeIndex = 0;

        this._dropdown.querySelectorAll('.ui-autocomplete__item').forEach(el => {
            el.addEventListener('click', () => this._select(el.dataset.value));
            el.addEventListener('mouseenter', () => {
                this._dropdown.querySelectorAll('.ui-autocomplete__item').forEach(e => e.classList.remove('ui-autocomplete__item--active'));
                el.classList.add('ui-autocomplete__item--active');
            });
        });
    }

    _select(value) {
        this._input.value = value;
        this.value = value;
        this.close();
        this.emit('autocomplete:select', { value });
        this.emit('field:change', { name: this.name, value: this.value });
    }

    _next() {
        const items = this._dropdown.querySelectorAll('.ui-autocomplete__item');
        if (!items.length) return;
        this._activeIndex = (this._activeIndex + 1) % items.length;
        items.forEach((el, i) => el.classList.toggle('ui-autocomplete__item--active', i === this._activeIndex));
    }

    _prev() {
        const items = this._dropdown.querySelectorAll('.ui-autocomplete__item');
        if (!items.length) return;
        this._activeIndex = (this._activeIndex - 1 + items.length) % items.length;
        items.forEach((el, i) => el.classList.toggle('ui-autocomplete__item--active', i === this._activeIndex));
    }

    _selectActive() {
        const active = this._dropdown.querySelector('.ui-autocomplete__item--active');
        if (active) this._select(active.dataset.value);
    }

    close() { this._dropdown.hidden = true; this._open = false; }
    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val; }
    reset() { this.setValue(''); }
}
```

```css
.ui-autocomplete { position: relative; }
.ui-autocomplete__loader { padding: 0 var(--spacing-sm); color: var(--color-text-muted); display: flex; animation: ui-spin 1s linear infinite; }

.ui-autocomplete__dropdown {
    position: absolute; top: 100%; left: 0; right: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg); max-height: 200px; overflow-y: auto;
}

.ui-autocomplete__item {
    padding: var(--spacing-sm) var(--spacing-md); cursor: pointer;
    font-size: var(--font-size-sm); transition: background var(--motion-fast);
}
.ui-autocomplete__item:hover, .ui-autocomplete__item--active { background: var(--color-surface-hover); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
