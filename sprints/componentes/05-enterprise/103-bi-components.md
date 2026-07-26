# FiscalUI Framework

## Documento 103 — BI Components

**Nível 5 — Enterprise Components**

**Versão 1.0**

Componentes de Business Intelligence: Scorecard, Driver Tree, What-If Analysis e Data Story.

---

```js
class UIBIComponents {
    static Scorecard(options = {}) {
        const title = options.title || '';
        const score = options.score || 0;
        const maxScore = options.maxScore || 100;
        const segments = options.segments || [
            { min: 0, max: 40, label: 'Ruim', color: 'var(--color-danger)' },
            { min: 40, max: 70, label: 'Médio', color: 'var(--color-warning)' },
            { min: 70, max: 100, label: 'Bom', color: 'var(--color-success)' }
        ];
        const pct = (score / maxScore) * 100;
        const currentSeg = segments.find(s => pct >= s.min && pct < s.max) || segments[0];
        return `
            <div class="ui-bi-scorecard">
                ${title ? `<h4 class="ui-bi-scorecard__title">${title}</h4>` : ''}
                <div class="ui-bi-scorecard__gauge">
                    <svg viewBox="0 0 120 120">
                        <circle cx="60" cy="60" r="54" fill="none" stroke="var(--color-surface-hover)" stroke-width="12"/>
                        <circle cx="60" cy="60" r="54" fill="none" stroke="${currentSeg.color}" stroke-width="12"
                                stroke-dasharray="${(pct / 100) * 339.292}" stroke-dashoffset="0"
                                transform="rotate(-90, 60, 60)" stroke-linecap="round"/>
                        <text x="60" y="55" text-anchor="middle" font-size="28" font-weight="bold" fill="var(--color-text)">${score}</text>
                        <text x="60" y="75" text-anchor="middle" font-size="10" fill="var(--color-text-muted)">${currentSeg.label}</text>
                    </svg>
                </div>
            </div>
        `;
    }

    static DriverTree(options = {}) {
        const root = options.root || { label: '', value: 0, children: [] };
        return `<div class="ui-bi-drivertree">${UIBIComponents._renderDriverNode(root, 0)}</div>`;
    }

    static _renderDriverNode(node, depth) {
        return `
            <div class="ui-bi-driver" style="padding-left: ${depth * 24}px">
                <div class="ui-bi-driver__node">
                    <span class="ui-bi-driver__label">${node.label}</span>
                    <span class="ui-bi-driver__value">${node.value}</span>
                    ${node.pct !== undefined ? `<span class="ui-bi-driver__pct ${node.pct >= 0 ? 'ui-bi-driver__pct--pos' : 'ui-bi-driver__pct--neg'}">${node.pct > 0 ? '+' : ''}${node.pct}%</span>` : ''}
                </div>
                ${node.children?.map(c => UIBIComponents._renderDriverNode(c, depth + 1)).join('') || ''}
            </div>
        `;
    }

    static DataStory(options = {}) {
        const title = options.title || '';
        const narrative = options.narrative || '';
        const data = options.data || {};
        const insights = options.insights || [];
        return `
            <div class="ui-bi-story">
                <h4 class="ui-bi-story__title">${title}</h4>
                <p class="ui-bi-story__narrative">${narrative}</p>
                <div class="ui-bi-story__highlights">
                    ${Object.entries(data).map(([k, v]) => `
                        <div class="ui-bi-story__highlight">
                            <span class="ui-bi-story__highlight-label">${k}</span>
                            <span class="ui-bi-story__highlight-value">${v}</span>
                        </div>
                    `).join('')}
                </div>
                <ul class="ui-bi-story__insights">
                    ${insights.map(i => `<li class="ui-bi-story__insight">${i}</li>`).join('')}
                </ul>
            </div>
        `;
    }
}
```

```css
.ui-bi-scorecard { text-align: center; padding: var(--spacing-md); }
.ui-bi-scorecard__title { font-size: var(--font-size-md); margin: 0 0 var(--spacing-sm); }
.ui-bi-scorecard__gauge { max-width: 180px; margin: 0 auto; }

.ui-bi-drivertree { display: flex; flex-direction: column; gap: 2px; }
.ui-bi-driver__node { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-xs) var(--spacing-sm); border-radius: var(--radius-sm); }
.ui-bi-driver__node:hover { background: var(--color-surface-hover); }
.ui-bi-driver__label { flex: 1; font-size: var(--font-size-sm); }
.ui-bi-driver__value { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); font-variant-numeric: tabular-nums; }
.ui-bi-driver__pct { font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); min-width: 50px; text-align: right; }
.ui-bi-driver__pct--pos { color: var(--color-success); }
.ui-bi-driver__pct--neg { color: var(--color-danger); }

.ui-bi-story { padding: var(--spacing-md); max-width: 600px; }
.ui-bi-story__title { font-size: var(--font-size-lg); margin: 0 0 var(--spacing-sm); }
.ui-bi-story__narrative { font-size: var(--font-size-sm); color: var(--color-text-secondary); line-height: 1.6; margin-bottom: var(--spacing-md); }
.ui-bi-story__highlights { display: flex; gap: var(--spacing-lg); margin-bottom: var(--spacing-md); flex-wrap: wrap; }
.ui-bi-story__highlight { text-align: center; }
.ui-bi-story__highlight-label { display: block; font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-bi-story__highlight-value { font-size: var(--font-size-xl); font-weight: var(--font-weight-bold); }
.ui-bi-story__insights { list-style: none; padding: 0; margin: 0; }
.ui-bi-story__insight { padding: var(--spacing-xs) 0; font-size: var(--font-size-sm); color: var(--color-text); }
.ui-bi-story__insight::before { content: '→ '; color: var(--color-primary); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
