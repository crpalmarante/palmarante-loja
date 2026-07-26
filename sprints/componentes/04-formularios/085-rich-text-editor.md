# FiscalUI Framework

## Documento 085 — Rich Text Editor

**Nível 4 — Formulários**

**Versão 1.0**

Editor de texto rico baseado em contenteditable. Suporta formatação básica (negrito, itálico, lista, link) e toolbar.

---

```js
class UIRichTextEditor extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.placeholder = options.placeholder || 'Digite aqui…';
        this.height = options.height || 300;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-rte">
                    <div class="ui-rte__toolbar">
                        <button class="ui-rte__btn" data-cmd="bold" title="Negrito"><strong>B</strong></button>
                        <button class="ui-rte__btn" data-cmd="italic" title="Itálico"><em>I</em></button>
                        <button class="ui-rte__btn" data-cmd="underline" title="Sublinhado"><u>U</u></button>
                        <span class="ui-toolbar__divider"></span>
                        <button class="ui-rte__btn" data-cmd="insertUnorderedList" title="Lista">•</button>
                        <button class="ui-rte__btn" data-cmd="insertOrderedList" title="Lista numerada">1.</button>
                        <span class="ui-toolbar__divider"></span>
                        <button class="ui-rte__btn" data-cmd="createLink" title="Link">🔗</button>
                        <button class="ui-rte__btn" data-cmd="removeFormat" title="Limpar">✕</button>
                    </div>
                    <div class="ui-rte__editor" contenteditable="true" style="min-height: ${this.height}px"
                         data-placeholder="${this.placeholder}">${this.value}</div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._editor = this.query('.ui-rte__editor');

        this.queryAll('.ui-rte__btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const cmd = btn.dataset.cmd;
                if (cmd === 'createLink') {
                    const url = prompt('URL:', 'https://');
                    if (url) document.execCommand(cmd, false, url);
                } else {
                    document.execCommand(cmd, false, null);
                }
                this._editor.focus();
                this._updateValue();
            });
        });

        this._editor.addEventListener('input', () => this._updateValue());
        this._editor.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));
    }

    _updateValue() {
        this.value = this._editor.innerHTML;
        this.emit('field:change', { name: this.name, value: this.value });
    }

    insertHTML(html) {
        document.execCommand('insertHTML', false, html);
        this._updateValue();
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._editor) this._editor.innerHTML = val; }
    reset() { this.setValue(''); }
}
```

```css
.ui-rte { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.ui-rte:focus-within { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-surface); }

.ui-rte__toolbar {
    display: flex; align-items: center; gap: 2px;
    padding: var(--spacing-xs); background: var(--color-surface-hover);
    border-bottom: 1px solid var(--color-border); flex-wrap: wrap;
}

.ui-rte__btn {
    border: none; background: transparent; cursor: pointer;
    padding: 4px 8px; border-radius: var(--radius-sm);
    color: var(--color-text-secondary); font-size: var(--font-size-sm);
    transition: background var(--motion-fast);
}
.ui-rte__btn:hover { background: var(--color-surface); color: var(--color-text); }

.ui-rte__editor {
    padding: var(--spacing-md); outline: none;
    font-size: var(--font-size-md); line-height: 1.6;
    overflow-y: auto;
}
.ui-rte__editor:empty::before {
    content: attr(data-placeholder); color: var(--color-text-muted);
    pointer-events: none;
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
