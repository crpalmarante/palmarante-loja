# FiscalUI Framework

## Documento 087 — Data Grid

**Nível 5 — Enterprise Components**

**Versão 1.0**

Grid de dados com colunas, linhas, ordenação, filtro, seleção, paginação, resize e reordenação de colunas.

---

```js
class UIDataGrid extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.columns = options.columns || [];
        this.data = options.data || [];
        this.pageSize = options.pageSize || 20;
        this.sortable = options.sortable !== false;
        this.filterable = options.filterable || false;
        this.selectable = options.selectable || false;
        this.resizable = options.resizable || false;
        this._page = 1;
        this._sortField = null;
        this._sortDir = null;
        this._filter = {};
        this._selected = new Set();
    }

    template() {
        return `
            <div class="ui-datagrid">
                <div class="ui-datagrid__toolbar">
                    ${this.filterable ? `<div class="ui-datagrid__search">
                        <input class="ui-field__input" type="search" placeholder="Buscar na tabela…" style="height:32px;font-size:13px">
                    </div>` : ''}
                    <div class="ui-datagrid__info">
                        <span class="ui-datagrid__total">${this.data.length} registros</span>
                    </div>
                </div>
                <div class="ui-datagrid__table-wrapper">
                    <table class="ui-datagrid__table">
                        <thead><tr>${this._renderHeaders()}</tr></thead>
                        <tbody>${this._renderRows()}</tbody>
                    </table>
                </div>
                <div class="ui-datagrid__footer">
                    <div class="ui-datagrid__pagination">${this._renderPagination()}</div>
                </div>
            </div>
        `;
    }

    _renderHeaders() {
        return this.columns.map((col, i) => `
            <th class="ui-datagrid__th ${this.sortable ? 'ui-datagrid__th--sortable' : ''}"
                data-field="${col.field}" data-index="${i}"
                ${col.width ? `style="width:${col.width}px"` : ''}>
                <span class="ui-datagrid__th-label">${col.label || col.field}</span>
                ${this.sortable ? `<span class="ui-datagrid__sort-icon">${this._sortIcon(col.field)}</span>` : ''}
            </th>
        `).join('');
    }

    _sortIcon(field) {
        if (this._sortField !== field) return '';
        return this._sortDir === 'asc' ? ' ▲' : ' ▼';
    }

    _renderRows() {
        const sorted = this._sortData();
        const paged = sorted.slice((this._page - 1) * this.pageSize, this._page * this.pageSize);
        if (!paged.length) return `<tr><td colspan="${this.columns.length}" class="ui-datagrid__empty">Nenhum registro encontrado</td></tr>`;
        return paged.map(row => `
            <tr class="ui-datagrid__row ${this._selected.has(row.id || row) ? 'ui-datagrid__row--selected' : ''}" data-id="${row.id || ''}">
                ${this.columns.map(col => `<td class="ui-datagrid__td">${this._formatCell(row, col)}</td>`).join('')}
            </tr>
        `).join('');
    }

    _sortData() {
        let data = [...this.data];
        if (this._sortField) {
            data.sort((a, b) => {
                const va = a[this._sortField]; const vb = b[this._sortField];
                if (va < vb) return this._sortDir === 'asc' ? -1 : 1;
                if (va > vb) return this._sortDir === 'asc' ? 1 : -1;
                return 0;
            });
        }
        return data;
    }

    _renderPagination() {
        const totalPages = Math.ceil(this.data.length / this.pageSize);
        if (totalPages <= 1) return '';
        let html = `<button class="ui-datagrid__page-btn" data-page="${this._page - 1}" ${this._page <= 1 ? 'disabled' : ''}>Anterior</button>`;
        for (let p = 1; p <= totalPages; p++) {
            html += `<button class="ui-datagrid__page-btn ${p === this._page ? 'ui-datagrid__page-btn--active' : ''}" data-page="${p}">${p}</button>`;
        }
        html += `<button class="ui-datagrid__page-btn" data-page="${this._page + 1}" ${this._page >= totalPages ? 'disabled' : ''}>Próximo</button>`;
        return html;
    }

    _formatCell(row, col) {
        const val = row[col.field];
        if (col.formatter) return col.formatter(val, row);
        if (val === null || val === undefined) return '';
        return String(val);
    }

    onInit() {
        this._tbody = this.query('.ui-datagrid__table tbody');
        this._pagination = this.query('.ui-datagrid__pagination');

        if (this.sortable) {
            this.queryAll('.ui-datagrid__th--sortable').forEach(th => {
                th.addEventListener('click', () => {
                    const field = th.dataset.field;
                    this._sortDir = this._sortField === field && this._sortDir === 'asc' ? 'desc' : 'asc';
                    this._sortField = field;
                    this._renderBody();
                });
            });
        }

        this._pagination?.addEventListener('click', (e) => {
            const btn = e.target.closest('.ui-datagrid__page-btn');
            if (!btn || btn.disabled) return;
            this._page = parseInt(btn.dataset.page);
            this._renderBody();
        });

        if (this.filterable) {
            this.query('.ui-datagrid__search input')?.addEventListener('input', (e) => {
                const q = e.target.value.toLowerCase();
                this.data = this._originalData.filter(r => Object.values(r).some(v => String(v).toLowerCase().includes(q)));
                this._page = 1;
                this._renderBody();
            });
        }

        if (this.selectable) {
            this._tbody.addEventListener('click', (e) => {
                const row = e.target.closest('.ui-datagrid__row');
                if (!row) return;
                const id = row.dataset.id;
                if (this._selected.has(id)) this._selected.delete(id);
                else this._selected.add(id);
                row.classList.toggle('ui-datagrid__row--selected');
                this.emit('datagrid:select', { selected: [...this._selected] });
            });
        }
    }

    _renderBody() {
        this._tbody.innerHTML = this._renderRows();
        this._pagination.innerHTML = this._renderPagination();
    }

    setData(data) { this._originalData = data; this.data = data; this._page = 1; this._renderBody(); }

    value() { return this.data; }
}
```

