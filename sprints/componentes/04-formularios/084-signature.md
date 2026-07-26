# FiscalUI Framework

## Documento 084 — Signature

**Nível 4 — Formulários**

**Versão 1.0**

Campo de assinatura digital (desenho à mão livre) via canvas. Suporta cor, espessura, limpar e undo.

---

```js
class UISignature extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || 'Assinatura';
        this.value = options.value || '';           // data URL
        this.penColor = options.penColor || '#000';
        this.penWidth = options.penWidth || 2;
        this.width = options.width || 400;
        this.height = options.height || 150;
        this.rules = options.rules || [];
        this._drawing = false;
        this._points = [];
        this._undoStack = [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-signature">
                    <canvas class="ui-signature__canvas" width="${this.width}" height="${this.height}"></canvas>
                    <div class="ui-signature__actions">
                        <button class="ui-btn ui-btn--ghost ui-btn--sm" type="button" data-action="undo">${FiscalUI.icons.render('undo', { size: 14 })} Desfazer</button>
                        <button class="ui-btn ui-btn--ghost ui-btn--sm" type="button" data-action="clear">Limpar</button>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    onInit() {
        this._canvas = this.query('.ui-signature__canvas');
        this._ctx = this._canvas.getContext('2d');
        this._ctx.lineCap = 'round';
        this._ctx.lineJoin = 'round';

        if (this.value) {
            const img = new Image();
            img.onload = () => this._ctx.drawImage(img, 0, 0);
            img.src = this.value;
        }

        this._canvas.addEventListener('mousedown', (e) => this._start(e));
        this._canvas.addEventListener('mousemove', (e) => this._move(e));
        this._canvas.addEventListener('mouseup', () => this._end());
        this._canvas.addEventListener('mouseleave', () => this._end());

        this._canvas.addEventListener('touchstart', (e) => { e.preventDefault(); this._start(e.touches[0]); });
        this._canvas.addEventListener('touchmove', (e) => { e.preventDefault(); this._move(e.touches[0]); });
        this._canvas.addEventListener('touchend', (e) => { e.preventDefault(); this._end(); });

        this.query('[data-action="undo"]').addEventListener('click', () => this.undo());
        this.query('[data-action="clear"]').addEventListener('click', () => this.clear());
    }

    _start(e) {
        this._drawing = true;
        const rect = this._canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.width / rect.width);
        const y = (e.clientY - rect.top) * (this.height / rect.height);
        this._points = [{ x, y }];
        this._ctx.beginPath();
        this._ctx.moveTo(x, y);
    }

    _move(e) {
        if (!this._drawing) return;
        const rect = this._canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) * (this.width / rect.width);
        const y = (e.clientY - rect.top) * (this.height / rect.height);
        this._points.push({ x, y });
        this._ctx.strokeStyle = this.penColor;
        this._ctx.lineWidth = this.penWidth;
        this._ctx.lineTo(x, y);
        this._ctx.stroke();
    }

    _end() {
        if (!this._drawing) return;
        this._drawing = false;
        if (this._points.length > 1) {
            this._undoStack.push([...this._points]);
            this._updateValue();
        }
        this._points = [];
    }

    undo() {
        if (!this._undoStack.length) return;
        this._undoStack.pop();
        this._redraw();
    }

    clear() {
        this._undoStack = [];
        this._ctx.clearRect(0, 0, this.width, this.height);
        this._updateValue();
    }

    _redraw() {
        this._ctx.clearRect(0, 0, this.width, this.height);
        this._undoStack.forEach(stroke => {
            if (stroke.length < 2) return;
            this._ctx.beginPath();
            this._ctx.strokeStyle = this.penColor;
            this._ctx.lineWidth = this.penWidth;
            this._ctx.moveTo(stroke[0].x, stroke[0].y);
            for (let i = 1; i < stroke.length; i++) {
                this._ctx.lineTo(stroke[i].x, stroke[i].y);
            }
            this._ctx.stroke();
        });
        this._updateValue();
    }

    _updateValue() {
        this.value = this._undoStack.length ? this._canvas.toDataURL() : '';
        this.emit('field:change', { name: this.name, value: this.value });
    }

    value() { return this.value; }
    setValue(val) { this.value = val; if (val) { const img = new Image(); img.onload = () => { this._ctx.drawImage(img, 0, 0); }; img.src = val; } }
    reset() { this.clear(); }
    isEmpty() { return !this._undoStack.length; }
}
```

```css
.ui-signature__canvas {
    border: 1px solid var(--color-border); border-radius: var(--radius-md);
    cursor: crosshair; width: 100%; height: auto; touch-action: none;
    background: #fff;
}
.ui-signature__actions { display: flex; gap: var(--spacing-sm); margin-top: var(--spacing-xs); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
