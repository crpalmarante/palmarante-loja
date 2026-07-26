# FiscalUI Framework

## Documento 177 — Marketplace

**Nível 10 — Developer Platform**

**Versão 1.0**

Marketplace de componentes, temas, plugins e widgets FiscalUI.

---

```json
// marketplace.json — metadados do pacote
{
  "id": "fiscalui-theme-corporate",
  "name": "Corporate Theme",
  "version": "1.2.0",
  "type": "theme",
  "description": "Tema corporativo com paleta azul escuro",
  "author": {
    "name": "FiscalUI Team",
    "email": "team@fiscalui.io",
    "url": "https://fiscalui.io"
  },
  "license": "MIT",
  "tags": ["theme", "corporate", "dark"],
  "fiscalui": {
    "minVersion": "1.0.0",
    "maxVersion": "2.0.0"
  },
  "screenshots": [
    "https://marketplace.fiscalui.io/screenshots/theme-1.png"
  ],
  "downloads": 1520,
  "rating": 4.5,
  "price": 0,
  "repository": "https://github.com/user/fiscalui-theme-corporate",
  "readme": "README.md"
}
```

```js
// Marketplace cliente
class MarketplaceClient {
  constructor() {
    this.apiUrl = 'https://marketplace.fiscalui.io/api';
    this._cache = new Map();
  }

  async search(query, filters = {}) {
    const params = new URLSearchParams({ q: query, ...filters });
    const res = await fetch(`${this.apiUrl}/packages?${params}`);
    return res.json();
  }

  async getPackage(id) {
    if (this._cache.has(id)) return this._cache.get(id);
    const res = await fetch(`${this.apiUrl}/packages/${id}`);
    const pkg = await res.json();
    this._cache.set(id, pkg);
    return pkg;
  }

  async install(packageId, version = 'latest') {
    const pkg = await this.getPackage(packageId);
    const url = `${this.apiUrl}/packages/${packageId}/download?version=${version}`;
    const res = await fetch(url);
    const blob = await res.blob();

    // Extrai no diretório de plugins/temas
    const dest = this._getDestDir(pkg.type);
    await this._extract(blob, dest);

    // Registra
    EventBus.emit('marketplace:installed', { id: packageId, type: pkg.type });

    return { id: packageId, type: pkg.type, path: dest };
  }

  async publish(packageDir, apiKey) {
    const formData = new FormData();
    formData.append('package', packageDir);
    formData.append('apiKey', apiKey);

    const res = await fetch(`${this.apiUrl}/packages`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  }

  async getUpdates() {
    const installed = this._getInstalledPackages();
    const res = await fetch(`${this.apiUrl}/updates`, {
      method: 'POST',
      body: JSON.stringify({ packages: installed })
    });
    return res.json();
  }

  _getDestDir(type) {
    const dirs = { theme: 'themes', plugin: 'plugins', component: 'components', widget: 'widgets' };
    return path.join(process.cwd(), 'fiscalui', dirs[type] || 'packages');
  }

  async _extract(blob, dest) {
    // Extrai zip/tar para o diretório de destino
  }

  _getInstalledPackages() {
    // Lê package.json ou fiscalui.json
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
