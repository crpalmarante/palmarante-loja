# FiscalUI Framework

## Documento 171 — Widget SDK

**Nível 10 — Developer Platform**

**Versão 1.0**

SDK para criação de widgets reutilizáveis — mini-componentes com dados dinâmicos.

---

```js
// Widget base class
class WidgetSDK {
  constructor(options = {}) {
    this.id = options.id || `widget-${Date.now()}`;
    this.title = options.title || '';
    this.size = options.size || 'medium'; // small, medium, large, full
    this.refreshInterval = options.refreshInterval || 0;
    this._data = null;
    this._timer = null;
    this._el = null;
  }

  async render(container) {
    this._el = document.createElement('div');
    this._el.className = `ui-widget ui-widget--${this.size}`;
    this._el.innerHTML = `
      <div class="ui-widget__header">
        <h3 class="ui-widget__title">${this.title}</h3>
        <div class="ui-widget__actions">
          <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="refresh">↻</button>
          <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="config">⚙</button>
        </div>
      </div>
      <div class="ui-widget__body" data-content></div>
    `;

    container.appendChild(this._el);
    await this.load();
    this._bindWidgetEvents();

    if (this.refreshInterval > 0) {
      this._timer = setInterval(() => this.load(), this.refreshInterval);
    }
  }

  async load() {
    // Override por subclasse
    this._data = await this.fetchData();
    this.update(this._data);
  }

  update(data) {
    // Override por subclasse
    this._el.querySelector('[data-content]').innerHTML = JSON.stringify(data);
  }

  destroy() {
    if (this._timer) clearInterval(this._timer);
    this._el?.remove();
  }

  _bindWidgetEvents() {
    this._el.querySelector('[data-action="refresh"]')
      ?.addEventListener('click', () => this.load());
  }

  setSize(size) {
    this.size = size;
    this._el.className = `ui-widget ui-widget--${size}`;
  }
}

// Exemplo de widget
class SalesWidget extends WidgetSDK {
  constructor() { super({ title: 'Vendas Hoje', size: 'medium', refreshInterval: 30000 }); }

  async fetchData() {
    const res = await fetch('/api/dashboard/sales-today');
    return res.json();
  }

  update(data) {
    this._el.querySelector('[data-content]').innerHTML = `
      <div class="ui-widget__kpi">
        <span class="ui-widget__kpi-value">R$ ${data.total}</span>
        <span class="ui-widget__kpi-label">Total</span>
      </div>
      <div class="ui-widget__kpi">
        <span class="ui-widget__kpi-value">${data.count}</span>
        <span class="ui-widget__kpi-label">Pedidos</span>
      </div>
    `;
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
