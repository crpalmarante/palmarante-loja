# FiscalUI Framework

## Documento 006 — Component Base

**Versão 1.0**

Este documento define a classe base da qual todos os componentes do FiscalUI herdam. Ciclo de vida, API pública, padrões de implementação, eventos, estado e ciclo de destruição.

Todo componente do FiscalUI segue este contrato.

---

# Índice

1. Introdução
2. Filosofia
3. Ciclo de Vida
4. Construtor
5. Método create()
6. Método init()
7. Método render()
8. Método update()
9. Método destroy()
10. Método template()
11. Gerenciamento de Eventos
12. Gerenciamento de Estado
13. Sub-componentes
14. Referências DOM
15. Utilitários
16. Padrões de Implementação
17. Componente Simples
18. Componente com Estado
19. Componente com Sub-componentes
20. Componente Assíncrono
21. Componente com Plugin
22. Decorators
23. Mixins
24. Herança
25. Composição vs Herança
26. Observabilidade
27. Performance
28. Memória e Vazamentos
29. Testabilidade
30. Boas Práticas
31. API Completa

---

# 1. Introdução

## 1.1 Propósito

`UIComponent` é a classe base de todos os componentes visuais do FiscalUI. Ela define:

- **Ciclo de vida** — como componentes nascem, vivem e morrem
- **API pública** — métodos que todo componente expõe
- **Eventos** — como componentes se comunicam
- **Estado** — como componentes gerenciam estado interno
- **DOM** — como componentes manipulam o DOM

Nenhum componente no FiscalUI escapa deste contrato. `UIButton`, `UICard`, `UIModal`, `UIDataGrid`, todos estendem `UIComponent`.

## 1.2 Princípios

```
1. Todo componente tem ciclo de vida gerenciado
2. Todo componente comunica-se via eventos
3. Todo componente gerencia seu próprio DOM
4. Todo componente é destruível (limpa memória)
5. Todo componente é testável isoladamente
6. Todo componente funciona sem o Framework (testabilidade)
7. Todo componente pode conter sub-componentes
```

## 1.3 Hierarquia

```
UIComponent (base)
    │
    ├── UIButton
    ├── UICard
    ├── UIModal
    ├── UIDataGrid
    ├── UIForm
    ├── UISidebar
    ├── UITabs
    └── ... (todos os componentes do FiscalUI)
```

---

# 2. Filosofia

## 2.1 Separação de Responsabilidades

```
UIComponent
    │
    ├── create()       → Constrói DOM (uma vez)
    ├── init()         → Registra eventos (uma vez)
    ├── render()       → Atualiza DOM (múltiplas vezes)
    ├── update()       → Atualiza estado + DOM (múltiplas vezes)
    └── destroy()      → Limpa tudo (uma vez)
```

## 2.2 Imutabilidade de Props

As opções passadas no construtor (`opts`) nunca devem ser modificadas pelo componente. Mudanças são feitas via `setState()` ou `update()`.

```js
// ❌ Errado — modifica props
this.opts.label = 'Novo texto';

// ✅ Correto — usa estado interno
this.setState({ label: 'Novo texto' });
```

## 2.3 DOM é Gerido pelo Componente

Cada componente cria, manipula e destrói seu próprio DOM. Nenhum componente externo deve acessar o `element` de outro componente diretamente.

```js
// ❌ Errado — acessa DOM de outro componente
document.querySelector('.ui-btn__label').textContent = 'x';

// ✅ Correto — chama método público
button.setLabel('x');
```

## 2.4 Eventos como Única Forma de Comunicação

Componentes nunca chamam métodos de outros componentes diretamente.

```js
// ❌ Errado — acoplamento direto
button.onClick = () => { grid.refresh(); };

// ✅ Correto — via EventBus
button.onClick = () => {
    FiscalUI.events.emit('grid:refresh');
};
```

---

# 3. Ciclo de Vida

## 3.1 Diagrama

```
constructor(opts)
    │
    ▼
create()
    │
    ▼
init()
    │
    ▼
render()
    │
    ▼
update()  ←─────────── setState() / props externas
    │
    ├── render()
    │
    ▼
destroy()
    │
    ├── removeEventListeners()
    ├── destroyChildren()
    ├── removeDOM()
    └── nullReferences()
```

## 3.2 Ciclo de Vida Completo

| Fase | Método | Quando | Quantas Vezes |
|------|--------|-------|----------------|
| 1 | `constructor(opts)` | Instanciação | 1 |
| 2 | `create()` | Montar DOM | 1 |
| 3 | `init()` | Registrar eventos | 1 |
| 4 | `render()` | Atualizar DOM | N (múltiplas) |
| 5 | `update(opts)` | Atualizar props + render | N (múltiplas) |
| 6 | `destroy()` | Limpar | 1 |

