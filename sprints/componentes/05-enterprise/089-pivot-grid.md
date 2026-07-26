# FiscalUI Framework

## Documento 089 — Pivot Grid

**Nível 5 — Enterprise Components**

**Versão 1.0**

Grid pivotante para análise multidimensional. Agrupa, sumariza e cruza dados em linhas × colunas.

---

```js
class UIPivotGrid extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.data = options.data || [];
        this.rows = options.rows || [];
        this.columns = options.columns || [];
        this.values = options.values || [];
        this.aggregator = options.aggregator || 'sum';
    }

    template() {
        return `<div class="ui-pivot"><table class="ui-pivot__table">${this._build()}</table></div>`;
    }

    _build() {
        const rowKeys = [...new Set(this.data.map(d => this.rows.map(r => d[r]).join('|')))];
        const colKeys = [...new Set(this.data.map(d => this.columns.map(c => d[c]).join('|')))];
        let html = '<thead><tr><th></th>';
        colKeys.forEach(ck => { html += `<th class="ui-pivot__th">${ck}</th>`; });
        html += `<th class="ui-pivot__th">Total</th></tr></thead><tbody>`;
        rowKeys.forEach(rk => {
            html += `<tr><td class="ui-pivot__row-label">${rk}</td>`;
            let rowTotal = 0;
            colKeys.forEach(ck => {
                const cells = this.data.filter(d => this.rows.map(r => d[r]).join('|') === rk && this.columns.map(c => d[c]).join('|') === ck);
                const val = this._aggregate(cells);
                rowTotal += val;
                html += `<td class="ui-pivot__td">${val}</td>`;
            });
            html += `<td class="ui-pivot__td ui-pivot__td--total">${rowTotal}</td></tr>`;
        });
        html += '</tbody>';
        return html;
    }

    _aggregate(cells) {
        if (this.aggregator === 'count') return cells.length;
        const vals = cells.map(d => {
            const v = parseFloat(d[this.values[0]]);
            return isNaN(v) ? 0 : v;
        });
        if (this.aggregator === 'sum') return vals.reduce((a, b) => a + b, 0);
        if (this.aggregator === 'avg') return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
        if (this.aggregator === 'min') return Math.min(...vals);
        if (this.aggregator === 'max') return Math.max(...vals);
        return 0;
    }

    setData(data) { this.data = data; this.render(); }
}
```

```css
.ui-pivot { overflow: auto; border: 1px solid var(--color-border); border-radius: var(--radius-md); }
.ui-pivot__table { border-collapse: collapse; width: 100%; }
.ui-pivot__th { padding: var(--spacing-sm) var(--spacing-md); font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); background: var(--color-surface-hover); border: 1px solid var(--color-border); white-space: nowrap; }
.ui-pivot__row-label { padding: var(--spacing-sm) var(--spacing-md); font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); background: var(--color-surface); border: 1px solid var(--color-border); }
.ui-pivot__td { padding: var(--spacing-sm) var(--spacing-md); font-size: var(--font-size-sm); text-align: right; border: 1px solid var(--color-border); font-variant-numeric: tabular-nums; }
.ui-pivot__td--total { font-weight: var(--font-weight-semibold); background: var(--color-primary-surface); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
