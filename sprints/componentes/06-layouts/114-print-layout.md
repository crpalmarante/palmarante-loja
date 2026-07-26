# FiscalUI Framework

## Documento 114 — Print Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout otimizado para impressão. Remove elementos interativos, aplica estilos de página e formatação de papel.

---

```js
class PrintLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.content = options.content || '';
        this.pageSize = options.pageSize || 'A4';
        this.orientation = options.orientation || 'portrait';
        this.margins = options.margins || '20mm';
        this.showHeader = options.showHeader !== false;
        this.showFooter = options.showFooter !== false;
    }

    template() {
        return `
            <div class="ui-layout-print" style="--page-size: ${this.pageSize}; --page-orientation: ${this.orientation}; --page-margins: ${this.margins}">
                ${this.showHeader ? `
                <header class="ui-layout-print__header">
                    <div class="ui-layout-print__brand">
                        <h1 class="ui-layout-print__title">${this.title}</h1>
                        <p class="ui-layout-print__date">${new Date().toLocaleDateString('pt-BR')}</p>
                    </div>
                </header>` : ''}
                <div class="ui-layout-print__body">${this.content || ''}</div>
                ${this.showFooter ? `
                <footer class="ui-layout-print__footer">
                    <span class="ui-layout-print__page-num"></span>
                </footer>` : ''}
            </div>
        `;
    }

    onInit() {
        this._body = this.query('.ui-layout-print__body');

        // Auto-print on load if triggered
        if (this.element.dataset.autoPrint) window.print();
    }

    setContent(html) { if (this._body) this._body.innerHTML = html; }
    print() { window.print(); }
}
```

```css
/* Screen preview */
.ui-layout-print { background: #fff; color: #000; font-size: 12pt; line-height: 1.6; font-family: 'Times New Roman', serif; }
.ui-layout-print__header { border-bottom: 2px solid #000; padding-bottom: 10pt; margin-bottom: 15pt; }
.ui-layout-print__title { font-size: 18pt; margin: 0; }
.ui-layout-print__date { font-size: 10pt; color: #666; margin: 4pt 0 0; }
.ui-layout-print__body { min-height: 500pt; }
.ui-layout-print__footer { border-top: 1px solid #ccc; padding-top: 10pt; margin-top: 15pt; font-size: 9pt; color: #666; text-align: center; }

/* Print styles */
@media print {
    @page { size: var(--page-size, A4) var(--page-orientation, portrait); margin: var(--page-margins, 20mm); }
    body { margin: 0; padding: 0; }
    .ui-layout-print { box-shadow: none; border: none; padding: 0; }
    .ui-layout-print__header { position: running(pageHeader); }
    .ui-layout-print__footer { position: running(pageFooter); }
    .ui-layout-print__page-num::after { content: counter(page); }
    .ui-btn, .ui-navbar, .ui-sidebar, [data-action] { display: none !important; }
}
```

```html
<ui-print-layout title="Relatório de Apuração" content="..." auto-print></ui-print-layout>
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
