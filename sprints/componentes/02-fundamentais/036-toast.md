# FiscalUI Framework

## Documento 036 — Toast

**Nível 2 — Basic Components**

**Versão 1.0**

Notificação temporária no canto da tela. Feedback de ações (sucesso, erro, aviso).

---

```js
class ToastService {
    constructor() {
        this._container = document.createElement('div');
        this._container.className = 'ui-toast-container';
        document.body.appendChild(this._container);
    }

    show(options = {}) {
        const toast = document.createElement('div');
        const variant = options.variant || 'info';    // info, success, warning, danger
        toast.className = `ui-toast ui-toast--${variant}`;
        toast.innerHTML = `
            <div class="ui-toast__icon">${this._icon(variant)}</div>
            <div class="ui-toast__body">
                <div class="ui-toast__title">${options.title || ''}</div>
                <div class="ui-toast__message">${options.message || ''}</div>
            </div>
            <button class="ui-toast__close" aria-label="Fechar">&times;</button>
        `;

        toast.querySelector('.ui-toast__close').addEventListener('click', () => this._remove(toast));
        this._container.appendChild(toast);

        if (options.duration !== 0) {
            setTimeout(() => this._remove(toast), options.duration || 4000);
        }

        return toast;
    }

    success(title, message) { return this.show({ variant: 'success', title, message }); }
    error(title, message) { return this.show({ variant: 'danger', title, message }); }
    warning(title, message) { return this.show({ variant: 'warning', title, message }); }
    info(title, message) { return this.show({ variant: 'info', title, message }); }

    _remove(toast) {
        toast.classList.add('ui-toast--exiting');
        setTimeout(() => toast.remove(), 300);
    }

    _icon(variant) {
        const icons = { success: 'check', danger: 'alert', warning: 'alert', info: 'info' };
        return FiscalUI.icons.render(icons[variant] || 'info', { size: 20 });
    }
}

const toast = new ToastService();
toast.success('Salvo!', 'Documento salvo com sucesso.');
toast.error('Erro!', 'Não foi possível salvar. Tente novamente.');
```

```css
.ui-toast-container {
    position: fixed;
    top: var(--spacing-xl);
    right: var(--spacing-xl);
    z-index: var(--z-toast);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    max-width: 400px;
}

.ui-toast {
    display: flex;
    align-items: flex-start;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    background: var(--color-surface);
    border-left: 4px solid;
    animation: ui-toast-in 0.3s var(--ease-out);
}

.ui-toast--exiting { animation: ui-toast-out 0.3s var(--ease-in); opacity: 0; transform: translateX(100%); }

.ui-toast--success { border-color: var(--color-success); }
.ui-toast--danger  { border-color: var(--color-danger); }
.ui-toast--warning { border-color: var(--color-warning); }
.ui-toast--info    { border-color: var(--color-primary); }

.ui-toast__icon { flex-shrink: 0; color: var(--color-text-secondary); }
.ui-toast__body { flex: 1; }
.ui-toast__title { font-weight: var(--font-weight-semibold); margin-bottom: 2px; }
.ui-toast__message { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
.ui-toast__close { border: none; background: transparent; cursor: pointer; font-size: 18px; color: var(--color-text-muted); line-height: 1; }

@keyframes ui-toast-in {
    from { opacity: 0; transform: translateX(100%); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes ui-toast-out {
    to { opacity: 0; transform: translateX(100%); }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
