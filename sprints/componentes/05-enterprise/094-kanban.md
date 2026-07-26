# FiscalUI Framework

## Documento 094 — Kanban

**Nível 5 — Enterprise Components**

**Versão 1.0**

Quadro Kanban com colunas e cartões. Suporta drag-and-drop entre colunas.

---

```js
class UIKanban extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.columns = options.columns || [];
        this.cards = options.cards || [];
        this.draggable = options.draggable !== false;
    }

    template() {
        return `
            <div class="ui-kanban">
                ${this.columns.map(col => `
                    <div class="ui-kanban__column" data-status="${col.status}">
                        <div class="ui-kanban__column-header">
                            <span class="ui-kanban__column-title">${col.title}</span>
                            <span class="ui-kanban__column-count">${this.cards.filter(c => c.status === col.status).length}</span>
                        </div>
                        <div class="ui-kanban__cards">
                            ${this.cards.filter(c => c.status === col.status).map(card => `
                                <div class="ui-kanban__card" draggable="${this.draggable}" data-id="${card.id}">
                                    ${card.priority ? `<span class="ui-kanban__priority ui-kanban__priority--${card.priority}"></span>` : ''}
                                    <div class="ui-kanban__card-title">${card.title}</div>
                                    ${card.description ? `<div class="ui-kanban__card-desc">${card.description}</div>` : ''}
                                    <div class="ui-kanban__card-footer">
                                        ${card.assignee ? `<span class="ui-kanban__assignee">${FiscalUI.icons.render('user', { size: 12 })} ${card.assignee}</span>` : ''}
                                        ${card.dueDate ? `<span class="ui-kanban__due">${card.dueDate}</span>` : ''}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    onInit() {
        if (!this.draggable) return;
        let dragCard = null;
        this.queryAll('.ui-kanban__card').forEach(card => {
            card.addEventListener('dragstart', () => { dragCard = card; card.classList.add('ui-kanban__card--dragging'); });
            card.addEventListener('dragend', () => { card.classList.remove('ui-kanban__card--dragging'); dragCard = null; document.querySelectorAll('.ui-kanban__column').forEach(c => c.classList.remove('ui-kanban__column--drag-over')); });
        });
        this.queryAll('.ui-kanban__cards').forEach(zone => {
            zone.addEventListener('dragover', (e) => e.preventDefault());
            zone.addEventListener('drop', (e) => {
                e.preventDefault();
                if (!dragCard) return;
                const newStatus = zone.closest('.ui-kanban__column').dataset.status;
                const cardId = dragCard.dataset.id;
                const card = this.cards.find(c => c.id === cardId);
                if (card && card.status !== newStatus) {
                    card.status = newStatus;
                    this.render();
                    this.emit('kanban:move', { id: cardId, status: newStatus });
                }
            });
        });
    }

    addCard(card) { this.cards.push(card); this.render(); }
    removeCard(id) { this.cards = this.cards.filter(c => c.id !== id); this.render(); }
}
```

```css
.ui-kanban { display: flex; gap: var(--spacing-md); overflow-x: auto; padding: var(--spacing-md); min-height: 400px; }

.ui-kanban__column { flex: 1; min-width: 260px; background: var(--color-surface-hover); border-radius: var(--radius-md); display: flex; flex-direction: column; }
.ui-kanban__column-header { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-kanban__column-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.ui-kanban__column-count { background: var(--color-surface); padding: 2px 8px; border-radius: 999px; font-size: var(--font-size-xs); }

.ui-kanban__cards { flex: 1; padding: var(--spacing-sm); display: flex; flex-direction: column; gap: var(--spacing-sm); overflow-y: auto; }
.ui-kanban__card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--spacing-sm); cursor: grab; transition: box-shadow var(--motion-fast); }
.ui-kanban__card:hover { box-shadow: var(--shadow-md); }
.ui-kanban__card--dragging { opacity: 0.4; }

.ui-kanban__priority { display: block; width: 100%; height: 3px; border-radius: 2px; margin-bottom: var(--spacing-xs); }
.ui-kanban__priority--high { background: var(--color-danger); }
.ui-kanban__priority--medium { background: var(--color-warning); }
.ui-kanban__priority--low { background: var(--color-success); }

.ui-kanban__card-title { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.ui-kanban__card-desc { font-size: var(--font-size-xs); color: var(--color-text-secondary); margin-top: 2px; }
.ui-kanban__card-footer { display: flex; justify-content: space-between; margin-top: var(--spacing-sm); font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-kanban__column--drag-over { background: var(--color-primary-surface); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
