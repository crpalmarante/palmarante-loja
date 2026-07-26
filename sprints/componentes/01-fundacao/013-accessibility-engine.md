# FiscalUI Framework

## Documento 013 — Accessibility Engine

**Versão 1.0**

Este documento define o sistema de acessibilidade do FiscalUI. Gerenciamento de foco, navegação por teclado, ARIA, leitores de tela, high contrast, reduced motion, e conformidade com WCAG 2.1 AA.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Gerenciamento de Foco
6. Focus Trap
7. Navegação por Teclado
8. ARIA
9. Anúncios para Leitores de Tela
10. High Contrast
11. Reduced Motion
12. Zoom e Escala
13. Touch Targets
14. Integração com EventBus
15. Integração com State Manager
16. Debugging e Auditoria
17. Testes
18. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Accessibility Engine garante que o FiscalUI seja utilizável por todas as pessoas, independentemente de suas capacidades. Ele gerencia foco, teclado, ARIA, e adaptações para diferentes necessidades, garantindo conformidade com WCAG 2.1 nível AA.

## 1.2 Princípios

```
1. Acessibilidade não é opcional — é requisito
2. Acessibilidade começa no HTML semântico, JS complementa
3. Todo componente interativo deve ser acessível por teclado
4. Toda informação visual deve ter equivalente textual (ARIA)
5. Toda animação deve respeitar prefers-reduced-motion
6. Toda cor deve ter contraste mínimo de 4.5:1
```

---

# 2. Filosofia

## 2.1 HTML Semântico Primeiro

```html
<!-- ❌ Div semântica -->
<div class="ui-btn" onclick="submit()">Salvar</div>

<!-- ✅ Botão semântico -->
<button class="ui-btn" type="button">Salvar</button>

<!-- ❌ Div semântica -->
<div class="ui-heading" role="heading" aria-level="1">Título</div>

<!-- ✅ Heading semântico -->
<h1 class="ui-heading">Título</h1>
```

## 2.2 Progressive Enhancement

```
Acessibilidade não é tudo-ou-nada:
1. HTML semântico funciona sem JS
2. ARIA melhora a experiência com leitores de tela
3. Gerenciamento de foco JS melhora navegação por teclado
4. Animações respeitam preferências do usuário
```

---

# 3. Arquitetura

## 3.1 Diagrama

```
┌──────────────────────────────────────────────┐
│             Accessibility Engine              │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Focus   │  │   ARIA   │  │ Keyboard │   │
│  │ Manager  │  │  Manager │  │ Manager  │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Announce │  │ Contrast │  │  Motion  │   │
│  │  Manager │  │  Manager │  │  Manager │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
└──────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│              Consumidores                     │
├──────────────────────────────────────────────┤
│  Componentes: Focus trap, ARIA attributes     │
│  EventBus: a11y:announce, a11y:focus-trap    │
│  State: ui.a11y.{reducedMotion, highContrast}│
└──────────────────────────────────────────────┘
```

---

# 4. API Pública

## 4.1 Implementação

