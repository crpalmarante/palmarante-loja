# FiscalUI Framework

## Documento 040 — Skeleton

**Nível 2 — Basic Components**

**Versão 1.0**

Placeholder animado para conteúdo em carregamento. Simula a estrutura visual enquanto os dados carregam.

---

```js
class UISkeleton extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.variant = options.variant || 'text';        // text, circle, rect, card
        this.width = options.width || '100%';
        this.height = options.height || null;
        this.lines = options.lines || 1;                 // only for 'text'
        this.animated = options.animated !== false;
    }

    template() {
        if (this.variant === 'text') {
            return `<div class="ui-skeleton ${this.animated ? 'ui-skeleton--animated' : ''}">
                ${Array.from({ length: this.lines }, (_, i) =>
                    `<div class="ui-skeleton__text" style="width: ${i === this.lines - 1 ? '60%' : '100%'}"></div>`
                ).join('')}
            </div>`;
        }

        return `<div class="ui-skeleton ${this.animated ? 'ui-skeleton--animated' : ''}">
            <div class="ui-skeleton__${this.variant}"
                 style="${this.width ? `width: ${typeof this.width === 'number' ? this.width + 'px' : this.width}` : ''};
                        ${this.height ? `height: ${typeof this.height === 'number' ? this.height + 'px' : this.height}` : ''}">
            </div>
        </div>`;
    }
}
```

```css
.ui-skeleton { display: flex; flex-direction: column; gap: var(--spacing-sm); }

.ui-skeleton--animated .ui-skeleton__text,
.ui-skeleton--animated .ui-skeleton__circle,
.ui-skeleton--animated .ui-skeleton__rect {
    background: linear-gradient(90deg, var(--color-surface-hover) 25%, var(--color-surface) 50%, var(--color-surface-hover) 75%);
    background-size: 200% 100%;
    animation: ui-skeleton-pulse 1.5s ease-in-out infinite;
}

.ui-skeleton__text { height: 12px; border-radius: var(--radius-sm); background: var(--color-surface-hover); }
.ui-skeleton__circle { border-radius: 50%; background: var(--color-surface-hover); }
.ui-skeleton__rect { border-radius: var(--radius-md); background: var(--color-surface-hover); }
.ui-skeleton__card { border-radius: var(--radius-md); background: var(--color-surface-hover); min-height: 120px; }

@keyframes ui-skeleton-pulse {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
```

```html
<!-- Esqueleto de card -->
<ui-skeleton variant="card" width="300" height="180"></ui-skeleton>

<!-- Esqueleto de texto com 3 linhas -->
<ui-skeleton variant="text" :lines="3"></ui-skeleton>

<!-- Avatar circular -->
<ui-skeleton variant="circle" width="48" height="48"></ui-skeleton>
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial |
