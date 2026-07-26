# FiscalUI Framework

## Documento 180 — Upgrade Manager

**Nível 10 — Developer Platform**

**Versão 1.0**

Gerenciador de upgrades: migração entre versões do fiscalUI, changelog automatizado e scripts de migração.

---

```bash
fiscalui upgrade                    # Upgrade para última versão
fiscalui upgrade --version 2.0.0    # Upgrade para versão específica
fiscalui upgrade --dry-run          # Simula upgrade sem aplicar
fiscalui upgrade --rollback         # Reverte último upgrade
fiscalui upgrade status             # Status da versão atual
fiscalui upgrade history            # Histórico de upgrades
```

```js
// Upgrade Manager
class UpgradeManager {
  constructor() {
    this.currentVersion = null;
    this._migrations = new Map();
    this._registerDefaultMigrations();
  }

  async check() {
    const res = await fetch('https://registry.fiscalui.io/framework/latest');
    const latest = await res.json();
    return {
      current: this.currentVersion,
      latest: latest.version,
      hasUpdate: this._compareVersions(latest.version, this.currentVersion) > 0,
      changelog: latest.changelog
    };
  }

  async upgrade(targetVersion = 'latest') {
    const status = await this.check();
    const version = targetVersion === 'latest' ? status.latest : targetVersion;

    if (version === this.currentVersion) {
      Logger.info('Já está na versão mais recente');
      return;
    }

    Logger.info(`⬆️  Upgrading ${this.currentVersion} → ${version}`);

    // Backup do projeto
    await this._backup();

    // Executa migrações uma a uma
    const migrations = this._getMigrationPath(this.currentVersion, version);
    for (const migration of migrations) {
      Logger.info(`  → Executando migração ${migration.id}`);
      await migration.up();
      this._saveMigrationLog(migration.id);
    }

    // Atualiza fiscalui.json
    this._updateConfig(version);

    Logger.info(`✅ Upgrade concluído para v${version}`);
    Logger.info('📋 Verifique o changelog para mais detalhes.');
  }

  async rollback() {
    const lastMigration = this._getLastMigration();
    if (!lastMigration) {
      Logger.info('Nenhum upgrade para reverter');
      return;
    }

    Logger.info(`↩️  Revertendo ${lastMigration.id}`);
    const migration = this._migrations.get(lastMigration.id);
    if (migration?.down) await migration.down();
    this._removeMigrationLog(lastMigration.id);
    Logger.info('✅ Rollback concluído');
  }

  _registerDefaultMigrations() {
    // v1.0.0 → v1.1.0
    this._register('1.0.0-to-1.1.0', {
      from: '1.0.0', to: '1.1.0',
      async up() {
        // Renomeia EventBus para EventBusService
        // Adiciona suporte a temas escuros
      },
      async down() {
        // Reverte renomeações
      }
    });

    // v1.1.0 → v2.0.0
    this._register('1.1.0-to-2.0.0', {
      from: '1.1.0', to: '2.0.0',
      async up() {
        // Migra BEM classes
        // Remove API deprecated
        // Atualiza fiscalui.json schema
      },
      async down() {
        // Reverte para schema antigo
      }
    });
  }

  _register(id, migration) {
    this._migrations.set(id, migration);
  }

  _getMigrationPath(from, to) {
    const path = [];
    for (const [id, migration] of this._migrations) {
      if (this._compareVersions(migration.from, from) >= 0 && this._compareVersions(migration.to, to) <= 0) {
        path.push(migration);
      }
    }
    return path.sort((a, b) => this._compareVersions(a.from, b.from));
  }

  _compareVersions(a, b) {
    const pa = a.split('.').map(Number);
    const pb = b.split('.').map(Number);
    for (let i = 0; i < 3; i++) {
      if (pa[i] > pb[i]) return 1;
      if (pa[i] < pb[i]) return -1;
    }
    return 0;
  }

  async _backup() {
    // Cria backup do projeto antes de migrar
  }

  _saveMigrationLog(id) {
    const logs = JSON.parse(localStorage.getItem('fiscalui_upgrade_log') || '[]');
    logs.push({ id, date: new Date().toISOString() });
    localStorage.setItem('fiscalui_upgrade_log', JSON.stringify(logs));
  }

  _getLastMigration() {
    const logs = JSON.parse(localStorage.getItem('fiscalui_upgrade_log') || '[]');
    return logs[logs.length - 1] || null;
  }

  _removeMigrationLog(id) {
    const logs = JSON.parse(localStorage.getItem('fiscalui_upgrade_log') || '[]');
    localStorage.setItem('fiscalui_upgrade_log', JSON.stringify(logs.filter(l => l.id !== id)));
  }

  _updateConfig(version) {
    // Atualiza fiscalui.json com nova versão
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