```js
class AccessibilityEngine {
    constructor(framework = null) {
        this.framework = framework;
        this._focusTrapStack = [];
        this._announceTimeout = null;
        this._announceElement = null;
        this._reducedMotion = false;
        this._highContrast = false;
        this._keyboardMode = false;
        this._tabKeyPressed = false;
        this._enabled = true;
    }

    // ─── Inicialização ──────────────────────────────────────

    init() {
        this._detectPreferences();
        this._createAnnounceRegion();
        this._listenKeyboardMode();
        this._listenPreferencesChange();
        this._log('info', 'Accessibility Engine iniciado');
        return this;
    }

    _detectPreferences() {
        // prefers-reduced-motion
        const motionMQL = window.matchMedia('(prefers-reduced-motion: reduce)');
        this._reducedMotion = motionMQL.matches;

        // prefers-contrast (high)
        const contrastMQL = window.matchMedia('(prefers-contrast: high)');
        this._highContrast = contrastMQL.matches;

        // Atualiza estado inicial
        this._updateState({
            reducedMotion: this._reducedMotion,
            highContrast: this._highContrast
        });
    }

    _listenPreferencesChange() {
        window.matchMedia('(prefers-reduced-motion: reduce)')
            .addEventListener('change', (e) => {
                this._reducedMotion = e.matches;
                this._updateState({ reducedMotion: this._reducedMotion });
                this._emitEvent('a11y:reduced-motion', { reduced: this._reducedMotion });

                if (this._reducedMotion) {
                    document.documentElement.classList.add('ui-reduced-motion');
                } else {
                    document.documentElement.classList.remove('ui-reduced-motion');
                }
            });

        window.matchMedia('(prefers-contrast: high)')
            .addEventListener('change', (e) => {
                this._highContrast = e.matches;
                this._updateState({ highContrast: this._highContrast });
                this._emitEvent('a11y:high-contrast', { high: this._highContrast });

                document.documentElement.classList.toggle('ui-high-contrast', this._highContrast);
            });
    }

    _listenKeyboardMode() {
        // Detecta quando usuário está navegando por teclado (Tab)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                this._tabKeyPressed = true;
                if (!this._keyboardMode) {
                    this._keyboardMode = true;
                    document.documentElement.classList.add('ui-keyboard-nav');
                }
            }
        });

        document.addEventListener('mousedown', () => {
            this._tabKeyPressed = false;
            if (this._keyboardMode) {
                this._keyboardMode = false;
                document.documentElement.classList.remove('ui-keyboard-nav');
            }
        });
    }

    // ─── Foco ────────────────────────────────────────────────

    focus(element, options = {}) {
        if (!element) return;

        const opts = {
            preventScroll: false,
            ...options
        };

        try {
            element.focus(opts);
        } catch (e) {
            this._log('warn', 'focus(): elemento não focável', e);
        }
    }

    focusFirst(container) {
        if (!container) return;

        const focusable = this._getFocusableElements(container);
        if (focusable.length > 0) {
            this.focus(focusable[0]);
        }
    }

    focusLast(container) {
        if (!container) return;

        const focusable = this._getFocusableElements(container);
        if (focusable.length > 0) {
            this.focus(focusable[focusable.length - 1]);
        }
    }

    focusNext(container) {
        const focusable = this._getFocusableElements(container);
        const active = document.activeElement;
        const idx = focusable.indexOf(active);
        if (idx >= 0 && idx < focusable.length - 1) {
            this.focus(focusable[idx + 1]);
        }
    }

    focusPrevious(container) {
        const focusable = this._getFocusableElements(container);
        const active = document.activeElement;
        const idx = focusable.indexOf(active);
        if (idx > 0) {
            this.focus(focusable[idx - 1]);
        }
    }

    // ─── Focus Trap ──────────────────────────────────────────

    createFocusTrap(container, options = {}) {
        if (!container) return null;

        const trap = {
            container,
            active: false,
            previousActive: null,
            options: {
                escapeDeactivates: true,
                returnFocusOnDeactivate: true,
                ...options
            },
            deactivate: () => this.deactivateFocusTrap(trap)
        };

        return trap;
    }

    activateFocusTrap(trap) {
        if (!trap || trap.active) return;

        trap.previousActive = document.activeElement;
        trap.active = true;

        // Adiciona ao stack
        this._focusTrapStack.push(trap);

        // Escuta Tab
        trap._handler = (e) => this._handleTrapTab(e, trap);
        document.addEventListener('keydown', trap._handler);

        // Foca primeiro elemento
        this.focusFirst(trap.container);

        // Adiciona classe
        trap.container.classList.add('ui-focus-trap');

        this._emitEvent('a11y:focus-trap', {
            trap: true,
            container: trap.container
        });

        this._log('debug', 'Focus trap ativado');
    }

    deactivateFocusTrap(trap) {
        if (!trap || !trap.active) return;

        trap.active = false;

        // Remove do stack
        const idx = this._focusTrapStack.indexOf(trap);
        if (idx >= 0) this._focusTrapStack.splice(idx, 1);

        // Remove listener
        if (trap._handler) {
            document.removeEventListener('keydown', trap._handler);
        }

        // Remove classe
        trap.container.classList.remove('ui-focus-trap');

        // Retorna foco
        if (trap.options.returnFocusOnDeactivate && trap.previousActive) {
            this.focus(trap.previousActive);
        }

        this._emitEvent('a11y:focus-release', {
            trap: false,
            container: trap.container
        });

        this._log('debug', 'Focus trap desativado');
    }

    deactivateAllFocusTraps() {
        for (const trap of [...this._focusTrapStack].reverse()) {
            this.deactivateFocusTrap(trap);
        }
    }

    _handleTrapTab(e, trap) {
        if (e.key !== 'Tab') return;

        if (trap.options.escapeDeactivates && e.key === 'Escape') {
            this.deactivateFocusTrap(trap);
            return;
        }

        const focusable = this._getFocusableElements(trap.container);
        if (focusable.length === 0) return;

        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        const active = document.activeElement;

        // Tab no último → volta para o primeiro
        if (!e.shiftKey && active === last) {
            e.preventDefault();
            this.focus(first);
        }

        // Shift+Tab no primeiro → vai para o último
        if (e.shiftKey && active === first) {
            e.preventDefault();
            this.focus(last);
        }
    }

    // ─── Anúncios (Screen Reader) ────────────────────────────

    announce(message, priority = 'polite') {
        if (!message || !this._announceElement) return;

        if (this._announceTimeout) {
            clearTimeout(this._announceTimeout);
        }

        this._announceTimeout = setTimeout(() => {
            this._announceElement.textContent = '';
            this._announceElement.textContent = message;
        }, 100);

        this._emitEvent('a11y:announce', { message, priority });
    }

    announcePolite(message) {
        this.announce(message, 'polite');
    }

    announceAssertive(message) {
        this.announce(message, 'assertive');
    }

    _createAnnounceRegion() {
        this._announceElement = document.createElement('div');
        this._announceElement.setAttribute('aria-live', 'polite');
        this._announceElement.setAttribute('aria-atomic', 'true');
        this._announceElement.className = 'ui-sr-only ui-announce-region';
        this._announceElement.style.cssText = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;';
        document.body.appendChild(this._announceElement);
    }

    // ─── ARIA ────────────────────────────────────────────────

    setAttribute(element, attr, value) {
        if (!element) return;
        element.setAttribute(attr, value);
    }

    setRole(element, role) {
        this.setAttribute(element, 'role', role);
    }

    setLabel(element, label) {
        this.setAttribute(element, 'aria-label', label);
    }

    setLabelledBy(element, id) {
        this.setAttribute(element, 'aria-labelledby', id);
    }

    setDescribedBy(element, id) {
        this.setAttribute(element, 'aria-describedby', id);
    }

    setExpanded(element, expanded) {
        this.setAttribute(element, 'aria-expanded', String(Boolean(expanded)));
    }

    setHidden(element, hidden) {
        this.setAttribute(element, 'aria-hidden', String(Boolean(hidden)));
    }

    setDisabled(element, disabled) {
        this.setAttribute(element, 'aria-disabled', String(Boolean(disabled)));
    }

    setSelected(element, selected) {
        this.setAttribute(element, 'aria-selected', String(Boolean(selected)));
    }

    setCurrent(element, current = 'page') {
        this.setAttribute(element, 'aria-current', current);
    }

    setLiveRegion(element, mode = 'polite') {
        this.setAttribute(element, 'aria-live', mode);
        this.setAttribute(element, 'aria-atomic', 'true');
    }

    // ─── Getters ────────────────────────────────────────────

    get reducedMotion() {
        return this._reducedMotion;
    }

    get highContrast() {
        return this._highContrast;
    }

    get keyboardMode() {
        return this._keyboardMode;
    }

    get hasActiveFocusTrap() {
        return this._focusTrapStack.length > 0;
    }

    // ─── Utilitários ────────────────────────────────────────

    isFocusable(element) {
        if (!element || element.disabled || element.hidden) return false;

        const tabIndex = element.getAttribute('tabindex');
        if (tabIndex !== null && parseInt(tabIndex) < 0) return false;

        const focusableSelectors = [
            'a[href]',
            'button:not([disabled])',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            '[tabindex]:not([tabindex="-1"])',
            'details summary',
            'audio[controls]',
            'video[controls]'
        ];

        return element.matches(focusableSelectors.join(','));
    }

    skipToContent(targetId) {
        const target = document.getElementById(targetId);
        if (target) {
            this.focus(target);
            this.announce('Navegação pulada para o conteúdo principal');
        }
    }

    // ─── Destruição ─────────────────────────────────────────

    destroy() {
        this.deactivateAllFocusTraps();
        if (this._announceElement) {
            this._announceElement.remove();
        }
        this._enabled = false;
    }

    // ─── Internos ───────────────────────────────────────────

    _getFocusableElements(container) {
        if (!container) return [];
        const selectors = [
            'a[href]',
            'button:not([disabled])',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            '[tabindex]:not([tabindex="-1"])',
            'details summary'
        ];

        const elements = container.querySelectorAll(selectors.join(','));
        return Array.from(elements).filter(el => {
            if (el.disabled) return false;
            if (el.hidden) return false;
            if (el.getAttribute('aria-hidden') === 'true') return false;
            const tabIndex = el.getAttribute('tabindex');
            if (tabIndex && parseInt(tabIndex) < 0) return false;
            return true;
        });
    }

    _emitEvent(event, data) {
        if (this.framework && this.framework.events) {
            this.framework.events.emit(event, { source: 'AccessibilityEngine', ...data });
        }
    }

    _updateState(data) {
        if (this.framework && this.framework.state) {
            this.framework.state.dispatch({
                type: 'a11y/update',
                payload: data
            });
        }
    }

    _log(level, message, error = null) {
        if (this.framework && this.framework.log) {
            this.framework.log(level, `AccessibilityEngine: ${message}`, error);
        } else if (level === 'error') {
            console.error(`[AccessibilityEngine] ${message}`, error || '');
        } else if (level === 'warn') {
            console.warn(`[AccessibilityEngine] ${message}`);
        } else if (level === 'debug' && this.framework?.config?.debug) {
            console.log(`[AccessibilityEngine] ${message}`);
        }
    }
}
```

