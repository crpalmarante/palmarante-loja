# FiscalUI Framework

## Documento 068 — Email

**Nível 4 — Formulários**

**Versão 1.0**

Campo de e-mail com validação de formato e sugestão de domínios comuns.

---

```js
class UIEmail extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || 'E-mail';
        this.value = options.value || '';
        this.placeholder = options.placeholder || 'nome@exemplo.com.br';
        this.suggestDomains = options.suggestDomains !== false;
        this.rules = options.rules || [{ type: 'email' }];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-field__input-wrapper">
                    <span class="ui-field__prefix-icon">${FiscalUI.icons.render('mail', { size: 16 })}</span>
                    <input class="ui-field__input ui-field__input--email" type="email" inputmode="email"
                           name="${this.name}" placeholder="${this.placeholder}"
                           value="${this.value || ''}" autocomplete="email">
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-field__input');
        this._suggestions = null;

        this._input.addEventListener('input', () => {
            this.value = this._input.value;
            this.emit('field:change', { name: this.name, value: this.value });
            if (this.suggestDomains) this._suggest();
        });

        this._input.addEventListener('blur', () => {
            if (this.value && !this._validate(this.value)) {
                this.element.classList.add('ui-field--error');
                this.query('.ui-field__error').textContent = 'E-mail inválido';
            }
            this.emit('field:blur', { name: this.name });
            setTimeout(() => this._removeSuggestions(), 200);
        });

        this._input.addEventListener('focus', () => { if (this.value.includes('@')) this._suggest(); });
    }

    _validate(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    _suggest() {
        this._removeSuggestions();
        const atIndex = this.value.indexOf('@');
        if (atIndex < 1) return;
        const domain = this.value.slice(atIndex + 1);
        const domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'uol.com.br', 'bol.com.br', 'ig.com.br', 'terra.com.br'];
        const matched = domain ? domains.filter(d => d.startsWith(domain) && d !== domain) : [];

        if (!matched.length) return;
        this._suggestions = document.createElement('div');
        this._suggestions.className = 'ui-email__suggestions';
        this._suggestions.innerHTML = matched.map(d =>
            `<div class="ui-email__suggestion" data-domain="${d}">${this.value.slice(0, atIndex + 1)}${d}</div>`
        ).join('');
        this.element.appendChild(this._suggestions);

        this._suggestions.querySelectorAll('.ui-email__suggestion').forEach(el => {
            el.addEventListener('click', () => {
                this._input.value = el.dataset.domain;
                this.value = el.dataset.domain;
                this.emit('field:change', { name: this.name, value: this.value });
                this._removeSuggestions();
            });
        });
    }

    _removeSuggestions() { this._suggestions?.remove(); this._suggestions = null; }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._input) this._input.value = val; }
    reset() { this.setValue(''); this.element.classList.remove('ui-field--error'); }
}
```

```css
.ui-field__input--email { letter-spacing: 0.3px; }

.ui-email__suggestions {
    position: absolute; top: 100%; left: 0; right: 0; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-md); margin-top: 2px; overflow: hidden;
}
.ui-email__suggestion {
    padding: var(--spacing-xs) var(--spacing-md); cursor: pointer;
    font-size: var(--font-size-sm); transition: background var(--motion-fast);
}
.ui-email__suggestion:hover { background: var(--color-surface-hover); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
