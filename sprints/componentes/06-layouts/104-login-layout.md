# FiscalUI Framework

## Documento 104 — Login Layout

**Nível 6 — Layouts**

**Versão 1.0**

Layout de tela de login com sidebar de branding, formulário centralizado e footer institucional.

---

```js
class LoginLayout extends UIComponent {
    constructor(options = {}) {
        super(options);
        this.logo = options.logo || '';
        this.appName = options.appName || 'FiscalUI';
        this.background = options.background || '';
        this.showRegister = options.showRegister || false;
        this.showPasswordReset = options.showPasswordReset || false;
        this.footerText = options.footerText || '';
    }

    template() {
        return `
            <div class="ui-layout-login">
                <div class="ui-layout-login__brand" ${this.background ? `style="background-image: url(${this.background})"` : ''}>
                    <div class="ui-layout-login__brand-content">
                        ${this.logo ? `<img class="ui-layout-login__logo" src="${this.logo}" alt="${this.appName}">` : ''}
                        <h1 class="ui-layout-login__app-name">${this.appName}</h1>
                        <p class="ui-layout-login__tagline">Sistema de Gestão Fiscal</p>
                    </div>
                </div>
                <div class="ui-layout-login__form">
                    <div class="ui-layout-login__form-card">
                        <div class="ui-layout-login__form-header">
                            <h2 class="ui-layout-login__form-title">Acessar Sistema</h2>
                            <p class="ui-layout-login__form-subtitle">Informe suas credenciais</p>
                        </div>
                        <div class="ui-layout-login__form-body"></div>
                        <div class="ui-layout-login__form-footer">
                            ${this.showPasswordReset ? `<a class="ui-layout-login__link" href="#">Esqueceu a senha?</a>` : ''}
                            ${this.showRegister ? `<a class="ui-layout-login__link" href="#">Criar conta</a>` : ''}
                        </div>
                    </div>
                    ${this.footerText ? `<p class="ui-layout-login__footer">${this.footerText}</p>` : ''}
                </div>
            </div>
        `;
    }

    onInit() {
        this._body = this.query('.ui-layout-login__form-body');
    }

    setForm(html) { if (this._body) this._body.innerHTML = html; }
}
```

```css
.ui-layout-login {
    display: flex; min-height: 100vh;
}

.ui-layout-login__brand {
    flex: 1; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
    color: #fff; padding: var(--spacing-xl);
}

.ui-layout-login__brand-content { text-align: center; }
.ui-layout-login__logo { height: 64px; margin-bottom: var(--spacing-md); }
.ui-layout-login__app-name { font-size: var(--font-size-3xl); font-weight: var(--font-weight-bold); margin: 0; }
.ui-layout-login__tagline { font-size: var(--font-size-md); opacity: 0.8; margin-top: var(--spacing-xs); }

.ui-layout-login__form {
    width: 480px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: var(--spacing-xl); background: var(--color-surface);
}

.ui-layout-login__form-card { width: 100%; max-width: 360px; }
.ui-layout-login__form-header { margin-bottom: var(--spacing-lg); text-align: center; }
.ui-layout-login__form-title { font-size: var(--font-size-xl); margin: 0; }
.ui-layout-login__form-subtitle { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin-top: var(--spacing-xs); }
.ui-layout-login__form-body { display: flex; flex-direction: column; gap: var(--spacing-md); }
.ui-layout-login__form-footer { display: flex; justify-content: space-between; margin-top: var(--spacing-lg); }
.ui-layout-login__link { font-size: var(--font-size-sm); color: var(--color-primary); text-decoration: none; }
.ui-layout-login__link:hover { text-decoration: underline; }
.ui-layout-login__footer { margin-top: var(--spacing-lg); font-size: var(--font-size-xs); color: var(--color-text-muted); text-align: center; }
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
