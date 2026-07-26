# FiscalUI Framework

## Documento 176 — Low-Code Engine

**Nível 10 — Developer Platform**

**Versão 1.0**

Motor low-code para criação de aplicações com lógica visual, data binding e workflows.

---

```js
// LowCodeEngine — interpreta JSON de página/aplicação
class LowCodeEngine {
  constructor(container) {
    this.container = container;
    this._components = new Map();
    this._state = {};
    this._listeners = new Map();
  }

  async render(schema) {
    this.container.innerHTML = '';
    for (const node of schema.children || []) {
      const el = await this._renderNode(node);
      if (el) this.container.appendChild(el);
    }
  }

  async _renderNode(node) {
    if (!node.type) return null;

    // Busca componente no registry
    const ComponentClass = Registry.get(node.type);
    if (!ComponentClass) {
      console.warn(`[LowCode] Componente '${node.type}' não encontrado`);
      const fallback = document.createElement('div');
      fallback.textContent = `[${node.type}]`;
      return fallback;
    }

    // Processa bindings
    const props = this._resolveBindings(node.props || {});

    // Instancia e renderiza
    const instance = new ComponentClass(props);
    instance.init();

    // Guarda referência
    const id = node.id || `lc-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
    instance.el.dataset.lcId = id;
    this._components.set(id, instance);

    // Renderiza filhos (se container)
    if (instance.el && (node.children?.length)) {
      for (const child of node.children) {
        const childEl = await this._renderNode(child);
        if (childEl) instance.el.appendChild(childEl);
      }
    }

    return instance.el;
  }

  _resolveBindings(props) {
    const result = {};
    for (const [key, value] of Object.entries(props)) {
      if (typeof value === 'string' && value.startsWith('{{') && value.endsWith('}}')) {
        const stateKey = value.slice(2, -2).trim();
        result[key] = this._state[stateKey];
      } else {
        result[key] = value;
      }
    }
    return result;
  }

  setState(key, value) {
    this._state[key] = value;
    this._notify(key, value);
  }

  getState(key) { return this._state[key]; }

  onStateChange(key, callback) {
    if (!this._listeners.has(key)) this._listeners.set(key, []);
    this._listeners.get(key).push(callback);
  }

  _notify(key, value) {
    (this._listeners.get(key) || []).forEach(cb => cb(value));
  }

  getComponent(id) { return this._components.get(id); }
}

// Schema JSON de página
const PAGE_SCHEMA = {
  type: 'Page',
  children: [
    {
      type: 'Navbar',
      props: { title: 'Meu ERP', logo: '/logo.svg' }
    },
    {
      type: 'Dashboard',
      children: [
        {
          type: 'Card',
          props: { title: 'Vendas Hoje' },
          children: [
            {
              type: 'KPIValue',
              props: { value: '{{salesTotal}}', label: 'Total' }
            }
          ]
        }
      ]
    }
  ]
};
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
