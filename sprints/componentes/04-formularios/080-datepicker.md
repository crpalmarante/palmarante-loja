# FiscalUI Framework

## Documento 080 — DatePicker

**Nível 4 — Formulários**

**Versão 1.0**

Seletor de data com calendário mensal, navegação entre meses e formatação pt-BR.

---

```js
class UIDatePicker extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.placeholder = options.placeholder || 'Selecione uma data';
        this.minDate = options.minDate || null;
        this.maxDate = options.maxDate || null;
        this.format = options.format || 'pt-BR';
        this.rules = options.rules || [];
        this._open = false;
        this._viewDate = this.value ? new Date(this.value + 'T12:00:00') : new Date();
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-datepicker">
                    <div class="ui-field__input-wrapper">
                        <span class="ui-field__prefix-icon">${FiscalUI.icons.render('calendar', { size: 16 })}</span>
                        <input class="ui-field__input ui-datepicker__input" type="text" readonly
                               placeholder="${this.placeholder}" value="${this._displayValue()}" autocomplete="off">
                        <button class="ui-datepicker__clear" ${this.value ? '' : 'hidden'} aria-label="Limpar">${FiscalUI.icons.render('x', { size: 14 })}</button>
                    </div>
                    <div class="ui-datepicker__dropdown" hidden>
                        <div class="ui-datepicker__header">
                            <button class="ui-datepicker__nav" data-dir="-1">${FiscalUI.icons.render('chevron-left', { size: 16 })}</button>
                            <span class="ui-datepicker__title">${this._formatTitle()}</span>
                            <button class="ui-datepicker__nav" data-dir="1">${FiscalUI.icons.render('chevron-right', { size: 16 })}</button>
                        </div>
                        <div class="ui-datepicker__days-header">
                            ${['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'].map(d => `<span class="ui-datepicker__day-name">${d}</span>`).join('')}
                        </div>
                        <div class="ui-datepicker__days">${this._renderDays()}</div>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _displayValue() {
        if (!this.value) return '';
        const d = new Date(this.value + 'T12:00:00');
        return d.toLocaleDateString('pt-BR');
    }

    _formatTitle() {
        return this._viewDate.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
    }

    _renderDays() {
        const year = this._viewDate.getFullYear();
        const month = this._viewDate.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();

        let html = '';
        for (let i = 0; i < firstDay; i++) html += '<span></span>';
        for (let d = 1; d <= daysInMonth; d++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            const isToday = today.getFullYear() === year && today.getMonth() === month && today.getDate() === d;
            const isSelected = this.value === dateStr;
            const isDisabled = (this.minDate && dateStr < this.minDate) || (this.maxDate && dateStr > this.maxDate);
            html += `<span class="ui-datepicker__day ${isToday ? 'ui-datepicker__day--today' : ''} ${isSelected ? 'ui-datepicker__day--selected' : ''} ${isDisabled ? 'ui-datepicker__day--disabled' : ''}" data-date="${dateStr}">${d}</span>`;
        }
        return html;
    }

    onInit() {
        this._input = this.query('.ui-datepicker__input');
        this._dropdown = this.query('.ui-datepicker__dropdown');
        this._title = this.query('.ui-datepicker__title');
        this._days = this.query('.ui-datepicker__days');
        this._clearBtn = this.query('.ui-datepicker__clear');

        this._input.addEventListener('click', () => this.toggle());
        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') this.close(); });

        this.queryAll('.ui-datepicker__nav').forEach(btn => {
            btn.addEventListener('click', (e) => { e.stopPropagation(); this._navigate(parseInt(btn.dataset.dir)); });
        });

        this._days.addEventListener('click', (e) => {
            const day = e.target.closest('.ui-datepicker__day');
            if (!day || day.classList.contains('ui-datepicker__day--disabled')) return;
            this.select(day.dataset.date);
        });

        this._clearBtn?.addEventListener('click', (e) => { e.stopPropagation(); this.clear(); });
    }

    _navigate(dir) {
        this._viewDate.setMonth(this._viewDate.getMonth() + dir);
        this._title.textContent = this._formatTitle();
        this._days.innerHTML = this._renderDays();
    }

    select(dateStr) {
        this.value = dateStr;
        this._input.value = this._displayValue();
        this._clearBtn.hidden = false;
        this.close();
        this.emit('field:change', { name: this.name, value: this.value });
    }

    clear() { this.value = ''; this._input.value = ''; this._clearBtn.hidden = true; this.emit('field:change', { name: this.name, value: '' }); }
    toggle() { this._open ? this.close() : this.open(); }
    open() { this._open = true; this._dropdown.hidden = false; this._days.innerHTML = this._renderDays(); }
    close() { this._open = false; this._dropdown.hidden = true; }

    value() { return this.value; }
    setValue(val) { this.value = val; this._viewDate = val ? new Date(val + 'T12:00:00') : new Date(); if (this._input) this._input.value = this._displayValue(); }
    reset() { this.clear(); }
}
```

```css
.ui-datepicker { position: relative; }
.ui-datepicker__input { cursor: pointer; }
.ui-datepicker__clear { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); padding: 0 var(--spacing-sm); display: flex; }
.ui-datepicker__clear:hover { color: var(--color-text); }

.ui-datepicker__dropdown {
    position: absolute; top: 100%; left: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg); padding: var(--spacing-md);
    width: 280px;
}

.ui-datepicker__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--spacing-sm); }
.ui-datepicker__nav { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); padding: 4px; border-radius: 50%; display: flex; }
.ui-datepicker__nav:hover { background: var(--color-surface-hover); color: var(--color-text); }
.ui-datepicker__title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); text-transform: capitalize; }

.ui-datepicker__days-header { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; margin-bottom: var(--spacing-xs); }
.ui-datepicker__day-name { text-align: center; font-size: var(--font-size-xs); color: var(--color-text-muted); padding: 2px; }

.ui-datepicker__days { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
.ui-datepicker__day {
    text-align: center; padding: 6px 2px; cursor: pointer; border-radius: var(--radius-sm);
    font-size: var(--font-size-sm); transition: background var(--motion-fast);
}
.ui-datepicker__day:hover { background: var(--color-surface-hover); }
.ui-datepicker__day--today { font-weight: var(--font-weight-bold); color: var(--color-primary); }
.ui-datepicker__day--selected { background: var(--color-primary); color: #fff; }
.ui-datepicker__day--disabled { opacity: 0.3; cursor: not-allowed; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
