# FiscalUI Framework

## Documento 052 — Command Palette

**Nível 3 — Navegação**

**Versão 1.0**

Paleta de comandos estilo VS Code (Cmd+K). Busca fuzzy por ações, navegação, configurações.

---

```js
class UICommandPalette extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.commands = options.commands || [];  // { id, label, description, category, icon, shortcut, action, keywords }
        this.placeholder = options.placeholder || 'Buscar comandos…';
        this.emptyMessage = options.emptyMessage || 'Nenhum comando encontrado';
        this._open = false;
        this._filtered = [];
    }

    template() {
        return `
            <div class="ui-palette__backdrop" hidden></div>
            <div class="ui-palette" hidden role="dialog" aria-label="Paleta de comandos">
                <div class="ui-palette__header">
                    <span class="ui-palette__search-icon">${FiscalUI.icons.render('search', { size: 18 })}</span>
                    <input class="ui-palette__input" type="text" placeholder="${this.placeholder}" autofocus>
                    <kbd class="ui-palette__hint">ESC</kbd>
                </div>
                <div class="ui-palette__results"></div>
                <div class="ui-palette__footer">
                    <span><kbd>↑↓</kbd> Navegar</span>
                    <span><kbd>↵</kbd> Selecionar</span>
                </div>
            </div>
        `;
    }

    onInit() {
        this._backdrop = this.query('.ui-palette__backdrop');
        this._palette = this.query('.ui-palette');
        this._input = this.query('.ui-palette__input');
        this._results = this.query('.ui-palette__results');
        this._activeIndex = 0;

        this._backdrop.addEventListener('click', () => this.close());
        this._input.addEventListener('input', () => this._search(this._input.value));
        this._input.addEventListener('keydown', (e) => this._onKeydown(e));
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); this.toggle(); }
            if (e.key === 'Escape' && this._open) this.close();
        });
    }

    toggle() { this._open ? this.close() : this.open(); }

    open() {
        this._open = true;
        this._backdrop.hidden = false;
        this._palette.hidden = false;
        this._filtered = [...this.commands];
        this._renderResults();
        setTimeout(() => this._input.focus(), 100);
        this.emit('palette:open');
    }

    close() {
        this._open = false;
        this._backdrop.hidden = true;
        this._palette.hidden = true;
        this._input.value = '';
        this._filtered = [];
        this.emit('palette:close');
    }

    _search(query) {
        const q = query.toLowerCase();
        this._filtered = q
            ? this.commands.filter(c =>
                c.label.toLowerCase().includes(q) ||
                c.description?.toLowerCase().includes(q) ||
                c.keywords?.some(k => k.toLowerCase().includes(q))
              )
            : this.commands;
        this._activeIndex = 0;
        this._renderResults();
    }

    _renderResults() {
        if (!this._filtered.length) {
            this._results.innerHTML = `<div class="ui-palette__empty">${this.emptyMessage}</div>`;
            return;
        }
        this._results.innerHTML = this._filtered.map((cmd, i) => `
            <div class="ui-palette__result ${i === this._activeIndex ? 'ui-palette__result--active' : ''}" data-index="${i}">
                ${cmd.icon ? `<span class="ui-palette__result-icon">${FiscalUI.icons.render(cmd.icon, { size: 16 })}</span>` : ''}
                <div class="ui-palette__result-info">
                    <span class="ui-palette__result-label">${cmd.label}</span>
                    ${cmd.description ? `<span class="ui-palette__result-desc">${cmd.description}</span>` : ''}
                </div>
                ${cmd.shortcut ? `<kbd class="ui-palette__result-shortcut">${cmd.shortcut}</kbd>` : ''}
                ${cmd.category ? `<span class="ui-palette__result-category">${cmd.category}</span>` : ''}
            </div>
        `).join('');

        this.queryAll('.ui-palette__result').forEach(el => {
            el.addEventListener('click', () => this._execute(parseInt(el.dataset.index)));
            el.addEventListener('mouseenter', () => {
                this._activeIndex = parseInt(el.dataset.index);
                this._updateActive();
            });
        });
        this._scrollIntoView();
    }

    _onKeydown(e) {
        if (e.key === 'ArrowDown') { e.preventDefault(); this._activeIndex = Math.min(this._activeIndex + 1, this._filtered.length - 1); this._updateActive(); this._scrollIntoView(); }
        if (e.key === 'ArrowUp') { e.preventDefault(); this._activeIndex = Math.max(this._activeIndex - 1, 0); this._updateActive(); this._scrollIntoView(); }
        if (e.key === 'Enter') { e.preventDefault(); this._execute(this._activeIndex); }
    }

    _execute(index) {
        const cmd = this._filtered[index];
        if (!cmd) return;
        this.close();
        cmd.action?.();
        this.emit('palette:execute', { id: cmd.id, label: cmd.label });
    }

    _updateActive() {
        this.queryAll('.ui-palette__result').forEach((el, i) => el.classList.toggle('ui-palette__result--active', i === this._activeIndex));
    }

    _scrollIntoView() {
        const active = this.query('.ui-palette__result--active');
        active?.scrollIntoView({ block: 'nearest' });
    }
}
```

```css
.ui-palette__backdrop {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: calc(var(--z-modal) - 1);
}

.ui-palette {
    position: fixed; top: 20%; left: 50%;
    transform: translateX(-50%);
    width: 600px; max-width: 90vw;
    z-index: var(--z-modal);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    overflow: hidden;
}

.ui-palette__header {
    display: flex; align-items: center;
    padding: var(--spacing-md); gap: var(--spacing-sm);
    border-bottom: 1px solid var(--color-border);
}

.ui-palette__search-icon { flex-shrink: 0; color: var(--color-text-muted); }
.ui-palette__input {
    flex: 1; border: none; outline: none;
    font-size: var(--font-size-lg); background: transparent;
    color: var(--color-text);
}
.ui-palette__hint { font-size: 11px; color: var(--color-text-muted); padding: 2px 6px; background: var(--color-surface-hover); border-radius: 4px; }

.ui-palette__results { max-height: 320px; overflow-y: auto; padding: var(--spacing-xs); }
.ui-palette__result {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-sm); cursor: pointer;
    transition: background var(--motion-fast);
}
.ui-palette__result:hover,
.ui-palette__result--active { background: var(--color-surface-hover); }

.ui-palette__result-info { display: flex; flex-direction: column; flex: 1; }
.ui-palette__result-label { font-size: var(--font-size-md); }
.ui-palette__result-desc { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-palette__result-shortcut { font-size: 11px; padding: 2px 4px; background: var(--color-surface-hover); border-radius: 4px; color: var(--color-text-muted); }
.ui-palette__result-category { font-size: 11px; color: var(--color-text-muted); background: var(--color-surface-hover); padding: 2px 6px; border-radius: 4px; }
.ui-palette__empty { padding: var(--spacing-xl); text-align: center; color: var(--color-text-muted); }
.ui-palette__footer { padding: var(--spacing-sm) var(--spacing-md); border-top: 1px solid var(--color-border); display: flex; gap: var(--spacing-lg); font-size: 11px; color: var(--color-text-muted); }
.ui-palette__footer kbd { font-size: 10px; padding: 1px 4px; background: var(--color-surface-hover); border-radius: 3px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
