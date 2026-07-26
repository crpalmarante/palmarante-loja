# FiscalUI Framework

## Documento 125 — Download

**Nível 7 — Services**

**Versão 1.0**

Serviço de download de arquivos com progresso, blob streaming e fallback para navegadores legados.

---

```js
class DownloadService {
    constructor(options = {}) {
        this.http = options.http || new HttpClient();
    }

    async download(url, options = {}) {
        const filename = options.filename || url.split('/').pop() || 'download';
        const onProgress = options.onProgress || null;

        try {
            const res = await this.http.request({ url, method: 'GET', responseType: 'blob' });
            const blob = res.data;
            onProgress?.(100);

            if (options.returnBlob) return blob;
            this._triggerDownload(blob, filename);
            return { blob, filename };
        } catch (err) {
            throw err;
        }
    }

    async downloadChunked(url, options = {}) {
        const filename = options.filename || url.split('/').pop() || 'download';
        const response = await fetch(url);
        const reader = response.body.getReader();
        const contentLength = +response.headers.get('Content-Length') || 0;
        const chunks = [];
        let received = 0;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            received += value.length;
            options.onProgress?.(Math.round((received / contentLength) * 100));
        }

        const blob = new Blob(chunks);
        if (options.returnBlob) return blob;
        this._triggerDownload(blob, filename);
        return { blob, filename };
    }

    _triggerDownload(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
    }

    // Abre em nova aba (PDF, imagens, etc.)
    openInTab(url) { window.open(url, '_blank', 'noopener'); }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
