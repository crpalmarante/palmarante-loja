# FiscalUI Framework

## Documento 097 — File Manager

**Nível 5 — Enterprise Components**

**Versão 1.0**

Gerenciador de arquivos com visualização em grid/lista, navegação por pastas, upload e ações.

---

```js
class UIFileManager extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.files = options.files || [];
        this.view = options.view || 'grid'; // grid, list
        this._path = options.path || '/';
    }

    template() {
        return `
            <div class="ui-filemanager">
                <div class="ui-filemanager__toolbar">
                    <div class="ui-filemanager__breadcrumb">${this._renderBreadcrumb()}</div>
                    <div class="ui-filemanager__view-toggle">
                        <button class="ui-filemanager__view-btn ${this.view === 'grid' ? 'ui-filemanager__view-btn--active' : ''}" data-view="grid">${FiscalUI.icons.render('grid', { size: 16 })}</button>
                        <button class="ui-filemanager__view-btn ${this.view === 'list' ? 'ui-filemanager__view-btn--active' : ''}" data-view="list">${FiscalUI.icons.render('list', { size: 16 })}</button>
                    </div>
                </div>
                <div class="ui-filemanager__body ${this.view === 'grid' ? 'ui-filemanager__body--grid' : 'ui-filemanager__body--list'}">
                    ${this.files.map(f => this.view === 'grid' ? this._renderGridItem(f) : this._renderListItem(f)).join('')}
                </div>
            </div>
        `;
    }

    _renderBreadcrumb() {
        const parts = this._path.split('/').filter(Boolean);
        return `<span class="ui-filemanager__bread-item" data-path="/">Raiz</span>` +
            parts.map((p, i) => {
                const path = '/' + parts.slice(0, i + 1).join('/');
                return `<span class="ui-filemanager__sep">/</span><span class="ui-filemanager__bread-item" data-path="${path}">${p}</span>`;
            }).join('');
    }

    _renderGridItem(f) {
        const isFolder = f.type === 'folder';
        return `<div class="ui-filemanager__item" data-name="${f.name}" data-type="${f.type}">
            <div class="ui-filemanager__item-icon">
                ${isFolder ? FiscalUI.icons.render('folder', { size: 32 }) : this._fileIcon(f.name)}
            </div>
            <span class="ui-filemanager__item-name">${f.name}</span>
            <span class="ui-filemanager__item-size">${f.size || ''}</span>
        </div>`;
    }

    _renderListItem(f) {
        const isFolder = f.type === 'folder';
        return `<div class="ui-filemanager__list-item" data-name="${f.name}" data-type="${f.type}">
            <span class="ui-filemanager__list-icon">${isFolder ? FiscalUI.icons.render('folder', { size: 18 }) : this._fileIcon(f.name, 18)}</span>
            <span class="ui-filemanager__list-name">${f.name}</span>
            <span class="ui-filemanager__list-size">${f.size || '-'}</span>
            <span class="ui-filemanager__list-date">${f.date || '-'}</span>
            <div class="ui-filemanager__list-actions">
                <button class="ui-filemanager__action" data-action="rename" title="Renomear">${FiscalUI.icons.render('edit', { size: 14 })}</button>
                <button class="ui-filemanager__action" data-action="delete" title="Excluir">${FiscalUI.icons.render('trash', { size: 14 })}</button>
            </div>
        </div>`;
    }

    _fileIcon(name, size = 32) {
        const ext = name.split('.').pop()?.toLowerCase();
        const icons = { pdf: 'file-text', doc: 'file-text', xls: 'grid', jpg: 'image', png: 'image', zip: 'archive' };
        return FiscalUI.icons.render(icons[ext] || 'file', { size });
    }

    onInit() {
        this.queryAll('.ui-filemanager__view-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.view = btn.dataset.view;
                this.query('.ui-filemanager__body').className = `ui-filemanager__body ui-filemanager__body--${this.view}`;
                this.queryAll('.ui-filemanager__view-btn').forEach(b => b.classList.remove('ui-filemanager__view-btn--active'));
                btn.classList.add('ui-filemanager__view-btn--active');
            });
        });

        this.queryAll('.ui-filemanager__bread-item, .ui-filemanager__item[data-type="folder"], .ui-filemanager__list-item[data-type="folder"]').forEach(el => {
            el.addEventListener('click', () => {
                const path = el.dataset.path || el.dataset.name;
                if (path) this.emit('filemanager:navigate', { path });
            });
        });
    }

    setFiles(files) { this.files = files; this.render(); }
    setPath(path) { this._path = path; this.render(); }
}
```

```css
.ui-filemanager { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }

.ui-filemanager__toolbar { display: flex; align-items: center; justify-content: space-between; padding: var(--spacing-sm) var(--spacing-md); border-bottom: 1px solid var(--color-border); background: var(--color-surface); }
.ui-filemanager__breadcrumb { display: flex; align-items: center; gap: 2px; font-size: var(--font-size-sm); }
.ui-filemanager__bread-item { cursor: pointer; color: var(--color-text-secondary); }
.ui-filemanager__bread-item:hover { color: var(--color-primary); }
.ui-filemanager__sep { color: var(--color-text-muted); }

.ui-filemanager__view-toggle { display: flex; gap: 2px; }
.ui-filemanager__view-btn { border: none; background: transparent; cursor: pointer; padding: 4px; border-radius: var(--radius-sm); color: var(--color-text-muted); display: flex; }
.ui-filemanager__view-btn:hover { background: var(--color-surface-hover); }
.ui-filemanager__view-btn--active { color: var(--color-primary); background: var(--color-primary-surface); }

.ui-filemanager__body--grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: var(--spacing-xs); padding: var(--spacing-sm); }
.ui-filemanager__body--list { display: flex; flex-direction: column; }

.ui-filemanager__item { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: var(--spacing-md); border-radius: var(--radius-md); cursor: pointer; transition: background var(--motion-fast); text-align: center; }
.ui-filemanager__item:hover { background: var(--color-surface-hover); }
.ui-filemanager__item-icon { color: var(--color-text-secondary); }
.ui-filemanager__item-name { font-size: var(--font-size-xs); word-break: break-all; line-height: 1.3; }
.ui-filemanager__item-size { font-size: 10px; color: var(--color-text-muted); }

.ui-filemanager__list-item { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-sm) var(--spacing-md); border-bottom: 1px solid var(--color-border); cursor: pointer; transition: background var(--motion-fast); }
.ui-filemanager__list-item:hover { background: var(--color-surface-hover); }
.ui-filemanager__list-icon { color: var(--color-text-secondary); }
.ui-filemanager__list-name { flex: 1; font-size: var(--font-size-sm); }
.ui-filemanager__list-size, .ui-filemanager__list-date { width: 80px; font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-filemanager__list-actions { display: flex; gap: 2px; opacity: 0; transition: opacity var(--motion-fast); }
.ui-filemanager__list-item:hover .ui-filemanager__list-actions { opacity: 1; }
.ui-filemanager__action { border: none; background: transparent; cursor: pointer; padding: 2px; border-radius: var(--radius-sm); color: var(--color-text-muted); display: flex; }
.ui-filemanager__action:hover { background: var(--color-surface-hover); color: var(--color-text); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
