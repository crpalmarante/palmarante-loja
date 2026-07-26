# FiscalUI Framework

## Documento 074 — Checkbox

**Nível 4 — Formulários**

**Versão 1.0**

Checkbox estilizado com label, estados checked, indeterminate e disabled. Suporta grupo.

---

```js
class UICheckbox extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value ?? false;
        this.indeterminate = options.indeterminate || false;
        this.disabled = options.disabled || false;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <label class="ui-checkbox ${this.disabled ? 'ui-checkbox--disabled' : ''}">
                <span class="ui-checkbox__box ${this.value ? 'ui-checkbox__box--checked' : ''} ${this.indeterminate ? 'ui-checkbox__box--indeterminate' : ''}">
                    <input class="ui-checkbox__input" type="checkbox"
                           name="${this.name}" ${this.value ? 'checked' : ''}
                           ${this.disabled ? 'disabled' : ''}>
                    ${this.value ? `<span class="ui-checkbox__icon">${FiscalUI.icons.render('check', { size: 14 })}</span>` : ''}
                    ${this.indeterminate ? `<span class="ui-checkbox__icon">${FiscalUI.icons.render('minus', { size: 14 })}</span>` : ''}
                </span>
                <span class="ui-checkbox__label">${this.label}</span>
            </label>
        `;
    }

    onInit() {
        this._input = this.query('.ui-checkbox__input');
        this._box = this.query('.ui-checkbox__box');

        this._input.addEventListener('change', () => {
            this.value = this._input.checked;
            this._box.classList.toggle('ui-checkbox__box--checked', this.value);
            this._updateIcon();
            this.emit('field:change', { name: this.name, value: this.value });
        });
    }

    _updateIcon() {
        let icon = this._box.querySelector('.ui-checkbox__icon');
        if (!icon) { icon = document.createElement('span'); icon.className = 'ui-checkbox__icon'; this._box.appendChild(icon); }
        icon.innerHTML = this.indeterminate
            ? FiscalUI.icons.render('minus', { size: 14 })
            : this.value ? FiscalUI.icons.render('check', { size: 14 }) : '';
        icon.style.display = this.value || this.indeterminate ? '' : 'none';
    }

    setIndeterminate(val) {
        this.indeterminate = val;
        this._input.indeterminate = val;
        this._box.classList.toggle('ui-checkbox__box--indeterminate', val);
        this._updateIcon();
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) { this._input.checked = val; this._box.classList.toggle('ui-checkbox__box--checked', val); this._updateIcon(); } }
    reset() { this.setValue(false); this.setIndeterminate(false); }
}
```

```css
.ui-checkbox {
    display: inline-flex; align-items: center; gap: var(--spacing-sm);
    cursor: pointer; font-size: var(--font-size-md);
}
.ui-checkbox--disabled { opacity: 0.5; cursor: not-allowed; }

.ui-checkbox__box {
    display: flex; align-items: center; justify-content: center;
    width: 20px; height: 20px;
    border: 2px solid var(--color-border); border-radius: var(--radius-sm);
    background: var(--color-surface); transition: border-color var(--motion-fast), background var(--motion-fast);
    position: relative; flex-shrink: 0;
}
.ui-checkbox__box--checked { border-color: var(--color-primary); background: var(--color-primary); }
.ui-checkbox__box--indeterminate { border-color: var(--color-primary); }

.ui-checkbox__input { position: absolute; opacity: 0; width: 0; height: 0; }
.ui-checkbox__icon { display: flex; color: #fff; }
.ui-checkbox__label { user-select: none; }

/* Grupo */
.ui-checkbox-group { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-checkbox-group--horizontal { flex-direction: row; flex-wrap: wrap; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
