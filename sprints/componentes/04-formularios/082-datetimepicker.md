# FiscalUI Framework

## Documento 082 — DateTimePicker

**Nível 4 — Formulários**

**Versão 1.0**

Seletor combinado de data e hora. Composto por DatePicker + TimePicker em um dropdown.

---

```js
class UIDateTimePicker extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.value = options.value || '';
        this.placeholder = options.placeholder || 'Selecione data e hora';
        this.rules = options.rules || [];
        this._open = false;
        this._date = this.value ? this.value.split('T')[0] : '';
        this._time = this.value ? this.value.split('T')[1] || '' : '';
        this._viewDate = this._date ? new Date(this._date + 'T12:00:00') : new Date();
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-datetime">
                    <div class="ui-field__input-wrapper">
                        <span class="ui-field__prefix-icon">${FiscalUI.icons.render('calendar', { size: 16 })}</span>
                        <input class="ui-field__input ui-datetime__input" type="text" readonly
                               placeholder="${this.placeholder}" value="${this._displayValue()}" autocomplete="off">
                    </div>
                    <div class="ui-datetime__dropdown" hidden>
                        <div class="ui-datepicker__header">
                            <button class="ui-datepicker__nav" data-dir="-1">${FiscalUI.icons.render('chevron-left', { size: 16 })}</button>
                            <span class="ui-datepicker__title">${this._formatTitle()}</span>
                            <button class="ui-datepicker__nav" data-dir="1">${FiscalUI.icons.render('chevron-right', { size: 16 })}</button>
                        </div>
                        <div class="ui-datepicker__days-header">
                            ${['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'].map(d => `<span class="ui-datepicker__day-name">${d}</span>`).join('')}
                        </div>
                        <div class="ui-datepicker__days">${this._renderDays()}</div>
                        <div class="ui-datetime__time">
                            ${Array.from({ length: 24 }, (_, h) => String(h).padStart(2, '0')).flatMap(h =>
                                Array.from({ length: 60 / 30 }, (_, m) => {
                                    const t = `${h}:${String(m * 30).padStart(2, '0')}`;
                                    return `<span class="ui-datetime__time-item ${this._time === t ? 'ui-datetime__time-item--selected' : ''}" data-time="${t}">${t}</span>`;
                                })
                            ).join('')}
                        </div>
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _displayValue() {
        if (!this._date) return '';
        const d = new Date(this._date + 'T12:00:00');
        return `${d.toLocaleDateString('pt-BR')} ${this._time || '00:00'}`;
    }

    _formatTitle() {
        return this._viewDate.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
    }

    _renderDays() {
        const year = this._viewDate.getFullYear();
        const month = this._viewDate.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        let html = '';
        for (let i = 0; i < firstDay; i++) html += '<span></span>';
        for (let d = 1; d <= daysInMonth; d++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            html += `<span class="ui-datepicker__day ${this._date === dateStr ? 'ui-datepicker__day--selected' : ''}" data-date="${dateStr}">${d}</span>`;
        }
        return html;
    }

    onInit() {
        this._input = this.query('.ui-datetime__input');
        this._dropdown = this.query('.ui-datetime__dropdown');

        this._input.addEventListener('click', () => this.toggle());
        document.addEventListener('click', (e) => { if (!this.element.contains(e.target)) this.close(); });

        this.queryAll('.ui-datepicker__nav').forEach(btn => {
            btn.addEventListener('click', (e) => { e.stopPropagation(); this._viewDate.setMonth(this._viewDate.getMonth() + parseInt(btn.dataset.dir)); this._render(); });
        });

        this.query('.ui-datepicker__days').addEventListener('click', (e) => {
            const day = e.target.closest('.ui-datepicker__day');
            if (!day) return;
            this._date = day.dataset.date;
            this._updateValue();
            this._render();
        });

        this._dropdown.querySelector('.ui-datetime__time').addEventListener('click', (e) => {
            const item = e.target.closest('.ui-datetime__time-item');
            if (!item) return;
            this._time = item.dataset.time;
            this._updateValue();
        });
    }

    _updateValue() {
        this.value = this._date ? `${this._date}T${this._time || '00:00'}` : '';
        this._input.value = this._displayValue();
        this.emit('field:change', { name: this.name, value: this.value });
    }

    _render() {
        this.query('.ui-datepicker__title').textContent = this._formatTitle();
        this.query('.ui-datepicker__days').innerHTML = this._renderDays();
    }

    toggle() { this._open ? this.close() : this.open(); }
    open() { this._open = true; this._dropdown.hidden = false; this._render(); }
    close() { this._open = false; this._dropdown.hidden = true; }

    value() { return this.value; }
    setValue(val) { this.value = val; const parts = val.split('T'); this._date = parts[0] || ''; this._time = parts[1] || ''; if (this._input) this._input.value = this._displayValue(); }
    reset() { this._date = ''; this._time = ''; this.value = ''; this._input.value = ''; }
}
```

```css
.ui-datetime { position: relative; }
.ui-datetime__input { cursor: pointer; }
.ui-datetime__dropdown {
    position: absolute; top: 100%; left: 0; margin-top: 2px; z-index: var(--z-popover);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg); padding: var(--spacing-md);
    width: 280px;
}
.ui-datetime__time {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px;
    margin-top: var(--spacing-sm); padding-top: var(--spacing-sm);
    border-top: 1px solid var(--color-border); max-height: 120px; overflow-y: auto;
}
.ui-datetime__time-item {
    text-align: center; padding: 4px 2px; cursor: pointer; border-radius: var(--radius-sm);
    font-size: var(--font-size-xs); font-family: monospace; transition: background var(--motion-fast);
}
.ui-datetime__time-item:hover { background: var(--color-surface-hover); }
.ui-datetime__time-item--selected { background: var(--color-primary); color: #fff; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
