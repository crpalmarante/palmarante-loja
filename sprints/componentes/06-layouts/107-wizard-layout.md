# FiscalUI Framework

## Documento 107 — Wizard Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout de assistente (wizard) com etapas, navegação anterior/próximo e stepper.

---

```js
class WizardLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.steps = options.steps || [];
        this._currentStep = 0;
    }

    template() {
        return `
            <div class="ui-layout-wizard">
                <div class="ui-layout-wizard__stepper">
                    ${this.steps.map((s, i) => `
                        <div class="ui-layout-wizard__step ${i <= this._currentStep ? 'ui-layout-wizard__step--completed' : ''} ${i === this._currentStep ? 'ui-layout-wizard__step--active' : ''}">
                            <span class="ui-layout-wizard__step-num">${i < this._currentStep ? '✓' : i + 1}</span>
                            <span class="ui-layout-wizard__step-label">${s.label}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="ui-layout-wizard__body">
                    <div class="ui-layout-wizard__content"></div>
                </div>
                <div class="ui-layout-wizard__footer">
                    <button class="ui-btn ui-btn--ghost" data-action="cancel">Cancelar</button>
                    <div class="ui-layout-wizard__nav">
                        <button class="ui-btn ui-btn--outline" data-action="prev" ${this._currentStep === 0 ? 'disabled' : ''}>Anterior</button>
                        <button class="ui-btn ui-btn--primary" data-action="next">${this._currentStep === this.steps.length - 1 ? 'Concluir' : 'Próximo'}</button>
                    </div>
                </div>
            </div>
        `;
    }

    onInit() {
        this._content = this.query('.ui-layout-wizard__content');
        this._steps = this.queryAll('.ui-layout-wizard__step');

        this.query('[data-action="prev"]')?.addEventListener('click', () => this.prev());
        this.query('[data-action="next"]')?.addEventListener('click', () => this.next());
        this.query('[data-action="cancel"]')?.addEventListener('click', () => this.emit('wizard:cancel'));
    }

    goTo(index) {
        if (index < 0 || index >= this.steps.length) return;
        this._currentStep = index;
        this.render();
        this.emit('wizard:change', { step: index, label: this.steps[index]?.label });
    }

    next() {
        if (this._currentStep === this.steps.length - 1) { this.emit('wizard:finish'); return; }
        this.goTo(this._currentStep + 1);
    }

    prev() { this.goTo(this._currentStep - 1); }

    setContent(html) { if (this._content) this._content.innerHTML = html; }
    currentStep() { return this._currentStep; }
}
```

```css
.ui-layout-wizard { display: flex; flex-direction: column; height: 100%; }

.ui-layout-wizard__stepper { display: flex; border-bottom: 1px solid var(--color-border); padding: var(--spacing-md) var(--spacing-lg); gap: 0; }
.ui-layout-wizard__step { display: flex; align-items: center; gap: var(--spacing-sm); flex: 1; position: relative; }
.ui-layout-wizard__step::after { content: ''; flex: 1; height: 1px; background: var(--color-border); margin-left: var(--spacing-sm); }
.ui-layout-wizard__step:last-child::after { display: none; }

.ui-layout-wizard__step-num { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); background: var(--color-surface-hover); color: var(--color-text-muted); flex-shrink: 0; }
.ui-layout-wizard__step--active .ui-layout-wizard__step-num { background: var(--color-primary); color: #fff; }
.ui-layout-wizard__step--completed .ui-layout-wizard__step-num { background: var(--color-success); color: #fff; }

.ui-layout-wizard__step-label { font-size: var(--font-size-sm); color: var(--color-text-muted); white-space: nowrap; }
.ui-layout-wizard__step--active .ui-layout-wizard__step-label { color: var(--color-text); font-weight: var(--font-weight-semibold); }

.ui-layout-wizard__body { flex: 1; overflow-y: auto; padding: var(--spacing-lg); }
.ui-layout-wizard__footer { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md) var(--spacing-lg); border-top: 1px solid var(--color-border); }
.ui-layout-wizard__nav { display: flex; gap: var(--spacing-sm); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
