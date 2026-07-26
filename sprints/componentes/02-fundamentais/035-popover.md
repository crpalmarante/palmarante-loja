# FiscalUI Framework

## Documento 035 — Popover

**Nível 2 — Basic Components**

**Versão 1.0**

Card flutuante com conteúdo rico. Diferente do Tooltip (texto simples), o Popover suporte HTML, formulários e ações.

---

```js
class UIPopover extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.content = options.content || '';
        this.position = options.position || 'bottom';
        this.width = options.width || 260;
        this.trigger = options.trigger || 'click';     // click, hover
        this._open = false;
    }

    template() {
        return `
            <div class="ui-popover">
                <div class="ui-popover__trigger"></div>
                <div class="ui-popover__content" hidden style="width: ${this.width}px">
                    <div class="ui-popover__body">${this.content}</div>
                </div>
            </div>
        `;
    }

    onInit() {
        this._trigger = this.query('.ui-popover__trigger');
        this._content = this.query('.ui-popover__content');

        if (this.trigger === 'click') {
            this._trigger.addEventListener('click', () => this.toggle());
            document.addEventListener('click', (e) => {
                if (this._open && !this.element.contains(e.target)) this.close();
            });
        } else {
            this._trigger.addEventListener('mouseenter', () => this.open());
            this.element.addEventListener('mouseleave', () => this.close());
        }
    }

    open() { this._open = true; this._content.hidden = false; this._position(); }
    close() { this._open = false; this._content.hidden = true; }
    toggle() { this._open ? this.close() : this.open(); }

    _position() {
        const triggerRect = this._trigger.getBoundingClientRect();
        const contentRect = this._content.getBoundingClientRect();
        const gap = 4;

        const positions = {
            top:    { top: triggerRect.top - contentRect.height - gap, left: triggerRect.left },
            bottom: { top: triggerRect.bottom + gap, left: triggerRect.left },
            left:   { top: triggerRect.top, left: triggerRect.left - contentRect.width - gap },
            right:  { top: triggerRect.top, left: triggerRect.right + gap }
        };

        const pos = positions[this.position] || positions.bottom;
        this._content.style.top = `${pos.top}px`;
        this._content.style.left = `${pos.left}px`;
    }
}
```

```css
.ui-popover { position: relative; display: inline-block; }

.ui-popover__content {
    position: fixed;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    z-index: var(--z-popover);
    padding: var(--spacing-sm);
    animation: ui-fade-in var(--motion-fast) var(--ease-out);
}
```

```js
new UIPopover({
    trigger: btn.element,
    content: '<p>Tem certeza que deseja excluir?</p><button class="ui-btn ui-btn--danger">Confirmar</button>',
    position: 'top'
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
