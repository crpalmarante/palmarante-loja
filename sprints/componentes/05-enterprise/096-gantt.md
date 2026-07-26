# FiscalUI Framework

## Documento 096 — Gantt

**Nível 5 — Enterprise Components**

**Versão 1.0**

Gráfico de Gantt para cronograma de projetos. Exibe tarefas como barras horizontais em uma timeline.

---

```js
class UIGantt extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.tasks = options.tasks || [];
        this.startDate = options.startDate || new Date();
        this.dayWidth = options.dayWidth || 24;
        this.rowHeight = options.rowHeight || 36;
        this._days = options.days || 30;
    }

    template() {
        const days = Array.from({ length: this._days }, (_, i) => {
            const d = new Date(this.startDate);
            d.setDate(d.getDate() + i);
            return d;
        });
        return `
            <div class="ui-gantt">
                <div class="ui-gantt__header">
                    <div class="ui-gantt__labels-header" style="min-width:200px"><span>Tarefa</span></div>
                    <div class="ui-gantt__timeline" style="grid-template-columns: repeat(${this._days}, ${this.dayWidth}px)">
                        ${days.map(d => `<div class="ui-gantt__day ${d.getDay() === 0 || d.getDay() === 6 ? 'ui-gantt__day--weekend' : ''}">
                            <span class="ui-gantt__day-name">${d.toLocaleDateString('pt-BR', { weekday: 'short' })}</span>
                            <span class="ui-gantt__day-num">${d.getDate()}</span>
                        </div>`).join('')}
                    </div>
                </div>
                <div class="ui-gantt__body">
                    ${this.tasks.map((task, i) => this._renderTask(task, i, days)).join('')}
                </div>
            </div>
        `;
    }

    _renderTask(task, index, days) {
        const start = new Date(task.start);
        const end = new Date(task.end);
        const startIdx = Math.floor((start - this.startDate) / (1000 * 60 * 60 * 24));
        const duration = Math.floor((end - start) / (1000 * 60 * 60 * 24)) + 1;
        const left = startIdx * this.dayWidth;
        const width = duration * this.dayWidth;
        return `
            <div class="ui-gantt__row" style="height:${this.rowHeight}px">
                <div class="ui-gantt__labels" style="min-width:200px">
                    <span class="ui-gantt__task-name" style="padding-left:${task.depth ? task.depth * 16 : 0}px">${task.name}</span>
                </div>
                <div class="ui-gantt__bars" style="position:relative">
                    <div class="ui-gantt__bar" style="left:${left}px;width:${width}px;background:${task.color || 'var(--color-primary)'}">
                        <span class="ui-gantt__bar-label">${task.name}</span>
                    </div>
                </div>
            </div>
        `;
    }

    onInit() {
        this.queryAll('.ui-gantt__bar').forEach(bar => {
            bar.addEventListener('click', () => {
                const idx = [...bar.closest('.ui-gantt__row').parentElement.children].indexOf(bar.closest('.ui-gantt__row'));
                this.emit('gantt:select', { task: this.tasks[idx] });
            });
        });
    }

    setTasks(tasks) { this.tasks = tasks; this.render(); }
}
```

```css
.ui-gantt { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: auto; }

.ui-gantt__header { display: flex; border-bottom: 1px solid var(--color-border); background: var(--color-surface); }
.ui-gantt__labels-header { padding: var(--spacing-sm) var(--spacing-md); font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); flex-shrink: 0; }
.ui-gantt__timeline { display: grid; flex: 1; }
.ui-gantt__day { text-align: center; padding: 2px 0; border-left: 1px solid var(--color-border); font-size: 10px; }
.ui-gantt__day--weekend { background: var(--color-surface-hover); }
.ui-gantt__day-name { display: block; color: var(--color-text-muted); }
.ui-gantt__day-num { font-weight: var(--font-weight-medium); }

.ui-gantt__row { display: flex; border-bottom: 1px solid var(--color-border); }
.ui-gantt__labels { padding: 0 var(--spacing-sm); display: flex; align-items: center; flex-shrink: 0; }
.ui-gantt__task-name { font-size: var(--font-size-sm); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.ui-gantt__bars { flex: 1; position: relative; }
.ui-gantt__bar {
    position: absolute; top: 4px; height: calc(100% - 8px);
    border-radius: var(--radius-sm); display: flex; align-items: center;
    padding: 0 4px; cursor: pointer; overflow: hidden; min-width: 4px;
}
.ui-gantt__bar-label { font-size: 10px; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
