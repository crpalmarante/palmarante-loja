# FiscalUI Framework

## Documento 050 — Tree Menu

**Nível 3 — Navegação**

**Versão 1.0**

Menu hierárquico em árvore. Suporta expansão/collapso de nós, seleção, ícones e ações contextuais.

---

```js
class UITreeMenu extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.nodes = options.nodes || [];   // { id, label, icon, children, expanded, selected, action }
    }

    template() {
        return `<nav class="ui-tree" role="tree">${this._renderNodes(this.nodes)}</nav>`;
    }

    _renderNodes(nodes, depth = 0) {
        return `<ul class="ui-tree__list" role="group" ${depth === 0 ? 'role="tree"' : ''}>
            ${nodes.map(node => `
                <li class="ui-tree__item" role="treeitem" data-id="${node.id}">
                    <div class="ui-tree__node ${node.selected ? 'ui-tree__node--selected' : ''} ${node.disabled ? 'ui-tree__node--disabled' : ''}"
                         style="padding-left: ${16 + depth * 20}px">
                        ${node.children?.length
                            ? `<button class="ui-tree__toggle" aria-label="${node.expanded ? 'Recolher' : 'Expandir'}">
                                ${FiscalUI.icons.render('chevron-right', { size: 14 })}</button>`
                            : '<span class="ui-tree__spacer"></span>'
                        }
                        ${node.icon ? `<span class="ui-tree__icon">${FiscalUI.icons.render(node.icon, { size: 16 })}</span>` : ''}
                        <span class="ui-tree__label">${node.label}</span>
                    </div>
                    ${node.children?.length ? `
                        <div class="ui-tree__children ${node.expanded ? '' : 'ui-tree__children--collapsed'}">
                            ${this._renderNodes(node.children, depth + 1)}
                        </div>` : ''}
                </li>
            `).join('')}
        </ul>`;
    }

    onInit() {
        this.queryAll('.ui-tree__toggle').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const item = btn.closest('.ui-tree__item');
                this._toggleNode(item);
            });
        });
        this.queryAll('.ui-tree__node').forEach(node => {
            node.addEventListener('click', () => {
                if (node.classList.contains('ui-tree__node--disabled')) return;
                this._selectNode(node);
            });
        });
    }

    _toggleNode(item) {
        const children = item.querySelector('.ui-tree__children');
        const expanded = children?.classList.contains('ui-tree__children--collapsed');
        if (children) children.classList.toggle('ui-tree__children--collapsed', !expanded);
        const toggle = item.querySelector('.ui-tree__toggle');
        if (toggle) toggle.classList.toggle('ui-tree__toggle--expanded', expanded);
        this.emit('tree:toggle', { id: item.dataset.id, expanded });
    }

    _selectNode(node) {
        this.queryAll('.ui-tree__node--selected').forEach(n => n.classList.remove('ui-tree__node--selected'));
        node.classList.add('ui-tree__node--selected');
        this.emit('tree:select', { id: node.closest('.ui-tree__item')?.dataset.id });
    }
}
```

```css
.ui-tree__list { list-style: none; margin: 0; padding: 0; }
.ui-tree__item { margin: 0; }
.ui-tree__node { display: flex; align-items: center; gap: var(--spacing-xs); padding: 4px var(--spacing-sm); cursor: pointer; border-radius: var(--radius-sm); transition: background var(--motion-fast); }
.ui-tree__node:hover { background: var(--color-surface-hover); }
.ui-tree__node--selected { background: var(--color-primary-surface); color: var(--color-primary); }
.ui-tree__node--disabled { opacity: 0.4; cursor: not-allowed; }
.ui-tree__toggle { border: none; background: transparent; cursor: pointer; padding: 0; display: flex; transition: transform var(--motion-fast); color: var(--color-text-muted); }
.ui-tree__toggle--expanded { transform: rotate(90deg); }
.ui-tree__spacer { width: 14px; }
.ui-tree__icon { flex-shrink: 0; color: var(--color-text-secondary); }
.ui-tree__label { font-size: var(--font-size-sm); }
.ui-tree__children { overflow: hidden; }
.ui-tree__children--collapsed { display: none; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
