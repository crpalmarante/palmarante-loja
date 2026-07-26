# FiscalUI Framework

## Documento 122 — Notifications

**Nível 7 — Services**

**Versão 1.0**

Serviço central de notificações (toast, alerta, banner). Gerencia fila, prioridade e agrupamento.

---

```js
class NotificationService {
    constructor(options = {}) {
        this.maxVisible = options.maxVisible || 5;
        this.container = options.container || document.body;
        this._queue = [];
        this._visible = [];
        this._containerEl = null;
    }

    init() {
        this._containerEl = document.createElement('div');
        this._containerEl.className = 'ui-notification-service';
        this.container.appendChild(this._containerEl);
    }

    show(options) {
        const notification = {
            id: Date.now() + Math.random(),
            type: options.type || 'info',        // info, success, warning, error
            title: options.title || '',
            message: options.message || '',
            duration: options.duration ?? 4000,
            action: options.action || null,       // { label, onClick }
            persistent: options.persistent || false,
            onClose: options.onClose || null
        };

        if (this._visible.length >= this.maxVisible) {
            this._queue.push(notification);
        } else {
            this._render(notification);
        }
        return notification;
    }

    success(title, message) { return this.show({ type: 'success', title, message }); }
    error(title, message) { return this.show({ type: 'error', title, message, duration: 0, persistent: true }); }
    warning(title, message) { return this.show({ type: 'warning', title, message }); }
    info(title, message) { return this.show({ type: 'info', title, message }); }

    _render(notification) {
        const el = document.createElement('div');
        el.className = `ui-notification-item ui-notification-item--${notification.type}`;
        el.dataset.id = notification.id;
        el.innerHTML = `
            <div class="ui-notification-item__icon"></div>
            <div class="ui-notification-item__body">
                <div class="ui-notification-item__title">${notification.title}</div>
                ${notification.message ? `<div class="ui-notification-item__message">${notification.message}</div>` : ''}
            </div>
            <div class="ui-notification-item__actions">
                ${notification.action ? `<button class="ui-btn ui-btn--ghost ui-btn--sm">${notification.action.label}</button>` : ''}
                <button class="ui-notification-item__close">&times;</button>
            </div>
        `;

        el.querySelector('.ui-notification-item__close').addEventListener('click', () => this._dismiss(notification.id));
        if (notification.action) {
            el.querySelector('.ui-notification-item__actions .ui-btn').addEventListener('click', () => {
                notification.action.onClick?.();
                if (!notification.persistent) this._dismiss(notification.id);
            });
        }

        this._containerEl.appendChild(el);
        this._visible.push(notification);

        if (notification.duration > 0 && !notification.persistent) {
            setTimeout(() => this._dismiss(notification.id), notification.duration);
        }

        requestAnimationFrame(() => el.classList.add('ui-notification-item--visible'));
    }

    _dismiss(id) {
        const idx = this._visible.findIndex(n => n.id === id);
        if (idx === -1) return;
        const notification = this._visible[idx];
        const el = this._containerEl.querySelector(`[data-id="${id}"]`);
        if (el) {
            el.classList.remove('ui-notification-item--visible');
            el.addEventListener('transitionend', () => el.remove());
        }
        this._visible.splice(idx, 1);
        notification.onClose?.();
        if (this._queue.length) this._render(this._queue.shift());
    }

    clear() {
        this._visible.forEach(n => this._dismiss(n.id));
        this._queue = [];
    }
}
```

```css
.ui-notification-service { position: fixed; top: var(--spacing-xl); right: var(--spacing-xl); z-index: var(--z-toast); display: flex; flex-direction: column; gap: var(--spacing-sm); max-width: 400px; }

.ui-notification-item { display: flex; gap: var(--spacing-sm); padding: var(--spacing-md); border-radius: var(--radius-md); box-shadow: var(--shadow-lg); background: var(--color-surface); border-left: 4px solid; transform: translateX(120%); opacity: 0; transition: transform 0.3s ease, opacity 0.3s ease; }
.ui-notification-item--visible { transform: translateX(0); opacity: 1; }
.ui-notification-item--info { border-left-color: var(--color-primary); }
.ui-notification-item--success { border-left-color: var(--color-success); }
.ui-notification-item--warning { border-left-color: var(--color-warning); }
.ui-notification-item--error { border-left-color: var(--color-danger); }

.ui-notification-item__body { flex: 1; }
.ui-notification-item__title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.ui-notification-item__message { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin-top: 2px; }
.ui-notification-item__actions { display: flex; align-items: flex-start; gap: var(--spacing-xs); }
.ui-notification-item__close { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); font-size: 18px; line-height: 1; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
