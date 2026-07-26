# FiscalUI Framework

## Documento 100 — Report Viewer

**Nível 5 — Enterprise Components**

**Versão 1.0**

Visualizador de relatórios com toolbar de ações (imprimir, exportar PDF/Excel, zoom, busca).

---

```js
class UIReportViewer extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || 'Relatório';
        this.content = options.content || '';
        this.zoom = options.zoom || 1;
        this.showToolbar = options.showToolbar !== false;
    }

    template() {
        return `
            <div class="ui-report">
                ${this.showToolbar ? `
                <div class="ui-report__toolbar">
                    <span class="ui-report__title">${this.title}</span>
                    <div class="ui-report__actions">
                        <button class="ui-report__btn" data-action="print" title="Imprimir">${FiscalUI.icons.render('printer', { size: 16 })}</button>
                        <button class="ui-report__btn" data-action="pdf" title="Exportar PDF">${FiscalUI.icons.render('file-text', { size: 16 })}</button>
                        <button class="ui-report__btn" data-action="excel" title="Exportar Excel">${FiscalUI.icons.render('grid', { size: 16 })}</button>
                        <span class="ui-toolbar__divider"></span>
                        <button class="ui-report__btn" data-action="zoom-out">${FiscalUI.icons.render('zoom-out', { size: 16 })}</button>
                        <span class="ui-report__zoom">${Math.round(this.zoom * 100)}%</span>
                        <button class="ui-report__btn" data-action="zoom-in">${FiscalUI.icons.render('zoom-in', { size: 16 })}</button>
                    </div>
                </div>` : ''}
                <div class="ui-report__body" style="transform: scale(${this.zoom}); transform-origin: top center;">
                    ${this.content || '<div class="ui-report__empty">Nenhum conteúdo</div>'}
                </div>
            </div>
        `;
    }

    onInit() {
        this._body = this.query('.ui-report__body');
        this._zoomEl = this.query('.ui-report__zoom');

        this.queryAll('.ui-report__btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                if (action === 'print') window.print();
                else if (action === 'zoom-in') this._zoom(0.1);
                else if (action === 'zoom-out') this._zoom(-0.1);
                else this.emit(`report:${action}`, { title: this.title });
            });
        });
    }

    _zoom(delta) {
        this.zoom = Math.max(0.5, Math.min(2, this.zoom + delta));
        this._body.style.transform = `scale(${this.zoom})`;
        if (this._zoomEl) this._zoomEl.textContent = `${Math.round(this.zoom * 100)}%`;
    }

    setContent(html) { this.content = html; this._body.innerHTML = html; }
}
```

```css
.ui-report { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.ui-report__toolbar { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-sm) var(--spacing-md); background: var(--color-surface); border-bottom: 1px solid var(--color-border); }
.ui-report__title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-md); }
.ui-report__actions { display: flex; align-items: center; gap: var(--spacing-xs); }
.ui-report__btn { border: none; background: transparent; cursor: pointer; padding: 4px; border-radius: var(--radius-sm); color: var(--color-text-secondary); display: flex; }
.ui-report__btn:hover { background: var(--color-surface-hover); }
.ui-report__zoom { font-size: var(--font-size-xs); color: var(--color-text-muted); min-width: 36px; text-align: center; }

.ui-report__body { overflow: auto; padding: var(--spacing-lg); background: #fff; min-height: 400px; }
.ui-report__empty { text-align: center; padding: var(--spacing-xl); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
