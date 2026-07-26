# FiscalUI Framework

## Documento 079 — Upload

**Nível 4 — Formulários**

**Versão 1.0**

Campo de upload de arquivos com drag-and-drop, preview, barra de progresso e lista de arquivos.

---

```js
class UIUpload extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.label = options.label || '';
        this.accept = options.accept || '';
        this.multiple = options.multiple || false;
        this.maxSize = options.maxSize || 0;
        this.maxFiles = options.maxFiles || 0;
        this.files = options.files || [];
        this.uploadUrl = options.uploadUrl || '';
        this.onUpload = options.onUpload || null;
        this.rules = options.rules || [];
    }

    template() {
        return `
            <div class="ui-field">
                ${this.label ? `<label class="ui-field__label">${this.label}</label>` : ''}
                <div class="ui-upload">
                    <div class="ui-upload__dropzone">
                        <input class="ui-upload__input" type="file" name="${this.name}"
                               ${this.accept ? `accept="${this.accept}"` : ''}
                               ${this.multiple ? 'multiple' : ''} hidden>
                        <div class="ui-upload__placeholder">
                            <span class="ui-upload__icon">${FiscalUI.icons.render('upload', { size: 32 })}</span>
                            <span class="ui-upload__text">Arraste arquivos aqui ou clique para selecionar</span>
                            <span class="ui-upload__hint">${this.accept ? `Formatos: ${this.accept}` : 'Qualquer formato'}</span>
                        </div>
                    </div>
                    <div class="ui-upload__files" ${this.files.length ? '' : 'hidden'}>
                        ${this.files.map(f => this._renderFile(f)).join('')}
                    </div>
                </div>
                <span class="ui-field__error"></span>
            </div>
        `;
    }

    _renderFile(file) {
        const isImage = file.type?.startsWith('image/');
        const progress = file._progress ?? 0;
        return `
            <div class="ui-upload__file" data-name="${file.name}">
                ${isImage ? `<img class="ui-upload__thumb" src="${file._preview || ''}" alt="">` : `<span class="ui-upload__file-icon">${FiscalUI.icons.render('file', { size: 20 })}</span>`}
                <div class="ui-upload__file-info">
                    <span class="ui-upload__file-name">${file.name}</span>
                    <span class="ui-upload__file-size">${this._formatSize(file.size)}</span>
                </div>
                ${progress > 0 && progress < 100 ? `<div class="ui-upload__progress"><div class="ui-upload__progress-bar" style="width: ${progress}%"></div></div>` : ''}
                <button class="ui-upload__file-remove" aria-label="Remover">&times;</button>
            </div>
        `;
    }

    onInit() {
        this._dropzone = this.query('.ui-upload__dropzone');
        this._input = this.query('.ui-upload__input');
        this._filesContainer = this.query('.ui-upload__files');

        this._dropzone.addEventListener('click', () => this._input.click());
        this._dropzone.addEventListener('dragover', (e) => { e.preventDefault(); this._dropzone.classList.add('ui-upload__dropzone--active'); });
        this._dropzone.addEventListener('dragleave', () => this._dropzone.classList.remove('ui-upload__dropzone--active'));
        this._dropzone.addEventListener('drop', (e) => { e.preventDefault(); this._dropzone.classList.remove('ui-upload__dropzone--active'); this._addFiles([...e.dataTransfer.files]); });

        this._input.addEventListener('change', () => {
            if (this._input.files?.length) this._addFiles([...this._input.files]);
            this._input.value = '';
        });

        this._filesContainer.addEventListener('click', (e) => {
            const remove = e.target.closest('.ui-upload__file-remove');
            if (remove) {
                const name = remove.closest('.ui-upload__file').dataset.name;
                this._removeFile(name);
            }
        });
    }

    _addFiles(newFiles) {
        const files = [...this.files, ...newFiles];
        if (this.maxFiles && files.length > this.maxFiles) {
            this.query('.ui-field__error').textContent = `Máximo de ${this.maxFiles} arquivo(s)`;
            return;
        }
        this.files = files.map(f => {
            if (!f._id) f._id = Date.now() + Math.random();
            if (f.type?.startsWith('image/') && !f._preview) {
                f._preview = URL.createObjectURL(f);
            }
            return f;
        });
        this._sync();
        this.emit('field:change', { name: this.name, files: this.files });
    }

    _removeFile(name) {
        this.files = this.files.filter(f => f.name !== name);
        this._sync();
    }

    _sync() {
        this._filesContainer.innerHTML = this.files.map(f => this._renderFile(f)).join('');
        this._filesContainer.hidden = !this.files.length;
    }

    async upload() {
        if (!this.uploadUrl || !this.files.length) return;
        const formData = new FormData();
        this.files.forEach(f => formData.append(this.name, f, f.name));
        try {
            const resp = await fetch(this.uploadUrl, { method: 'POST', body: formData });
            const result = await resp.json();
            this.onUpload?.(result);
            this.emit('upload:complete', result);
            return result;
        } catch (err) {
            this.emit('upload:error', err);
            throw err;
        }
    }

    _formatSize(bytes) {
        if (!bytes) return '';
        const units = ['B', 'KB', 'MB', 'GB'];
        let i = 0; let size = bytes;
        while (size >= 1024 && i < units.length - 1) { size /= 1024; i++; }
        return `${size.toFixed(1)} ${units[i]}`;
    }

    value() { return this.files; }
    setValue(files) { this.files = files; this._sync(); }
    reset() { this.files = []; this._sync(); }
}
```

```css
.ui-upload__dropzone {
    border: 2px dashed var(--color-border); border-radius: var(--radius-md);
    padding: var(--spacing-xl); text-align: center; cursor: pointer;
    transition: border-color var(--motion-fast), background var(--motion-fast);
}
.ui-upload__dropzone:hover,
.ui-upload__dropzone--active { border-color: var(--color-primary); background: var(--color-primary-surface); }

.ui-upload__placeholder { display: flex; flex-direction: column; align-items: center; gap: var(--spacing-sm); }
.ui-upload__icon { color: var(--color-text-muted); }
.ui-upload__text { font-size: var(--font-size-md); color: var(--color-text); }
.ui-upload__hint { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ui-upload__files { display: flex; flex-direction: column; gap: var(--spacing-xs); margin-top: var(--spacing-sm); }
.ui-upload__file {
    display: flex; align-items: center; gap: var(--spacing-sm);
    padding: var(--spacing-sm); border: 1px solid var(--color-border);
    border-radius: var(--radius-sm); background: var(--color-surface);
}
.ui-upload__thumb { width: 36px; height: 36px; border-radius: var(--radius-sm); object-fit: cover; }
.ui-upload__file-icon { color: var(--color-text-secondary); }
.ui-upload__file-info { flex: 1; }
.ui-upload__file-name { font-size: var(--font-size-sm); display: block; }
.ui-upload__file-size { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-upload__file-remove { border: none; background: transparent; cursor: pointer; color: var(--color-text-muted); font-size: 18px; line-height: 1; padding: 2px; }
.ui-upload__file-remove:hover { color: var(--color-danger); }

.ui-upload__progress { height: 4px; background: var(--color-surface-hover); border-radius: 2px; min-width: 60px; }
.ui-upload__progress-bar { height: 100%; background: var(--color-primary); border-radius: 2px; transition: width var(--motion-normal); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
