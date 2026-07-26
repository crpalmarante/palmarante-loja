# FiscalUI Framework

## Documento 098 — PDF Viewer

**Nível 5 — Enterprise Components**

**Versão 1.0**

Visualizador de PDF embutido via PDF.js. Suporta navegação de páginas, zoom e download.

---

```js
class UIPDFViewer extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.url = options.url || '';
        this.page = options.page || 1;
        this.zoom = options.zoom || 1;
        this._totalPages = 0;
        this._pdfDoc = null;
    }

    template() {
        return `
            <div class="ui-pdfviewer">
                <div class="ui-pdfviewer__toolbar">
                    <button class="ui-pdfviewer__btn" data-action="prev" ${this.page <= 1 ? 'disabled' : ''}>${FiscalUI.icons.render('chevron-left', { size: 16 })}</button>
                    <span class="ui-pdfviewer__page-info">Página <span class="ui-pdfviewer__current">${this.page}</span> de <span class="ui-pdfviewer__total">${this._totalPages || '?'}</span></span>
                    <button class="ui-pdfviewer__btn" data-action="next" ${this.page >= this._totalPages ? 'disabled' : ''}>${FiscalUI.icons.render('chevron-right', { size: 16 })}</button>
                    <span class="ui-toolbar__divider"></span>
                    <button class="ui-pdfviewer__btn" data-action="zoom-in">${FiscalUI.icons.render('zoom-in', { size: 16 })}</button>
                    <span class="ui-pdfviewer__zoom-level">${Math.round(this.zoom * 100)}%</span>
                    <button class="ui-pdfviewer__btn" data-action="zoom-out">${FiscalUI.icons.render('zoom-out', { size: 16 })}</button>
                    <span class="ui-toolbar__divider"></span>
                    <button class="ui-pdfviewer__btn" data-action="download" title="Download">${FiscalUI.icons.render('download', { size: 16 })}</button>
                </div>
                <div class="ui-pdfviewer__canvas-wrapper">
                    <canvas class="ui-pdfviewer__canvas"></canvas>
                </div>
            </div>
        `;
    }

    onInit() {
        this._canvas = this.query('.ui-pdfviewer__canvas');
        this._ctx = this._canvas.getContext('2d');
        this._currentEl = this.query('.ui-pdfviewer__current');
        this._totalEl = this.query('.ui-pdfviewer__total');
        this._zoomEl = this.query('.ui-pdfviewer__zoom-level');

        if (this.url) this.load(this.url);

        this.queryAll('.ui-pdfviewer__btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                if (action === 'prev' && this.page > 1) this.goTo(this.page - 1);
                else if (action === 'next' && this.page < this._totalPages) this.goTo(this.page + 1);
                else if (action === 'zoom-in') this.zoom = Math.min(3, this.zoom + 0.25);
                else if (action === 'zoom-out') this.zoom = Math.max(0.25, this.zoom - 0.25);
                else if (action === 'download') this._download();
                if (action.startsWith('zoom') && this._pdfDoc) this._renderPage(this.page);
                if (this._zoomEl) this._zoomEl.textContent = `${Math.round(this.zoom * 100)}%`;
            });
        });
    }

    async load(url) {
        this.url = url;
        if (typeof pdfjsLib === 'undefined') {
            this.query('.ui-pdfviewer__canvas-wrapper').innerHTML = '<div class="ui-chart__fallback">PDF.js não carregado</div>';
            return;
        }
        this._pdfDoc = await pdfjsLib.getDocument(url).promise;
        this._totalPages = this._pdfDoc.numPages;
        if (this._totalEl) this._totalEl.textContent = this._totalPages;
        this._renderPage(this.page);
    }

    async _renderPage(num) {
        if (!this._pdfDoc) return;
        const page = await this._pdfDoc.getPage(num);
        const viewport = page.getViewport({ scale: this.zoom });
        this._canvas.width = viewport.width;
        this._canvas.height = viewport.height;
        await page.render({ canvasContext: this._ctx, viewport }).promise;
        this.page = num;
        if (this._currentEl) this._currentEl.textContent = num;
        this.query('[data-action="prev"]').disabled = num <= 1;
        this.query('[data-action="next"]').disabled = num >= this._totalPages;
    }

    goTo(num) { if (num >= 1 && num <= this._totalPages) this._renderPage(num); }

    _download() {
        const a = document.createElement('a');
        a.href = this.url;
        a.download = this.url.split('/').pop() || 'documento.pdf';
        a.click();
    }

    destroy() { this._pdfDoc = null; super.destroy(); }
}
```

```css
.ui-pdfviewer { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; display: flex; flex-direction: column; }

.ui-pdfviewer__toolbar { display: flex; align-items: center; gap: var(--spacing-xs); padding: var(--spacing-xs) var(--spacing-sm); background: var(--color-surface); border-bottom: 1px solid var(--color-border); }
.ui-pdfviewer__btn { border: none; background: transparent; cursor: pointer; padding: 4px; border-radius: var(--radius-sm); color: var(--color-text-secondary); display: flex; }
.ui-pdfviewer__btn:hover { background: var(--color-surface-hover); }
.ui-pdfviewer__btn:disabled { opacity: 0.4; cursor: not-allowed; }
.ui-pdfviewer__page-info { font-size: var(--font-size-sm); color: var(--color-text); }
.ui-pdfviewer__zoom-level { font-size: var(--font-size-xs); color: var(--color-text-muted); min-width: 40px; text-align: center; }

.ui-pdfviewer__canvas-wrapper { flex: 1; overflow: auto; background: #525659; display: flex; justify-content: center; padding: var(--spacing-md); }
.ui-pdfviewer__canvas { box-shadow: var(--shadow-lg); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
