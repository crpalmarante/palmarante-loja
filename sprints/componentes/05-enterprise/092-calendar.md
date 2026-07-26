# FiscalUI Framework

## Documento 092 — Calendar

**Nível 5 — Enterprise Components**

**Versão 1.0**

Calendário mensal com eventos, navegação entre meses e visualização dia/semana/mês.

---

```js
class UICalendar extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.events = options.events || [];
        this.view = options.view || 'month'; // month, week, day
        this._date = options.date ? new Date(options.date) : new Date();
        this.firstDay = options.firstDay || 0;
    }

    template() {
        return `
            <div class="ui-calendar">
                <div class="ui-calendar__header">
                    <button class="ui-calendar__nav" data-dir="-1">${FiscalUI.icons.render('chevron-left', { size: 18 })}</button>
                    <h3 class="ui-calendar__title">${this._formatTitle()}</h3>
                    <button class="ui-calendar__nav" data-dir="1">${FiscalUI.icons.render('chevron-right', { size: 18 })}</button>
                    <div class="ui-calendar__view-switcher">
                        ${['month', 'week', 'day'].map(v => `<button class="ui-calendar__view-btn ${this.view === v ? 'ui-calendar__view-btn--active' : ''}" data-view="${v}">${v.charAt(0).toUpperCase() + v.slice(1)}</button>`).join('')}
                    </div>
                </div>
                <div class="ui-calendar__body">${this._renderView()}</div>
            </div>
        `;
    }

    _formatTitle() {
        return this._date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
    }

    _renderView() {
        if (this.view === 'month') return this._renderMonth();
        if (this.view === 'week') return this._renderWeek();
        return this._renderDay();
    }

    _renderMonth() {
        const year = this._date.getFullYear();
        const month = this._date.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();

        let html = '<div class="ui-calendar__weekdays">';
        const dayNames = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        for (let i = 0; i < 7; i++) html += `<span class="ui-calendar__weekday">${dayNames[(i + this.firstDay) % 7]}</span>`;
        html += '</div><div class="ui-calendar__days">';

        for (let i = 0; i < (firstDay - this.firstDay + 7) % 7; i++) html += '<span></span>';
        for (let d = 1; d <= daysInMonth; d++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            const isToday = today.getFullYear() === year && today.getMonth() === month && today.getDate() === d;
            const dayEvents = this.events.filter(e => e.date === dateStr);
            html += `<div class="ui-calendar__day ${isToday ? 'ui-calendar__day--today' : ''}" data-date="${dateStr}">
                <span class="ui-calendar__day-num">${d}</span>
                ${dayEvents.slice(0, 2).map(e => `<span class="ui-calendar__event-dot" style="background:${e.color || 'var(--color-primary)'}"></span>`).join('')}
                ${dayEvents.length > 2 ? `<span class="ui-calendar__event-more">+${dayEvents.length - 2}</span>` : ''}
            </div>`;
        }
        html += '</div>';
        return html;
    }

    _renderWeek() { return '<div class="ui-calendar__placeholder">Visão semanal</div>'; }
    _renderDay() { return '<div class="ui-calendar__placeholder">Visão diária</div>'; }

    onInit() {
        this.queryAll('.ui-calendar__nav').forEach(btn => {
            btn.addEventListener('click', () => {
                const dir = parseInt(btn.dataset.dir);
                if (this.view === 'month') this._date.setMonth(this._date.getMonth() + dir);
                else if (this.view === 'week') this._date.setDate(this._date.getDate() + 7 * dir);
                else this._date.setDate(this._date.getDate() + dir);
                this._renderAll();
            });
        });

        this.queryAll('.ui-calendar__view-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.view = btn.dataset.view;
                this._renderAll();
            });
        });

        this.query('.ui-calendar__days')?.addEventListener('click', (e) => {
            const day = e.target.closest('.ui-calendar__day');
            if (day) this.emit('calendar:select', { date: day.dataset.date });
        });
    }

    _renderAll() {
        this.query('.ui-calendar__title').textContent = this._formatTitle();
        this.query('.ui-calendar__body').innerHTML = this._renderView();
        this.queryAll('.ui-calendar__view-btn').forEach(btn => btn.classList.toggle('ui-calendar__view-btn--active', btn.dataset.view === this.view));
        this.onInit();
    }

    setEvents(events) { this.events = events; this._renderAll(); }
    goToday() { this._date = new Date(); this._renderAll(); }
}
```

```css
.ui-calendar { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }

.ui-calendar__header { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-calendar__nav { border: none; background: transparent; cursor: pointer; color: var(--color-text-secondary); padding: 4px; border-radius: 50%; display: flex; }
.ui-calendar__nav:hover { background: var(--color-surface-hover); }
.ui-calendar__title { flex: 1; font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); margin: 0; }
.ui-calendar__view-switcher { display: flex; gap: 2px; }
.ui-calendar__view-btn { padding: var(--spacing-xs) var(--spacing-sm); border: 1px solid var(--color-border); background: transparent; cursor: pointer; font-size: var(--font-size-xs); border-radius: var(--radius-sm); }
.ui-calendar__view-btn--active { background: var(--color-primary); color: #fff; border-color: var(--color-primary); }

.ui-calendar__weekdays { display: grid; grid-template-columns: repeat(7, 1fr); background: var(--color-surface-hover); }
.ui-calendar__weekday { text-align: center; padding: var(--spacing-xs); font-size: var(--font-size-xs); color: var(--color-text-muted); font-weight: var(--font-weight-semibold); }

.ui-calendar__days { display: grid; grid-template-columns: repeat(7, 1fr); }
.ui-calendar__day { min-height: 80px; padding: var(--spacing-xs); border: 1px solid var(--color-border); cursor: pointer; transition: background var(--motion-fast); position: relative; }
.ui-calendar__day:hover { background: var(--color-surface-hover); }
.ui-calendar__day--today .ui-calendar__day-num { background: var(--color-primary); color: #fff; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; }

.ui-calendar__day-num { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.ui-calendar__event-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin: 1px; }
.ui-calendar__event-more { font-size: 10px; color: var(--color-text-muted); }
.ui-calendar__placeholder { padding: var(--spacing-xl); text-align: center; color: var(--color-text-muted); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
