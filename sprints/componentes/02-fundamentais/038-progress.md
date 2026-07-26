# FiscalUI Framework

## Documento 038 — Progress

**Nível 2 — Basic Components**

**Versão 1.0**

Barra de progresso linear. Usada para uploads, processamento, carregamento de etapas.

---

```js
class UIProgress extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.value = options.value || 0;           // 0-100
        this.variant = options.variant || 'primary';
        this.size = options.size || 'md';
        this.label = options.label || '';
        this.showValue = options.showValue || false;
        this.indeterminate = options.indeterminate || false;
    }

    template() {
        return `
            <div class="ui-progress ui-progress--${this.size}">
                ${this.label ? `<div class="ui-progress__label">${this.label}</div>` : ''}
                <div class="ui-progress__track">
                    <div class="ui-progress__bar ui-progress__bar--${this.variant}
                                ${this.indeterminate ? 'ui-progress__bar--indeterminate' : ''}"
                         style="${this.indeterminate ? '' : `width: ${this.value}%`}">
                    </div>
                </div>
                ${this.showValue && !this.indeterminate ? `<div class="ui-progress__value">${this.value}%</div>` : ''}
            </div>
        `;
    }

    setValue(value) { this.value = Math.min(100, Math.max(0, value)); this.render(); }
}
```

```css
.ui-progress { width: 100%; }
.ui-progress__label { font-size: var(--font-size-sm); margin-bottom: var(--spacing-xs); }
.ui-progress__track { background: var(--color-surface-hover); border-radius: 999px; overflow: hidden; }
.ui-progress__bar { height: 100%; border-radius: 999px; transition: width var(--motion-normal) var(--ease-out); }

.ui-progress__bar--primary { background: var(--color-primary); }
.ui-progress__bar--success { background: var(--color-success); }
.ui-progress__bar--warning { background: var(--color-warning); }
.ui-progress__bar--danger  { background: var(--color-danger); }

.ui-progress__bar--indeterminate {
    width: 30% !important;
    animation: ui-progress-indeterminate 1.5s ease-in-out infinite;
}

.ui-progress__value { font-size: var(--font-size-sm); color: var(--color-text-secondary); text-align: right; margin-top: var(--spacing-xs); }

.ui-progress--sm .ui-progress__track { height: 4px; }
.ui-progress--md .ui-progress__track { height: 8px; }
.ui-progress--lg .ui-progress__track { height: 12px; }

@keyframes ui-progress-indeterminate {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(400%); }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
