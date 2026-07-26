# FiscalUI Framework

## Documento 078 — Rating

**Nível 4 — Formulários**

**Versão 1.0**

Componente de classificação por estrelas. Suporta avaliação parcial (meia estrela), leitura e hover.

---

```js
class UIRating extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value ?? 0;
        this.max = options.max ?? 5;
        this.half = options.half || false;
        this.readonly = options.readonly || false;
        this.size = options.size || 'md';
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-rating ui-rating--${this.size} ${this.readonly ? 'ui-rating--readonly' : ''}">
                    ${Array.from({ length: this.max }, (_, i) => {
                        const starValue = i + 1;
                        const filled = this.value >= starValue;
                        const halfFilled = this.half && this.value >= starValue - 0.5 && this.value < starValue;
                        return `
                            <span class="ui-rating__star ${filled ? 'ui-rating__star--filled' : ''} ${halfFilled ? 'ui-rating__star--half' : ''}"
                                  data-value="${starValue}">
                                ${this._starIcon(filled, halfFilled)}
                            </span>`;
                    }).join('')}
                    <span class="ui-rating__value">${this.value}</span>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _starIcon(filled, half) {
        if (filled) return FiscalUI.icons.render('star', { size: this._iconSize() });
        if (half) {
            return `
                <span class="ui-rating__star-bg">${FiscalUI.icons.render('star', { size: this._iconSize() })}</span>
                <span class="ui-rating__star-fg">${FiscalUI.icons.render('star', { size: this._iconSize() })}</span>`;
        }
        return `<span class="ui-rating__star-empty">${FiscalUI.icons.render('star', { size: this._iconSize() })}</span>`;
    }

    _iconSize() {
        const sizes = { sm: 16, md: 22, lg: 30 };
        return sizes[this.size] || 22;
    }

    onInit() {
        if (this.readonly) return;
        this._stars = this.queryAll('.ui-rating__star');
        this._valueEl = this.query('.ui-rating__value');

        this._stars.forEach(star => {
            star.addEventListener('click', () => {
                const val = parseFloat(star.dataset.value);
                this.setValue(val);
                this.emit('field:change', { name: this.name, value: this.value });
            });
            star.addEventListener('mouseenter', () => this._hover(parseFloat(star.dataset.value)));
        });

        this.element.addEventListener('mouseleave', () => this._renderStars());
    }

    _hover(val) {
        this._stars.forEach(star => {
            const sv = parseFloat(star.dataset.value);
            star.classList.toggle('ui-rating__star--hover', sv <= val);
        });
    }

    _renderStars() {
        this._stars.forEach((star, i) => {
            const sv = i + 1;
            const filled = this.value >= sv;
            const halfFilled = this.half && this.value >= sv - 0.5 && this.value < sv;
            star.classList.toggle('ui-rating__star--filled', filled);
            star.classList.toggle('ui-rating__star--half', halfFilled);
            star.classList.remove('ui-rating__star--hover');
        });
        if (this._valueEl) this._valueEl.textContent = this.value;
    }

    value() { return this.value; }
    setValue(val) { this.value = Math.min(this.max, Math.max(0, val)); this._renderStars(); }
    reset() { this.setValue(0); }
}
```

```css
.ui-rating { display: inline-flex; align-items: center; gap: 2px; }
.ui-rating--readonly { pointer-events: none; }

.ui-rating__star { cursor: pointer; display: flex; position: relative; color: var(--color-border); transition: color var(--motion-fast); }
.ui-rating__star--filled, .ui-rating__star--hover { color: var(--color-warning); }
.ui-rating__star--half { position: relative; }
.ui-rating__star-bg { color: var(--color-border); }
.ui-rating__star-fg { position: absolute; left: 0; top: 0; color: var(--color-warning); clip-path: inset(0 50% 0 0); }
.ui-rating__star-empty { color: var(--color-border); }

.ui-rating__value { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin-left: var(--spacing-sm); min-width: 24px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