## 3.3 Hooks Automáticos

```js
lifecycle: {
    beforeCreate:   'beforeCreate()',
    created:        'create()',
    beforeInit:     'beforeInit()',
    initialized:    'init()',
    beforeRender:   'beforeRender()',
    rendered:       'afterRender()',
    beforeUpdate:   'beforeUpdate()',
    updated:        'afterUpdate()',
    beforeDestroy:  'beforeDestroy()',
    destroyed:      'afterDestroy()'
}
```

---

# 4. Construtor

## 4.1 Assinatura

```js
constructor(opts = {})
```

## 4.2 Responsabilidades

1. Armazenar opções
2. Inicializar estado interno
3. Inicializar arrays de listeners e filhos
4. NÃO manipular DOM
5. NÃO registrar eventos
6. NÃO fazer chamadas assíncronas

## 4.3 Implementação Padrão

```js
class UIComponent {
    constructor(opts = {}) {
        // Identificação
        this.uid = UIComponent._uid++;
        this.name = opts.name || this.constructor.name;

        // Opções
        this.opts = { ...this.getDefaultOpts(), ...opts };

        // Estado interno
        this.state = {};

        // DOM
        this.element = null;
        this.refs = {};

        // Ciclo de vida
        this._initialized = false;
        this._destroyed = false;

        // Sub-componentes
        this.children = [];

        // Event listeners (para auto cleanup)
        this._domListeners = [];
        this._eventListeners = [];

        // Framework reference
        this.framework = window.FiscalUI || null;

        // Debug
        this._debug = this.opts.debug || false;

        if (this._debug) {
            console.log(`[${this.name}#${this.uid}] constructor`, opts);
        }
    }
}
```

## 4.4 Opções Padrão

```js
getDefaultOpts() {
    return {
        debug: false,
        visible: true,
        enabled: true,
        theme: null, // herda do Framework
        locale: null // herda do Framework
    };
}
```

---

# 5. Método create()

## 5.1 Assinatura

```js
create()
```

## 5.2 Responsabilidades

1. Criar elemento DOM principal
2. Atribuir classes CSS iniciais
3. Inserir estrutura HTML inicial
4. NÃO registrar eventos
5. NÃO manipular estado

## 5.3 Quando Chamar

Chamado manualmente após o construtor ou automaticamente pelo método `mount()`.

## 5.4 Implementação Padrão

```js
create() {
    if (this._destroyed) return;

    if (this._debug) {
        console.log(`[${this.name}#${this.uid}] create()`);
    }

    // Cria elemento a partir do template
    const html = this.template();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html.trim();
    this.element = wrapper.firstChild;

    // Se template retornar múltiplos elementos, usa wrapper
    if (!this.element) {
        this.element = wrapper;
    }

    // Aplica estado inicial de visibilidade
    if (!this.opts.visible) {
        this.element.classList.add('ui-component--hidden');
    }

    // Busca refs
    this._cacheRefs();

    return this;
}
```

## 5.5 Cache de Refs

```js
_cacheRefs() {
    this.refs = {};

    if (!this.element) return;

    // Elementos com data-ref
    this.element.querySelectorAll('[data-ref]').forEach(el => {
        this.refs[el.dataset.ref] = el;
    });

    // Elementos com id dentro do componente
    this.element.querySelectorAll('[id]').forEach(el => {
        this.refs[el.id] = el;
    });
}
```

---

# 6. Método init()

## 6.1 Assinatura

```js
init()
```

## 6.2 Responsabilidades

1. Registrar event listeners DOM
2. Registrar eventos do EventBus
3. Inicializar sub-componentes
4. NÃO manipular DOM visual (isso é render)
5. NÃO fazer chamadas assíncronas longas

## 6.3 Quando Chamar

Chamado manualmente após `create()` ou automaticamente por `mount()`.

## 6.4 Implementação Padrão

```js
init() {
    if (this._initialized || this._destroyed) return;

    if (this._debug) {
        console.log(`[${this.name}#${this.uid}] init()`);
    }

    // Registra eventos DOM
    this._bindDOMEvents();

    // Registra eventos do Framework
    this._bindFrameworkEvents();

    // Inicializa sub-componentes
    this.children.forEach(child => {
        if (!child._initialized) {
            child.init();
        }
    });

    this._initialized = true;
    this.emit('component:init', { name: this.name });

    return this;
}
```

## 6.5 Bind DOM Events

```js
_bindDOMEvents() {
    // Método a ser sobrescrito por subclasses
}
```

## 6.6 Bind Framework Events

```js
_bindFrameworkEvents() {
    // Método a ser sobrescrito por subclasses
}
```

---

# 7. Método render()

## 7.1 Assinatura

```js
render()
```

## 7.2 Responsabilidades

1. Atualizar classes CSS baseadas no estado
2. Atualizar conteúdo textual
3. Atualizar atributos (disabled, hidden, etc.)
4. NÃO recriar o elemento
5. NÃO registrar eventos
6. NÃO fazer chamadas assíncronas

## 7.3 Quando Chamar

- Chamado automaticamente por `update()`
- Chamado manualmente para forçar re-render
- Chamado por observadores de estado

## 7.4 Implementação Padrão

```js
render() {
    if (this._destroyed || !this.element) return this;

    if (this._debug) {
        console.log(`[${this.name}#${this.uid}] render()`);
    }

    // Visibilidade
    if (this.state.visible !== undefined) {
        this.element.classList.toggle(
            'ui-component--hidden',
            !this.state.visible
        );
    }

    // Estado disabled
    if (this.state.disabled !== undefined) {
        this.element.classList.toggle(
            'ui-component--disabled',
            this.state.disabled
        );
    }

    // Tema específico
    if (this.state.theme) {
        this.element.dataset.theme = this.state.theme;
    }

    this.emit('component:render', { name: this.name });

    return this;
}
```

## 7.5 Re-render Completo (Template)

Para mudanças drásticas, é possível reexecutar o template:

```js
render() {
    if (this._destroyed || !this.element) return this;

    // Salva referência do pai
    const parent = this.element.parentNode;

    // Cria novo elemento
    const html = this.template();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = html.trim();
    const newElement = wrapper.firstChild;

    // Substitui no DOM
    if (parent) {
        parent.replaceChild(newElement, this.element);
    }

    this.element = newElement;
    this._cacheRefs();

    // Re-inicializa eventos
    this._bindDOMEvents();

    return this;
}
```

---

# 8. Método update()

## 8.1 Assinatura

```js
update(opts = {})
```

## 8.2 Responsabilidades

1. Atualizar `this.opts` com novas opções (merge)
2. Atualizar `this.state` se necessário
3. Chamar `render()`
4. NÃO recriar o elemento

## 8.3 Implementação Padrão

```js
update(opts = {}) {
    if (this._destroyed) return this;

    if (this._debug) {
        console.log(`[${this.name}#${this.uid}] update()`, opts);
    }

    // Atualiza opções (merge)
    Object.assign(this.opts, opts);

    // Hook beforeUpdate
    this.beforeUpdate();

    // Re-render
    this.render();

    // Hook afterUpdate
    this.afterUpdate();

    this.emit('component:update', {
        name: this.name,
        opts
    });

    return this;
}
```

## 8.4 setState()

```js
setState(state = {}) {
    if (this._destroyed) return this;

    const prevState = { ...this.state };
    Object.assign(this.state, state);

    if (this._debug) {
        console.log(`[${this.name}#${this.uid}] setState()`, state);
    }

    this.emit('component:state-change', {
        name: this.name,
        prevState,
        nextState: { ...this.state },
        changed: Object.keys(state)
    });

    this.render();

    return this;
}

