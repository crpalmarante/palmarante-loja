# FiscalUI Framework

## Documento 081 — TimePicker

**Nível 4 — Formulários**

**Versão 1.0**

Seletor de horário com input de hora e minuto, formato 24h e lista de opções.

---

```js
class UITimePicker extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.placeholder = options.placeholder || '00:00';
        this.format24 = options.format24 !== false;
        this.interval = options.interval || 30;
        this.rules = options.rules || [];
        this._open = false;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-timepicker">
                    <div class="ui-field__input-wrapper">
                        <span class="ui-field__prefix-icon">${FiscalUI.icons.render('clock', { size: 16 })}</span>
                        <input class="ui-field__input ui-timepicker__input" type="text" readonly
                               placeholder="${this.placeholder}" value="${this.value}" autocomplete="off">
                    </div>
                    <div class="ui-timepicker__dropdown" hidden>
                        <div class="ui-timepicker__list">${this._renderOptions()}</div>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _renderOptions() {
        const items = [];
        for (let h = 0; h < 24; h++) {
            for (let m = 0; m < 60; m += this.interval) {
                items.push(`${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`);
            }
        }
        return items.map(t => `
            <div class="ui-timepicker__item ${t === this.value ? 'ui-timepicker__item--selected' : ''}" data-value="${t}">${t}</div>
        `).join('');
    }

    onInit() {
        this._input = this.query('.ui-timepicker__input');
        this._dropdown = this.query('.ui-timepicker__dropdown');

        this._input.addEventListener('click', () => this.toggle());
        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.close(); });

        this._dropdown.addEventListener('click', (e) => {
            const item = e.target.closest('.ui-timepicker__item');
            if (!item) return;
            this.select(item.dataset.value);
        });
    }

    select(value) {
        this.value = value;
        this._input.value = value;
        this.close();
        this.emit('field:change', { name: this.name, value: this.value });
    }

    toggle() { this._open ? this.close() : this.open(); }
    open() { this._open = true; this._dropdown.hidden = false; }
    close() { this._open = false; this._dropdown.hidden = true; }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val; }
    reset() { this.setValue(''); }
}
```

```css
.ui-timepicker { position: relative; }
.ui-timepicker__input { cursor: pointer; }

.ui-timepicker__dropdown {
    position: absolute; top: 100%; left: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
    width: 120px; max-height: 200px; overflow-y: auto;
}

.ui-timepicker__list { padding: var(--spacing-xs); }
.ui-timepicker__item {
    padding: var(--spacing-xs) var(--spacing-md); cursor: pointer;
    border-radius: var(--radius-sm); font-size: var(--font-size-sm);
    font-family: monospace; transition: background var(--motion-fast);
}
.ui-timepicker__item:hover { background: var(--color-surface-hover); }
.ui-timepicker__item--selected { background: var(--color-primary-surface); color: var(--color-primary); font-weight: var(--font-weight-semibold); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
