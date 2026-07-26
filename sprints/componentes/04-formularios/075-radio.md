# FiscalUI Framework

## Documento 075 — Radio

**Nível 4 — Formulários**

**Versão 1.0**

Radio button estilizado com label e agrupamento automático pelo atributo `name`.

---

```js
class UIRadio extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.checked = options.checked || false;
        this.disabled = options.disabled || false;
    }

    template() {
        return `
            <label class="ui-radio ${this.disabled ? 'ui-radio--disabled' : ''}">
                <span class="ui-radio__circle ${this.checked ? 'ui-radio__circle--checked' : ''}">
                    <input class="ui-radio__input" type="radio"
                           name="${this.name}" value="${this.value}"
                           ${this.checked ? 'checked' : ''} ${this.disabled ? 'disabled' : ''}>
                    <span class="ui-radio__dot"></span>
                </span>
                <span class="ui-radio__label">${this.label}</span>
            </label>
        `;
    }

    onInit() {
        this._input = this.query('.ui-radio__input');
        this._circle = this.query('.ui-radio__circle');

        this._input.addEventListener('change', () => {
            if (this._input.checked) {
                this.checked = true;
                this._circle.classList.add('ui-radio__circle--checked');
                this.emit('field:change', { name: this.name, value: this.value });
            }
        });
    }
}
```

```css
.ui-radio {
    display: inline-flex; align-items: center; gap: var(--spacing-sm);
    cursor: pointer; font-size: var(--font-size-md);
}
.ui-radio--disabled { opacity: 0.5; cursor: not-allowed; }

.ui-radio__circle {
    display: flex; align-items: center; justify-content: center;
    width: 20px; height: 20px;
    border: 2px solid var(--color-border); border-radius: 50%;
    background: var(--color-surface); transition: border-color var(--motion-fast);
    position: relative; flex-shrink: 0;
}
.ui-radio__circle--checked { border-color: var(--color-primary); }

.ui-radio__input { position: absolute; opacity: 0; width: 0; height: 0; }
.ui-radio__dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: transparent; transition: background var(--motion-fast);
}
.ui-radio__circle--checked .ui-radio__dot { background: var(--color-primary); }
.ui-radio__label { user-select: none; }

/* Grupo */
.ui-radio-group { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-radio-group--horizontal { flex-direction: row; flex-wrap: wrap; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
