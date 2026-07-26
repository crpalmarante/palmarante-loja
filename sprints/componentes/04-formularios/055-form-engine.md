# FiscalUI Framework

## Documento 055 — Form Engine

**Nível 4 — Formulários**

**Versão 1.0**

Motor de formulários. Gerencia estado, validação, submissão, campos dinâmicos e integração com o StateManager.

---

```js
class FormEngine {
    constructor(options = {}) {
        this.element = options.element || null;
        this.fields = new Map();
        this.validators = options.validators || {};
        this.onSubmit = options.onSubmit || null;
        this._touched = new Set();
        this._dirty = new Set();
        this._errors = new Map();
    }

    register(field) {
        this.fields.set(field.name, field);
        field.on('field:change', () => {
            this._dirty.add(field.name);
            this.validate(field.name);
            this.emit('form:change', { name: field.name, value: field.value() });
        });
        field.on('field:blur', () => {
            this._touched.add(field.name);
            this.validate(field.name);
        });
    }

    unregister(name) {
        this.fields.delete(name);
        this._touched.delete(name);
        this._dirty.delete(name);
        this._errors.delete(name);
    }

    value() {
        const data = {};
        this.fields.forEach((field, name) => { data[name] = field.value(); });
        return data;
    }

    setValues(data) {
        Object.entries(data).forEach(([name, value]) => {
            this.fields.get(name)?.setValue(value);
        });
    }

    reset() {
        this.fields.forEach(f => f.reset());
        this._touched.clear();
        this._dirty.clear();
        this._errors.clear();
        this._renderErrors();
    }

    validate(fieldName) {
        if (fieldName) {
            const field = this.fields.get(fieldName);
            if (!field) return true;
            const error = this._validateField(field);
            if (error) this._errors.set(fieldName, error);
            else this._errors.delete(fieldName);
            this._renderFieldError(fieldName);
            return !error;
        }

        let valid = true;
        this.fields.forEach((field, name) => {
            const error = this._validateField(field);
            if (error) { this._errors.set(name, error); valid = false; }
            else this._errors.delete(name);
        });
        this._renderErrors();
        return valid;
    }

    _validateField(field) {
        const rules = field.rules || [];
        for (const rule of rules) {
            const error = this._applyRule(rule, field);
            if (error) return error;
        }
        return null;
    }

    _applyRule(rule, field) {
        const value = field.value();
        if (rule.required && !value) return rule.message || 'Campo obrigatório';
        if (!value) return null;
        if (rule.minLength && value.length < rule.minLength) return rule.message || `Mínimo ${rule.minLength} caracteres`;
        if (rule.maxLength && value.length > rule.maxLength) return rule.message || `Máximo ${rule.maxLength} caracteres`;
        if (rule.min && value < rule.min) return rule.message || `Valor mínimo ${rule.min}`;
        if (rule.max && value > rule.max) return rule.message || `Valor máximo ${rule.max}`;
        if (rule.pattern && !rule.pattern.test(value)) return rule.message || 'Formato inválido';
        if (rule.custom) return rule.custom(value, field) || null;
        if (typeof this.validators[rule.type] === 'function') return this.validators[rule.type](value, field) || null;
        return null;
    }

    submit() {
        this._touched = new Set(this.fields.keys());
        if (!this.validate()) return false;
        this.onSubmit?.(this.value());
        this.emit('form:submit', { data: this.value() });
        return true;
    }

    isValid() { return this._errors.size === 0; }
    isDirty() { return this._dirty.size > 0; }
    isTouched(name) { return name ? this._touched.has(name) : this._touched.size > 0; }
    errors(name) { return name ? this._errors.get(name) : Object.fromEntries(this._errors); }

    _renderErrors() {
        this.fields.forEach((_, name) => this._renderFieldError(name));
    }

    _renderFieldError(name) {
        const field = this.fields.get(name);
        if (!field?.element) return;
        const errorEl = field.element.querySelector('.ui-field__error');
        const error = this._errors.get(name);
        if (error) {
            field.element.classList.add('ui-field--error');
            if (errorEl) errorEl.textContent = error;
        } else {
            field.element.classList.remove('ui-field--error');
            if (errorEl) errorEl.textContent = '';
        }
    }

    emit(event, data) {
        FiscalUI.events.emit(event, data);
    }

    on(event, handler) {
        FiscalUI.events.on(event, handler);
    }
}
```

```css
.ui-form { display: flex; flex-direction: column; gap: var(--spacing-lg); }
.ui-form__actions { display: flex; justify-content: flex-end; gap: var(--spacing-sm); padding-top: var(--spacing-md); border-top: 1px solid var(--color-border); }

.ui-field { display: flex; flex-direction: column; gap: var(--spacing-xs); }
.ui-field__label { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); color: var(--color-text); }
.ui-field__required { color: var(--color-danger); margin-left: 2px; }
.ui-field__hint { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-field__error { font-size: var(--font-size-xs); color: var(--color-danger); min-height: 16px; }
.ui-field--error .ui-field__input { border-color: var(--color-danger); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