```css
.ui-datagrid { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }

.ui-datagrid__toolbar { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-sm); background: var(--color-surface-hover); border-bottom: 1px solid var(--color-border); }
.ui-datagrid__search input { width: 240px; }
.ui-datagrid__info { font-size: var(--font-size-sm); color: var(--color-text-muted); }

.ui-datagrid__table-wrapper { overflow-x: auto; }
.ui-datagrid__table { width: 100%; border-collapse: collapse; }
.ui-datagrid__th { padding: var(--spacing-sm) var(--spacing-md); text-align: left; font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); color: var(--color-text-secondary); background: var(--color-surface); border-bottom: 2px solid var(--color-border); white-space: nowrap; user-select: none; }
.ui-datagrid__th--sortable { cursor: pointer; }
.ui-datagrid__th--sortable:hover { background: var(--color-surface-hover); }
.ui-datagrid__sort-icon { font-size: 10px; margin-left: 4px; }

.ui-datagrid__row { transition: background var(--motion-fast); }
.ui-datagrid__row:nth-child(even) { background: var(--color-surface-hover); }
.ui-datagrid__row:hover { background: var(--color-primary-surface); }
.ui-datagrid__row--selected { background: var(--color-primary-surface) !important; }
.ui-datagrid__td { padding: var(--spacing-sm) var(--spacing-md); font-size: var(--font-size-sm); border-bottom: 1px solid var(--color-border); }
.ui-datagrid__empty { text-align: center; padding: var(--spacing-xl); color: var(--color-text-muted); }

.ui-datagrid__footer { display: flex; align-items: center; justify-content: center; padding: var(--spacing-sm); border-top: 1px solid var(--color-border); background: var(--color-surface); }
.ui-datagrid__pagination { display: flex; gap: 2px; }
.ui-datagrid__page-btn { padding: var(--spacing-xs) var(--spacing-sm); border: 1px solid var(--color-border); background: var(--color-surface); cursor: pointer; border-radius: var(--radius-sm); font-size: var(--font-size-sm); }
.ui-datagrid__page-btn:hover { background: var(--color-surface-hover); }
.ui-datagrid__page-btn--active { background: var(--color-primary); color: #fff; border-color: var(--color-primary); }
.ui-datagrid__page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
