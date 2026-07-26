# FiscalUI Framework

## Documento 168 — Component Generator

**Nível 10 — Developer Platform**

**Versão 1.0**

Gerador de componentes. Cria scaffold de componentes seguindo o padrão FiscalUI.

---

```bash
fiscalui generate component Button
fiscalui generate component DataGrid --with-styles --with-tests
```

```text
src/components/Button/
├── button.js           # Classe do componente
├── button.css          # Estilos BEM
├── button.test.js      # Testes unitários
├── button.md           # Documentação
└── index.js            # Re-export
```

```js
// Template gerado para button.js
class Button extends UIComponent {
  static get tagName() { return 'ui-button'; }

  static get defaultOptions() {
    return {
      label: 'Button',
      variant: 'primary',
      size: 'md',
      disabled: false
    };
  }

  init() {
    this._render();
    this._bindEvents();
  }

  _render() {
    this.el.innerHTML = `
      <button class="ui-btn ui-btn--${this.options.variant} ui-btn--${this.options.size}"
              ${this.options.disabled ? 'disabled' : ''}>
        <span class="ui-btn__label">${this.options.label}</span>
      </button>
    `;
  }

  _bindEvents() {
    this._btn = this.el.querySelector('button');
    this._btn.addEventListener('click', (e) => {
      this.emit('click', e);
    });
  }

  setLabel(label) {
    this.options.label = label;
    this.el.querySelector('.ui-btn__label').textContent = label;
  }

  setDisabled(disabled) {
    this.options.disabled = disabled;
    this._btn.disabled = disabled;
  }
}
```

```js
// Gerador
class ComponentGenerator {
  generate(name, options = {}) {
    return {
      name,
      files: [
        { path: `${name}.js`, content: this._templateJS(name) },
        { path: `${name}.css`, content: this._templateCSS(name) },
        ...(options['with-tests'] ? [{ path: `${name}.test.js`, content: this._templateTest(name) }] : []),
        ...(options['with-docs'] ? [{ path: `${name}.md`, content: this._templateDoc(name) }] : []),
        { path: 'index.js', content: `export { default as ${name} } from './${name}.js';` }
      ]
    };
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
