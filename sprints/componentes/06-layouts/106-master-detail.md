# FiscalUI Framework

## Documento 106 — Master/Detail

**Nível 6 — Layouts**

**Versão 1.0**

Layout de mestre-detalhe com lista à esquerda e conteúdo detalhado à direita.

---

```js
class MasterDetailLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.masterTitle = options.masterTitle || 'Lista';
        this.masterWidth = options.masterWidth || 360;
        this.master = options.master || '';
        this.detail = options.detail || '';
        this._detailVisible = false;
    }

    template() {
        return `
            <div class="ui-layout-md">
                <div class="ui-layout-md__master" style="width: ${this.masterWidth}px">
                    <div class="ui-layout-md__master-header">
                        <h3 class="ui-layout-md__master-title">${this.masterTitle}</h3>
                        <div class="ui-layout-md__master-actions"></div>
                    </div>
                    <div class="ui-layout-md__master-list">${this.master}</div>
                </div>
                <div class="ui-layout-md__divider"></div>
                <div class="ui-layout-md__detail" ${this.detail ? '' : 'hidden'}>
                    <div class="ui-layout-md__detail-header">
                        <button class="ui-layout-md__back" aria-label="Voltar">${FiscalUI.icons.render('chevron-left', { size: 16 })}</button>
                        <h3 class="ui-layout-md__detail-title">Detalhes</h3>
                        <div class="ui-layout-md__detail-actions"></div>
                    </div>
                    <div class="ui-layout-md__detail-body">${this.detail}</div>
                </div>
            </div>
        `;
    }

    onInit() {
        this._master = this.query('.ui-layout-md__master-list');
        this._detail = this.query('.ui-layout-md__detail');
        this._detailBody = this.query('.ui-layout-md__detail-body');
        this._detailTitle = this.query('.ui-layout-md__detail-title');
        this._detailActions = this.query('.ui-layout-md__detail-actions');

        this.query('.ui-layout-md__back')?.addEventListener('click', () => this.hideDetail());
    }

    showDetail(title, content) {
        if (this._detailTitle) this._detailTitle.textContent = title || 'Detalhes';
        if (this._detailBody) this._detailBody.innerHTML = content || '';
        this._detail.hidden = false;
        this._detailVisible = true;
        this.element.classList.add('ui-layout-md--detail-open');
        this.emit('layout:detail-open', { title });
    }

    hideDetail() {
        this._detail.hidden = true;
        this._detailVisible = false;
        this.element.classList.remove('ui-layout-md--detail-open');
        this.emit('layout:detail-close');
    }

    setMaster(html) { if (this._master) this._master.innerHTML = html; }
    setDetailActions(html) { if (this._detailActions) this._detailActions.innerHTML = html; }
}
```

```css
.ui-layout-md { display: flex; height: 100%; overflow: hidden; }

.ui-layout-md__master { display: flex; flex-direction: column; border-right: 1px solid var(--color-border); flex-shrink: 0; }
.ui-layout-md__master-header { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-layout-md__master-title { font-size: var(--font-size-md); margin: 0; font-weight: var(--font-weight-semibold); }
.ui-layout-md__master-list { flex: 1; overflow-y: auto; }

.ui-layout-md__divider { width: 4px; cursor: col-resize; background: var(--color-surface-hover); flex-shrink: 0; }
.ui-layout-md__divider:hover { background: var(--color-primary-surface); }

.ui-layout-md__detail { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.ui-layout-md__detail-header { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-layout-md__back { border: none; background: transparent; cursor: pointer; color: var(--color-text-secondary); padding: 4px; border-radius: var(--radius-sm); display: flex; }
.ui-layout-md__back:hover { background: var(--color-surface-hover); }
.ui-layout-md__detail-title { flex: 1; font-size: var(--font-size-md); margin: 0; font-weight: var(--font-weight-semibold); }
.ui-layout-md__detail-body { flex: 1; overflow-y: auto; padding: var(--spacing-md); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
