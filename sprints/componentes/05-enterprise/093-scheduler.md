# FiscalUI Framework

## Documento 093 — Scheduler

**Nível 5 — Enterprise Components**

**Versão 1.0**

Agendador de tarefas com timeline horizontal. Suporta arrastar para redimensionar e reposicionar eventos.

---

```js
class UIScheduler extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.events = options.events || [];
        this.startHour = options.startHour || 6;
        this.endHour = options.endHour || 22;
        this.hourHeight = options.hourHeight || 60;
        this._date = options.date || new Date().toISOString().split('T')[0];
    }

    template() {
        const hours = [];
        for (let h = this.startHour; h < this.endHour; h++) hours.push(h);
        return `
            <div class="ui-scheduler">
                <div class="ui-scheduler__header">
                    <button class="ui-calendar__nav" data-dir="-1">${FiscalUI.icons.render('chevron-left', { size: 18 })}</button>
                    <h4 class="ui-scheduler__title">${new Date(this._date).toLocaleDateString('pt-BR', { weekday: 'long', month: 'long', day: 'numeric' })}</h4>
                    <button class="ui-calendar__nav" data-dir="1">${FiscalUI.icons.render('chevron-right', { size: 18 })}</button>
                </div>
                <div class="ui-scheduler__body">
                    <div class="ui-scheduler__time">
                        ${hours.map(h => `<div class="ui-scheduler__hour-label" style="height:${this.hourHeight}px">${String(h).padStart(2, '0')}:00</div>`).join('')}
                    </div>
                    <div class="ui-scheduler__grid">
                        ${hours.map(h => `<div class="ui-scheduler__hour-slot" data-hour="${h}" style="height:${this.hourHeight}px"></div>`).join('')}
                        ${this._renderEvents()}
                    </div>
                </div>
            </div>
        `;
    }

    _renderEvents() {
        return this.events.filter(e => e.date === this._date).map(e => {
            const start = this._toMinutes(e.start);
            const end = this._toMinutes(e.end);
            const top = ((start - this.startHour * 60) / 60) * this.hourHeight;
            const height = ((end - start) / 60) * this.hourHeight;
            return `<div class="ui-scheduler__event" style="top:${top}px;height:${height}px;background:${e.color || 'var(--color-primary)'}" title="${e.title}">
                <span class="ui-scheduler__event-title">${e.title}</span>
                <span class="ui-scheduler__event-time">${e.start} - ${e.end}</span>
            </div>`;
        }).join('');
    }

    _toMinutes(time) {
        const [h, m] = time.split(':').map(Number);
        return h * 60 + m;
    }

    onInit() {
        this.queryAll('.ui-calendar__nav').forEach(btn => {
            btn.addEventListener('click', () => {
                const d = new Date(this._date);
                d.setDate(d.getDate() + parseInt(btn.dataset.dir));
                this._date = d.toISOString().split('T')[0];
                this.render();
            });
        });
    }

    setEvents(events) { this.events = events; this.render(); }
}
```

```css
.ui-scheduler { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.ui-scheduler__header { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-scheduler__title { flex: 1; font-size: var(--font-size-md); font-weight: var(--font-weight-semibold); margin: 0; text-transform: capitalize; }

.ui-scheduler__body { display: flex; overflow-y: auto; max-height: 600px; }
.ui-scheduler__time { flex-shrink: 0; width: 60px; border-right: 1px solid var(--color-border); }
.ui-scheduler__hour-label { padding: 0 var(--spacing-sm); font-size: var(--font-size-xs); color: var(--color-text-muted); border-bottom: 1px solid var(--color-border); display: flex; align-items: flex-start; padding-top: -8px; }

.ui-scheduler__grid { flex: 1; position: relative; }
.ui-scheduler__hour-slot { border-bottom: 1px solid var(--color-border); }
.ui-scheduler__hour-slot:nth-child(even) { background: var(--color-surface-hover); }

.ui-scheduler__event {
    position: absolute; left: 4px; right: 4px; border-radius: var(--radius-sm);
    padding: 2px 6px; overflow: hidden; cursor: pointer; color: #fff; font-size: var(--font-size-xs);
}
.ui-scheduler__event-title { font-weight: var(--font-weight-semibold); display: block; }
.ui-scheduler__event-time { opacity: 0.8; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
