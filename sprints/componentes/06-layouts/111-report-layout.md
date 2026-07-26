# FiscalUI Framework

## Documento 111 — Report Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout otimizado para visualização e exportação de relatórios. Cabeçalho, filtros, corpo e rodapé.

---

```js
class ReportLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || 'Relatório';
        this.subtitle = options.subtitle || '';
        this.filters = options.filters || '';
        this.content = options.content || '';
        this.footer = options.footer || '';
        this.showHeader = options.showHeader !== false;
        this.showFilters = options.showFilters !== false;
    }

    template() {
        return `
            <div class="ui-layout-report">
                ${this.showHeader ? `
                <div class="ui-layout-report__header">
                    <div class="ui-layout-report__header-main">
                        <h2 class="ui-layout-report__title">${this.title}</h2>
                        ${this.subtitle ? `<p class="ui-layout-report__subtitle">${this.subtitle}</p>` : ''}
                    </div>
                    <div class="ui-layout-report__header-actions">
                        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="print">${FiscalUI.icons.render('printer', { size: 14 })} Imprimir</button>
                        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="export-pdf">${FiscalUI.icons.render('file-text', { size: 14 })} PDF</button>
                        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="export-excel">${FiscalUI.icons.render('grid', { size: 14 })} Excel</button>
                    </div>
                </div>` : ''}
                ${this.showFilters && this.filters ? `
                <div class="ui-layout-report__filters">
                    <div class="ui-layout-report__filters-body">${this.filters}</div>
                    <button class="ui-btn ui-btn--primary ui-btn--sm" data-action="apply-filters">Aplicar</button>
                </div>` : ''}
                <div class="ui-layout-report__body">
                    ${this.content || '<div class="ui-layout-report__empty">Nenhum dado disponível</div>'}
                </div>
                ${this.footer ? `
                <div class="ui-layout-report__footer">
                    <span class="ui-layout-report__footer-text">${this.footer}</span>
                    <span class="ui-layout-report__footer-date">Gerado em ${new Date().toLocaleDateString('pt-BR')}</span>
                </div>` : ''}
            </div>
        `;
    }

    onInit() {
        this._body = this.query('.ui-layout-report__body');

        this.queryAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', () => this.emit(`report:${btn.dataset.action}`));
        });
    }

    setContent(html) { if (this._body) this._body.innerHTML = html; }
    setTitle(title) { this.title = title; this.query('.ui-layout-report__title').textContent = title; }
}
```

```css
.ui-layout-report { max-width: 900px; margin: 0 auto; padding: var(--spacing-lg); }

.ui-layout-report__header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: var(--spacing-lg); padding-bottom: var(--spacing-md); border-bottom: 2px solid var(--color-border); }
.ui-layout-report__title { font-size: var(--font-size-2xl); margin: 0; font-weight: var(--font-weight-bold); }
.ui-layout-report__subtitle { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin: var(--spacing-xs) 0 0; }
.ui-layout-report__header-actions { display: flex; gap: var(--spacing-xs); flex-shrink: 0; }

.ui-layout-report__filters { display: flex; align-items: flex-end; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); padding: var(--spacing-md); background: var(--color-surface-hover); border-radius: var(--radius-md); }
.ui-layout-report__filters-body { flex: 1; display: flex; gap: var(--spacing-md); flex-wrap: wrap; }

.ui-layout-report__body { min-height: 300px; }
.ui-layout-report__empty { text-align: center; padding: var(--spacing-xl); color: var(--color-text-muted); }

.ui-layout-report__footer { display: flex; justify-content: space-between; margin-top: var(--spacing-lg); padding-top: var(--spacing-md); border-top: 1px solid var(--color-border); font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
