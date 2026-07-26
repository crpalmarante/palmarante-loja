# FiscalUI Framework

## Documento 155 — Company Widget

**Nível 9 — ERP Business Components**

**Versão 1.0**

Widget de dados da empresa (emitente) com CNPJ, IE, CRT, endereço e regime tributário.

---

```html
<div class="ui-company-widget">
    <div class="ui-company-widget__header">
        <div class="ui-company-widget__brand">
            <div class="ui-company-widget__logo">
                <img src="logo-empresa.png" alt="Logo">
            </div>
            <div class="ui-company-widget__identification">
                <h3 class="ui-company-widget__name">Empresa Exemplo Ltda</h3>
                <span class="ui-company-widget__alias">Nome Fantasia</span>
            </div>
        </div>
        <div class="ui-company-widget__regime-badge ui-company-widget__regime-badge--simples">
            Simples Nacional
        </div>
    </div>

    <div class="ui-company-widget__body">
        <div class="ui-company-widget__section">
            <h4>Dados Cadastrais</h4>
            <div class="ui-company-widget__field"><label>CNPJ</label><span>11.222.333/0001-44</span></div>
            <div class="ui-company-widget__field"><label>IE</label><span>123.456.789.000</span></div>
            <div class="ui-company-widget__field"><label>IM</label><span>8.765</span></div>
            <div class="ui-company-widget__field"><label>CRT</label><span>1 — Simples Nacional</span></div>
            <div class="ui-company-widget__field"><label>CNAE</label><span>47.11-3-00</span></div>
            <div class="ui-company-widget__field"><label>Regime PIS/COFINS</label><span>Monofásico</span></div>
        </div>
        <div class="ui-company-widget__section">
            <h4>Endereço</h4>
            <div class="ui-company-widget__field"><label>CEP</label><span>01001-000</span></div>
            <div class="ui-company-widget__field"><label>Logradouro</label><span>Rua Exemplo, 123</span></div>
            <div class="ui-company-widget__field"><label>Bairro</label><span>Centro</span></div>
            <div class="ui-company-widget__field"><label>Cidade</label><span>São Paulo - SP</span></div>
        </div>
        <div class="ui-company-widget__section">
            <h4>Certificado Digital</h4>
            <div class="ui-company-widget__field"><label>Tipo</label><span>A1 (ICP-Brasil)</span></div>
            <div class="ui-company-widget__field"><label>Vencimento</label><span>31/12/2026</span></div>
            <div class="ui-company-widget__field"><label>Emissor</label><span>Certisign</span></div>
            <div class="ui-company-widget__status-indicator ui-company-widget__status-indicator--valid">
                Certificado Válido (180 dias restantes)
            </div>
        </div>
    </div>
</div>
```

```css
.ui-company-widget { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.ui-company-widget__header { display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-md); border-bottom: 1px solid var(--color-border); }
.ui-company-widget__brand { display: flex; align-items: center; gap: var(--spacing-md); }
.ui-company-widget__logo { width: 48px; height: 48px; border-radius: var(--radius-md); overflow: hidden; background: var(--color-surface-alt); }
.ui-company-widget__logo img { width: 100%; height: 100%; object-fit: contain; }
.ui-company-widget__name { margin: 0; font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold); }
.ui-company-widget__alias { font-size: var(--font-size-sm); color: var(--color-text-secondary); }
.ui-company-widget__regime-badge { padding: 4px 12px; border-radius: var(--radius-full); font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); }
.ui-company-widget__regime-badge--simples { background: var(--color-success-light); color: var(--color-success); }
.ui-company-widget__regime-badge--normal { background: var(--color-primary-light); color: var(--color-primary); }
.ui-company-widget__regime-badge--mei { background: var(--color-warning-light); color: var(--color-warning); }
.ui-company-widget__body { padding: var(--spacing-md); display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--spacing-md); }
.ui-company-widget__section h4 { margin: 0 0 var(--spacing-xs); font-size: var(--font-size-xs); text-transform: uppercase; color: var(--color-text-muted); letter-spacing: 0.5px; }
.ui-company-widget__field { display: flex; justify-content: space-between; padding: 2px 0; font-size: var(--font-size-sm); }
.ui-company-widget__field label { color: var(--color-text-secondary); }
.ui-company-widget__field span { font-weight: var(--font-weight-medium); }
.ui-company-widget__status-indicator { margin-top: var(--spacing-sm); padding: var(--spacing-xs) var(--spacing-sm); border-radius: var(--radius-sm); font-size: var(--font-size-xs); font-weight: var(--font-weight-medium); }
.ui-company-widget__status-indicator--valid { background: var(--color-success-light); color: var(--color-success); }
.ui-company-widget__status-indicator--expiring { background: var(--color-warning-light); color: var(--color-warning); }
.ui-company-widget__status-indicator--expired { background: var(--color-danger-light); color: var(--color-danger); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