getState() {
    return { ...this.state };
}
```

---

# 9. Método destroy()

## 9.1 Assinatura

```js
destroy()
```

## 9.2 Responsabilidades

1. Remover todos os event listeners DOM
2. Remover eventos do EventBus
3. Destruir sub-componentes
4. Remover elemento do DOM
5. Anular referências para evitar memory leaks
6. Marcar como destruído

## 9.3 Implementação Padrão

```js
destroy() {
    if (this._destroyed) return;

    if (this._debug) {
        console.log(`[${this.name}#${this.uid}] destroy()`);
    }

    this.emit('component:before-destroy', { name: this.name });

    // Hook beforeDestroy
    this.beforeDestroy();

    // Remove DOM event listeners
    this._domListeners.forEach(({ el, event, handler }) => {
        el.removeEventListener(event, handler);
    });
    this._domListeners = [];

    // Remove EventBus listeners
    this._eventListeners.forEach(({ event, handler }) => {
        if (this.framework && this.framework.events) {
            this.framework.events.off(event, handler);
        }
    });
    this._eventListeners = [];

    // Destroy children
    this.children.forEach(child => {
        if (child.destroy) {
            child.destroy();
        }
    });
    this.children = [];

    // Remove do DOM
    if (this.element && this.element.parentNode) {
        this.element.parentNode.removeChild(this.element);
    }

    // Null references
    this.element = null;
    this.refs = {};
    this.opts = {};
    this.state = {};

    this._destroyed = true;
    this._initialized = false;

    // Hook afterDestroy
    this.afterDestroy();

    this.emit('component:destroyed', { name: this.name });

    return this;
}
```

## 9.4 listenTo() — Auto Cleanup

```js
listenTo(el, event, handler, options = {}) {
    el.addEventListener(event, handler, options);
    this._domListeners.push({ el, event, handler });

    // Retorna função de cleanup manual
    return () => {
        el.removeEventListener(event, handler);
        this._domListeners = this._domListeners.filter(
            l => l.handler !== handler
        );
    };
}
```

## 9.5 on() — EventBus com Auto Cleanup

```js
on(event, handler) {
    if (!this.framework || !this.framework.events) {
        console.warn(`[${this.name}] Framework not available for event: ${event}`);
        return () => {};
    }

    this.framework.events.on(event, handler);
    this._eventListeners.push({ event, handler });

    return () => {
        this.framework.events.off(event, handler);
        this._eventListeners = this._eventListeners.filter(
            l => l.handler !== handler
        );
    };
}
```

## 9.6 emit()

```js
emit(event, payload = {}) {
    if (!this.framework || !this.framework.events) return;

    this.framework.events.emit(event, {
        source: this.name,
        uid: this.uid,
        ...payload
    });
}
```

---

# 10. Método template()

## 10.1 Assinatura

```js
template()
```

## 10.2 Responsabilidades

1. Retornar string HTML que representa o componente
2. Usar dados de `this.opts` e `this.state`
3. NÃO fazer chamadas assíncronas
4. NÃO manipular DOM

## 10.3 Implementação Padrão

```js
template() {
    return '<div class="ui-component"></div>';
}
```

## 10.4 Exemplo Real

```js
// UIButton
template() {
    const { label, variant = 'primary', size = 'md', icon } = this.opts;
    const classes = [
        'ui-btn',
        `ui-btn--${variant}`,
        `ui-btn--${size}`,
        this.state.loading ? 'ui-btn--loading' : '',
        this.state.disabled ? 'ui-btn--disabled' : ''
    ].filter(Boolean).join(' ');

    const iconHtml = icon
        ? `<svg class="ui-btn__icon icon icon-sm"><use href="#${icon}"/></svg>`
        : '';

    const spinnerHtml = '<span class="ui-btn__spinner spinner" aria-hidden="true" hidden></span>';

    return `
        <button class="${classes}" type="button" ${this.state.disabled ? 'disabled' : ''}>
            ${iconHtml}
            <span class="ui-btn__label">${label}</span>
            ${spinnerHtml}
        </button>
    `;
}
```

---

# 11. Gerenciamento de Eventos

## 11.1 Eventos DOM

```js
// Exemplo em subclasse
class UIButton extends UIComponent {
    _bindDOMEvents() {
        this.listenTo(this.element, 'click', (e) => this._onClick(e));
        this.listenTo(this.element, 'mouseenter', () => this._onHover());
        this.listenTo(this.element, 'mouseleave', () => this._onLeave());
    }

