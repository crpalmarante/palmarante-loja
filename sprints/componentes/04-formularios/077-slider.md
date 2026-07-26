# FiscalUI Framework

## Documento 077 — Slider

**Nível 4 — Formulários**

**Versão 1.0**

Controle deslizante para seleção de valor numérico em um intervalo. Suporta exibição de valor e steps.

---

```js
class UISlider extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value ?? 0;
        this.min = options.min ?? 0;
        this.max = options.max ?? 100;
        this.step = options.step ?? 1;
        this.showValue = options.showValue !== false;
        this.variant = options.variant || 'primary';
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-slider">
                    <input class="ui-slider__input" type="range" name="${this.name}"
                           min="${this.min}" max="${this.max}" step="${this.step}"
                           value="${this.value}">
                    <div class="ui-slider__track">
                        <div class="ui-slider__fill ui-slider__fill--${this.variant}" style="width: ${this._percent()}%"></div>
                        <div class="ui-slider__thumb" style="left: ${this._percent()}%"></div>
                    </div>
                    ${this.showValue ? `<span class="ui-slider__value">${this.value}</span>` : ''}
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-slider__input');
        this._fill = this.query('.ui-slider__fill');
        this._thumb = this.query('.ui-slider__thumb');
        this._valueEl = this.query('.ui-slider__value');

        this._input.addEventListener('input', () => {
            this.value = parseFloat(this._input.value);
            const pct = this._percent();
            this._fill.style.width = `${pct}%`;
            this._thumb.style.left = `${pct}%`;
            if (this._valueEl) this._valueEl.textContent = this.value;
            this.emit('field:change', { name: this.name, value: this.value });
        });
    }

    _percent() {
        return ((this.value - this.min) / (this.max - this.min)) * 100;
    }

    value() { return this.value; }
    setValue(val) {
        this.value = Math.min(this.max, Math.max(this.min, val));
        if (this._input) {
            this._input.value = this.value;
            const pct = this._percent();
            this._fill.style.width = `${pct}%`;
            this._thumb.style.left = `${pct}%`;
            if (this._valueEl) this._valueEl.textContent = this.value;
        }
    }
    reset() { this.setValue(0); }
}
```

```css
.ui-slider { display: flex; align-items: center; gap: var(--spacing-md); position: relative; padding: var(--spacing-sm) 0; }

.ui-slider__input {
    position: absolute; opacity: 0; width: 100%; height: 100%;
    cursor: pointer; z-index: 2; margin: 0; top: 0; left: 0;
}

.ui-slider__track {
    flex: 1; height: 6px; background: var(--color-surface-hover);
    border-radius: 3px; position: relative;
}

.ui-slider__fill { height: 100%; border-radius: 3px; transition: width var(--motion-fast); }
.ui-slider__fill--primary { background: var(--color-primary); }
.ui-slider__fill--success { background: var(--color-success); }
.ui-slider__fill--warning { background: var(--color-warning); }
.ui-slider__fill--danger  { background: var(--color-danger); }

.ui-slider__thumb {
    position: absolute; top: 50%; transform: translate(-50%, -50%);
    width: 18px; height: 18px; background: #fff;
    border: 2px solid var(--color-primary); border-radius: 50%;
    box-shadow: var(--shadow-sm); pointer-events: none;
    transition: left var(--motion-fast);
}

.ui-slider__value {
    font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold);
    min-width: 36px; text-align: center; color: var(--color-text);
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
