# FiscalUI Framework

## Documento 049 — Drawer

**Nível 3 — Navegação**

**Versão 1.0**

Painel deslizante lateral (direita ou esquerda). Usado para detalhes, configurações ou navegação complementar.

---

```js
class UIDrawer extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.placement = options.placement || 'right';  // left, right
        this.width = options.width || 360;
        this.title = options.title || '';
        this.body = options.body || '';
        this.footer = options.footer || '';
        this.backdrop = options.backdrop !== false;
        this._open = false;
    }

    template() {
        return `
            <div class="ui-drawer__backdrop" hidden></div>
            <aside class="ui-drawer ui-drawer--${this.placement}" style="width: ${this.width}px" hidden role="dialog" aria-modal="true">
                <div class="ui-drawer__header">
                    <span class="ui-drawer__title">${this.title}</span>
                    <button class="ui-drawer__close" aria-label="Fechar">&times;</button>
                </div>
                <div class="ui-drawer__body">${this.body}</div>
                <div class="ui-drawer__footer" ${this.footer ? '' : 'hidden'}>${this.footer}</div>
            </aside>
        `;
    }

    onInit() {
        this._backdrop = this.query('.ui-drawer__backdrop');
        this._drawer = this.query('.ui-drawer');
        this._drawer.querySelector('.ui-drawer__close').addEventListener('click', () => this.close());
        if (this.backdrop) {
            this._backdrop.addEventListener('click', () => this.close());
        }
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this._open) this.close();
        });
    }

    open() {
        this._open = true;
        this._drawer.hidden = false;
        if (this.backdrop) this._backdrop.hidden = false;
        requestAnimationFrame(() => {
            this._drawer.classList.add('ui-drawer--open');
            if (this.backdrop) this._backdrop.classList.add('ui-drawer__backdrop--visible');
        });
        this.emit('drawer:open');
    }

    close() {
        this._drawer.classList.remove('ui-drawer--open');
        if (this.backdrop) this._backdrop.classList.remove('ui-drawer__backdrop--visible');
        setTimeout(() => {
            this._open = false;
            this._drawer.hidden = true;
            if (this.backdrop) this._backdrop.hidden = true;
        }, 300);
        this.emit('drawer:close');
    }

    setBody(html) { this._drawer.querySelector('.ui-drawer__body').innerHTML = html; }
}
```

```css
.ui-drawer__backdrop {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.4);
    z-index: calc(var(--z-drawer) - 1);
    transition: opacity var(--motion-normal) var(--ease-out);
    opacity: 0;
}
.ui-drawer__backdrop--visible { opacity: 1; }

.ui-drawer {
    position: fixed; top: 0; bottom: 0;
    z-index: var(--z-drawer);
    background: var(--color-surface);
    box-shadow: var(--shadow-xl);
    display: flex; flex-direction: column;
    transition: transform var(--motion-normal) var(--ease-out);
}

.ui-drawer--right { right: 0; transform: translateX(100%); }
.ui-drawer--left  { left: 0; transform: translateX(-100%); }
.ui-drawer--open { transform: translateX(0); }

.ui-drawer__header {
    display: flex; align-items: center; justify-content: space-between;
    padding: var(--spacing-md); border-bottom: 1px solid var(--color-border);
}
.ui-drawer__title { font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.ui-drawer__close { border: none; background: transparent; cursor: pointer; font-size: 22px; color: var(--color-text-muted); line-height: 1; }

.ui-drawer__body { flex: 1; overflow-y: auto; padding: var(--spacing-md); }
.ui-drawer__footer { padding: var(--spacing-md); border-top: 1px solid var(--color-border); display: flex; justify-content: flex-end; gap: var(--spacing-sm); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
