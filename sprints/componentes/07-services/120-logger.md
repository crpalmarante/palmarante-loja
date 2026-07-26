# FiscalUI Framework

## Documento 120 — Logger

**Nível 7 — Services**

**Versão 1.0**

Serviço de logging com níveis (debug, info, warn, error), formatação e transporte configurável.

---

```js
class LoggerService {
    constructor(options = {}) {
        this.level = options.level || 'debug';
        this.prefix = options.prefix || '[FiscalUI]';
        this.transports = options.transports || [new ConsoleTransport()];
        this.levels = { debug: 0, info: 1, warn: 2, error: 3 };
    }

    debug(...args) { this._log('debug', ...args); }
    info(...args) { this._log('info', ...args); }
    warn(...args) { this._log('warn', ...args); }
    error(...args) { this._log('error', ...args); }

    _log(level, ...args) {
        if (this.levels[level] < this.levels[this.level]) return;
        const entry = { level, timestamp: new Date().toISOString(), prefix: this.prefix, args };
        this.transports.forEach(t => t.log(entry));
    }

    addTransport(transport) { this.transports.push(transport); }
    setLevel(level) { this.level = level; }
}

class ConsoleTransport {
    log(entry) {
        const fn = { debug: 'console.debug', info: 'console.info', warn: 'console.warn', error: 'console.error' }[entry.level] || 'console.log';
        const msg = `${entry.timestamp} ${entry.prefix} [${entry.level.toUpperCase()}]`;
        console[fn.replace('console.', '')](msg, ...entry.args);
    }
}

class RemoteTransport {
    constructor(endpoint) { this.endpoint = endpoint; this.queue = []; }
    log(entry) {
        this.queue.push(entry);
        if (this.queue.length >= 10) this.flush();
    }
    async flush() {
        if (!this.queue.length) return;
        try { await fetch(this.endpoint, { method: 'POST', body: JSON.stringify(this.queue), headers: { 'Content-Type': 'application/json' } }); this.queue = []; } catch { /* keep for retry */ }
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
