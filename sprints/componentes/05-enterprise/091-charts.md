# FiscalUI Framework

## Documento 091 — Charts

**Nível 5 — Enterprise Components**

**Versão 1.0**

Container de gráficos com integração a Chart.js. Suporta tipos bar, line, pie, doughnut, area.

---

```js
class UIChart extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.type = options.type || 'bar';
        this.labels = options.labels || [];
        this.datasets = options.datasets || [];
        this.options = options.options || {};
        this.height = options.height || 300;
        this._chart = null;
    }

    template() {
        return `
            <div class="ui-chart" style="height: ${this.height}px">
                <canvas class="ui-chart__canvas"></canvas>
            </div>
        `;
    }

    onInit() {
        this._canvas = this.query('.ui-chart__canvas');
        this._renderChart();
    }

    _renderChart() {
        if (this._chart) this._chart.destroy();
        if (typeof Chart === 'undefined') {
            this._canvas.parentElement.innerHTML = '<div class="ui-chart__fallback">Chart.js não carregado</div>';
            return;
        }
        const config = {
            type: this.type,
            data: { labels: this.labels, datasets: this.datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } },
                ...this.options
            }
        };
        this._chart = new Chart(this._canvas, config);
    }

    setData(labels, datasets) { this.labels = labels; this.datasets = datasets; this._renderChart(); }
    addDataset(dataset) { this.datasets.push(dataset); this._renderChart(); }

    destroy() { if (this._chart) this._chart.destroy(); super.destroy(); }
}
```

```css
.ui-chart { position: relative; width: 100%; }
.ui-chart__canvas { width: 100% !important; height: 100% !important; }
.ui-chart__fallback { display: flex; align-items: center; justify-content: center; height: 100%; color: var(--color-text-muted); font-size: var(--font-size-sm); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
