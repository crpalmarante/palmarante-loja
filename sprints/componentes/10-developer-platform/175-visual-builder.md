# FiscalUI Framework

## Documento 175 — Visual Builder

**Nível 10 — Developer Platform**

**Versão 1.0**

Construtor visual de interfaces — drag & drop, canvas, paleta de componentes e property grid.

---

```html
<div class="ui-visual-builder">
    <div class="ui-visual-builder__toolbar">
        <div class="ui-visual-builder__actions">
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="undo">↩ Desfazer</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="redo">↪ Refazer</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="preview">👁 Preview</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="code">&lt;/&gt; Código</button>
            <button class="ui-btn ui-btn--primary ui-btn--sm" data-action="save">💾 Salvar</button>
        </div>
        <div class="ui-visual-builder__view-options">
            <button class="ui-btn ui-btn--ghost ui-btn--xs" data-view="desktop">🖥</button>
            <button class="ui-btn ui-btn--ghost ui-btn--xs" data-view="tablet">📱</button>
            <button class="ui-btn ui-btn--ghost ui-btn--xs" data-view="mobile">📲</button>
        </div>
    </div>

    <div class="ui-visual-builder__main">
        <div class="ui-visual-builder__palette">
            <h4 class="ui-visual-builder__palette-title">Componentes</h4>
            <div class="ui-visual-builder__palette-search">
                <input class="ui-field__input" placeholder="Buscar...">
            </div>
            <div class="ui-visual-builder__palette-items">
                <div class="ui-visual-builder__palette-item" draggable="true" data-component="Button">
                    <span class="ui-visual-builder__palette-icon">▢</span>
                    <span>Button</span>
                </div>
                <div class="ui-visual-builder__palette-item" draggable="true" data-component="Input">
                    <span class="ui-visual-builder__palette-icon">⎕</span>
                    <span>Input</span>
                </div>
                <div class="ui-visual-builder__palette-item" draggable="true" data-component="Card">
                    <span class="ui-visual-builder__palette-icon">▬</span>
                    <span>Card</span>
                </div>
                <div class="ui-visual-builder__palette-item" draggable="true" data-component="DataGrid">
                    <span class="ui-visual-builder__palette-icon">⊞</span>
                    <span>Data Grid</span>
                </div>
            </div>
        </div>

        <div class="ui-visual-builder__canvas">
            <div class="ui-visual-builder__canvas-area" data-drop-zone>
                <div class="ui-visual-builder__placeholder">
                    Arraste componentes aqui
                </div>
            </div>
        </div>

        <div class="ui-visual-builder__properties">
            <h4 class="ui-visual-builder__properties-title">Propriedades</h4>
            <div class="ui-visual-builder__property-group">
                <label class="ui-visual-builder__property-label">Label</label>
                <input class="ui-field__input" value="Button">
            </div>
            <div class="ui-visual-builder__property-group">
                <label class="ui-visual-builder__property-label">Variant</label>
                <select class="ui-field__select">
                    <option>primary</option>
                    <option>secondary</option>
                    <option>ghost</option>
                    <option>danger</option>
                </select>
            </div>
            <div class="ui-visual-builder__property-group">
                <label class="ui-visual-builder__property-label">Size</label>
                <select class="ui-field__select">
                    <option>sm</option>
                    <option selected>md</option>
                    <option>lg</option>
                </select>
            </div>
        </div>
    </div>
</div>
```

```css
.ui-visual-builder { display: flex; flex-direction: column; height: 100vh; background: var(--color-bg); }
.ui-visual-builder__toolbar { display: flex; justify-content: space-between; padding: var(--spacing-sm); background: var(--color-surface); border-bottom: 1px solid var(--color-border); }
.ui-visual-builder__main { display: flex; flex: 1; overflow: hidden; }
.ui-visual-builder__palette { width: 240px; background: var(--color-surface); border-right: 1px solid var(--color-border); display: flex; flex-direction: column; }
.ui-visual-builder__palette-title { padding: var(--spacing-sm); margin: 0; font-size: var(--font-size-sm); border-bottom: 1px solid var(--color-border); }
.ui-visual-builder__palette-search { padding: var(--spacing-sm); }
.ui-visual-builder__palette-items { flex: 1; overflow-y: auto; padding: var(--spacing-sm); display: flex; flex-direction: column; gap: 4px; }
.ui-visual-builder__palette-item { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-xs) var(--spacing-sm); background: var(--color-surface-alt); border-radius: var(--radius-sm); cursor: grab; font-size: var(--font-size-sm); }
.ui-visual-builder__palette-item:hover { background: var(--color-primary-light); }
.ui-visual-builder__canvas { flex: 1; padding: var(--spacing-md); overflow: auto; }
.ui-visual-builder__canvas-area { min-height: 100%; border: 2px dashed var(--color-border); border-radius: var(--radius-lg); padding: var(--spacing-md); }
.ui-visual-builder__placeholder { display: flex; align-items: center; justify-content: center; height: 200px; color: var(--color-text-muted); font-size: var(--font-size-lg); }
.ui-visual-builder__properties { width: 280px; background: var(--color-surface); border-left: 1px solid var(--color-border); padding: var(--spacing-sm); }
.ui-visual-builder__properties-title { margin: 0 0 var(--spacing-sm); font-size: var(--font-size-sm); }
.ui-visual-builder__property-group { margin-bottom: var(--spacing-sm); }
.ui-visual-builder__property-label { display: block; font-size: var(--font-size-xs); color: var(--color-text-muted); margin-bottom: 2px; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
