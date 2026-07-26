# FiscalUI Framework

## Documento 088 — Tree Grid

**Nível 5 — Enterprise Components**

**Versão 1.0**

Grid hierárquico com linhas pai/filho expansíveis. Combina Data Grid + Tree Menu.

---

```js
class UITreeGrid extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.columns = options.columns || [];
        this.data = options.data || [];
        this.childrenField = options.childrenField || 'children';
        this.idField = options.idField || 'id';
        this._expanded = new Set();
    }

    template() {
        return `
            <div class="ui-treegrid">
                <table class="ui-treegrid__table">
                    <thead><tr>${this.columns.map(c => `<th class="ui-datagrid__th">${c.label || c.field}</th>`).join('')}</tr></thead>
                    <tbody>${this._renderNodes(this.data, 0)}</tbody>
                </table>
            </div>
        `;
    }

    _renderNodes(nodes, depth) {
        return nodes.map(node => {
            const hasChildren = node[this.childrenField]?.length;
            const expanded = this._expanded.has(node[this.idField]);
            return `
                <tr class="ui-treegrid__row" data-id="${node[this.idField]}">
                    ${this.columns.map((col, i) => {
                        const val = node[col.field];
                        if (i === 0) {
                            return `<td class="ui-treegrid__td" style="padding-left: ${16 + depth * 24}px">
                                ${hasChildren ? `<button class="ui-treegrid__toggle">${FiscalUI.icons.render(expanded ? 'chevron-down' : 'chevron-right', { size: 14 })}</button>` : '<span class="ui-treegrid__spacer"></span>'}
                                ${col.formatter ? col.formatter(val, node) : val}
                            </td>`;
                        }
                        return `<td class="ui-treegrid__td">${col.formatter ? col.formatter(val, node) : val}</td>`;
                    }).join('')}
                </tr>
                ${hasChildren && expanded ? this._renderNodes(node[this.childrenField], depth + 1) : ''}
            `;
        }).join('');
    }

    onInit() {
        this._tbody = this.query('.ui-treegrid__table tbody');
        this._tbody.addEventListener('click', (e) => {
            const toggle = e.target.closest('.ui-treegrid__toggle');
            if (!toggle) return;
            const row = toggle.closest('.ui-treegrid__row');
            const id = row.dataset.id;
            if (this._expanded.has(id)) this._expanded.delete(id);
            else this._expanded.add(id);
            this._renderBody();
            this.emit('treegrid:toggle', { id, expanded: this._expanded.has(id) });
        });
    }

    _renderBody() { this._tbody.innerHTML = this._renderNodes(this.data, 0); }

    setData(data) { this.data = data; this._renderBody(); }
    expandAll() { this._collectIds(this.data).forEach(id => this._expanded.add(id)); this._renderBody(); }
    collapseAll() { this._expanded.clear(); this._renderBody(); }
    _collectIds(nodes) { let ids = []; nodes.forEach(n => { ids.push(n[this.idField]); if (n[this.childrenField]) ids = ids.concat(this._collectIds(n[this.childrenField])); }); return ids; }
}
```

```css
.ui-treegrid { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: auto; }
.ui-treegrid__table { width: 100%; border-collapse: collapse; }

.ui-treegrid__row:nth-child(even) { background: var(--color-surface-hover); }
.ui-treegrid__row:hover { background: var(--color-primary-surface); }
.ui-treegrid__td { padding: var(--spacing-sm) var(--spacing-md); font-size: var(--font-size-sm); border-bottom: 1px solid var(--color-border); }

.ui-treegrid__toggle { border: none; background: transparent; cursor: pointer; padding: 0; margin-right: var(--spacing-xs); display: inline-flex; vertical-align: middle; color: var(--color-text-muted); }
.ui-treegrid__toggle:hover { color: var(--color-text); }
.ui-treegrid__spacer { display: inline-block; width: 14px; margin-right: var(--spacing-xs); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
