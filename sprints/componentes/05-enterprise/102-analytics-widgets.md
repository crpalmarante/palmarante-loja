# FiscalUI Framework

## Documento 102 — Analytics Widgets

**Nível 5 — Enterprise Components**

**Versão 1.0**

Widgets analíticos reutilizáveis: tabela de top N, funnel, heatmap, comparativo, métricas inline.

---

```js
class UIAnalyticsWidgets {
    static TopN(data, options = {}) {
        const labelField = options.labelField || 'label';
        const valueField = options.valueField || 'value';
        const limit = options.limit || 10;
        const sorted = [...data].sort((a, b) => b[valueField] - a[valueField]).slice(0, limit);
        const max = sorted[0]?.[valueField] || 1;
        return `<div class="ui-analytics-topn">
            ${sorted.map((item, i) => `
                <div class="ui-analytics-topn__item">
                    <span class="ui-analytics-topn__rank">${i + 1}</span>
                    <span class="ui-analytics-topn__label">${item[labelField]}</span>
                    <div class="ui-analytics-topn__bar-track">
                        <div class="ui-analytics-topn__bar" style="width:${(item[valueField] / max) * 100}%"></div>
                    </div>
                    <span class="ui-analytics-topn__value">${item[valueField]}</span>
                </div>
            `).join('')}
        </div>`;
    }

    static Funnel(stages, options = {}) {
        const max = stages[0]?.value || 1;
        return `<div class="ui-analytics-funnel">
            ${stages.map((s, i) => `
                <div class="ui-analytics-funnel__stage">
                    <div class="ui-analytics-funnel__bar" style="width:${(s.value / max) * 100}%">
                        <span class="ui-analytics-funnel__label">${s.label}</span>
                        <span class="ui-analytics-funnel__value">${s.value}</span>
                        ${i > 0 ? `<span class="ui-analytics-funnel__pct">${Math.round((s.value / stages[i - 1].value) * 100)}%</span>` : ''}
                    </div>
                </div>
            `).join('')}
        </div>`;
    }

    static Comparison(before, after, options = {}) {
        const labelField = options.labelField || 'label';
        const valueField = options.valueField || 'value';
        return `<div class="ui-analytics-compare">
            ${before.map((b, i) => {
                const a = after[i];
                const bpct = a ? Math.round(((a[valueField] - b[valueField]) / b[valueField]) * 100) : 0;
                return `<div class="ui-analytics-compare__item">
                    <span class="ui-analytics-compare__label">${b[labelField]}</span>
                    <div class="ui-analytics-compare__bars">
                        <div class="ui-analytics-compare__bar ui-analytics-compare__bar--before" style="width:${b[valueField]}px"><span>${b[valueField]}</span></div>
                        ${a ? `<div class="ui-analytics-compare__bar ui-analytics-compare__bar--after" style="width:${a[valueField]}px"><span>${a[valueField]}</span></div>` : ''}
                    </div>
                    <span class="ui-analytics-compare__pct ${bpct > 0 ? 'ui-analytics-compare__pct--up' : bpct < 0 ? 'ui-analytics-compare__pct--down' : ''}">${bpct > 0 ? '+' : ''}${bpct}%</span>
                </div>`;
            }).join('')}
        </div>`;
    }
}
```

```css
.ui-analytics-topn { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-analytics-topn__item { display: flex; align-items: center; gap: var(--spacing-sm); }
.ui-analytics-topn__rank { width: 20px; text-align: center; font-weight: var(--font-weight-bold); font-size: var(--font-size-sm); color: var(--color-text-muted); }
.ui-analytics-topn__label { flex: 1; font-size: var(--font-size-sm); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ui-analytics-topn__bar-track { flex: 2; height: 20px; background: var(--color-surface-hover); border-radius: 999px; overflow: hidden; }
.ui-analytics-topn__bar { height: 100%; background: var(--color-primary); border-radius: 999px; transition: width var(--motion-normal); }
.ui-analytics-topn__value { min-width: 40px; text-align: right; font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; }

.ui-analytics-funnel { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.ui-analytics-funnel__stage { width: 100%; display: flex; justify-content: center; }
.ui-analytics-funnel__bar { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-sm) var(--spacing-md); background: var(--color-primary-surface); color: var(--color-primary); border-radius: var(--radius-sm); transition: width var(--motion-normal); min-width: max-content; }
.ui-analytics-funnel__label { font-weight: var(--font-weight-medium); font-size: var(--font-size-sm); }
.ui-analytics-funnel__value { font-weight: var(--font-weight-bold); font-size: var(--font-size-sm); }
.ui-analytics-funnel__pct { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-analytics-compare { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-analytics-compare__item { display: flex; align-items: center; gap: var(--spacing-sm); }
.ui-analytics-compare__label { width: 120px; font-size: var(--font-size-sm); }
.ui-analytics-compare__bars { flex: 1; display: flex; gap: 2px; }
.ui-analytics-compare__bar { height: 20px; border-radius: var(--radius-sm); display: flex; align-items: center; padding: 0 4px; font-size: 10px; color: #fff; white-space: nowrap; }
.ui-analytics-compare__bar--before { background: var(--color-text-muted); }
.ui-analytics-compare__bar--after { background: var(--color-primary); }
.ui-analytics-compare__pct { min-width: 50px; text-align: right; font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); }
.ui-analytics-compare__pct--up { color: var(--color-success); }
.ui-analytics-compare__pct--down { color: var(--color-danger); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
