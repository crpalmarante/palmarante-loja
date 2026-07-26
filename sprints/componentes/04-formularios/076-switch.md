# FiscalUI Framework

## Documento 076 — Switch

**Nível 4 — Formulários**

**Versão 1.0**

Toggle switch (ligado/desligado). Alternativa visual ao checkbox para valores booleanos.

---

```js
class UISwitch extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value ?? false;
        this.disabled = options.disabled || false;
        this.size = options.size || 'md';        // sm, md, lg
        this.rules = options.rules || [];
    }

    template() {
        return `
            <label class="ui-switch ui-switch--${this.size} ${this.disabled ? 'ui-switch--disabled' : ''}">
                <span class="ui-switch__track ${this.value ? 'ui-switch__track--on' : ''}">
                    <input class="ui-switch__input" type="checkbox" role="switch"
                           name="${this.name}" ${this.value ? 'checked' : ''}
                           ${this.disabled ? 'disabled' : ''}>
                    <span class="ui-switch__thumb"></span>
                </span>
                ${this.label ? `<span class="ui-switch__label">${this.label}</span>` : ''}
            </label>
        `;
    }

    onInit() {
        this._input = this.query('.ui-switch__input');
        this._track = this.query('.ui-switch__track');

        this._input.addEventListener('change', () => {
            this.value = this._input.checked;
            this._track.classList.toggle('ui-switch__track--on', this.value);
            this.emit('field:change', { name: this.name, value: this.value });
        });
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) { this._input.checked = val; this._track.classList.toggle('ui-switch__track--on', val); } }
    reset() { this.setValue(false); }
}
```

```css
.ui-switch { display: inline-flex; align-items: center; gap: var(--spacing-sm); cursor: pointer; }
.ui-switch--disabled { opacity: 0.5; cursor: not-allowed; }

.ui-switch__track {
    position: relative; display: inline-block;
    border-radius: 999px; background: var(--color-surface-hover);
    border: 1px solid var(--color-border);
    transition: background var(--motion-fast);
    cursor: pointer;
}
.ui-switch__track--on { background: var(--color-primary); border-color: var(--color-primary); }

.ui-switch__input { position: absolute; opacity: 0; width: 0; height: 0; }

.ui-switch__thumb {
    position: absolute; top: 2px; left: 2px;
    background: #fff; border-radius: 50%;
    box-shadow: var(--shadow-sm);
    transition: transform var(--motion-fast);
}
.ui-switch__track--on .ui-switch__thumb { transform: translateX(100%); }

.ui-switch__label { user-select: none; font-size: var(--font-size-md); }

.ui-switch--sm .ui-switch__track { width: 32px; height: 20px; }
.ui-switch--sm .ui-switch__thumb { width: 14px; height: 14px; }

.ui-switch--md .ui-switch__track { width: 44px; height: 26px; }
.ui-switch--md .ui-switch__thumb { width: 20px; height: 20px; }

.ui-switch--lg .ui-switch__track { width: 56px; height: 32px; }
.ui-switch--lg .ui-switch__thumb { width: 26px; height: 26px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