    _onClick(e) {
        if (this.state.disabled || this.state.loading) return;
        this.emit('button:click', { originalEvent: e });
        if (typeof this.opts.onClick === 'function') {
            this.opts.onClick(e);
        }
    }
}
```

## 11.2 Eventos do EventBus

```js
class UIDataGrid extends UIComponent {
    _bindFrameworkEvents() {
        // Escuta eventos do Framework
        this.on('theme:change', () => this.render());
        this.on('responsive:breakpoint', (p) => this._onBreakpoint(p));
        this.on('state:change:user', (p) => this._onUserChange(p));
    }
}
```

## 11.3 Eventos Customizados

```js
// Disparar
this.emit('custom:event', { data: 'value' });

// Escutar (em outro componente)
otherComponent.on('custom:event', (payload) => {
    console.log(payload.data); // 'value'
});
```

---

# 12. Gerenciamento de Estado

## 12.1 Estado Interno

```js
class UICounter extends UIComponent {
    constructor(opts = {}) {
        super(opts);
        this.state = { count: 0 };
    }

    increment() {
        this.setState({ count: this.state.count + 1 });
    }

    decrement() {
        this.setState({ count: this.state.count - 1 });
    }

    render() {
        super.render();
        if (this.refs.countLabel) {
            this.refs.countLabel.textContent = this.state.count;
        }
    }
}
```

## 12.2 Estado Externo (StateManager)

```js
class UIUserAvatar extends UIComponent {
    init() {
        super.init();
        // Observa estado global
        this._unsubscribe = FiscalUI.state.observe('user', (user) => {
            this.setState({ name: user.name, avatar: user.avatar });
        });
    }

