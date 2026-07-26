# FiscalUI Framework

## Documento 018 — Testing Framework

**Versão 1.0**

Este documento define a estratégia de testes do FiscalUI. Testes unitários, de integração, e2e, ferramentas, convenções, e cobertura mínima. Todo componente e serviço do FiscalUI deve ser testável.

---

# Índice

1. Introdução
2. Filosofia
3. Pirâmide de Testes
4. Testes Unitários
5. Testes de Integração
6. Testes E2E
7. Testes de Acessibilidade
8. Testes de Performance
9. Mocks e Stubs
10. Cobertura
11. CI/CD
12. Convenções

---

# 1. Introdução

## 1.1 Propósito

Este documento estabelece as diretrizes de testes para o FiscalUI. Todo código deve ser testável, testado, e a cobertura deve ser mantida como parte do processo de desenvolvimento.

---

# 2. Filosofia

```
1. Código não testado é código quebrado
2. Testes são documentação viva
3. Prefira testes unitários (rápidos, isolados)
4. Teste comportamento, não implementação
5. Um bug sem teste vai voltar
```

---

# 3. Pirâmide de Testes

```
        ┌──────┐
        │ E2E  │   ← Poucos testes (fluxos críticos)
       ┌┴──────┴┐
       │ Integ. │   ← Alguns testes (interação entre módulos)
      ┌┴────────┴┐
      │ Unitário │   ← Muitos testes (cada função, cada componente)
     ┌┴──────────┴┐
     │   Estático │   ← Lint, type-check (todos arquivos)
```

---

# 4. Testes Unitários

## 4.1 Ferramenta

```
Framework: Jasmine ou Vitest
Runner: Karma ou Vitest
Browser: Headless Chrome (CI), Chrome (dev)
```

## 4.2 Estrutura

```js
// Componente: src/js/components/button.js
// Teste:      test/components/button.test.js

describe('UIButton', () => {
    let button;

    beforeEach(() => {
        button = new UIButton({ label: 'Salvar' });
    });

    afterEach(() => {
        button.destroy();
    });

    it('should render label text', () => {
        button.render();
        expect(button.element.textContent).toContain('Salvar');
    });

    it('should emit click event', () => {
        const spy = jasmine.createSpy();
        button.on('click', spy);
        button.element.click();
        expect(spy).toHaveBeenCalled();
    });

    it('should be disabled when disabled option is true', () => {
        button = new UIButton({ label: 'OK', disabled: true });
        button.render();
        expect(button.element.disabled).toBe(true);
    });
});
```

---

# 5. Convenções

```
1. Arquivo de teste: {nome-do-modulo}.test.js
2. Teste junto do código: test/{caminho-correspondente}
3. describe: nome do módulo/classe
4. it: descrição do comportamento em português
5. beforeEach: criar instância limpa
6. afterEach: destruir instância
```

---

# 6. Cobertura Mínima

```
Linhas:      80% (core), 70% (componentes)
Funções:     85% (core), 75% (componentes)
Branches:    75% (core), 60% (componentes)
```

---

# 7. Testes de Acessibilidade

```js
describe('UIButton Accessibility', () => {
    it('should have role button', () => {
        const btn = new UIButton({ label: 'OK' });
        btn.render();
        expect(btn.element.getAttribute('role')).toBe('button');
    });

    it('should be keyboard accessible', () => {
        const spy = jasmine.createSpy();
        const btn = new UIButton({ label: 'OK' });
        btn.render();
        btn.on('click', spy);
        btn.element.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
        expect(spy).toHaveBeenCalled();
    });
});
```

---

# 8. Scripts

```json
{
    "scripts": {
        "test": "vitest run",
        "test:watch": "vitest",
        "test:coverage": "vitest run --coverage",
        "test:a11y": "axe --exit",
        "lint": "eslint src/ test/"
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Testing Framework |