## 4.2 Resumo da API

| Método | Descrição |
|--------|-----------|
| `init()` | Inicia engine, detecta preferências |
| `focus(element, opts)` | Foca um elemento |
| `focusFirst(container)` | Foca primeiro elemento focável |
| `focusLast(container)` | Foca último elemento focável |
| `focusNext(container)` | Foca próximo elemento |
| `focusPrevious(container)` | Foca elemento anterior |
| `createFocusTrap(container, opts)` | Cria focus trap |
| `activateFocusTrap(trap)` | Ativa focus trap |
| `deactivateFocusTrap(trap)` | Desativa focus trap |
| `deactivateAllFocusTraps()` | Desativa todos traps |
| `announce(message, priority)` | Anuncia para leitores de tela |
| `announcePolite(message)` | Anúncio educado |
| `announceAssertive(message)` | Anúncio assertivo |
| `setAttribute(el, attr, value)` | Define atributo ARIA |
| `setRole(el, role)` | Define role |
| `setLabel(el, label)` | Define aria-label |
| `setLabelledBy(el, id)` | Define aria-labelledby |
| `setDescribedBy(el, id)` | Define aria-describedby |
| `setExpanded(el, expanded)` | Define aria-expanded |
| `setHidden(el, hidden)` | Define aria-hidden |
| `setDisabled(el, disabled)` | Define aria-disabled |
| `setSelected(el, selected)` | Define aria-selected |
| `setCurrent(el, current)` | Define aria-current |
| `setLiveRegion(el, mode)` | Torna região live |
| `isFocusable(element)` | Verifica se é focável |
| `skipToContent(targetId)` | Pula para conteúdo |
| `destroy()` | Remove tudo |

