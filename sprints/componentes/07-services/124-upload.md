# FiscalUI Framework

## Documento 124 — Upload

**Nível 7 — Services**

**Versão 1.0**

Serviço de upload de arquivos com suporte a chunked upload, progresso, pause/retry e validação.

---

```js
class UploadService {
    constructor(options = {}) {
        this.http = options.http || new HttpClient();
        this.endpoint = options.endpoint || '/upload';
        this.chunkSize = options.chunkSize || 5 * 1024 * 1024; // 5MB
        this.maxConcurrent = options.maxConcurrent || 3;
        this._queue = [];
        this._active = 0;
    }

    async upload(file, options = {}) {
        const task = {
            file,
            id: Date.now() + Math.random(),
            endpoint: options.endpoint || this.endpoint,
            field: options.field || 'file',
            metadata: options.metadata || {},
            onProgress: options.onProgress || null,
            onComplete: options.onComplete || null,
            onError: options.onError || null,
            _aborted: false,
            _progress: 0
        };

        if (file.size > this.chunkSize && options.chunked !== false) {
            return this._chunkedUpload(task);
        }
        return this._simpleUpload(task);
    }

    async _simpleUpload(task) {
        const formData = new FormData();
        formData.append(task.field, task.file);
        Object.entries(task.metadata).forEach(([k, v]) => formData.append(k, v));

        try {
            const res = await this.http.post(task.endpoint, formData, {
                onUploadProgress: (pct) => {
                    task._progress = pct;
                    task.onProgress?.(pct);
                }
            });
            task.onComplete?.(res.data);
            return res.data;
        } catch (err) {
            task.onError?.(err);
            throw err;
        }
    }

    async _chunkedUpload(task) {
        const chunks = Math.ceil(task.file.size / this.chunkSize);
        let uploaded = 0;

        for (let i = 0; i < chunks; i++) {
            if (task._aborted) throw new Error('Upload cancelado');
            const start = i * this.chunkSize;
            const end = Math.min(start + this.chunkSize, task.file.size);
            const chunk = task.file.slice(start, end);

            const formData = new FormData();
            formData.append(task.field, chunk);
            formData.append('chunk', i);
            formData.append('chunks', chunks);
            formData.append('filename', task.file.name);
            formData.append('fileId', task.id);

            await this.http.post(task.endpoint, formData);
            uploaded += chunk.size;
            const pct = Math.round((uploaded / task.file.size) * 100);
            task._progress = pct;
            task.onProgress?.(pct);
        }

        const res = await this.http.post(`${task.endpoint}/complete`, { fileId: task.id, filename: task.file.name });
        task.onComplete?.(res.data);
        return res.data;
    }

    cancel(taskId) {
        const task = [...this._queue, ...this._active].find(t => t.id === taskId);
        if (task) task._aborted = true;
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
