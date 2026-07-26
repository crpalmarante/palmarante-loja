# FiscalUI Framework

## Documento 083 — ColorPicker

**Nível 4 — Formulários**

**Versão 1.0**

Seletor de cores com preview, input hex, paleta rápida e seletor visual.

---

```js
class UIColorPicker extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '#1976d2';
        this.presets = options.presets || [
            '#1976d2', '#388e3c', '#f57c00', '#d32f2f', '#7b1fa2',
            '#00796b', '#5d4037', '#455a64', '#000000', '#ffffff',
            '#e0e0e0', '#f5f5f5'
        ];
        this.rules = options.rules || [];
        this._open = false;
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-colorpicker">
                    <div class="ui-field__input-wrapper">
                        <span class="ui-colorpicker__swatch" style="background: ${this.value}"></span>
                        <input class="ui-field__input ui-colorpicker__input" type="text"
                               value="${this.value}" placeholder="#000000" maxlength="7" autocomplete="off">
                    </div>
                    <div class="ui-colorpicker__dropdown" hidden>
                        <div class="ui-colorpicker__preview">
                            <span class="ui-colorpicker__preview-swatch" style="background: ${this.value}"></span>
                            <span class="ui-colorpicker__preview-value">${this.value}</span>
                        </div>
                        <div class="ui-colorpicker__canvas">
                            <input class="ui-colorpicker__canvas-input" type="color" value="${this.value}">
                        </div>
                        <div class="ui-colorpicker__presets">
                            ${this.presets.map(c => `
                                <span class="ui-colorpicker__preset ${c === this.value ? 'ui-colorpicker__preset--active' : ''}"
                                      style="background: ${c}" data-color="${c}"></span>
                            `).join('')}
                        </div>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-colorpicker__input');
        this._swatch = this.query('.ui-colorpicker__swatch');
        this._dropdown = this.query('.ui-colorpicker__dropdown');
        this._previewSwatch = this.query('.ui-colorpicker__preview-swatch');
        this._previewValue = this.query('.ui-colorpicker__preview-value');
        this._canvasInput = this.query('.ui-colorpicker__canvas-input');

        this._input.addEventListener('focus', () => this.open());
        this._input.addEventListener('input', () => {
            if (/^#[0-9a-f]{6}$/i.test(this._input.value)) {
                this._setColor(this._input.value);
            }
        });

        this._canvasInput.addEventListener('input', () => this._setColor(this._canvasInput.value));

        this._dropdown.querySelector('.ui-colorpicker__presets').addEventListener('click', (e) => {
            const preset = e.target.closest('.ui-colorpicker__preset');
            if (preset) this._setColor(preset.dataset.color);
        });

        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.close(); });
    }

    _setColor(color) {
        this.value = color;
        this._input.value = color;
        this._swatch.style.background = color;
        this._previewSwatch.style.background = color;
        this._previewValue.textContent = color;
        this._canvasInput.value = color;
        this.queryAll('.ui-colorpicker__preset').forEach(p => p.classList.toggle('ui-colorpicker__preset--active', p.dataset.color === color));
        this.emit('field:change', { name: this.name, value: this.value });
    }

    open() { this._open = true; this._dropdown.hidden = false; }
    close() { this._open = false; this._dropdown.hidden = true; }
    toggle() { this._open ? this.close() : this.open(); }

    value() { return this.value; }
    setValue(val) { this._setColor(val); }
    reset() { this.setValue('#1976d2'); }
}
```

```css
.ui-colorpicker { position: relative; }
.ui-colorpicker__swatch {
    width: 28px; height: 28px; border-radius: var(--radius-sm);
    border: 1px solid var(--color-border); margin: 0 var(--spacing-xs);
    flex-shrink: 0; cursor: pointer;
}

.ui-colorpicker__dropdown {
    position: absolute; top: 100%; left: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
    padding: var(--spacing-md); width: 220px;
}

.ui-colorpicker__preview {
    display: flex; align-items: center; gap: var(--spacing-sm);
    margin-bottom: var(--spacing-sm); padding-bottom: var(--spacing-sm);
    border-bottom: 1px solid var(--color-border);
}
.ui-colorpicker__preview-swatch {
    width: 32px; height: 32px; border-radius: var(--radius-sm);
    border: 1px solid var(--color-border);
}
.ui-colorpicker__preview-value { font-family: monospace; font-size: var(--font-size-sm); color: var(--color-text); }

.ui-colorpicker__canvas { margin-bottom: var(--spacing-sm); }
.ui-colorpicker__canvas-input { width: 100%; height: 36px; border: none; padding: 0; cursor: pointer; border-radius: var(--radius-sm); }

.ui-colorpicker__presets { display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px; }
.ui-colorpicker__preset {
    width: 100%; aspect-ratio: 1; border-radius: var(--radius-sm);
    border: 2px solid transparent; cursor: pointer;
    transition: border-color var(--motion-fast);
}
.ui-colorpicker__preset:hover { border-color: var(--color-border); }
.ui-colorpicker__preset--active { border-color: var(--color-primary); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
