# FiscalUI Framework

## Documento 108 — Split View

**Nível 6 — Layouts**

**Versão 1.0**

Layout de painéis redimensionáveis. Suporta divisão horizontal e vertical com draggable divider.

---

```js
class SplitViewLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.panels = options.panels || [{ content: '' }, { content: '' }];
        this.direction = options.direction || 'horizontal'; // horizontal, vertical
        this.sizes = options.sizes || [50, 50];
        this._drag = null;
    }

    template() {
        return `
            <div class="ui-layout-split ui-layout-split--${this.direction}">
                ${this.panels.map((p, i) => `
                    <div class="ui-layout-split__panel" style="${this.direction === 'horizontal' ? `width: ${this.sizes[i]}%` : `height: ${this.sizes[i]}%`}">
                        ${p.content || ''}
                    </div>
                    ${i < this.panels.length - 1 ? `<div class="ui-layout-split__divider"></div>` : ''}
                `).join('')}
            </div>
        `;
    }

    onInit() {
        const dividers = this.queryAll('.ui-layout-split__divider');
        dividers.forEach((divider, idx) => {
            divider.addEventListener('mousedown', (e) => {
                this._drag = { index: idx, start: this.direction === 'horizontal' ? e.clientX : e.clientY };
                document.addEventListener('mousemove', this._onMove);
                document.addEventListener('mouseup', this._onUp);
                divider.classList.add('ui-layout-split__divider--active');
            });
        });
    }

    _onMove = (e) => {
        if (!this._drag) return;
        const rect = this.element.getBoundingClientRect();
        const pos = this.direction === 'horizontal' ? e.clientX - rect.left : e.clientY - rect.top;
        const totalSize = this.direction === 'horizontal' ? rect.width : rect.height;
        const pct = Math.min(90, Math.max(10, (pos / totalSize) * 100));
        const diff = pct - this.sizes[this._drag.index];
        this.sizes[this._drag.index] += diff;
        this.sizes[this._drag.index + 1] -= diff;
        this._updatePanels();
    };

    _onUp = () => {
        this._drag = null;
        document.removeEventListener('mousemove', this._onMove);
        document.removeEventListener('mouseup', this._onUp);
        this.queryAll('.ui-layout-split__divider').forEach(d => d.classList.remove('ui-layout-split__divider--active'));
    };

    _updatePanels() {
        this.queryAll('.ui-layout-split__panel').forEach((p, i) => {
            p.style[this.direction === 'horizontal' ? 'width' : 'height'] = `${this.sizes[i]}%`;
        });
    }

    destroy() { this._onUp(); super.destroy(); }
}
```

```css
.ui-layout-split { display: flex; height: 100%; overflow: hidden; }
.ui-layout-split--vertical { flex-direction: column; }

.ui-layout-split__panel { overflow: auto; }
.ui-layout-split__divider {
    flex-shrink: 0; transition: background var(--motion-fast);
    z-index: 1;
}
.ui-layout-split--horizontal .ui-layout-split__divider { width: 4px; cursor: col-resize; background: var(--color-surface-hover); }
.ui-layout-split--vertical .ui-layout-split__divider { height: 4px; cursor: row-resize; background: var(--color-surface-hover); }
.ui-layout-split__divider:hover,
.ui-layout-split__divider--active { background: var(--color-primary); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
