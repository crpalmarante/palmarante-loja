# FiscalUI Framework

## Documento 086 — Code Editor

**Nível 4 — Formulários**

**Versão 1.0**

Editor de código simples com realce de sintaxe via contenteditable + Prism.js ou highlight.js. Suporta linhas numeradas e indentação.

---

```js
class UICodeEditor extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.language = options.language || 'javascript';
        this.height = options.height || 300;
        this.showLineNumbers = options.showLineNumbers !== false;
        this.readonly = options.readonly || false;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-codeeditor">
                    <div class="ui-codeeditor__header">
                        <span class="ui-codeeditor__lang">${this.language}</span>
                        <button class="ui-codeeditor__copy" type="button" aria-label="Copiar">${FiscalUI.icons.render('copy', { size: 14 })} Copiar</button>
                    </div>
                    <div class="ui-codeeditor__body" style="min-height: ${this.height}px">
                        ${this.showLineNumbers ? `<div class="ui-codeeditor__gutter"></div>` : ''}
                        <pre class="ui-codeeditor__pre"><code class="ui-codeeditor__code language-${this.language}" ${this.readonly ? '' : 'contenteditable="true"'} spellcheck="false">${this._escape(this.value)}</code></pre>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._code = this.query('.ui-codeeditor__code');
        this._gutter = this.query('.ui-codeeditor__gutter');
        this._copyBtn = this.query('.ui-codeeditor__copy');

        this._updateGutter();

        if (!this.readonly) {
            this._code.addEventListener('input', () => {
                this.value = this._code.textContent;
                this._updateGutter();
                this.emit('field:change', { name: this.name, value: this.value });
            });

            this._code.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    e.preventDefault();
                    document.execCommand('insertHTML', false, '    ');
                }
            });

            this._code.addEventListener('blur', () => this.emit('field:blur', { name: this.name }));
        }

        this._copyBtn?.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(this.value);
                this._copyBtn.textContent = 'Copiado!';
                setTimeout(() => this._copyBtn.innerHTML = `${FiscalUI.icons.render('copy', { size: 14 })} Copiar`, 2000);
            } catch { /* fallback */ }
        });

        // Aplica highlight via lib externa se disponível
        if (window.hljs) {
            window.hljs.highlightElement(this._code);
        }
    }

    _updateGutter() {
        if (!this._gutter) return;
        const lines = this._code.textContent.split('\n').length;
        this._gutter.innerHTML = Array.from({ length: lines }, (_, i) => `<span>${i + 1}</span>`).join('');
    }

    _escape(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (this._code) { this._code.textContent = val; this._updateGutter(); } }
    reset() { this.setValue(''); }
}
```

```css
.ui-codeeditor { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.ui-codeeditor:focus-within { border-color: var(--color-primary); }

.ui-codeeditor__header {
    display: flex; align-items: center; justify-content: space-between;
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--color-surface-hover); border-bottom: 1px solid var(--color-border);
}
.ui-codeeditor__lang {
    font-size: var(--font-size-xs); color: var(--color-text-muted);
    text-transform: uppercase; font-weight: var(--font-weight-semibold);
}
.ui-codeeditor__copy {
    border: none; background: transparent; cursor: pointer;
    font-size: var(--font-size-xs); color: var(--color-text-secondary);
    display: flex; align-items: center; gap: 4px; padding: 2px 6px; border-radius: var(--radius-sm);
    transition: background var(--motion-fast);
}
.ui-codeeditor__copy:hover { background: var(--color-surface); }

.ui-codeeditor__body { display: flex; background: #1e1e1e; color: #d4d4d4; }
.ui-codeeditor__gutter {
    padding: var(--spacing-sm) var(--spacing-sm); text-align: right;
    color: #858585; user-select: none; font-size: var(--font-size-sm);
    line-height: 1.5; font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    min-width: 40px; border-right: 1px solid #333;
}
.ui-codeeditor__gutter span { display: block; }

.ui-codeeditor__pre { margin: 0; padding: 0; flex: 1; }
.ui-codeeditor__code {
    display: block; padding: var(--spacing-sm); outline: none;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: var(--font-size-sm); line-height: 1.5;
    white-space: pre-wrap; tab-size: 4; min-height: 100%;
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
