# FiscalUI Framework

## Documento 048 — Accordion

**Nível 3 — Navegação**

**Versão 1.0**

Container vertical de seções expandíveis. Suporta modo single (apenas um aberto) ou múltiplo.

---

```js
class UIAccordion extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.sections = options.sections || [];  // { id, title, content, icon, expanded }
        this.multiple = options.multiple || false;
        this._expanded = new Set(
            this.sections.filter(s => s.expanded).map(s => s.id)
        );
    }

    template() {
        return `
            <div class="ui-accordion">
                ${this.sections.map(section => `
                    <div class="ui-accordion__section ${this._expanded.has(section.id) ? 'ui-accordion__section--expanded' : ''}">
                        <button class="ui-accordion__header" data-section="${section.id}">
                            ${section.icon ? `<span class="ui-accordion__icon">${FiscalUI.icons.render(section.icon, { size: 16 })}</span>` : ''}
                            <span class="ui-accordion__title">${section.title}</span>
                            <span class="ui-accordion__arrow">${FiscalUI.icons.render('chevron-down', { size: 16 })}</span>
                        </button>
                        <div class="ui-accordion__body" ${this._expanded.has(section.id) ? '' : 'hidden'}>
                            <div class="ui-accordion__content">${section.content || ''}</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    onInit() {
        this.queryAll('.ui-accordion__header').forEach(header => {
            header.addEventListener('click', () => this.toggle(header.dataset.section));
        });
    }

    toggle(sectionId) {
        if (this._expanded.has(sectionId)) {
            this.collapse(sectionId);
        } else {
            this.expand(sectionId);
        }
    }

    expand(sectionId) {
        if (!this.multiple) {
            this._expanded.forEach(id => {
                if (id !== sectionId) this._setExpanded(id, false);
            });
            this._expanded.clear();
        }
        this._expanded.add(sectionId);
        this._setExpanded(sectionId, true);
        this.emit('accordion:expand', { section: sectionId });
    }

    collapse(sectionId) {
        this._expanded.delete(sectionId);
        this._setExpanded(sectionId, false);
        this.emit('accordion:collapse', { section: sectionId });
    }

    _setExpanded(sectionId, expanded) {
        const section = this.query(`.ui-accordion__header[data-section="${sectionId}"]`)?.closest('.ui-accordion__section');
        if (!section) return;
        section.classList.toggle('ui-accordion__section--expanded', expanded);
        const body = section.querySelector('.ui-accordion__body');
        if (body) body.hidden = !expanded;
    }
}
```

```css
.ui-accordion__section {
    border: 1px solid var(--color-border);
    border-top: none;
}
.ui-accordion__section:first-child { border-top: 1px solid var(--color-border); border-radius: var(--radius-md) var(--radius-md) 0 0; }
.ui-accordion__section:last-child { border-radius: 0 0 var(--radius-md) var(--radius-md); }

.ui-accordion__header {
    display: flex; align-items: center; gap: var(--spacing-sm);
    width: 100%; padding: var(--spacing-md);
    border: none; background: transparent; cursor: pointer;
    font-size: var(--font-size-md); color: var(--color-text);
    text-align: left; transition: background var(--motion-fast);
}
.ui-accordion__header:hover { background: var(--color-surface-hover); }

.ui-accordion__title { flex: 1; font-weight: var(--font-weight-medium); }
.ui-accordion__arrow { transition: transform var(--motion-fast); color: var(--color-text-secondary); }
.ui-accordion__section--expanded .ui-accordion__arrow { transform: rotate(180deg); }

.ui-accordion__body { border-top: 1px solid var(--color-border); }
.ui-accordion__content { padding: var(--spacing-md); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
