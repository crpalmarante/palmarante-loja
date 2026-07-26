# FiscalUI Framework

## Documento 131 — Offline Sync

**Nível 7 — Services**

**Versão 1.0**

Serviço de sincronização offline com fila de operações, detecção de conectividade e merge de conflitos.

---

```js
class OfflineSyncService {
    constructor(options = {}) {
        this.storage = options.storage || localStorage;
        this.http = options.http || new HttpClient();
        this.syncEndpoint = options.syncEndpoint || '/sync';
        this._queueKey = 'fiscalui_offline_queue';
        this._conflictStrategy = options.conflictStrategy || 'last-write-wins'; // last-write-wins, server-wins, client-wins, manual
        this._online = navigator.onLine;
        this._syncing = false;
        this._init();
    }

    _init() {
        window.addEventListener('online', () => { this._online = true; this.sync(); });
        window.addEventListener('offline', () => { this._online = false; });
    }

    enqueue(operation) {
        const queue = this._getQueue();
        queue.push({
            id: Date.now() + Math.random(),
            type: operation.type,      // create, update, delete
            resource: operation.resource,
            data: operation.data,
            timestamp: Date.now(),
            retries: 0
        });
        this._saveQueue(queue);

        if (this._online) this.sync();
    }

    getQueueLength() { return this._getQueue().length; }

    isOnline() { return this._online; }

    async sync() {
        if (this._syncing || !this._online) return;
        this._syncing = true;

        const queue = this._getQueue();
        if (!queue.length) { this._syncing = false; return; }

        let remaining = [...queue];

        try {
            const res = await this.http.post(this.syncEndpoint, { operations: remaining });
            const conflicts = res.data?.conflicts || [];

            // Resolver conflitos
            remaining = remaining.filter(op => !conflicts.some(c => c.id === op.id));

            for (const conflict of conflicts) {
                const resolved = this._resolveConflict(conflict);
                if (!resolved) remaining.push(conflict.operation); // mantém para retry
            }

            this._saveQueue(remaining);
        } catch (err) {
            console.error('[OfflineSync] Erro na sincronização:', err);
            // Incrementa retries
            remaining = remaining.map(op => ({ ...op, retries: op.retries + 1 }));
            this._saveQueue(remaining);
        }

        this._syncing = false;

        if (remaining.length < queue.length) this.sync(); // continua
    }

    _resolveConflict(conflict) {
        switch (this._conflictStrategy) {
            case 'server-wins': return true;
            case 'client-wins': return false; // mantém operação local
            case 'last-write-wins':
                return conflict.serverTimestamp >= conflict.clientTimestamp;
            case 'manual':
                this._emit('conflict', conflict);
                return false;
            default: return true;
        }
    }

    clearQueue() { this._saveQueue([]); }

    _getQueue() {
        try { return JSON.parse(this.storage.getItem(this._queueKey) || '[]'); } catch { return []; }
    }

    _saveQueue(queue) {
        this.storage.setItem(this._queueKey, JSON.stringify(queue));
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
