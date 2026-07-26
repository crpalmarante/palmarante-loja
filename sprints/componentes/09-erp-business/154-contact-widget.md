# FiscalUI Framework

## Documento 154 — Contact Widget

**Nível 9 — ERP Business Components**

**Versão 1.0**

Widget de contato com telefone, email, redes sociais e pessoa de referência.

---

```html
<div class="ui-contact-widget">
    <div class="ui-contact-widget__header">
        <h3 class="ui-contact-widget__title">Informações de Contato</h3>
        <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="add-contact">+ Adicionar</button>
    </div>

    <div class="ui-contact-widget__list">
        <div class="ui-contact-widget__item">
            <div class="ui-contact-widget__item-icon ui-contact-widget__item-icon--phone"></div>
            <div class="ui-contact-widget__item-info">
                <span class="ui-contact-widget__item-type">Telefone Principal</span>
                <span class="ui-contact-widget__item-value">(11) 99999-8888</span>
            </div>
            <div class="ui-contact-widget__item-actions">
                <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="call">📞</button>
                <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="whatsapp">💬</button>
                <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="edit">✏️</button>
            </div>
        </div>

        <div class="ui-contact-widget__item">
            <div class="ui-contact-widget__item-icon ui-contact-widget__item-icon--email"></div>
            <div class="ui-contact-widget__item-info">
                <span class="ui-contact-widget__item-type">Email</span>
                <span class="ui-contact-widget__item-value">contato@empresa.com</span>
            </div>
            <div class="ui-contact-widget__item-actions">
                <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="email">✉️</button>
                <button class="ui-btn ui-btn--ghost ui-btn--xs" data-action="edit">✏️</button>
            </div>
        </div>
    </div>

    <div class="ui-contact-widget__social">
        <h4 class="ui-contact-widget__social-title">Redes Sociais</h4>
        <div class="ui-contact-widget__social-grid">
            <div class="ui-contact-widget__social-item">
                <span class="ui-contact-widget__social-label">WhatsApp</span>
                <span class="ui-contact-widget__social-value">(11) 98888-7777</span>
            </div>
            <div class="ui-contact-widget__social-item">
                <span class="ui-contact-widget__social-label">Instagram</span>
                <span class="ui-contact-widget__social-value">@empresa_oficial</span>
            </div>
        </div>
    </div>
</div>
```

```css
.ui-contact-widget { background: var(--color-surface); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: var(--spacing-md); }
.ui-contact-widget__header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-md); }
.ui-contact-widget__title { margin: 0; font-size: var(--font-size-md); font-weight: var(--font-weight-semibold); }
.ui-contact-widget__list { display: flex; flex-direction: column; gap: var(--spacing-sm); }
.ui-contact-widget__item { display: flex; align-items: center; gap: var(--spacing-sm); padding: var(--spacing-sm); border-radius: var(--radius-md); transition: background 0.2s; }
.ui-contact-widget__item:hover { background: var(--color-surface-hover); }
.ui-contact-widget__item-icon { width: 36px; height: 36px; border-radius: var(--radius-full); background: var(--color-primary-light); display: flex; align-items: center; justify-content: center; }
.ui-contact-widget__item-info { flex: 1; display: flex; flex-direction: column; }
.ui-contact-widget__item-type { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-contact-widget__item-value { font-weight: var(--font-weight-medium); }
.ui-contact-widget__item-actions { display: flex; gap: 4px; opacity: 0; transition: opacity 0.2s; }
.ui-contact-widget__item:hover .ui-contact-widget__item-actions { opacity: 1; }
.ui-contact-widget__social { margin-top: var(--spacing-md); padding-top: var(--spacing-md); border-top: 1px solid var(--color-border); }
.ui-contact-widget__social-title { font-size: var(--font-size-xs); text-transform: uppercase; color: var(--color-text-muted); margin: 0 0 var(--spacing-sm); }
.ui-contact-widget__social-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-sm); }
.ui-contact-widget__social-item { padding: var(--spacing-xs) 0; }
.ui-contact-widget__social-label { display: block; font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ui-contact-widget__social-value { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