    render() {
        super.render();
        if (this.refs.name) {
            this.refs.name.textContent = this.state.name;
        }
    }

    destroy() {
        if (this._unsubscribe) {
            this._unsubscribe();
        }
        super.destroy();
    }
}
```

---

# 13. Sub-componentes

## 13.1 Gerenciamento de Filhos

```js
class UICard extends UIComponent {
    create() {
        super.create();

        // Cria sub-componentes
        this.header = new UICardHeader({ title: this.opts.title });
        this.body = new UICardBody({ content: this.opts.content });
        this.footer = new UICardFooter({ actions: this.opts.actions });

        // Adiciona como filhos (gerenciamento de ciclo de vida)
        this.addChild(this.header);
        this.addChild(this.body);
        this.addChild(this.footer);

        // Monta no DOM
        this.header.mount(this.refs.headerContainer);
        this.body.mount(this.refs.bodyContainer);
        this.footer.mount(this.refs.footerContainer);
    }
}
```

## 13.2 addChild() / removeChild()

```js
addChild(child) {
    if (!child || !(child instanceof UIComponent)) return;
    this.children.push(child);
    child.parent = this;
    return this;
}

removeChild(child) {
    const index = this.children.indexOf(child);
    if (index > -1) {
        this.children.splice(index, 1);
        child.parent = null;
        child.destroy();
    }
    return this;
}
```

## 13.3 mount()

```js
mount(container) {
    if (!container) return this;

    this.create();
    this.init();
    this.render();

    if (this.element) {
        container.appendChild(this.element);
    }

    this.emit('component:mounted', { name: this.name });

    return this;
}
```

---

# 14. Referências DOM

## 14.1 findByRef()

```js
// No template: <div data-ref="container">...</div>
// Acesso via: this.refs.container
```

## 14.2 find() / findAll()

```js
find(selector) {
    if (!this.element) return null;
    return this.element.querySelector(selector);
}

findAll(selector) {
    if (!this.element) return [];
    return Array.from(this.element.querySelectorAll(selector));
}
```

---

# 15. Utilitários

## 15.1 show() / hide() / toggle()

```js
show() {
    this.setState({ visible: true });
    return this;
}

hide() {
    this.setState({ visible: false });
    return this;
}

toggle() {
    this.setState({ visible: !this.state.visible });
    return this;
}
```

## 15.2 enable() / disable()

```js
enable() {
    this.setState({ disabled: false });
    return this;
}

disable() {
    this.setState({ disabled: true });
    return this;
}
```

## 15.3 Classes

```js
addClass(className) {
    if (this.element) {
        this.element.classList.add(className);
    }
    return this;
}

removeClass(className) {
    if (this.element) {
        this.element.classList.remove(className);
    }
    return this;
}

toggleClass(className) {
    if (this.element) {
        this.element.classList.toggle(className);
    }
    return this;
}

hasClass(className) {
    return this.element && this.element.classList.contains(className);
}
```

## 15.4 Attr

```js
setAttr(name, value) {
    if (this.element) {
        this.element.setAttribute(name, value);
    }
    return this;
}

getAttr(name) {
    return this.element ? this.element.getAttribute(name) : null;
}

removeAttr(name) {
    if (this.element) {
        this.element.removeAttribute(name);
    }
    return this;
}
```

---

# 16. Padrões de Implementação

## 16.1 Componente Simples

```js
class UIBadge extends UIComponent {
    getDefaultOpts() {
        return {
            ...super.getDefaultOpts(),
            text: '',
            variant: 'default', // default | success | warning | danger | info
            size: 'md'           // sm | md | lg
        };
    }

    template() {
        const { text, variant, size } = this.opts;
        return `
            <span class="ui-badge ui-badge--${variant} ui-badge--${size}">
                ${text}
            </span>
        `;
    }

    setText(text) {
        this.update({ text });
    }
}
```

## 16.2 Componente com Estado

```js
class UIToggle extends UIComponent {
    getDefaultOpts() {
        return {
            ...super.getDefaultOpts(),
            label: '',
            checked: false,
            onChange: null
        };
    }

    constructor(opts = {}) {
        super(opts);
        this.state = { checked: this.opts.checked };
    }

    template() {
        const { label } = this.opts;
        const checked = this.state.checked ? 'checked' : '';
        return `
            <label class="ui-toggle">
                <input type="checkbox" class="ui-toggle__input" ${checked}>
                <span class="ui-toggle__slider"></span>
                <span class="ui-toggle__label">${label}</span>
            </label>
        `;
    }

