# FiscalUI Framework

## Documento 174 — DevTools

**Nível 10 — Developer Platform**

**Versão 1.0**

Ferramentas de desenvolvimento: inspetor de componentes, debug fiscal, monitor de eventos e performance.

---

```js
// DevTools Panel — extensão de navegador / painel embutido
class DevTools {
  constructor() {
    this.panel = null;
    this._active = false;
  }

  activate() {
    if (this._active) return;
    this._active = true;
    this._createPanel();
    this._hookComponentLifecycle();
    this._hookEventBus();
    this._observeMutations();
  }

  deactivate() {
    this.panel?.remove();
    this._active = false;
  }

  _createPanel() {
    this.panel = document.createElement('div');
    this.panel.className = 'ui-devtools';
    this.panel.innerHTML = `
      <div class="ui-devtools__header">
        <span class="ui-devtools__title">🔧 FiscalUI DevTools</span>
        <button class="ui-devtools__close">&times;</button>
      </div>
      <div class="ui-devtools__tabs">
        <button class="ui-devtools__tab ui-devtools__tab--active" data-tab="components">Componentes</button>
        <button class="ui-devtools__tab" data-tab="events">Eventos</button>
        <button class="ui-devtools__tab" data-tab="fiscal">Fiscal</button>
        <button class="ui-devtools__tab" data-tab="performance">Performance</button>
      </div>
      <div class="ui-devtools__content" id="devtools-components">
        <div class="ui-devtools__tree"></div>
        <div class="ui-devtools__inspector"></div>
      </div>
      <div class="ui-devtools__content" id="devtools-events" style="display:none">
        <div class="ui-devtools__event-log"></div>
      </div>
      <div class="ui-devtools__content" id="devtools-fiscal" style="display:none">
        <div class="ui-devtools__fiscal-info"></div>
      </div>
      <div class="ui-devtools__content" id="devtools-performance" style="display:none">
        <div class="ui-devtools__metrics"></div>
      </div>
    `;
    document.body.appendChild(this.panel);
  }

  _hookComponentLifecycle() {
    const originalCreate = UIComponent.prototype.init;
    UIComponent.prototype.init = function() {
      originalCreate.call(this);
      DevTools._trackComponent(this);
    };
  }

  static _trackComponent(component) {
    // Adiciona ao tree view
    const tree = document.querySelector('.ui-devtools__tree');
    const node = document.createElement('div');
    node.className = 'ui-devtools__node';
    node.textContent = `${component.constructor.name} (${component.id})`;
    node.addEventListener('click', () => DevTools._inspectComponent(component));
    tree?.appendChild(node);
  }

  static _inspectComponent(component) {
    const inspector = document.querySelector('.ui-devtools__inspector');
    inspector.innerHTML = `
      <h4>${component.constructor.name}</h4>
      <pre>${JSON.stringify(component.options, null, 2)}</pre>
      <h5>Eventos</h5>
      <pre>${JSON.stringify(component._events || {}, null, 2)}</pre>
      <h5>DOM</h5>
      <pre>${component.el?.outerHTML?.slice(0, 500)}</pre>
    `;
  }

  // Atalho de teclado: Ctrl+Shift+F
  static registerShortcut() {
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'F') {
        const dt = window.__fiscaluiDevTools;
        dt?._active ? dt.deactivate() : dt?.activate();
      }
    });
  }
}
```

```css
.ui-devtools { position: fixed; bottom: 0; left: 0; right: 0; height: 300px; background: #1e1e1e; color: #d4d4d4; z-index: calc(var(--z-modal) + 1000); font-family: monospace; font-size: 12px; display: flex; flex-direction: column; }
.ui-devtools__header { display: flex; justify-content: space-between; padding: 6px 12px; background: #2d2d2d; }
.ui-devtools__tabs { display: flex; border-bottom: 1px solid #3c3c3c; }
.ui-devtools__tab { padding: 6px 12px; cursor: pointer; background: transparent; border: none; color: #888; border-bottom: 2px solid transparent; }
.ui-devtools__tab--active { color: #fff; border-bottom-color: #569cd6; }
.ui-devtools__content { flex: 1; display: flex; overflow: auto; padding: 8px; }
.ui-devtools__tree { width: 300px; border-right: 1px solid #3c3c3c; overflow: auto; }
.ui-devtools__inspector { flex: 1; padding: 8px; overflow: auto; }
.ui-devtools__node { padding: 4px 8px; cursor: pointer; border-radius: 3px; }
.ui-devtools__node:hover { background: #2d2d2d; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