---

# 5. Gerenciamento de Foco

## 5.1 Foco Programático

```js
// Focar um elemento específico
FiscalUI.a11y.focus(document.getElementById('nome-input'));

// Focar primeiro elemento de um container
FiscalUI.a11y.focusFirst(document.querySelector('.ui-modal__body'));

// Focar último
FiscalUI.a11y.focusLast(document.querySelector('.ui-modal__footer'));

// Navegar entre elementos
FiscalUI.a11y.focusNext(container);
FiscalUI.a11y.focusPrevious(container);
```

## 5.2 Foco em Componentes

```js
class Modal extends UIComponent {
    onOpen() {
        // Foca o primeiro input ou botão do modal
        FiscalUI.a11y.focusFirst(this.element);
    }

    onClose() {
        // Retorna foco ao botão que abriu o modal
        FiscalUI.a11y.focus(this._triggerElement);
    }
}
```

---

# 6. Focus Trap

## 6.1 Uso em Modais e Drawers

```js
class Modal extends UIComponent {
    onOpen() {
        // Cria focus trap
        this._focusTrap = FiscalUI.a11y.createFocusTrap(this.element, {
            escapeDeactivates: true,
            returnFocusOnDeactivate: true
        });

        // Ativa
        FiscalUI.a11y.activateFocusTrap(this._focusTrap);
    }

    onClose() {
        // Desativa (foco retorna automaticamente)
        FiscalUI.a11y.deactivateFocusTrap(this._focusTrap);
    }
}
```

