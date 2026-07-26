# FiscalUI Framework

## Documento 034 — Tooltip

**Nível 2 — Basic Components**

**Versão 1.0**

Texto de ajuda exibido ao passar o mouse ou focar um elemento. Posicionamento automático com fallback.

---

```js
class UITooltip extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.content = options.content || '';
        this.position = options.position || 'top';       // top, bottom, left, right
        this.delay = options.delay || 300;
        this._timer = null;
    }

    init() {
        this._tooltip = document.createElement('div');
        this._tooltip.className = `ui-tooltip ui-tooltip--${this.position}`;
        this._tooltip.textContent = this.content;
        this._tooltip.hidden = true;
        document.body.appendChild(this._tooltip);

        this._target = this.element;
        this._target.addEventListener('mouseenter', () => this._show());
        this._target.addEventListener('mouseleave', () => this._hide());
        this._target.addEventListener('focus', () => this._show());
        this._target.addEventListener('blur', () => this._hide());
    }

    _show() {
        clearTimeout(this._timer);
        this._timer = setTimeout(() => {
            this._position();
            this._tooltip.hidden = false;
        }, this.delay);
    }

    _hide() {
        clearTimeout(this._timer);
        this._tooltip.hidden = true;
    }

    _position() {
        const targetRect = this._target.getBoundingClientRect();
        const tipRect = this._tooltip.getBoundingClientRect();
        const gap = 8;

        const positions = {
            top:    { top: targetRect.top - tipRect.height - gap, left: targetRect.left + (targetRect.width - tipRect.width) / 2 },
            bottom: { top: targetRect.bottom + gap, left: targetRect.left + (targetRect.width - tipRect.width) / 2 },
            left:   { top: targetRect.top + (targetRect.height - tipRect.height) / 2, left: targetRect.left - tipRect.width - gap },
            right:  { top: targetRect.top + (targetRect.height - tipRect.height) / 2, left: targetRect.right + gap }
        };

        const pos = positions[this.position];
        this._tooltip.style.top = `${pos.top}px`;
        this._tooltip.style.left = `${pos.left}px`;
    }

    destroy() {
        clearTimeout(this._timer);
        this._tooltip?.remove();
        super.destroy();
    }
}
```

```css
.ui-tooltip {
    position: fixed;
    padding: var(--spacing-xs) var(--spacing-sm);
    background: var(--color-text);
    color: var(--color-bg);
    font-size: var(--font-size-sm);
    border-radius: var(--radius-sm);
    white-space: nowrap;
    z-index: var(--z-tooltip);
    pointer-events: none;
    animation: ui-fade-in var(--motion-fast) var(--ease-out);
}

@keyframes ui-fade-in {
    from { opacity: 0; transform: translateY(2px); }
    to { opacity: 1; transform: translateY(0); }
}
```

```html
<!-- Uso declarativo -->
<button class="ui-btn" data-tooltip="Clique para salvar">Salvar</button>

<!-- Uso via JS -->
const tip = new UITooltip({ target: btn.element, content: 'Salvar documento', position: 'top' });
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
