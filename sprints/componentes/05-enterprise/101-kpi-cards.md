# FiscalUI Framework

## Documento 101 — KPI Cards

**Nível 5 — Enterprise Components**

**Versão 1.0**

Cards de indicadores-chave (KPI) com valor, label, tendência, sparkline e variação percentual.

---

```js
class UIKPICard extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.value = options.value || '';
        this.subtitle = options.subtitle || '';
        this.icon = options.icon || null;
        this.trend = options.trend || null;        // { value: 12.5, direction: 'up'|'down', label: 'vs. mês anterior' }
        this.color = options.color || 'var(--color-primary)';
        this.sparkline = options.sparkline || null; // array de números
    }

    template() {
        const trendIcon = this.trend?.direction === 'up' ? 'trending-up' : this.trend?.direction === 'down' ? 'trending-down' : null;
        return `
            <div class="ui-kpicard" style="--kpi-color: ${this.color}">
                <div class="ui-kpicard__header">
                    <span class="ui-kpicard__title">${this.title}</span>
                    ${this.icon ? `<span class="ui-kpicard__icon">${FiscalUI.icons.render(this.icon, { size: 20 })}</span>` : ''}
                </div>
                <div class="ui-kpicard__body">
                    <span class="ui-kpicard__value">${this.value}</span>
                    ${this.subtitle ? `<span class="ui-kpicard__subtitle">${this.subtitle}</span>` : ''}
                </div>
                ${this.trend ? `
                <div class="ui-kpicard__trend ui-kpicard__trend--${this.trend.direction}">
                    ${trendIcon ? FiscalUI.icons.render(trendIcon, { size: 16 }) : ''}
                    <span>${this.trend.value}%</span>
                    ${this.trend.label ? `<span class="ui-kpicard__trend-label">${this.trend.label}</span>` : ''}
                </div>` : ''}
                ${this.sparkline ? `<div class="ui-kpicard__sparkline">${this._renderSparkline()}</div>` : ''}
            </div>
        `;
    }

    _renderSparkline() {
        const max = Math.max(...this.sparkline);
        const min = Math.min(...this.sparkline);
        const range = max - min || 1;
        const points = this.sparkline.map((v, i) => {
            const x = (i / (this.sparkline.length - 1)) * 100;
            const y = 100 - ((v - min) / range) * 80 - 10;
            return `${x},${y}`;
        }).join(' ');
        return `<svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline fill="none" stroke="var(--kpi-color)" stroke-width="2" points="${points}"/></svg>`;
    }

    setValue(val) { this.value = val; this.query('.ui-kpicard__value').textContent = val; }
}
```

```css
.ui-kpicard { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--spacing-md); }
.ui-kpicard__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--spacing-sm); }
.ui-kpicard__title { font-size: var(--font-size-xs); color: var(--color-text-secondary); text-transform: uppercase; font-weight: var(--font-weight-semibold); letter-spacing: 0.5px; }
.ui-kpicard__icon { color: var(--kpi-color); }

.ui-kpicard__body { display: flex; flex-direction: column; gap: 2px; margin-bottom: var(--spacing-sm); }
.ui-kpicard__value { font-size: var(--font-size-2xl); font-weight: var(--font-weight-bold); line-height: 1; color: var(--color-text); font-variant-numeric: tabular-nums; }
.ui-kpicard__subtitle { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-kpicard__trend { display: flex; align-items: center; gap: var(--spacing-xs); font-size: var(--font-size-sm); }
.ui-kpicard__trend--up { color: var(--color-success); }
.ui-kpicard__trend--down { color: var(--color-danger); }
.ui-kpicard__trend-label { color: var(--color-text-muted); font-size: var(--font-size-xs); }

.ui-kpicard__sparkline { height: 40px; margin-top: var(--spacing-sm); }
.ui-kpicard__sparkline svg { width: 100%; height: 100%; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
