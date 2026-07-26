# FiscalUI Framework

## Documento 053 — Search Bar

**Nível 3 — Navegação**

**Versão 1.0**

Barra de busca com suporte a autocomplete, filtros rápidos e histórico. Usada como controle principal de pesquisa na aplicação.

---

```js
class UISearchBar extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.placeholder = options.placeholder || 'Pesquisar…';
        this.suggestions = options.suggestions || [];   // [{ label, category, icon }]
        this.filters = options.filters || [];
        this.minChars = options.minChars || 2;
        this.debounce = options.debounce || 300;
        this._timer = null;
        this._open = false;
    }

    template() {
        return `
            <div class="ui-search">
                <div class="ui-search__input-wrapper">
                    <span class="ui-search__icon">${FiscalUI.icons.render('search', { size: 18 })}</span>
                    <input class="ui-search__input" type="text" placeholder="${this.placeholder}" autocomplete="off">
                    <button class="ui-search__clear" hidden aria-label="Limpar">${FiscalUI.icons.render('x', { size: 14 })}</button>
                    <kbd class="ui-search__hint">/</kbd>
                </div>
                ${this.filters.length ? `
                <div class="ui-search__filters">
                    ${this.filters.map(f => `
                        <button class="ui-chip ui-chip--sm ${f.active ? 'ui-chip--primary' : ''}" data-filter="${f.value}">
                            ${f.label}
                        </button>
                    `).join('')}
                </div>` : ''}
                <div class="ui-search__dropdown" hidden>
                    <div class="ui-search__results"></div>
                </div>
            </div>
        `;
    }

    onInit() {
        this._input = this.query('.ui-search__input');
        this._clear = this.query('.ui-search__clear');
        this._dropdown = this.query('.ui-search__dropdown');
        this._results = this.query('.ui-search__results');
        this._activeFilter = null;

        this._input.addEventListener('input', () => {
            this._clear.hidden = !this._input.value;
            clearTimeout(this._timer);
            this._timer = setTimeout(() => this._search(), this.debounce);
        });

        this._input.addEventListener('focus', () => { if (this._input.value.length >= this.minChars) this._openDropdown(); });
        this._input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this._closeDropdown();
            if (e.key === 'Enter') {
                this.emit('search:submit', { value: this._input.value, filter: this._activeFilter });
                this._closeDropdown();
            }
        });

        this._clear.addEventListener('click', () => { this._input.value = ''; this._clear.hidden = true; this._search(); this._input.focus(); });

        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this._closeDropdown(); });

        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && !e.ctrlKey && !e.metaKey && document.activeElement !== this._input) {
                e.preventDefault(); this._input.focus();
            }
        });

        this.queryAll('.ui-search__filters .ui-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                this.queryAll('.ui-search__filters .ui-chip').forEach(c => c.classList.remove('ui-chip--primary'));
                chip.classList.add('ui-chip--primary');
                this._activeFilter = chip.dataset.filter;
                this._search();
            });
        });
    }

    _search() {
        const value = this._input.value.trim();
        if (value.length < this.minChars) { this._closeDropdown(); return; }
        this.emit('search:query', { value, filter: this._activeFilter });
    }

    showSuggestions(suggestions) {
        if (!suggestions.length) { this._closeDropdown(); return; }
        this._results.innerHTML = suggestions.map(s => `
            <div class="ui-search__result" data-value="${s.label}">
                ${s.icon ? `<span class="ui-search__result-icon">${FiscalUI.icons.render(s.icon, { size: 16 })}</span>` : ''}
                <div class="ui-search__result-info">
                    <span>${s.label}</span>
                    ${s.category ? `<span class="ui-search__result-category">${s.category}</span>` : ''}
                </div>
            </div>
        `).join('');
        this.queryAll('.ui-search__result').forEach(el => {
            el.addEventListener('click', () => {
                this._input.value = el.dataset.value;
                this.emit('search:select', { value: el.dataset.value });
                this._closeDropdown();
            });
        });
        this._openDropdown();
    }

    _openDropdown() { this._dropdown.hidden = false; this._open = true; this.element.classList.add('ui-search--open'); }
    _closeDropdown() { this._dropdown.hidden = true; this._open = false; this.element.classList.remove('ui-search--open'); }

    getValue() { return this._input.value; }
    setValue(val) { this._input.value = val; this._clear.hidden = !val; }
    focus() { this._input.focus(); }
}
```

```css
.ui-search { position: relative; width: 100%; max-width: 480px; }

.ui-search__input-wrapper {
    display: flex; align-items: center;
    padding: 0 var(--spacing-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    background: var(--color-surface);
    gap: var(--spacing-sm);
    transition: border-color var(--motion-fast), box-shadow var(--motion-fast);
}
.ui-search--open .ui-search__input-wrapper,
.ui-search__input-wrapper:focus-within { border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-surface); }

.ui-search__icon { flex-shrink: 0; color: var(--color-text-muted); }
.ui-search__input { flex: 1; border: none; outline: none; background: transparent; font-size: var(--font-size-md); padding: var(--spacing-sm) 0; color: var(--color-text); }
.ui-search__clear { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); display: flex; padding: 2px; border-radius: 50%; }
.ui-search__clear:hover { background: var(--color-surface-hover); }
.ui-search__hint { font-size: 11px; color: var(--color-text-muted); padding: 1px 6px; background: var(--color-surface-hover); border-radius: 4px; }

.ui-search__filters { display: flex; gap: var(--spacing-xs); margin-top: var(--spacing-xs); flex-wrap: wrap; }

.ui-search__dropdown {
    position: absolute; top: 100%; left: 0; right: 0; margin-top: var(--spacing-xs);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
    z-index: var(--z-popover); max-height: 300px; overflow-y: auto;
}

.ui-search__result {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md); cursor: pointer;
    transition: background var(--motion-fast);
}
.ui-search__result:hover { background: var(--color-surface-hover); }
.ui-search__result-icon { flex-shrink: 0; color: var(--color-text-muted); }
.ui-search__result-info { display: flex; flex-direction: column; flex: 1; font-size: var(--font-size-sm); }
.ui-search__result-category { font-size: var(--font-size-xs); color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
