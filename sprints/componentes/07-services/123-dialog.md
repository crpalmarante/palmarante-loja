# FiscalUI Framework

## Documento 123 — Dialog

**Nível 7 — Services**

**Versão 1.0**

Serviço de diálogos modais programáticos: alerta, confirmação, prompt e diálogo customizado.

---

```js
class DialogService {
    constructor() {
        this._container = null;
        this._init();
    }

    _init() {
        this._container = document.createElement('div');
        this._container.className = 'ui-dialog-service';
        document.body.appendChild(this._container);
    }

    alert(options) {
        return this._show({
            type: 'alert',
            title: options.title || 'Aviso',
            message: options.message || '',
            icon: options.icon || 'alert-circle',
            confirmText: options.confirmText || 'OK',
            ...options
        });
    }

    confirm(options) {
        return this._show({
            type: 'confirm',
            title: options.title || 'Confirmação',
            message: options.message || '',
            icon: options.icon || 'help-circle',
            confirmText: options.confirmText || 'Confirmar',
            cancelText: options.cancelText || 'Cancelar',
            variant: options.variant || 'primary',
            ...options
        });
    }

    prompt(options) {
        return this._show({
            type: 'prompt',
            title: options.title || 'Informe',
            message: options.message || '',
            icon: options.icon || 'edit',
            confirmText: options.confirmText || 'OK',
            cancelText: options.cancelText || 'Cancelar',
            defaultValue: options.defaultValue || '',
            placeholder: options.placeholder || '',
            ...options
        });
    }

    custom(options) {
        return this._show({ type: 'custom', ...options });
    }

    async _show(options) {
        return new Promise((resolve) => {
            const backdrop = document.createElement('div');
            backdrop.className = 'ui-dialog-backdrop';

            const dialog = document.createElement('div');
            dialog.className = 'ui-dialog';
            dialog.innerHTML = `
                <div class="ui-dialog__header">
                    <h3 class="ui-dialog__title">${options.title || ''}</h3>
                    <button class="ui-dialog__close">&times;</button>
                </div>
                <div class="ui-dialog__body">
                    ${options.message ? `<p class="ui-dialog__message">${options.message}</p>` : ''}
                    ${options.type === 'prompt' ? `<input class="ui-field__input" value="${options.defaultValue || ''}" placeholder="${options.placeholder || ''}" style="width:100%">` : ''}
                    ${options.content || ''}
                </div>
                <div class="ui-dialog__footer">
                    ${options.type !== 'alert' ? `<button class="ui-btn ui-btn--ghost" data-action="cancel">${options.cancelText || 'Cancelar'}</button>` : ''}
                    <button class="ui-btn ui-btn--${options.variant || 'primary'}" data-action="confirm">${options.confirmText || 'OK'}</button>
                </div>
            `;

            this._container.appendChild(backdrop);
            this._container.appendChild(dialog);
            requestAnimationFrame(() => { backdrop.classList.add('ui-dialog-backdrop--visible'); dialog.classList.add('ui-dialog--visible'); });

            const input = dialog.querySelector('input');
            if (input) setTimeout(() => input.focus(), 100);

            const close = () => {
                backdrop.classList.remove('ui-dialog-backdrop--visible');
                dialog.classList.remove('ui-dialog--visible');
                setTimeout(() => { backdrop.remove(); dialog.remove(); }, 300);
            };

            dialog.querySelector('.ui-dialog__close').addEventListener('click', () => { close(); resolve(null); });
            backdrop.addEventListener('click', () => { if (options.backdropClose !== false) { close(); resolve(null); } });
            dialog.querySelector('[data-action="cancel"]')?.addEventListener('click', () => { close(); resolve(false); });
            dialog.querySelector('[data-action="confirm"]').addEventListener('click', () => {
                close();
                if (options.type === 'prompt') resolve(input?.value || '');
                else resolve(true);
            });
        });
    }
}
```

```css
.ui-dialog-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: calc(var(--z-modal) - 1); opacity: 0; transition: opacity 0.3s ease; }
.ui-dialog-backdrop--visible { opacity: 1; }

.ui-dialog { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.95); z-index: var(--z-modal); background: var(--color-surface); border-radius: var(--radius-lg); box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 420px; max-width: 90vw; opacity: 0; transition: opacity 0.3s ease, transform 0.3s ease; }
.ui-dialog--visible { opacity: 1; transform: translate(-50%, -50%) scale(1); }

.ui-dialog__header { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-dialog__title { font-size: var(--font-size-lg); margin: 0; font-weight: var(--font-weight-semibold); }
.ui-dialog__close { border: none; background: transparent; cursor: pointer; font-size: 22px; color: var(--color-text-muted); line-height: 1; }

.ui-dialog__body { padding: var(--spacing-md); }
.ui-dialog__message { margin: 0; font-size: var(--font-size-md); color: var(--color-text-secondary); line-height: 1.6; }

.ui-dialog__footer { display: flex; justify-content: flex-end; gap: var(--spacing-sm); padding: var(--spacing-md); border-top: 1px solid var(--color-border); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
