# FiscalUI Framework

## Documento 095 — Timeline

**Nível 5 — Enterprise Components**

**Versão 1.0**

Linha do tempo vertical com eventos ordenados por data. Suporta ícones, descrição e marcação de períodos.

---

```js
class UITimeline extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.items = options.items || [];
        this.alternate = options.alternate || false;
        this.animated = options.animated || false;
    }

    template() {
        return `
            <div class="ui-timeline ${this.alternate ? 'ui-timeline--alternate' : ''} ${this.animated ? 'ui-timeline--animated' : ''}">
                ${this.items.map((item, i) => `
                    <div class="ui-timeline__item ${this.alternate && i % 2 ? 'ui-timeline__item--right' : ''}">
                        <div class="ui-timeline__dot ${item.variant ? `ui-timeline__dot--${item.variant}` : ''}">
                            ${item.icon ? `<span class="ui-timeline__dot-icon">${FiscalUI.icons.render(item.icon, { size: 14 })}</span>` : ''}
                        </div>
                        <div class="ui-timeline__content">
                            <div class="ui-timeline__date">${item.date || ''}</div>
                            <div class="ui-timeline__title">${item.title || ''}</div>
                            ${item.description ? `<div class="ui-timeline__desc">${item.description}</div>` : ''}
                            ${item.footer ? `<div class="ui-timeline__footer">${item.footer}</div>` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    onInit() {
        if (this.animated) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('ui-timeline__item--visible'); observer.unobserve(e.target); } });
            }, { threshold: 0.2 });
            this.queryAll('.ui-timeline__item').forEach(el => observer.observe(el));
        }
    }

    addItem(item) { this.items.push(item); this.render(); }
}
```

```css
.ui-timeline { position: relative; padding-left: 40px; }
.ui-timeline::before { content: ''; position: absolute; left: 18px; top: 0; bottom: 0; width: 2px; background: var(--color-border); }

.ui-timeline--alternate { padding-left: 0; }
.ui-timeline--alternate::before { left: 50%; margin-left: -1px; }

.ui-timeline__item { position: relative; margin-bottom: var(--spacing-lg); }
.ui-timeline--alternate .ui-timeline__item { width: 50%; }
.ui-timeline--alternate .ui-timeline__item--right { margin-left: 50%; padding-left: var(--spacing-lg); }
.ui-timeline--alternate .ui-timeline__item:not(.ui-timeline__item--right) { padding-right: var(--spacing-lg); text-align: right; }

.ui-timeline__dot {
    position: absolute; left: -30px; top: 4px;
    width: 20px; height: 20px; border-radius: 50%;
    background: var(--color-surface); border: 2px solid var(--color-border);
    display: flex; align-items: center; justify-content: center; z-index: 1;
}
.ui-timeline__dot--primary { border-color: var(--color-primary); }
.ui-timeline__dot--success { border-color: var(--color-success); }
.ui-timeline__dot--warning { border-color: var(--color-warning); }
.ui-timeline__dot--danger { border-color: var(--color-danger); }
.ui-timeline__dot-icon { color: var(--color-text-secondary); }
.ui-timeline--alternate .ui-timeline__item--right .ui-timeline__dot { left: -10px; }
.ui-timeline--alternate .ui-timeline__item:not(.ui-timeline__item--right) .ui-timeline__dot { right: -10px; left: auto; }

.ui-timeline__content { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--spacing-md); }
.ui-timeline__date { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-timeline__title { font-size: var(--font-size-md); font-weight: var(--font-weight-semibold); margin: 2px 0; }
.ui-timeline__desc { font-size: var(--font-size-sm); color: var(--color-text-secondary); line-height: 1.5; }
.ui-timeline__footer { margin-top: var(--spacing-sm); font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-timeline--animated .ui-timeline__item { opacity: 0; transform: translateY(20px); transition: opacity 0.4s ease, transform 0.4s ease; }
.ui-timeline--animated .ui-timeline__item--visible { opacity: 1; transform: translateY(0); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
