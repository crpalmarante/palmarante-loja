# FiscalUI Framework

## Documento 152 — Product Card

**Nível 9 — ERP Business Components**

**Versão 1.0**

Ficha resumo do produto com dados comerciais, fiscais (NCM, CST, CFOP) e estoque.

---

```html
<div class="ui-product-card">
    <div class="ui-product-card__header">
        <div class="ui-product-card__thumb">
            <img src="placeholder.png" alt="Produto">
        </div>
        <div class="ui-product-card__info">
            <h3 class="ui-product-card__name">Arroz Parboilizado Tipo 1 5kg</h3>
            <span class="ui-product-card__sku">SKU: ARZ-001</span>
            <span class="ui-product-card__gtin">GTIN: 7891234567890</span>
        </div>
        <div class="ui-product-card__price">
            <span class="ui-product-card__price-value">R$ 22,90</span>
            <span class="ui-product-card__price-unit">unidade</span>
        </div>
    </div>

    <div class="ui-product-card__body">
        <div class="ui-product-card__section">
            <h4>Classificação Fiscal</h4>
            <div class="ui-product-card__field"><label>NCM</label><span>1006.30.11</span></div>
            <div class="ui-product-card__field"><label>CST ICMS</label><span>00</span></div>
            <div class="ui-product-card__field"><label>CST PIS</label><span>01</span></div>
            <div class="ui-product-card__field"><label>CST COFINS</label><span>01</span></div>
            <div class="ui-product-card__field"><label>CFOP</label><span>5.102</span></div>
            <div class="ui-product-card__field"><label>NCM Ex</label><span>0</span></div>
        </div>
        <div class="ui-product-card__section">
            <h4>Estoque</h4>
            <div class="ui-product-card__field"><label>Atual</label><span>342</span></div>
            <div class="ui-product-card__field"><label>Mínimo</label><span>50</span></div>
            <div class="ui-product-card__field"><label>Máximo</label><span>500</span></div>
            <div class="ui-product-card__field"><label>Local</label><span>Armazém A - Rack 12</span></div>
            <div class="ui-product-card__stock-bar">
                <div class="ui-product-card__stock-fill" style="width:68%"></div>
            </div>
        </div>
        <div class="ui-product-card__section">
            <h4>Dimensões</h4>
            <div class="ui-product-card__field"><label>Peso</label><span>5,200 kg</span></div>
            <div class="ui-product-card__field"><label>Volume</label><span>0,008 m³</span></div>
        </div>
    </div>

    <div class="ui-product-card__footer">
        <button class="ui-btn ui-btn--ghost ui-btn--sm">Editar</button>
        <button class="ui-btn ui-btn--ghost ui-btn--sm">Histórico</button>
        <button class="ui-btn ui-btn--primary ui-btn--sm" data-action="sell">Vender</button>
    </div>
</div>
```

```css
.ui-product-card { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.ui-product-card__header { display: flex; align-items: center; gap: var(--spacing-md); padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-product-card__thumb { width: 64px; height: 64px; border-radius: var(--radius-md); background: var(--color-surface-alt); overflow: hidden; }
.ui-product-card__thumb img { width: 100%; height: 100%; object-fit: cover; }
.ui-product-card__info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.ui-product-card__name { margin: 0; font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.ui-product-card__sku, .ui-product-card__gtin { font-size: var(--font-size-xs); color: var(--color-text-secondary); }
.ui-product-card__price { text-align: right; }
.ui-product-card__price-value { display: block; font-size: var(--font-size-xl); font-weight: var(--font-weight-bold); color: var(--color-primary); }
.ui-product-card__price-unit { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-product-card__body { padding: var(--spacing-md); display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--spacing-md); }
.ui-product-card__section h4 { margin: 0 0 var(--spacing-xs); font-size: var(--font-size-xs); text-transform: uppercase; color: var(--color-text-muted); letter-spacing: 0.5px; }
.ui-product-card__field { display: flex; justify-content: space-between; padding: 2px 0; font-size: var(--font-size-sm); }
.ui-product-card__field label { color: var(--color-text-secondary); }
.ui-product-card__field span { font-weight: var(--font-weight-medium); }
.ui-product-card__stock-bar { height: 6px; background: var(--color-surface-alt); border-radius: var(--radius-full); margin-top: var(--spacing-sm); }
.ui-product-card__stock-fill { height: 100%; background: var(--color-success); border-radius: var(--radius-full); transition: width 0.3s; }

.ui-product-card__footer { display: flex; justify-content: flex-end; gap: var(--spacing-sm); padding: var(--spacing-sm) var(--spacing-md); border-top: 1px solid var(--color-border); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
