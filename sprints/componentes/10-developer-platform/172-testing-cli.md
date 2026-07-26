# FiscalUI Framework

## Documento 172 — Testing CLI

**Nível 10 — Developer Platform**

**Versão 1.0**

CLI integrada de testes: runner, cobertura, snapshots e modo watch.

---

```bash
# Comandos
fiscalui test                    # Executa todos os testes
fiscalui test --watch            # Modo watch
fiscalui test --coverage         # Com cobertura
fiscalui test --component Button # Testa componente específico
fiscalui test --e2e              # Testes end-to-end
fiscalui test --snapshot         # Atualiza snapshots
```

```js
// fiscalui.test.js — config de testes
{
  "framework": "jest",
  "rootDir": "src",
  "testMatch": ["**/*.test.js", "**/*.spec.js"],
  "coverage": {
    "statements": 80,
    "branches": 75,
    "functions": 80,
    "lines": 80
  },
  "environment": "jsdom",
  "setupFiles": ["fiscalui-test-setup.js"],
  "moduleNameMapper": {
    "\\.css$": "identity-obj-proxy"
  }
}
```

```js
// Test setup automático
// fiscalui-test-setup.js
import { FiscalUI } from '@fiscalui/core';

beforeEach(() => {
  document.body.innerHTML = '';
  FiscalUI.init({ testing: true });
});

afterEach(() => {
  FiscalUI.destroy();
});

// Helpers de teste
function render(component) {
  document.body.appendChild(component.el);
  return component;
}

function click(el) {
  el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
}

function type(input, value) {
  input.value = value;
  input.dispatchEvent(new Event('input', { bubbles: true }));
}

function wait(duration = 0) {
  return new Promise(resolve => setTimeout(resolve, duration));
}
```

```js
// Exemplo de teste de componente
describe('Button', () => {
  it('deve renderizar com label', () => {
    const btn = new Button({ label: 'Salvar' });
    render(btn);
    expect(btn.el.textContent).toContain('Salvar');
  });

  it('deve emitir evento click', () => {
    const spy = jest.fn();
    const btn = new Button({ label: 'OK' });
    render(btn);
    btn.on('click', spy);
    click(btn.el.querySelector('button'));
    expect(spy).toHaveBeenCalledTimes(1);
  });
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
