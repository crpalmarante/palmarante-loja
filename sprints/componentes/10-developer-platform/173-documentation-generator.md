# FiscalUI Framework

## Documento 173 — Documentation Generator

**Nível 10 — Developer Platform**

**Versão 1.0**

Gerador automático de documentação a partir do código fonte e comentários JSDoc.

---

```bash
fiscalui docs                   # Gera docs da aplicação
fiscalui docs --serve           # Gera + servidor local
fiscalui docs --component Card  # Documenta componente específico
fiscalui docs --publish         # Publica no GitHub Pages
```

```js
// Comentários JSDoc extraídos
/**
 * @component Button
 * @description Botão com variantes de cor, tamanho e estado.
 * @extends UIComponent
 * @tag ui-button
 *
 * @prop {string} label - Texto do botão
 * @prop {'primary'|'secondary'|'ghost'|'danger'} variant - Variante visual
 * @prop {'sm'|'md'|'lg'} size - Tamanho
 * @prop {boolean} disabled - Estado desabilitado
 *
 * @slot default - Conteúdo do botão
 *
 * @event click - Disparado ao clicar
 * @event focus - Disparado ao receber foco
 *
 * @css .ui-btn - Botão base
 * @css .ui-btn__label - Label interno
 * @css .ui-btn--primary - Variante primary
 * @css .ui-btn--lg - Tamanho large
 *
 * @example
 * <ui-button label="Salvar" variant="primary"></ui-button>
 */
```

```markdown
<!-- Documentação gerada -->
# Button

> Botão com variantes de cor, tamanho e estado.

## Propriedades

| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| label | `string` | `'Button'` | Texto do botão |
| variant | `'primary' \| 'secondary' \| 'ghost' \| 'danger'` | `'primary'` | Variante visual |
| size | `'sm' \| 'md' \| 'lg'` | `'md'` | Tamanho |
| disabled | `boolean` | `false` | Estado desabilitado |

## Eventos

| Evento | Descrição |
|--------|-----------|
| `click` | Disparado ao clicar |
| `focus` | Disparado ao receber foco |

## Exemplo

```html
<ui-button label="Salvar" variant="primary"></ui-button>
```
```

```js
// Gerador
class DocGenerator {
  constructor(sourceDir, outDir) {
    this.sourceDir = sourceDir;
    this.outDir = outDir;
  }

  generate() {
    const files = this._findSourceFiles();
    const docs = files.map(f => this._parseJSDoc(f));
    this._renderIndex(docs);
    this._renderComponents(docs);
    this._renderSidebar(docs);
  }

  _parseJSDoc(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const comments = content.match(/\/\*\*[\s\S]*?\*\//g) || [];
    return comments.map(c => this._extractTags(c));
  }

  _extractTags(comment) {
    return {
      component: comment.match(/@component\s+(\w+)/)?.[1],
      description: comment.match(/@description\s+(.+)/)?.[1],
      props: [...comment.matchAll(/@prop\s+\{(\S+)\}\s+(\w+)\s*-\s*(.+)/g)].map(m => ({ type: m[1], name: m[2], desc: m[3] })),
      events: [...comment.matchAll(/@event\s+(\w+)\s*-\s*(.+)/g)].map(m => ({ name: m[1], desc: m[2] })),
      examples: [...comment.matchAll(/@example\s+([\s\S]*?)(?=\n\s*\*\/|\n\s*\* @)/g)].map(m => m[1].trim())
    };
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
