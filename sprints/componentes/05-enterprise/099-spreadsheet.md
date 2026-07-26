# FiscalUI Framework

## Documento 099 — Spreadsheet

**Nível 5 — Enterprise Components**

**Versão 1.0**

Planilha com células editáveis, suporte a fórmulas básicas, seleção de range e atalhos de teclado.

---

```js
class UISpreadsheet extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.cols = options.cols || 10;
        this.rows = options.rows || 20;
        this.data = options.data || {};
        this._selected = null;
        this._edit = null;
    }

    template() {
        const colLetters = Array.from({ length: this.cols }, (_, i) => String.fromCharCode(65 + i));
        return `
            <div class="ui-spreadsheet">
                <div class="ui-spreadsheet__header">
                    <div class="ui-spreadsheet__corner"></div>
                    ${colLetters.map(l => `<div class="ui-spreadsheet__col-header">${l}</div>`).join('')}
                </div>
                <div class="ui-spreadsheet__body">
                    ${Array.from({ length: this.rows }, (_, r) => `
                        <div class="ui-spreadsheet__row">
                            <div class="ui-spreadsheet__row-header">${r + 1}</div>
                            ${colLetters.map((l, c) => {
                                const key = `${l}${r + 1}`;
                                const val = this.data[key] || '';
                                return `<div class="ui-spreadsheet__cell" data-cell="${key}" contenteditable="false">${val}</div>`;
                            }).join('')}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    onInit() {
        this.queryAll('.ui-spreadsheet__cell').forEach(cell => {
            cell.addEventListener('click', () => this._select(cell));
            cell.addEventListener('dblclick', () => this._edit(cell));
            cell.addEventListener('blur', () => this._finishEdit(cell));
            cell.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') { e.preventDefault(); this._finishEdit(cell); this._move(0, 1); }
                if (e.key === 'Tab') { e.preventDefault(); this._finishEdit(cell); this._move(1, 0); }
                if (e.key === 'Escape') { cell.textContent = this.data[cell.dataset.cell] || ''; cell.contentEditable = 'false'; }
            });
        });

        document.addEventListener('keydown', (e) => {
            if (!this._selected) return;
            if (e.key === 'ArrowDown') { e.preventDefault(); this._move(0, 1); }
            if (e.key === 'ArrowUp') { e.preventDefault(); this._move(0, -1); }
            if (e.key === 'ArrowLeft') { e.preventDefault(); this._move(-1, 0); }
            if (e.key === 'ArrowRight') { e.preventDefault(); this._move(1, 0); }
            if (e.key === 'F2') { e.preventDefault(); this._edit(this._selected); }
            if ((e.ctrlKey || e.metaKey) && e.key === 'c') this._copy();
            if ((e.ctrlKey || e.metaKey) && e.key === 'v') this._paste();
        });
    }

    _select(cell) {
        this.queryAll('.ui-spreadsheet__cell--selected').forEach(c => c.classList.remove('ui-spreadsheet__cell--selected'));
        cell.classList.add('ui-spreadsheet__cell--selected');
        this._selected = cell;
    }

    _edit(cell) {
        cell.contentEditable = 'true';
        cell.focus();
        this._edit = cell;
    }

    _finishEdit(cell) {
        if (cell.contentEditable === 'false') return;
        cell.contentEditable = 'false';
        const key = cell.dataset.cell;
        const val = cell.textContent.trim();
        if (val.startsWith('=')) {
            cell.textContent = this._evalFormula(val.slice(1));
        }
        this.data[key] = cell.textContent;
        this._edit = null;
    }

    _move(dx, dy) {
        if (!this._selected) return;
        const cell = this._selected.dataset.cell;
        const col = cell.charCodeAt(0) - 65;
        const row = parseInt(cell.slice(1)) - 1;
        const nc = Math.max(0, Math.min(this.cols - 1, col + dx));
        const nr = Math.max(0, Math.min(this.rows - 1, row + dy));
        const next = this.query(`[data-cell="${String.fromCharCode(65 + nc)}${nr + 1}"]`);
        if (next) this._select(next);
    }

    _evalFormula(formula) {
        try {
            const cols = {}; Object.keys(this.data).forEach(k => { cols[k] = parseFloat(this.data[k]) || 0; });
            const fn = new Function(...Object.keys(cols), `return (${formula})`);
            return fn(...Object.values(cols));
        } catch { return '#ERRO'; }
    }

    _copy() {
        if (this._selected) navigator.clipboard.writeText(this._selected.textContent);
    }
    _paste() {
        if (this._selected) navigator.clipboard.readText().then(t => { this._selected.textContent = t; this._finishEdit(this._selected); });
    }

    getData() { return this.data; }
    setData(data) { this.data = data; this.render(); }
}
```

```css
.ui-spreadsheet { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: auto; font-size: var(--font-size-sm); }
.ui-spreadsheet__header { display: flex; position: sticky; top: 0; z-index: 1; }
.ui-spreadsheet__corner { width: 40px; flex-shrink: 0; background: var(--color-surface-hover); border-bottom: 1px solid var(--color-border); }
.ui-spreadsheet__col-header { flex: 1; min-width: 80px; padding: 4px; text-align: center; background: var(--color-surface-hover); border-bottom: 1px solid var(--color-border); border-left: 1px solid var(--color-border); font-weight: var(--font-weight-semibold); font-size: var(--font-size-xs); }

.ui-spreadsheet__row { display: flex; }
.ui-spreadsheet__row-header { width: 40px; flex-shrink: 0; padding: 4px; text-align: center; background: var(--color-surface-hover); border-bottom: 1px solid var(--color-border); font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-spreadsheet__cell { flex: 1; min-width: 80px; padding: 4px 6px; border-bottom: 1px solid var(--color-border); border-left: 1px solid var(--color-border); cursor: cell; outline: none; }
.ui-spreadsheet__cell--selected { outline: 2px solid var(--color-primary); outline-offset: -1px; background: var(--color-primary-surface); z-index: 1; position: relative; }
.ui-spreadsheet__cell[contenteditable="true"] { background: #fff; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
