# FiscalUI Framework

## Documento 117 — Authorization

**Nível 7 — Services**

**Versão 1.0**

Serviço de autorização baseado em papéis (RBAC) e permissões. Controla acesso a recursos e ações.

---

```js
class AuthzService {
    constructor(options = {}) {
        this.permissions = options.permissions || {};
        this.roles = options.roles || {};
        this._userRoles = [];
        this._userPermissions = [];
    }

    setUser(roles, permissions) {
        this._userRoles = roles || [];
        this._userPermissions = permissions || [];
    }

    hasRole(role) { return this._userRoles.includes(role); }

    hasAnyRole(...roles) { return roles.some(r => this._userRoles.includes(r)); }

    hasPermission(permission) { return this._userPermissions.includes(permission); }

    hasAnyPermission(...perms) { return perms.some(p => this._userPermissions.includes(p)); }

    can(action, resource) { return this.hasPermission(`${action}:${resource}`); }

    canAny(actions) { return actions.some(a => this.can(a.action, a.resource)); }

    filterMenu(items) {
        return items.filter(item => {
            if (item.permission) return this.hasPermission(item.permission);
            if (item.role) return this.hasRole(item.role);
            return true;
        });
    }

    // Decorator para usar em métodos
    static require(permission) {
        return function (target, key, descriptor) {
            const original = descriptor.value;
            descriptor.value = function (...args) {
                if (!this.authz?.hasPermission(permission)) {
                    throw new Error(`Acesso negado: necessário "${permission}"`);
                }
                return original.apply(this, args);
            };
            return descriptor;
        };
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
