# FiscalUI Framework

## Documento 178 — Package Manager

**Nível 10 — Developer Platform**

**Versão 1.0**

Gerenciador de pacotes FiscalUI — instalação, atualização, dependências e resolução.

---

```bash
# Comandos
fiscalui pkg install fiscalui-grid       # Instala pacote
fiscalui pkg uninstall fiscalui-grid      # Remove pacote
fiscalui pkg update                       # Atualiza todos
fiscalui pkg update fiscalui-grid         # Atualiza específico
fiscalui pkg list                         # Lista instalados
fiscalui pkg info fiscalui-grid           # Info do pacote
fiscalui pkg search grid                  # Busca pacotes
fiscalui pkg outdated                     # Verifica atualizações
```

```js
// Package Manager
class PackageManager {
  constructor() {
    this.registry = new Map();
    this.installed = new Map();
    this._loadInstalled();
  }

  async install(name, version = 'latest') {
    if (this.installed.has(name)) {
      throw new Error(`Pacote '${name}' já instalado`);
    }

    const pkg = await this._resolvePackage(name, version);

    // Resolve e instala dependências primeiro
    for (const [dep, depVer] of Object.entries(pkg.dependencies || {})) {
      if (!this.installed.has(dep)) {
        await this.install(dep, depVer);
      }
    }

    // Verifica conflitos
    this._checkConflicts(pkg);

    // Download e extração
    await this._download(pkg);
    this.installed.set(name, { version, path: pkg.path, dependencies: pkg.dependencies });
    this._saveInstalled();

    EventBus.emit('package:installed', { name, version });
  }

  async uninstall(name) {
    if (!this.installed.has(name)) return;

    // Verifica dependentes
    const dependents = this._getDependents(name);
    if (dependents.length) {
      throw new Error(`Não é possível remover '${name}': dependências: ${dependents.join(', ')}`);
    }

    this._removeFiles(name);
    this.installed.delete(name);
    this._saveInstalled();
    EventBus.emit('package:uninstalled', { name });
  }

  async update(name) {
    const current = this.installed.get(name);
    if (!current) throw new Error(`Pacote '${name}' não instalado`);
    const latest = await this._getLatestVersion(name);
    if (latest === current.version) return;
    await this.install(name, latest);
    EventBus.emit('package:updated', { name, from: current.version, to: latest });
  }

  list() {
    return Array.from(this.installed.entries()).map(([name, info]) => ({
      name, version: info.version, path: info.path
    }));
  }

  async search(query) {
    const res = await fetch(`https://registry.fiscalui.io/search?q=${query}`);
    return res.json();
  }

  async outdated() {
    const result = [];
    for (const [name, current] of this.installed) {
      const latest = await this._getLatestVersion(name);
      if (latest !== current.version) result.push({ name, current: current.version, latest });
    }
    return result;
  }

  // --- Internos ---

  _loadInstalled() {
    const data = localStorage.getItem('fiscalui_packages');
    if (data) this.installed = new Map(JSON.parse(data));
  }

  _saveInstalled() {
    localStorage.setItem('fiscalui_packages', JSON.stringify([...this.installed]));
  }

  async _resolvePackage(name, version) {
    const res = await fetch(`https://registry.fiscalui.io/packages/${name}/${version}`);
    return res.json();
  }

  async _getLatestVersion(name) {
    const res = await fetch(`https://registry.fiscalui.io/packages/${name}/latest`);
    const data = await res.json();
    return data.version;
  }

  _checkConflicts(pkg) {
    const conflicts = pkg.conflicts || [];
    for (const c of conflicts) {
      if (this.installed.has(c)) {
        throw new Error(`Conflito: '${pkg.name}' é incompatível com '${c}'`);
      }
    }
  }

  _getDependents(name) {
    return Array.from(this.installed.entries())
      .filter(([_, info]) => info.dependencies?.[name])
      .map(([n]) => n);
  }

  async _download(pkg) {
    // Download e extrai o pacote
  }

  _removeFiles(name) {
    // Remove arquivos do pacote
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
