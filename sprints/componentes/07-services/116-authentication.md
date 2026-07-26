# FiscalUI Framework

## Documento 116 — Authentication

**Nível 7 — Services**

**Versão 1.0**

Serviço de autenticação com suporte a JWT, refresh token, login social e sessão.

---

```js
class AuthService {
    constructor(options = {}) {
        this.http = options.http || new HttpClient();
        this.loginEndpoint = options.loginEndpoint || '/auth/login';
        this.refreshEndpoint = options.refreshEndpoint || '/auth/refresh';
        this.logoutEndpoint = options.logoutEndpoint || '/auth/logout';
        this.tokenKey = options.tokenKey || 'fiscalui_token';
        this.refreshKey = options.refreshKey || 'fiscalui_refresh';
        this._user = null;
        this._listeners = [];
    }

    async login(credentials) {
        const res = await this.http.post(this.loginEndpoint, credentials);
        this._setTokens(res.data);
        this._user = res.data.user;
        this._notify('login', this._user);
        return this._user;
    }

    async logout() {
        try { await this.http.post(this.logoutEndpoint); } catch { /* ignore */ }
        this._clearTokens();
        this._user = null;
        this._notify('logout');
    }

    async refresh() {
        const refreshToken = this._getRefreshToken();
        if (!refreshToken) throw new Error('No refresh token');
        const res = await this.http.post(this.refreshEndpoint, { refreshToken });
        this._setTokens(res.data);
        return res.data;
    }

    isAuthenticated() { return !!this._getToken(); }

    async getUser() {
        if (this._user) return this._user;
        const token = this._getToken();
        if (!token) return null;
        this._user = this._decodeToken(token);
        return this._user;
    }

    getToken() { return this._getToken(); }

    on(event, handler) { this._listeners.push({ event, handler }); }

    _setTokens(data) {
        localStorage.setItem(this.tokenKey, data.token);
        if (data.refreshToken) localStorage.setItem(this.refreshKey, data.refreshToken);
    }

    _clearTokens() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.refreshKey);
    }

    _getToken() { return localStorage.getItem(this.tokenKey); }
    _getRefreshToken() { return localStorage.getItem(this.refreshKey); }

    _decodeToken(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return { id: payload.sub, name: payload.name, email: payload.email, roles: payload.roles };
        } catch { return null; }
    }

    _notify(event, data) {
        this._listeners.filter(l => l.event === event).forEach(l => l.handler(data));
        FiscalUI.events.emit(`auth:${event}`, data);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