    _bindDOMEvents() {
        this.listenTo(this.element.querySelector('.ui-toggle__input'), 'change', (e) => {
            this.setState({ checked: e.target.checked });
            this.emit('toggle:change', { checked: e.target.checked });
            if (typeof this.opts.onChange === 'function') {
                this.opts.onChange(e.target.checked);
            }
        });
    }

    isChecked() {
        return this.state.checked;
    }

    setChecked(checked) {
        this.setState({ checked });
        if (this.refs.input) {
            this.refs.input.checked = checked;
        }
    }
}
```

## 16.3 Componente com Sub-componentes

```js
class UIModal extends UIComponent {
    getDefaultOpts() {
        return {
            ...super.getDefaultOpts(),
            title: '',
            size: 'md',
            closable: true,
            onClose: null
        };
    }

    constructor(opts = {}) {
        super(opts);
        this.state = { open: false };
    }

    template() {
        const { title, size } = this.opts;
        return `
            <div class="modal-backdrop" data-ref="backdrop">
                <div class="modal modal--${size}" role="dialog" aria-modal="true" data-ref="modal">
                    <div class="modal__header" data-ref="header">
                        <h2 class="modal__title">${title}</h2>
                        <button class="modal__close" data-ref="closeBtn" aria-label="Fechar">
                            <svg class="icon icon-md"><use href="#icon-x"/></svg>
                        </button>
                    </div>
                    <div class="modal__body" data-ref="body"></div>
                    <div class="modal__footer" data-ref="footer"></div>
                </div>
            </div>
        `;
    }

    _bindDOMEvents() {
        this.listenTo(this.refs.closeBtn, 'click', () => this.close());
        this.listenTo(this.refs.backdrop, 'click', (e) => {
            if (e.target === this.refs.backdrop) this.close();
        });
        this.listenTo(document, 'keydown', (e) => {
            if (e.key === 'Escape' && this.state.open) this.close();
        });
    }

    open() {
        this.setState({ open: true });
        document.body.appendChild(this.element);
        this._initialized = false;
        this.init();
        this.emit('modal:open', { name: this.opts.title });
    }

    close() {
        this.setState({ open: false });
        this.destroy();
        this.emit('modal:close', { name: this.opts.title });
        if (typeof this.opts.onClose === 'function') {
            this.opts.onClose();
        }
    }

    setBody(content) {
        if (this.refs.body) {
            if (typeof content === 'string') {
                this.refs.body.innerHTML = content;
            } else if (content instanceof UIComponent) {
                content.mount(this.refs.body);
                this.addChild(content);
            } else if (content instanceof HTMLElement) {
                this.refs.body.appendChild(content);
            }
        }
    }
}
```

## 16.4 Componente Assíncrono

```js
class UIAsyncContent extends UIComponent {
    getDefaultOpts() {
        return {
            ...super.getDefaultOpts(),
            loader: null, // função que retorna Promise
            loadingText: 'Carregando...',
            errorText: 'Erro ao carregar'
        };
    }

    constructor(opts = {}) {
        super(opts);
        this.state = {
            loading: false,
            error: null,
            data: null
        };
    }

    template() {
        if (this.state.loading) {
            return `<div class="async-loading"><span class="spinner"></span> ${this.opts.loadingText}</div>`;
        }
        if (this.state.error) {
            return `<div class="async-error">${this.opts.errorText}: ${this.state.error}</div>`;
        }
        if (this.state.data) {
            return `<div class="async-content" data-ref="content"></div>`;
        }
        return `<div class="async-empty">${this.opts.loadingText}</div>`;
    }

    async load() {
        if (!this.opts.loader) return;
        this.setState({ loading: true, error: null });
        try {
            const data = await this.opts.loader();
            this.setState({ loading: false, data });
        } catch (err) {
            this.setState({ loading: false, error: err.message });
        }
    }

    afterRender() {
        if (this.state.data && this.refs.content && this.opts.renderContent) {
            this.opts.renderContent(this.refs.content, this.state.data);
        }
    }
}
```

---

# 17. Decorators

## 17.1 Uso de Decorators (Opcional)

```js
// @log
function log(target, key, descriptor) {
    const original = descriptor.value;
    descriptor.value = function(...args) {
        console.log(`[${this.name}] ${key}()`, args);
        return original.apply(this, args);
    };
    return descriptor;
}

class UIButton extends UIComponent {
    @log
    setLabel(label) {
        this.update({ label });
    }
}
```

---

# 18. Mixins

## 18.1 Exemplo de Mixin

```js
// Mixin de validação
const Validatable = (superclass) => class extends superclass {
    validate() {
        return true;
    }

    getErrors() {
        return [];
    }

    showErrors() {
        // implementação
    }

    clearErrors() {
        // implementação
    }
};