## 6.2 Stack de Focus Traps

```js
// Modal 1 abre → focus trap 1 ativado
// Modal 2 abre sobre modal 1 → focus trap 2 ativado (stack)
// Modal 2 fecha → focus trap 2 desativado, trap 1 restaurando
// Modal 1 fecha → focus trap 1 desativado

// O stack gerencia automaticamente a ordem correta
```

## 6.3 Escape para Fechar

```js
const trap = FiscalUI.a11y.createFocusTrap(container, {
    escapeDeactivates: true, // Escape fecha o trap
    returnFocusOnDeactivate: true // Foco volta para quem abriu
});
```

---

# 7. Navegação por Teclado

## 7.1 Modo Teclado

```js
// O engine detecta automaticamente quando usuário navega por teclado
// Adiciona classe .ui-keyboard-nav ao <html>

// CSS:
.ui-keyboard-nav .ui-btn:focus {
    outline: 3px solid var(--color-primary);
    outline-offset: 2px;
}

// Quando usuário volta ao mouse, a classe é removida
// (focus outline só aparece na navegação por teclado)
```

## 7.2 Shortcuts Padrão

```
Tecla       | Ação
------------|----------------------
Tab         | Navegar para próximo elemento
Shift+Tab   | Navegar para elemento anterior
Enter/Space | Ativar botão, link
Escape      | Fechar modal, dropdown, menu
Arrow Up    | Navegar para item anterior (lista, menu)
Arrow Down  | Navegar para próximo item (lista, menu)
Arrow Left  | Navegar para aba anterior
Arrow Right | Navegar para próxima aba
Home        | Ir para primeiro item
End         | Ir para último item
```

## 7.3 Implementação em Componentes

```js
class Dropdown extends UIComponent {
    init() {
        this.on('keydown', this._onKeyDown.bind(this));
    }

    _onKeyDown(e) {
        const items = this._getMenuItems();

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                FiscalUI.a11y.focusNext(this._menu);
                break;
            case 'ArrowUp':
                e.preventDefault();
                FiscalUI.a11y.focusPrevious(this._menu);
                break;
            case 'Escape':
                e.preventDefault();
                this.close();
                break;
            case 'Home':
                e.preventDefault();
                FiscalUI.a11y.focusFirst(this._menu);
                break;
            case 'End':
                e.preventDefault();
                FiscalUI.a11y.focusLast(this._menu);
                break;
        }
    }
}
```

---

# 8. ARIA

## 8.1 Atributos Gerenciados

```js
// O engine fornece helpers para definir atributos ARIA
// Mas a responsabilidade de USAR é do componente

class Accordion extends UIComponent {
    render() {
        // Cada item do accordion
        this._items.forEach((item, i) => {
            const btn = item.querySelector('.ui-accordion__btn');
            const panel = item.querySelector('.ui-accordion__panel');

            FiscalUI.a11y.setExpanded(btn, item.expanded);
            FiscalUI.a11y.setAttribute(btn, 'aria-controls', `panel-${i}`);
            FiscalUI.a11y.setAttribute(panel, 'id', `panel-${i}`);
            FiscalUI.a11y.setAttribute(panel, 'role', 'region');
            FiscalUI.a11y.setLabelledBy(panel, btn.id);
        });
    }
}
```

## 8.2 Padrões ARIA por Componente

