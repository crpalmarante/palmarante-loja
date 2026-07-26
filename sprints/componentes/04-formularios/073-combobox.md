# FiscalUI Framework

## Documento 073 — ComboBox

**Nível 4 — Formulários**

**Versão 1.0**

Select editável com input + dropdown. Usuário pode digitar ou selecionar. Combina Input + Select.

---

```js
class UIComboBox extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.options = options.options || [];
        this.value = options.value || '';
        this.placeholder = options.placeholder || '';
        this.creatable = options.creatable || false;
        this.rules = options.rules || [];
        this._open = false;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-combobox">
                    <div class="ui-field__input-wrapper">
                        <input class="ui-field__input ui-combobox__input" type="text"
                               name="${this.name}" placeholder="${this.placeholder}"
                               value="${this.value}" autocomplete="off">
                        <button class="ui-combobox__toggle" type="button" aria-label="Abrir" tabindex="-1">
                            ${FiscalUI.icons.render('chevron-down', { size: 16 })}
                        </button>
                    </div>
                    <div class="ui-combobox__dropdown" hidden>
                        <div class="ui-combobox__options">${this._renderOptions()}</div>
                        ${this.creatable ? `<div class="ui-combobox__create" hidden><button type="button">Adicionar "<span></span>"</button></div>` : ''}
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _renderOptions() {
        return this.options.map(o => `
            <div class="ui-combobox__option ${o.value === this.value ? 'ui-combobox__option--selected' : ''} ${o.disabled ? 'ui-combobox__option--disabled' : ''}"
                 data-value="${o.value}">${o.label}</div>
        `).join('');
    }

    onInit() {
        this._input = this.query('.ui-combobox__input');
        this._toggle = this.query('.ui-combobox__toggle');
        this._dropdown = this.query('.ui-combobox__dropdown');
        this._optionsEl = this.query('.ui-combobox__options');
        this._createEl = this.query('.ui-combobox__create');

        this._toggle.addEventListener('click', () => this.toggle());
        this._input.addEventListener('focus', () => this.open());
        this._input.addEventListener('input', () => {
            this.value = this._input.value;
            this._filter();
            this.emit('field:change', { name: this.name, value: this.value });
        });
        this._input.addEventListener('blur', () => setTimeout(() => this.close(), 200));
        this._input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.close();
            if (e.key === 'ArrowDown') { e.preventDefault(); this._next(); }
            if (e.key === 'ArrowUp') { e.preventDefault(); this._prev(); }
            if (e.key === 'Enter') { e.preventDefault(); this._selectActive(); }
        });

        this._optionsEl.addEventListener('click', (e) => {
            const opt = e.target.closest('.ui-combobox__option');
            if (opt && !opt.classList.contains('ui-combobox__option--disabled')) this._select(opt.dataset.value, opt.textContent);
        });

        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });
    }

    _filter() {
        const q = this._input.value.toLowerCase();
        let visible = 0;
        this.queryAll('.ui-combobox__option').forEach(el => {
            const match = el.textContent.toLowerCase().includes(q);
            el.hidden = !match;
            if (match) visible++;
        });
        this.open();
        if (this.creatable) {
            const exists = this.options.some(o => o.label.toLowerCase() === q);
            if (q && !exists) {
                this._createEl.hidden = false;
                this._createEl.querySelector('span').textContent = q;
            } else {
                this._createEl.hidden = true;
            }
        }
    }

    _select(value, label) {
        this.value = value;
        this._input.value = label || value;
        this.close();
        this.emit('field:change', { name: this.name, value: this.value });
    }

    _selectActive() {
        const active = this._optionsEl.querySelector('.ui-combobox__option:not([hidden])');
        if (active) { this._select(active.dataset.value, active.textContent); return; }
        if (this.creatable && !this._createEl.hidden) {
            const val = this._createEl.querySelector('span').textContent;
            this._select(val, val);
        }
    }

    _next() { this._move(1); }
    _prev() { this._move(-1); }
    _move(dir) {
        const items = [...this._optionsEl.querySelectorAll('.ui-combobox__option:not([hidden])')];
        if (!items.length) return;
        const idx = items.findIndex(el => el.classList.contains('ui-combobox__option--active'));
        items.forEach(el => el.classList.remove('ui-combobox__option--active'));
        const next = Math.max(0, Math.min(items.length - 1, (idx === -1 ? -1 : idx) + dir));
        items[next]?.classList.add('ui-combobox__option--active');
    }

    toggle() { this._open ? this.close() : this.open(); }
    open() { this._open = true; this._dropdown.hidden = false; }
    close() { this._open = false; this._dropdown.hidden = true; }

    value() { return this.value; }
    setValue(val) { this.value = val; const opt = this.options.find(o => o.value === val); if (this._input) this._input.value = opt?.label || val; }
    reset() { this.setValue(''); }
}
```

```css
.ui-combobox { position: relative; }
.ui-combobox__toggle {
    border: none; background: transparent; cursor: pointer;
    padding: 0 var(--spacing-sm); color: var(--color-text-muted);
    display: flex; align-items: center;
}
.ui-combobox__toggle:hover { color: var(--color-text); }

.ui-combobox__dropdown {
    position: absolute; top: 100%; left: 0; right: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg); max-height: 200px; overflow-y: auto;
}

.ui-combobox__option {
    padding: var(--spacing-sm) var(--spacing-md); cursor: pointer;
    font-size: var(--font-size-sm); transition: background var(--motion-fast);
}
.ui-combobox__option:hover, .ui-combobox__option--active { background: var(--color-surface-hover); }
.ui-combobox__option--selected { background: var(--color-primary-surface); color: var(--color-primary); }
.ui-combobox__option--disabled { opacity: 0.4; cursor: not-allowed; }

.ui-combobox__create { border-top: 1px solid var(--color-border); padding: var(--spacing-xs); }
.ui-combobox__create button { width: 100%; padding: var(--spacing-sm); border: none; background: transparent; cursor: pointer; font-size: var(--font-size-sm); color: var(--color-primary); border-radius: var(--radius-sm); }
.ui-combobox__create button:hover { background: var(--color-primary-surface); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
