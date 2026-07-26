# FiscalUI Framework

## Documento 054 — Quick Launcher

**Nível 3 — Navegação**

**Versão 1.0**

Lançador rápido de módulos/features. Similar à paleta de comandos, mas focado em abrir telas/navegação em vez de comandos arbitrários.

---

```js
class UIQuickLauncher extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.items = options.items || [];       // { id, label, icon, description, category, href, action, recent, favorite }
        this.recentItems = options.recentItems || [];
        this.favorites = options.favorites || [];
        this._open = false;
    }

    template() {
        return `
            <div class="ui-launcher__backdrop" hidden></div>
            <div class="ui-launcher" hidden role="dialog" aria-label="Lançador rápido">
                <div class="ui-launcher__header">
                    <input class="ui-launcher__input" type="text" placeholder="Buscar módulos…" autofocus>
                </div>
                <div class="ui-launcher__body">
                    ${this.favorites.length ? `
                    <div class="ui-launcher__section">
                        <span class="ui-launcher__section-title">Favoritos</span>
                        <div class="ui-launcher__favorites">
                            ${this.favorites.map(f => `
                                <button class="ui-launcher__fav" data-id="${f.id}">
                                    ${FiscalUI.icons.render(f.icon || 'star', { size: 24 })}
                                    <span>${f.label}</span>
                                </button>
                            `).join('')}
                        </div>
                    </div>` : ''}
                    <div class="ui-launcher__section">
                        <span class="ui-launcher__section-title">Módulos</span>
                        <div class="ui-launcher__grid">
                            ${this.items.map(item => `
                                <button class="ui-launcher__item" data-id="${item.id}">
                                    <span class="ui-launcher__item-icon">${FiscalUI.icons.render(item.icon || 'module', { size: 20 })}</span>
                                    <div class="ui-launcher__item-info">
                                        <span class="ui-launcher__item-label">${item.label}</span>
                                        <span class="ui-launcher__item-desc">${item.description || ''}</span>
                                    </div>
                                </button>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    onInit() {
        this._backdrop = this.query('.ui-launcher__backdrop');
        this._launcher = this.query('.ui-launcher');
        this._input = this.query('.ui-launcher__input');
        this._allItems = [...this.favorites.map(f => ({ ...f, _isFavorite: true })), ...this.items];

        this._backdrop.addEventListener('click', () => this.close());
        this._input.addEventListener('input', () => this._filter(this._input.value));

        this.queryAll('.ui-launcher__item, .ui-launcher__fav').forEach(el => {
            el.addEventListener('click', () => this._launch(el.dataset.id));
        });

        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === '\\') { e.preventDefault(); this.toggle(); }
            if (e.key === 'Escape' && this._open) this.close();
        });

        super.onInit();
    }

    toggle() { this._open ? this.close() : this.open(); }

    open() {
        this._open = true;
        this._backdrop.hidden = false;
        this._launcher.hidden = false;
        this._filter('');
        setTimeout(() => this._input?.focus(), 100);
        this.emit('launcher:open');
    }

    close() {
        this._open = false;
        this._backdrop.hidden = true;
        this._launcher.hidden = true;
        this._input.value = '';
        this.emit('launcher:close');
    }

    _filter(query) {
        const q = query.toLowerCase();
        this.queryAll('.ui-launcher__item, .ui-launcher__fav, .ui-launcher__section').forEach(el => {
            const label = el.querySelector('span')?.textContent?.toLowerCase() || '';
            const match = !q || label.includes(q);
            el.style.display = match ? '' : 'none';
        });
    }

    _launch(id) {
        const item = this._allItems.find(i => i.id === id);
        if (!item) return;
        this.close();
        if (item.href) window.location.href = item.href;
        item.action?.();
        this.emit('launcher:launch', { id, label: item.label });

        // Adiciona aos recentes
        const recent = this.recentItems.filter(r => r.id !== id);
        recent.unshift({ id: item.id, label: item.label, icon: item.icon });
        this.recentItems = recent.slice(0, 5);
    }
}
```

```css
.ui-launcher__backdrop {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: calc(var(--z-modal) - 1);
}

.ui-launcher {
    position: fixed; top: 15%; left: 50%;
    transform: translateX(-50%);
    width: 640px; max-width: 90vw;
    max-height: 70vh;
    z-index: var(--z-modal);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    display: flex; flex-direction: column;
    overflow: hidden;
}

.ui-launcher__header { padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-launcher__input {
    width: 100%; border: none; outline: none;
    font-size: var(--font-size-lg); background: transparent;
    color: var(--color-text);
}

.ui-launcher__body { overflow-y: auto; padding: var(--spacing-md); display: flex; flex-direction: column; gap: var(--spacing-lg); }
.ui-launcher__section-title { font-size: var(--font-size-xs); color: var(--color-text-muted); text-transform: uppercase; font-weight: var(--font-weight-semibold); letter-spacing: 0.5px; margin-bottom: var(--spacing-sm); display: block; }

.ui-launcher__favorites { display: flex; gap: var(--spacing-sm); flex-wrap: wrap; }
.ui-launcher__fav {
    display: flex; flex-direction: column; align-items: center; gap: var(--spacing-xs);
    padding: var(--spacing-md); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); background: transparent; cursor: pointer;
    min-width: 80px; color: var(--color-text); font-size: var(--font-size-xs);
    transition: background var(--motion-fast), border-color var(--motion-fast);
}
.ui-launcher__fav:hover { background: var(--color-surface-hover); border-color: var(--color-primary); }

.ui-launcher__grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--spacing-xs); }
.ui-launcher__item {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    border: none; background: transparent; cursor: pointer;
    border-radius: var(--radius-sm); color: var(--color-text);
    text-align: left; transition: background var(--motion-fast);
}
.ui-launcher__item:hover { background: var(--color-surface-hover); }

.ui-launcher__item-icon { flex-shrink: 0; color: var(--color-text-secondary); }
.ui-launcher__item-info { display: flex; flex-direction: column; }
.ui-launcher__item-label { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.ui-launcher__item-desc { font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
