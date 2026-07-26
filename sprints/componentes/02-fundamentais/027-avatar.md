# FiscalUI Framework

## Documento 027 — Avatar

**Nível 2 — Basic Components**

**Versão 1.0**

Foto ou iniciais do usuário. Suporta imagem, fallback com iniciais, e indicador de status.

---

```js
class UIAvatar extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.name = options.name || '';
        this.src = options.src || null;
        this.size = options.size || 'md';
        this.shape = options.shape || 'circle';       // circle, square
        this.status = options.status || null;          // online, busy, away, offline
        this.onClick = options.onClick || null;
    }

    template() {
        const initials = this._getInitials();
        return `
            <div class="ui-avatar ui-avatar--${this.size} ui-avatar--${this.shape}
                        ${this.onClick ? 'ui-avatar--clickable' : ''}"
                 role="${this.onClick ? 'button' : 'img'}"
                 ${this.onClick ? 'tabindex="0"' : ''}
                 aria-label="${this.name}">
                ${this.src
                    ? `<img class="ui-avatar__img" src="${this.src}" alt="${this.name}" />`
                    : `<span class="ui-avatar__initials">${initials}</span>`
                }
                ${this.status ? `<span class="ui-avatar__status ui-avatar__status--${this.status}"></span>` : ''}
            </div>
        `;
    }

    _getInitials() {
        if (!this.name) return '?';
        return this.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
    }

    onInit() {
        if (this.onClick) {
            this.element.addEventListener('click', () => this.onClick());
            this.element.addEventListener('keydown', (e) => { if (e.key === 'Enter') this.onClick(); });
        }
    }
}
```

```css
.ui-avatar {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background: var(--color-primary-light);
    color: var(--color-primary);
    font-weight: var(--font-weight-bold);
    user-select: none;
}

.ui-avatar--circle { border-radius: 50%; }
.ui-avatar--square { border-radius: var(--radius-md); }
.ui-avatar--clickable { cursor: pointer; }

.ui-avatar--xs { width: 24px; height: 24px; font-size: 10px; }
.ui-avatar--sm { width: 32px; height: 32px; font-size: 12px; }
.ui-avatar--md { width: 40px; height: 40px; font-size: 14px; }
.ui-avatar--lg { width: 48px; height: 48px; font-size: 16px; }
.ui-avatar--xl { width: 64px; height: 64px; font-size: 24px; }

.ui-avatar__img { width: 100%; height: 100%; object-fit: cover; }

.ui-avatar__status {
    position: absolute;
    bottom: 0; right: 0;
    width: 10px; height: 10px;
    border-radius: 50%;
    border: 2px solid var(--color-surface);
}
.ui-avatar__status--online  { background: var(--color-success); }
.ui-avatar__status--busy    { background: var(--color-danger); }
.ui-avatar__status--away    { background: var(--color-warning); }
.ui-avatar__status--offline { background: var(--color-text-muted); }
```

```js
// Exemplos
new UIAvatar({ name: 'João Silva' });                        // → JS
new UIAvatar({ name: 'Maria Souza', src: '/fotos/maria.jpg' });  // → foto
new UIAvatar({ name: 'Admin', size: 'xl', status: 'online' });   // → A + bolinha verde
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