| Componente | Role | Atributos Chave |
|-----------|------|-----------------|
| Button | `button` | `aria-label`, `aria-expanded` |
| Modal | `dialog` | `aria-modal="true"`, `aria-labelledby` |
| Tablist | `tablist` | `aria-orientation` |
| Tab | `tab` | `aria-selected`, `aria-controls` |
| Tabpanel | `tabpanel` | `aria-labelledby` |
| Accordion | — | `aria-expanded`, `aria-controls` |
| Menu | `menu` / `menubar` | `aria-orientation` |
| MenuItem | `menuitem` | — |
| Tooltip | `tooltip` | — |
| Alert | `alert` | — |
| Progressbar | `progressbar` | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| Grid | `grid` | `aria-colcount`, `aria-rowcount` |
| Gridcell | `gridcell` | — |

---

# 9. Anúncios para Leitores de Tela

## 9.1 announce()

```js
// Anúncio educado (padrão) — não interrompe
FiscalUI.a11y.announce('Formulário salvo com sucesso');

// Anúncio assertivo — interrompe leitura atual
FiscalUI.a11y.announceAssertive('Erro: campo obrigatório');
```

## 9.2 Quando Usar

```js
// ✅ Anúncios apropriados:
FiscalUI.a11y.announce('Tabela atualizada com 15 registros');
FiscalUI.a11y.announce('Modal aberto: Detalhes da NF-e');
FiscalUI.a11y.announceAssertive('Erro de conexão. Tentando reconectar...');

// ❌ Não anunciar:
FiscalUI.a11y.announce(''); // Vazio
FiscalUI.a11y.announce('Clique aqui'); // Não descritivo
```

## 9.3 Região de Anúncio

```html
<!-- Criada automaticamente pelo engine -->
<div
    aria-live="polite"
    aria-atomic="true"
    class="ui-sr-only ui-announce-region"
>
</div>
```

---

# 10. High Contrast

## 10.1 Modo High Contrast

```js
// Detectado automaticamente via prefers-contrast: high
// Adiciona classe .ui-high-contrast ao <html>

if (FiscalUI.a11y.highContrast) {
    // Estilos específicos para alto contraste são ativados
}
```

## 10.2 CSS para High Contrast

```css
/* Estilos padrão */
.ui-card {
    border: 1px solid var(--color-border);
    background: var(--color-surface);
}

/* High contrast */
.ui-high-contrast .ui-card {
    border: 2px solid var(--color-text);
    background: var(--color-bg);
}

.ui-high-contrast .ui-btn--primary {
    text-decoration: underline;
}
```

---

# 11. Reduced Motion

## 11.1 Detecção

```js
// Detectado via prefers-reduced-motion: reduce
// Adiciona classe .ui-reduced-motion ao <html>

if (FiscalUI.a11y.reducedMotion) {
    // Desativa animações
    this._disableAnimations();
}
```

## 11.2 CSS

```css
/* Transições suaves (padrão) */
.ui-modal {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.ui-fade-enter { opacity: 0; transform: translateY(-10px); }
.ui-fade-enter-active { opacity: 1; transform: translateY(0); }

/* Reduced motion: sem animação */
.ui-reduced-motion .ui-modal {
    transition: none;
}

.ui-reduced-motion .ui-fade-enter,
.ui-reduced-motion .ui-fade-enter-active {
    opacity: 1;
    transform: none;
}
```

## 11.3 Animações Condicionais

```js
class Toast extends UIComponent {
    show(message) {
        this.element.textContent = message;

        if (FiscalUI.a11y.reducedMotion) {
            // Aparece instantaneamente
            this.element.style.opacity = '1';
        } else {
            // Animação suave
            this.element.classList.add('ui-toast--enter');
            requestAnimationFrame(() => {
                this.element.classList.remove('ui-toast--enter');
                this.element.classList.add('ui-toast--enter-active');
            });
        }
    }
}
```

---

# 12. Zoom e Escala

## 12.1 Suporte a Zoom

```js
// O FiscalUI não bloqueia zoom (viewport não tem user-scalable=no)
// Todos os componentes são responsivos e suportam zoom até 200%

// Meta tag correta:
// <meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## 12.2 Unidades Relativas

```css
/* ❌ Pixel fixo — não escala com zoom do navegador */
.ui-text { font-size: 14px; }
.ui-card { width: 300px; }

/* ✅ Unidade relativa — escala com zoom */
.ui-text { font-size: 0.875rem; }
.ui-card { width: 18.75rem; }
```

---

# 13. Touch Targets

## 13.1 Tamanho Mínimo

```css
/* Touch targets mínimos: 44x44px (WCAG 2.5.5) */
.ui-btn {
    min-height: 44px;
    min-width: 44px;
    padding: 0.5rem 1rem;
}

