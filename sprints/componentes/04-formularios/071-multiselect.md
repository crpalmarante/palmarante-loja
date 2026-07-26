# FiscalUI Framework

## Documento 071 — MultiSelect

**Nível 4 — Formulários**

**Versão 1.0**

Select múltiplo com tags selecionadas, busca e seleção em lote.

---

```js
class UIMultiSelect extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.options = options.options || [];
        this.value = options.value || [];
        this.placeholder = options.placeholder || 'Selecione…';
        this.maxItems = options.maxItems || 0;
        this.searchable = options.searchable !== false;
        this.rules = options.rules || [];
        this._open = false;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-multiselect" tabindex="0">
                    <div class="ui-multiselect__trigger">
                        <div class="ui-multiselect__tags">
                            ${this.value.map(v => {
                                const opt = this.options.find(o => o.value === v);
                                return opt ? `<span class="ui-multiselect__tag">${opt.label} <button class="ui-multiselect__tag-remove" data-value="${v}">&times;</button></span>` : '';
                            }).join('')}
                            <input class="ui-multiselect__input" type="text" placeholder="${this.value.length ? '' : this.placeholder}">
                        </div>
                        <span class="ui-select__arrow">${FiscalUI.icons.render('chevron-down', { size: 16 })}</span>
                    </div>
                    <div class="ui-multiselect__dropdown" hidden>
                        <div class="ui-multiselect__options">${this._renderOptions()}</div>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _renderOptions() {
        return this.options.map(o => `
            <label class="ui-multiselect__option ${this.value.includes(o.value) ? 'ui-multiselect__option--selected' : ''} ${o.disabled ? 'ui-multiselect__option--disabled' : ''}">
                <input type="checkbox" class="ui-multiselect__checkbox"
                       value="${o.value}" ${this.value.includes(o.value) ? 'checked' : ''} ${o.disabled ? 'disabled' : ''}>
                <span>${o.label}</span>
            </label>
        `).join('');
    }

    onInit() {
        this._trigger = this.query('.ui-multiselect__trigger');
        this._dropdown = this.query('.ui-multiselect__dropdown');
        this._tags = this.query('.ui-multiselect__tags');
        this._input = this.query('.ui-multiselect__input');

        this._trigger.addEventListener('click', (e) => { if (!e.target.closest('.ui-multiselect__tag-remove')) this.toggle(); });
        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });

        this._dropdown.addEventListener('click', (e) => {
            const opt = e.target.closest('.ui-multiselect__option');
            if (!opt || opt.classList.contains('ui-multiselect__option--disabled')) return;
            const checkbox = opt.querySelector('input');
            const val = checkbox.value;
            if (this.value.includes(val)) this._remove(val);
            else this._add(val);
        });

        this._tags.addEventListener('click', (e) => {
            const remove = e.target.closest('.ui-multiselect__tag-remove');
            if (remove) this._remove(remove.dataset.value);
        });

        this._input.addEventListener('input', () => {
            const q = this._input.value.toLowerCase();
            this.queryAll('.ui-multiselect__option').forEach(el => {
                el.hidden = !el.textContent.toLowerCase().includes(q);
            });
        });

        this._input.addEventListener('focus', () => this.open());
    }

    toggle() { this._open ? this.close() : this.open(); }
    open() { this._open = true; this._dropdown.hidden = false; this.element.classList.add('ui-select--open'); this._input.focus(); }
    close() { this._open = false; this._dropdown.hidden = true; this.element.classList.remove('ui-select--open'); }

    _add(val) {
        if (this.maxItems && this.value.length >= this.maxItems) return;
        if (!this.value.includes(val)) {
            this.value = [...this.value, val];
            this._sync();
        }
    }

    _remove(val) {
        this.value = this.value.filter(v => v !== val);
        this._sync();
    }

    _sync() {
        this.render();
        this.onInit();
        this.emit('field:change', { name: this.name, value: this.value });
    }

    value() { return [...this.value]; }
    setValue(val) { this.value = [...val]; this._sync(); }
    reset() { this.value = []; this._sync(); }
}
```

```css
.ui-multiselect { position: relative; }
.ui-multiselect__trigger {
    display: flex; align-items: center; gap: var(--spacing-xs);
    min-height: 40px; padding: 2px var(--spacing-sm);
    border: 1px solid var(--color-border); border-radius: var(--radius-md);
    background: var(--color-surface); cursor: text;
    transition: border-color var(--motion-fast);
}
.ui-select--open .ui-multiselect__trigger { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-surface); }

.ui-multiselect__tags { display: flex; flex-wrap: wrap; gap: 2px; flex: 1; }
.ui-multiselect__tag {
    display: inline-flex; align-items: center; gap: 2px;
    padding: 1px 6px; background: var(--color-primary-surface);
    color: var(--color-primary); border-radius: var(--radius-sm);
    font-size: var(--font-size-sm); line-height: 1.5;
}
.ui-multiselect__tag-remove { border: none; background: transparent; cursor: pointer; color: inherit; font-size: 14px; line-height: 1; padding: 0; margin-left: 2px; }

.ui-multiselect__input { border: none; outline: none; background: transparent; font-size: var(--font-size-sm); min-width: 80px; flex: 1; min-height: 28px; }
.ui-multiselect__input::placeholder { color: var(--color-text-muted); }

.ui-multiselect__dropdown {
    position: absolute; top: 100%; left: 0; right: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg); max-height: 200px; overflow-y: auto;
}

.ui-multiselect__option {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md); cursor: pointer;
    font-size: var(--font-size-sm); transition: background var(--motion-fast);
}
.ui-multiselect__option:hover { background: var(--color-surface-hover); }
.ui-multiselect__option--selected { background: var(--color-primary-surface); }
.ui-multiselect__option--disabled { opacity: 0.4; cursor: not-allowed; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
