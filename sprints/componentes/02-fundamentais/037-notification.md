# FiscalUI Framework

## Documento 037 — Notification

**Nível 2 — Basic Components**

**Versão 1.0**

Notificação persistente com ações. Diferente do Toast (temporário), a Notification fica até ser dispensada, agrupada em um centro de notificações.

---

```js
class UINotification extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.title = options.title || '';
        this.message = options.message || '';
        this.variant = options.variant || 'info';
        this.icon = options.icon || null;
        this.time = options.time || new Date();
        this.actions = options.actions || [];        // { label, onClick }
        this.read = options.read || false;
        this.onDismiss = options.onDismiss || null;
    }

    template() {
        return `
            <div class="ui-notification ui-notification--${this.variant} ${this.read ? 'ui-notification--read' : ''}">
                <div class="ui-notification__icon">${this.icon ? FiscalUI.icons.render(this.icon, { size: 20 }) : ''}</div>
                <div class="ui-notification__body">
                    <div class="ui-notification__title">${this.title}</div>
                    <div class="ui-notification__message">${this.message}</div>
                    <div class="ui-notification__time">${this._formatTime(this.time)}</div>
                    ${this.actions.length ? `<div class="ui-notification__actions">
                        ${this.actions.map(a => `<button class="ui-btn ui-btn--ghost ui-btn--sm">${a.label}</button>`).join('')}
                    </div>` : ''}
                </div>
                <button class="ui-notification__dismiss" aria-label="Dispensar">&times;</button>
            </div>
        `;
    }

    onInit() {
        this.query('.ui-notification__dismiss').addEventListener('click', () => {
            this.emit('notification:dismiss');
            this.onDismiss?.();
            this.destroy();
        });
        this.queryAll('.ui-notification__actions .ui-btn').forEach((btn, i) => {
            btn.addEventListener('click', () => this.actions[i]?.onClick?.());
        });
    }

    _formatTime(date) {
        const d = date instanceof Date ? date : new Date(date);
        const now = new Date();
        const diff = now - d;
        if (diff < 60000) return 'Agora';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} min`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`;
        return d.toLocaleDateString('pt-BR');
    }
}

// Notification Center (gerencia lista)
class NotificationCenter {
    constructor() {
        this._container = document.createElement('div');
        this._container.className = 'ui-notification-center';
        this._notifications = [];
        document.body.appendChild(this._container);
    }

    add(options) {
        const notif = new UINotification(options);
        notif.render();
        this._container.prepend(notif.element);
        this._notifications.push(notif);
        return notif;
    }

    clear() { this._notifications.forEach(n => n.destroy()); this._notifications = []; }
    count() { return this._notifications.filter(n => !n.read).length; }
}
```

```css
.ui-notification-center {
    position: fixed;
    top: var(--spacing-xl);
    right: var(--spacing-xl);
    z-index: var(--z-notification);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    width: 360px;
    max-height: 80vh;
    overflow-y: auto;
}

.ui-notification {
    display: flex;
    gap: var(--spacing-sm);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-md);
}

.ui-notification--read { opacity: 0.6; }
.ui-notification__body { flex: 1; }
.ui-notification__title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.ui-notification__message { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin-top: 2px; }
.ui-notification__time { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-top: 4px; }
.ui-notification__actions { display: flex; gap: var(--spacing-xs); margin-top: var(--spacing-sm); }
.ui-notification__dismiss { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); font-size: 18px; line-height: 1; align-self: flex-start; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