.ui-icon-btn {
    min-width: 44px;
    min-height: 44px;
}
```

## 13.2 Espaçamento

```css
/* Espaçamento entre touch targets */
.ui-btn-group {
    display: flex;
    gap: 0.5rem; /* Mínimo 8px entre alvos */
}
```

---

# 14. Integração com EventBus

## 14.1 Eventos

```js
'a11y:announce'           // Anúncio para leitor de tela
'a11y:focus-trap'         // Focus trap ativado
'a11y:focus-release'      // Focus trap desativado
'a11y:reduced-motion'     // prefers-reduced-motion mudou
'a11y:high-contrast'      // prefers-contrast mudou
```

---

# 15. Integração com State Manager

## 15.1 Slice na Store

```js
{
    ui: {
        a11y: {
            reducedMotion: false,
            highContrast: false,
            keyboardMode: false,
            focusTrapActive: false
        }
    }
}
```

## 15.2 Ações

```js
'a11y/update'   // Atualiza preferências de acessibilidade
```

---

# 16. Debugging e Auditoria

## 16.1 Modo Debug

```js
FiscalUI.config.debug = true;

// Logs:
// [AccessibilityEngine] Focus trap ativado
// [AccessibilityEngine] Anúncio: "Formulário salvo"
```

## 16.2 Auditoria de ARIA

```js
// Helper de debug para verificar ARIA
function auditARIA() {
    const issues = [];

    // Verifica modal sem aria-labelledby
    document.querySelectorAll('[role="dialog"]').forEach(dialog => {
        if (!dialog.hasAttribute('aria-labelledby') && !dialog.hasAttribute('aria-label')) {
            issues.push(`Modal sem label: ${dialog.id || 'sem id'}`);
        }
    });

    // Verifica botões sem label acessível
    document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])').forEach(btn => {
        if (!btn.textContent.trim()) {
            issues.push(`Botão vazio: ${btn.className}`);
        }
    });

    if (issues.length > 0) {
        console.warn('[A11y Audit] Problemas encontrados:', issues);
    } else {
        console.log('[A11y Audit] Nenhum problema encontrado');
    }
}
```

---

# 17. Testes

## 17.1 Teste Unitário

```js
describe('AccessibilityEngine', () => {
    let engine;

    beforeEach(() => {
        engine = new AccessibilityEngine();
    });

    afterEach(() => {
        engine.destroy();
    });

    it('should detect reduced motion preference', () => {
        // Simula prefers-reduced-motion
        spyOn(window, 'matchMedia').and.returnValue({
            matches: true,
            addEventListener: () => {}
        });

        engine._detectPreferences();
        expect(engine.reducedMotion).toBe(true);
    });

    it('should focus an element', () => {
        const el = document.createElement('button');
        spyOn(el, 'focus');
        engine.focus(el);
        expect(el.focus).toHaveBeenCalled();
    });

    it('should get focusable elements', () => {
        const container = document.createElement('div');
        container.innerHTML = `
            <button>OK</button>
            <input type="text">
            <select><option>1</option></select>
            <a href="#">Link</a>
            <button disabled>Disabled</button>
            <span>Não focável</span>
        `;

        const focusable = engine._getFocusableElements(container);
        expect(focusable.length).toBe(4);
    });

    it('should activate and deactivate focus trap', () => {
        const container = document.createElement('div');
        container.innerHTML = `
            <button>Primeiro</button>
            <button>Segundo</button>
            <button>Terceiro</button>
        `;
        document.body.appendChild(container);

        const trap = engine.createFocusTrap(container);
        engine.activateFocusTrap(trap);

        expect(trap.active).toBe(true);
        expect(engine.hasActiveFocusTrap).toBe(true);

        engine.deactivateFocusTrap(trap);
        expect(trap.active).toBe(false);
        expect(engine.hasActiveFocusTrap).toBe(false);

        document.body.removeChild(container);
    });

    it('should manage focus trap stack', () => {
        const c1 = document.createElement('div'); c1.innerHTML = '<button>A</button>';
        const c2 = document.createElement('div'); c2.innerHTML = '<button>B</button>';
        document.body.appendChild(c1);
        document.body.appendChild(c2);

        const t1 = engine.createFocusTrap(c1);
        const t2 = engine.createFocusTrap(c2);

        engine.activateFocusTrap(t1);
        engine.activateFocusTrap(t2);

        expect(engine._focusTrapStack.length).toBe(2);

        engine.deactivateFocusTrap(t2);
        expect(engine._focusTrapStack.length).toBe(1);

        engine.destroy();
        document.body.removeChild(c1);
        document.body.removeChild(c2);
    });

    it('should announce messages to screen readers', () => {
        engine._createAnnounceRegion();

        engine.announce('Test message');
        expect(engine._announceElement.textContent).toBe('Test message');
    });

    it('should set ARIA attributes', () => {
        const el = document.createElement('div');

        engine.setRole(el, 'button');
        expect(el.getAttribute('role')).toBe('button');

        engine.setLabel(el, 'Salvar');
        expect(el.getAttribute('aria-label')).toBe('Salvar');

        engine.setExpanded(el, true);
        expect(el.getAttribute('aria-expanded')).toBe('true');

        engine.setHidden(el, true);
        expect(el.getAttribute('aria-hidden')).toBe('true');
    });

    it('should detect keyboard mode', () => {
        expect(engine.keyboardMode).toBe(false);

        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab' }));
        expect(engine.keyboardMode).toBe(true);

        document.dispatchEvent(new MouseEvent('mousedown'));
        expect(engine.keyboardMode).toBe(false);
    });

    it('should skip to content', () => {
        const target = document.createElement('div');
        target.id = 'main-content';
        document.body.appendChild(target);

        spyOn(engine, 'focus');
        engine.skipToContent('main-content');
        expect(engine.focus).toHaveBeenCalledWith(target);

        document.body.removeChild(target);
    });
});
```

## 17.2 Teste de Foco

```js
describe('Focus Management', () => {
    let engine;
    let container;

    beforeEach(() => {
        engine = new AccessibilityEngine();
        container = document.createElement('div');
        container.innerHTML = `
            <button id="btn1">Um</button>
            <button id="btn2">Dois</button>
            <button id="btn3">Três</button>
        `;
        document.body.appendChild(container);
    });

    afterEach(() => {
        document.body.removeChild(container);
        engine.destroy();
    });

    it('should focus first element', () => {
        engine.focusFirst(container);
        expect(document.activeElement.id).toBe('btn1');
    });

    it('should focus last element', () => {
        engine.focusLast(container);
        expect(document.activeElement.id).toBe('btn3');
    });

    it('should navigate to next element', () => {
        engine.focus(container.querySelector('#btn1'));
        engine.focusNext(container);
        expect(document.activeElement.id).toBe('btn2');
    });

    it('should navigate to previous element', () => {
        engine.focus(container.querySelector('#btn2'));
        engine.focusPrevious(container);
        expect(document.activeElement.id).toBe('btn1');
    });
});
```

---

# 18. Boas Práticas

## 18.1 Regras de Ouro

```
1. NUNCA remova outline de foco — sempre use :focus-visible
2. SEMPRE use HTML semântico antes de ARIA
3. NUNCA use role="presentation" em elementos interativos
4. SEMPRE forneça aria-label para botões sem texto
5. NUNCA coloque aria-hidden="true" em elementos focáveis
6. SEMPRE use focus trap em modais e drawers
7. NUNCA bloqueie zoom (user-scalable=no)
8. SEMPRE anuncie mudanças dinâmicas relevantes
9. NUNCA esconda o foco do teclado
10. SEMPRE respeite prefers-reduced-motion
```

## 18.2 Checklist

```
☐ HTML semântico (h1-h6, button, nav, main, etc.)
☐ Títulos de página (document.title) atualizados por rota
☐ Skip to content link presente
☐ Focus trap em modais/drawers
☐ aria-label em botões sem texto
☐ aria-expanded em accordions/dropdowns
☐ aria-selected em tabs
☐ aria-current em navegação ativa
☐ aria-live para regiões dinâmicas
☐ prefers-reduced-motion respeitado
☐ Contraste mínimo 4.5:1 verificado
☐ Touch targets ≥ 44px
☐ Navegação por teclado testada
☐ Leitores de tela testados (NVDA, VoiceOver)
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Accessibility Engine completo |
