# FiscalUI Framework

## Documento 130 — Worker

**Nível 7 — Services**

**Versão 1.0**

Serviço de abstração para Web Workers com pool, task queue e comunicação estruturada.

---

```js
class WorkerService {
    constructor(options = {}) {
        this.maxWorkers = options.maxWorkers || navigator.hardwareConcurrency || 4;
        this._pool = [];
        this._queue = [];
        this._idle = [];
        this._handlers = new Map();
        this._msgId = 0;
    }

    init(scriptUrl) {
        for (let i = 0; i < this.maxWorkers; i++) {
            const worker = new Worker(scriptUrl);
            worker._busy = false;
            worker.onmessage = (e) => this._handleMessage(worker, e);
            worker.onerror = (err) => this._handleError(worker, err);
            this._pool.push(worker);
            this._idle.push(worker);
        }
    }

    execute(task, data) {
        return new Promise((resolve, reject) => {
            const id = ++this._msgId;
            this._handlers.set(id, { resolve, reject });

            const msg = { id, task, data };

            const worker = this._idle.pop();
            if (worker) {
                worker._busy = true;
                worker.postMessage(msg);
            } else {
                this._queue.push(msg);
            }
        });
    }

    terminate() {
        this._pool.forEach(w => w.terminate());
        this._pool = [];
        this._idle = [];
        this._queue = [];
        this._handlers.clear();
    }

    _handleMessage(worker, e) {
        const { id, result, error } = e.data;
        const handler = this._handlers.get(id);
        if (handler) {
            if (error) handler.reject(new Error(error));
            else handler.resolve(result);
            this._handlers.delete(id);
        }
        worker._busy = false;
        this._idle.push(worker);
        this._processQueue();
    }

    _handleError(worker, err) {
        console.error('[Worker] Error:', err);
        worker._busy = false;
        this._idle.push(worker);
        this._processQueue();
    }

    _processQueue() {
        while (this._queue.length && this._idle.length) {
            const msg = this._queue.shift();
            const worker = this._idle.pop();
            worker._busy = true;
            worker.postMessage(msg);
        }
    }

    getStatus() {
        return {
            total: this._pool.length,
            idle: this._idle.length,
            busy: this._pool.length - this._idle.length,
            queued: this._queue.length
        };
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