// Uso
class UIFormField extends Validatable(UIComponent) {
    // Agora tem métodos validate(), getErrors(), etc.
}
```

---

# 19. Herança

## 19.1 Exemplo de Herança

```js
class UIButton extends UIComponent {
    getDefaultOpts() {
        return {
            ...super.getDefaultOpts(),
            label: 'Button',
            variant: 'primary',
            size: 'md',
            icon: null,
            onClick: null
        };
    }

    template() {
        const { label, variant, size, icon } = this.opts;
        const loading = this.state.loading ? 'ui-btn--loading' : '';
        const disabled = this.state.disabled ? 'disabled' : '';

        return `
            <button class="ui-btn ui-btn--${variant} ui-btn--${size} ${loading}" ${disabled}>
                ${icon ? `<svg class="ui-btn__icon icon icon-sm"><use href="#${icon}"/></svg>` : ''}
                <span class="ui-btn__label">${label}</span>
                <span class="ui-btn__spinner spinner" aria-hidden="true" hidden></span>
            </button>
        `;
    }

    _bindDOMEvents() {
        this.listenTo(this.element, 'click', (e) => this._onClick(e));
    }

    _onClick(e) {
        if (this.state.loading || this.state.disabled) return;
        this.emit('button:click', { variant: this.opts.variant });
        if (typeof this.opts.onClick === 'function') {
            this.opts.onClick(e);
        }
    }

    setLoading(loading) {
        this.setState({ loading });
    }
}

class UIIconButton extends UIButton {
    getDefaultOpts() {
        return {
            ...super.getDefaultOpts(),
            label: '',
            icon: 'icon-star',
            ariaLabel: 'Botão'
        };
    }

    template() {
        const { icon, size, ariaLabel } = this.opts;

        return `
            <button class="ui-btn ui-btn--icon ui-btn--${size}"
                    aria-label="${ariaLabel}"
                    ${this.state.disabled ? 'disabled' : ''}>
                <svg class="ui-btn__icon icon icon-md"><use href="#${icon}"/></svg>
            </button>
        `;
    }
}
```

---

# 20. Composição vs Herança

## 20.1 Prefira Composição

```js
// ❌ Herança excessiva
class UIDangerButton extends UIButton { /* ... */ }
class UIPrimaryButton extends UIButton { /* ... */ }
class UILargeButton extends UIButton { /* ... */ }

// ✅ Composição (via opts)
const btn = new UIButton({ variant: 'danger', size: 'lg' });
```

## 20.2 Composição de Componentes

```js
class UIForm extends UIComponent {
    create() {
        super.create();
        this.fields = this.opts.fields.map(field => {
            return new UIFormField(field);
        });
        this.fields.forEach(f => {
            f.mount(this.refs.formBody);
            this.addChild(f);
        });
    }
}
```

---

# 21. Observabilidade

## 21.1 Observer Pattern

```js
class UIComponent {
    constructor() {
        this._observers = [];
    }

    observe(callback) {
        this._observers.push(callback);
        return () => {
            this._observers = this._observers.filter(cb => cb !== callback);
        };
    }

    _notify(event, data) {
        this._observers.forEach(cb => {
            try {
                cb(event, data);
            } catch (e) {
                console.error(`[${this.name}] Observer error:`, e);
            }
        });
    }
}
```

---

# 22. Performance

## 22.1 Regras de Performance

```
1. NUNCA criar elementos DOM dentro de render() — usar template()
2. SEMPRE usar refs em vez de querySelector em render()
3. NUNCA registrar eventos em render() — fazer em init()
4. SEMPRE remover listeners em destroy()
5. NUNCA manter referências após destroy()
6. USAR requestAnimationFrame para animações
7. USAR debounce para eventos de alto volume
```

## 22.2 Batch Updates

```js
class UIDataGrid extends UIComponent {
    constructor() {
        super();
        this._batch = [];
        this._rafId = null;
    }

    addRows(rows) {
        this._batch.push(...rows);
        this._scheduleRender();
    }

