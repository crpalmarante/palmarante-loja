# FiscalUI Framework

## Documento 070 — Select

**Nível 4 — Formulários**

**Versão 1.0**

Select estilizado com busca, grupos e valor vazio. Substitui o `<select>` nativo.

---

```js
class UISelect extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.options = options.options || [];
        this.value = options.value ?? '';
        this.placeholder = options.placeholder || 'Selecione…';
        this.searchable = options.searchable || false;
        this.clearable = options.clearable || false;
        this.rules = options.rules || [{ type: 'required' }];
        this._open = false;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-select" tabindex="0">
                    <div class="ui-select__trigger">
                        <span class="ui-select__value">${this._selectedLabel() || this.placeholder}</span>
                        ${this.clearable && this.value ? `<button class="ui-select__clear" aria-label="Limpar">${FiscalUI.icons.render('x', { size: 14 })}</button>` : ''}
                        <span class="ui-select__arrow">${FiscalUI.icons.render('chevron-down', { size: 16 })}</span>
                    </div>
                    <div class="ui-select__dropdown" hidden>
                        ${this.searchable ? `<div class="ui-select__search"><input class="ui-select__search-input" type="text" placeholder="Buscar..."></div>` : ''}
                        <div class="ui-select__options">${this._renderOptions()}</div>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _selectedLabel() {
        const opt = this.options.find(o => o.value === this.value);
        return opt?.label || '';
    }

    _renderOptions() {
        const groups = {};
        this.options.forEach(o => {
            const g = o.group || '_default';
            if (!groups[g]) groups[g] = [];
            groups[g].push(o);
        });
        return Object.entries(groups).map(([group, opts]) => `
            ${group !== '_default' ? `<div class="ui-select__group-label">${group}</div>` : ''}
            ${opts.map(o => `
                <div class="ui-select__option ${o.value === this.value ? 'ui-select__option--selected' : ''} ${o.disabled ? 'ui-select__option--disabled' : ''}"
                     data-value="${o.value}">${o.label}</div>
            `).join('')}
        `).join('');
    }

    onInit() {
        this._trigger = this.query('.ui-select__trigger');
        this._dropdown = this.query('.ui-select__dropdown');
        this._valueEl = this.query('.ui-select__value');
        this._optionsEl = this.query('.ui-select__options');

        this._trigger.addEventListener('click', () => this.toggle());
        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.close(); });

        this._optionsEl.addEventListener('click', (e) => {
            const opt = e.target.closest('.ui-select__option');
            if (!opt || opt.classList.contains('ui-select__option--disabled')) return;
            this.select(opt.dataset.value);
        });

        this.query('.ui-select__clear')?.addEventListener('click', (e) => { e.stopPropagation(); this.clear(); });

        if (this.searchable) {
            const searchInput = this.query('.ui-select__search-input');
            searchInput?.addEventListener('input', () => {
                const q = searchInput.value.toLowerCase();
                this.queryAll('.ui-select__option').forEach(el => {
                    el.hidden = !el.textContent.toLowerCase().includes(q);
                });
            });
        }
    }

    toggle() { this._open ? this.close() : this.open(); }
    open() { this._open = true; this._dropdown.hidden = false; this.element.classList.add('ui-select--open'); }
    close() { this._open = false; this._dropdown.hidden = true; this.element.classList.remove('ui-select--open'); }

    select(value) {
        this.value = value;
        this._valueEl.textContent = this._selectedLabel() || this.placeholder;
        this.queryAll('.ui-select__option').forEach(el => el.classList.toggle('ui-select__option--selected', el.dataset.value === value));
        this.close();
        this.emit('field:change', { name: this.name, value: this.value });
    }

    clear() { this.select(''); }

    value() { return this.value; }
    setValue(val) { this.select(val); }
    reset() { this.clear(); }
}
```

```css
.ui-select { position: relative; }
.ui-select__trigger {
    display: flex; align-items: center; gap: var(--spacing-xs);
    padding: 0 var(--spacing-sm); height: 40px;
    border: 1px solid var(--color-border); border-radius: var(--radius-md);
    background: var(--color-surface); cursor: pointer;
    transition: border-color var(--motion-fast);
}
.ui-select--open .ui-select__trigger,
.ui-select__trigger:focus-within { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-surface); }
.ui-select__value { flex: 1; color: var(--color-text); font-size: var(--font-size-md); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ui-select__trigger .ui-select__value:empty::before { content: attr(placeholder); color: var(--color-text-muted); }
.ui-select__clear { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); padding: 2px; border-radius: 50%; display: flex; }
.ui-select__clear:hover { background: var(--color-surface-hover); }
.ui-select__arrow { color: var(--color-text-muted); transition: transform var(--motion-fast); }
.ui-select--open .ui-select__arrow { transform: rotate(180deg); }

.ui-select__dropdown {
    position: absolute; top: 100%; left: 0; right: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
    max-height: 260px; overflow: hidden; display: flex; flex-direction: column;
}

.ui-select__search { padding: var(--spacing-xs); border-bottom: 1px solid var(--color-border); }
.ui-select__search-input { width: 100%; padding: var(--spacing-xs) var(--spacing-sm); border: 1px solid var(--color-border); border-radius: var(--radius-sm); font-size: var(--font-size-sm); outline: none; }

.ui-select__options { overflow-y: auto; max-height: 200px; padding: var(--spacing-xs); }
.ui-select__group-label { font-size: var(--font-size-xs); color: var(--color-text-muted); padding: var(--spacing-xs) var(--spacing-sm); font-weight: var(--font-weight-semibold); text-transform: uppercase; }
.ui-select__option { padding: var(--spacing-sm) var(--spacing-md); cursor: pointer; border-radius: var(--radius-sm); font-size: var(--font-size-sm); transition: background var(--motion-fast); }
.ui-select__option:hover { background: var(--color-surface-hover); }
.ui-select__option--selected { background: var(--color-primary-surface); color: var(--color-primary); }
.ui-select__option--disabled { opacity: 0.4; cursor: not-allowed; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
