# FiscalUI Framework

## Documento 158 — XML Viewer

**Nível 9 — ERP Business Components**

**Versão 1.0**

Visualizador de XML com syntax highlighting, formatação, busca e download.

---

```html
<div class="ui-xml-viewer">
    <div class="ui-xml-viewer__toolbar">
        <div class="ui-xml-viewer__toolbar-left">
            <span class="ui-xml-viewer__file-info">nfe-3526071234567890.xml</span>
            <span class="ui-xml-viewer__file-size">12,4 KB</span>
        </div>
        <div class="ui-xml-viewer__toolbar-right">
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="format">Formatar</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="copy">Copiar</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="download">Download</button>
            <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="validate">Validar</button>
        </div>
    </div>

    <div class="ui-xml-viewer__search">
        <div class="ui-field ui-field--sm ui-field--inline">
            <span class="ui-icon ui-icon--search"></span>
            <input class="ui-field__input" placeholder="Buscar no XML..." data-search>
            <span class="ui-xml-viewer__search-count">0 resultados</span>
        </div>
        <div class="ui-xml-viewer__search-nav">
            <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="prev">▲</button>
            <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="next">▼</button>
        </div>
    </div>

    <div class="ui-xml-viewer__editor">
        <pre class="ui-xml-viewer__content"><code class="language-xml"><span class="ui-xml-tag">&lt;?xml version="1.0" encoding="UTF-8"?&gt;</span>
<span class="ui-xml-tag">&lt;<span class="ui-xml-tagname">nfeProc</span> <span class="ui-xml-attr">xmlns</span>=<span class="ui-xml-value">"http://www.portalfiscal.inf.br/nfe"</span>&gt;</span>
<span class="ui-xml-tag">  &lt;<span class="ui-xml-tagname">NFe</span>&gt;</span>
<span class="ui-xml-tag">    &lt;<span class="ui-xml-tagname">infNFe</span> <span class="ui-xml-attr">Id</span>=<span class="ui-xml-value">"NFe35260712345678901234567890123456781234567890"</span> <span class="ui-xml-attr">versao</span>=<span class="ui-xml-value">"4.00"</span>&gt;</span>
<span class="ui-xml-tag">      &lt;<span class="ui-xml-tagname">ide</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">cUF</span>&gt;</span>35<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">cUF</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">cNF</span>&gt;</span>12345678<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">cNF</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">natOp</span>&gt;</span>Venda de mercadoria<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">natOp</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">mod</span>&gt;</span>55<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">mod</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">serie</span>&gt;</span>1<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">serie</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">nNF</span>&gt;</span>123456<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">nNF</span>&gt;</span>
<span class="ui-xml-tag">        &lt;<span class="ui-xml-tagname">dhEmi</span>&gt;</span>2026-07-15T14:32:05-03:00<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">dhEmi</span>&gt;</span>
<span class="ui-xml-tag">      &lt;/<span class="ui-xml-tagname">ide</span>&gt;</span>
<span class="ui-xml-tag">    &lt;/<span class="ui-xml-tagname">infNFe</span>&gt;</span>
<span class="ui-xml-tag">  &lt;/<span class="ui-xml-tagname">NFe</span>&gt;</span>
<span class="ui-xml-tag">&lt;/<span class="ui-xml-tagname">nfeProc</span>&gt;</span></code></pre>
    </div>

    <div class="ui-xml-viewer__status-bar">
        <span class="ui-xml-viewer__line-info">Linha 15, Coluna 32</span>
        <span class="ui-xml-viewer__validation-info">✅ XML válido — Schema 4.00</span>
    </div>
</div>
```

```css
.ui-xml-viewer { background: #1e1e1e; color: #d4d4d4; border-radius: var(--radius-lg); overflow: hidden; font-family: 'Consolas', 'Monaco', monospace; font-size: var(--font-size-sm); }
.ui-xml-viewer__toolbar, .ui-xml-viewer__status-bar { display: flex; justify-content: space-between; align-items: center; padding: var(--spacing-xs) var(--spacing-md); background: #2d2d2d; border-bottom: 1px solid #3c3c3c; }
.ui-xml-viewer__file-info { font-weight: var(--font-weight-medium); }
.ui-xml-viewer__file-size { font-size: var(--font-size-xs); color: #888; margin-left: var(--spacing-sm); }
.ui-xml-viewer__search { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-xs) var(--spacing-md); background: #252526; border-bottom: 1px solid #3c3c3c; }
.ui-xml-viewer__search .ui-field { flex: 1; }
.ui-xml-viewer__search-count { font-size: var(--font-size-xs); color: #888; }
.ui-xml-viewer__editor { overflow: auto; max-height: 500px; padding: var(--spacing-sm) 0; }
.ui-xml-viewer__content { margin: 0; padding: var(--spacing-sm) var(--spacing-md); line-height: 1.6; }
.ui-xml-tag { color: #569cd6; }
.ui-xml-tagname { color: #569cd6; }
.ui-xml-attr { color: #9cdcfe; }
.ui-xml-value { color: #ce9178; }
.ui-xml-viewer__status-bar { border-top: 1px solid #3c3c3c; border-bottom: none; }
.ui-xml-viewer__line-info { color: #888; font-size: var(--font-size-xs); }
.ui-xml-viewer__validation-info { color: #4ec9b0; font-size: var(--font-size-xs); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