    _scheduleRender() {
        if (this._rafId) return;
        this._rafId = requestAnimationFrame(() => {
            this.render();
            this._batch = [];
            this._rafId = null;
        });
    }
}
```

---

# 23. Memória e Vazamentos

## 23.1 Causas Comuns de Memory Leak

```
❌ Não remover event listeners do DOM
❌ Não remover observers do StateManager
❌ Manter referências circulares
❌ Sub-componentes não destruídos
❌ Timers não limpos (setInterval, setTimeout)
❌ Promises não canceladas
```

## 23.2 Prevenção

```js
class UIComponent {
    destroy() {
        // Limpa timers
        if (this._timer) {
            clearInterval(this._timer);
            this._timer = null;
        }

        // Limpa observers
        if (this._unsubscribe) {
            this._unsubscribe();
            this._unsubscribe = null;
        }

        // Remove listeners (automático via super)
        super.destroy();
    }
}
```

---

# 24. Testabilidade

## 24.1 Teste Unitário

```js
describe('UIButton', () => {
    let btn;

    beforeEach(() => {
        btn = new UIButton({ label: 'Salvar' });
        btn.create();
    });

    afterEach(() => {
        btn.destroy();
    });

    it('should render with correct label', () => {
        expect(btn.find('.ui-btn__label').textContent).toBe('Salvar');
    });

    it('should emit click event when clicked', () => {
        const spy = jasmine.createSpy();
        btn.on('button:click', spy);
        btn.find('.ui-btn').click();
        expect(spy).toHaveBeenCalled();
    });

    it('should not emit click when disabled', () => {
        const spy = jasmine.createSpy();
        btn.setDisabled(true);
        btn.on('button:click', spy);
        btn.find('.ui-btn').click();
        expect(spy).not.toHaveBeenCalled();
    });
});
```

---

# 25. Boas Práticas

## 25.1 Regras de Ouro

```
1. SEMPRE chamar super.create(), super.init(), super.render(), super.destroy()
2. NUNCA estender mais de 2 níveis de herança
3. SEMPRE usar opts para configurar o componente
4. NUNCA modificar opts após a criação
5. SEMPRE usar setState() para mudanças de estado
6. NUNCA manipular DOM de outros componentes
7. SEMPRE destruir sub-componentes no destroy()
8. NUNCA esquecer de chamar super.destroy()
9. SEMPRE usar listenTo() em vez de addEventListener()
10. NUNCA criar métodos com mais de 20 linhas
```

## 25.2 Checklist de Componente

```
☐ Extende UIComponent
☐ Implementa getDefaultOpts()
☐ Implementa template()
☐ Implementa _bindDOMEvents()
☐ Implementa _bindFrameworkEvents() (se necessário)
☐ Chama super.create()
☐ Chama super.init()
☐ Chama super.render()
☐ Chama super.destroy()
☐ Usa setState() para estado interno
☐ Usa emit() para comunicação
☐ Usa listenTo() para eventos DOM
☐ Usa on() para eventos do Framework
☐ Remove listeners no destroy()
☐ Destroi sub-componentes no destroy()
☐ Testes unitários escritos
```

---

# 26. API Completa

## 26.1 Resumo de Métodos

| Método | Retorno | Descrição |
|--------|---------|-----------|
| `constructor(opts)` | `UIComponent` | Instancia o componente |
| `create()` | `UIComponent` | Cria o elemento DOM |
| `init()` | `UIComponent` | Registra eventos |
| `render()` | `UIComponent` | Atualiza DOM |
| `update(opts)` | `UIComponent` | Atualiza props + render |
| `destroy()` | `UIComponent` | Remove tudo |
| `template()` | `string` | Retorna HTML |
| `setState(state)` | `UIComponent` | Atualiza estado interno |
| `getState()` | `object` | Retorna estado atual |
| `mount(container)` | `UIComponent` | Monta no DOM |
| `show()` | `UIComponent` | Torna visível |
| `hide()` | `UIComponent` | Torna invisível |
| `toggle()` | `UIComponent` | Alterna visibilidade |
| `enable()` | `UIComponent` | Habilita |
| `disable()` | `UIComponent` | Desabilita |
| `addChild(child)` | `UIComponent` | Adiciona sub-componente |
| `removeChild(child)` | `UIComponent` | Remove sub-componente |
| `on(event, handler)` | `function` | Escuta evento do Framework |
| `emit(event, payload)` | `void` | Dispara evento |
| `listenTo(el, event, fn)` | `function` | Escuta evento DOM |
| `find(selector)` | `Element` | Query selector no componente |
| `findAll(selector)` | `Element[]` | Query selector all |
| `addClass(name)` | `UIComponent` | Adiciona classe CSS |
| `removeClass(name)` | `UIComponent` | Remove classe CSS |
| `toggleClass(name)` | `UIComponent` | Alterna classe CSS |
| `hasClass(name)` | `boolean` | Verifica classe CSS |
| `setAttr(name, val)` | `UIComponent` | Define atributo |
| `getAttr(name)` | `string` | Retorna atributo |
| `removeAttr(name)` | `UIComponent` | Remove atributo |

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Component Base completo |
