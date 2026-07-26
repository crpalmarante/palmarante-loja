# FiscalUI Framework

## Documento 090 — Dashboard

**Nível 5 — Enterprise Components**

**Versão 1.0**

Layout de dashboard com grid responsivo de widgets. Suporta drag-and-drop para reordenar widgets.

---

```js
class UIDashboard extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.widgets = options.widgets || [];
        this.columns = options.columns || 3;
        this.gap = options.gap || 16;
        this.draggable = options.draggable !== false;
        this._dragItem = null;
    }

    template() {
        return `
            <div class="ui-dashboard" style="--dashboard-cols: ${this.columns}; --dashboard-gap: ${this.gap}px">
                ${this.widgets.map((w, i) => `
                    <div class="ui-dashboard__widget ${w.colspan ? `ui-dashboard__widget--col-${w.colspan}` : ''}"
                         data-index="${i}" draggable="${this.draggable}">
                        <div class="ui-dashboard__widget-header">
                            <span class="ui-dashboard__widget-title">${w.title || ''}</span>
                            <div class="ui-dashboard__widget-actions">
                                <button class="ui-dashboard__widget-btn" data-action="refresh" title="Atualizar">${FiscalUI.icons.render('refresh', { size: 14 })}</button>
                                <button class="ui-dashboard__widget-btn" data-action="remove" title="Remover">${FiscalUI.icons.render('x', { size: 14 })}</button>
                            </div>
                        </div>
                        <div class="ui-dashboard__widget-body">${w.content || ''}</div>
                        <div class="ui-dashboard__widget-footer" ${w.footer ? '' : 'hidden'}>${w.footer || ''}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    onInit() {
        if (!this.draggable) return;
        let dragEl = null;
        this.queryAll('.ui-dashboard__widget').forEach(w => {
            w.addEventListener('dragstart', () => { dragEl = w; w.classList.add('ui-dashboard__widget--dragging'); });
            w.addEventListener('dragend', () => { w.classList.remove('ui-dashboard__widget--dragging'); dragEl = null; });
            w.addEventListener('dragover', (e) => { e.preventDefault(); w.classList.add('ui-dashboard__widget--drag-over'); });
            w.addEventListener('dragleave', () => w.classList.remove('ui-dashboard__widget--drag-over'));
            w.addEventListener('drop', (e) => {
                e.preventDefault();
                w.classList.remove('ui-dashboard__widget--drag-over');
                if (dragEl && dragEl !== w) {
                    const parent = this.element.querySelector('.ui-dashboard');
                    const idx = [...parent.children].indexOf(dragEl);
                    const targetIdx = [...parent.children].indexOf(w);
                    if (idx < targetIdx) parent.insertBefore(dragEl, w.nextSibling);
                    else parent.insertBefore(dragEl, w);
                    this.emit('dashboard:reorder', { from: idx, to: targetIdx });
                }
            });
        });
    }

    addWidget(widget) { this.widgets.push(widget); this.render(); }
    removeWidget(index) { this.widgets.splice(index, 1); this.render(); }
}
```

```css
.ui-dashboard {
    display: grid;
    grid-template-columns: repeat(var(--dashboard-cols, 3), 1fr);
    gap: var(--dashboard-gap, 16px);
}

.ui-dashboard__widget {
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); overflow: hidden;
    transition: box-shadow var(--motion-fast);
}
.ui-dashboard__widget--col-2 { grid-column: span 2; }
.ui-dashboard__widget--col-3 { grid-column: span 3; }
.ui-dashboard__widget--dragging { opacity: 0.4; }
.ui-dashboard__widget--drag-over { border-color: var(--color-primary); box-shadow: 0 0 0 2px var(--color-primary-surface); }

.ui-dashboard__widget-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: var(--spacing-sm) var(--spacing-md);
    border-bottom: 1px solid var(--color-border); cursor: grab;
}
.ui-dashboard__widget-title { font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); }
.ui-dashboard__widget-actions { display: flex; gap: 2px; }
.ui-dashboard__widget-btn { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); padding: 2px; border-radius: var(--radius-sm); display: flex; }
.ui-dashboard__widget-btn:hover { background: var(--color-surface-hover); color: var(--color-text); }

.ui-dashboard__widget-body { padding: var(--spacing-md); min-height: 100px; }
.ui-dashboard__widget-footer { padding: var(--spacing-sm) var(--spacing-md); border-top: 1px solid var(--color-border); font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
