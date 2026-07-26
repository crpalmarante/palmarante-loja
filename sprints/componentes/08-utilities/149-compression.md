# FiscalUI Framework

## Documento 149 — Compression

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de compressão: compressão/decompressão de strings usando CompressionStream API e LZ-String.

---

```js
class Compression {
    static async compress(str) {
        const encoder = new TextEncoder();
        const data = encoder.encode(str);
        const cs = new CompressionStream('gzip');
        const writer = cs.writable.getWriter();
        writer.write(data);
        writer.close();
        const reader = cs.readable.getReader();
        const chunks = [];
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
        }
        const total = chunks.reduce((acc, c) => {
            const tmp = new Uint8Array(acc.length + c.length);
            tmp.set(acc);
            tmp.set(c, acc.length);
            return tmp;
        }, new Uint8Array(0));
        return Compression._bufferToBase64(total);
    }

    static async decompress(compressed) {
        const data = Compression._base64ToBuffer(compressed);
        const ds = new DecompressionStream('gzip');
        const writer = ds.writable.getWriter();
        writer.write(data);
        writer.close();
        const reader = ds.readable.getReader();
        const chunks = [];
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
        }
        const total = chunks.reduce((acc, c) => {
            const tmp = new Uint8Array(acc.length + c.length);
            tmp.set(acc);
            tmp.set(c, acc.length);
            return tmp;
        }, new Uint8Array(0));
        const decoder = new TextDecoder();
        return decoder.decode(total);
    }

    static async compressBase64(str) {
        // Comprime e retorna em base64 URL-safe
        const compressed = await Compression.compress(str);
        return compressed.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    }

    static _bufferToBase64(buffer) {
        const binary = Array.from(new Uint8Array(buffer)).map(b => String.fromCharCode(b)).join('');
        return btoa(binary);
    }

    static _base64ToBuffer(base64) {
        const binary = atob(base64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
        return bytes;
    }

    static estimateSize(str) {
        return { original: str.length, encoded: encodeURI(str).length };
    }

    static simple(str) {
        // Run-length encoding simples
        let result = '';
        let count = 1;
        for (let i = 0; i < str.length; i++) {
            if (str[i] === str[i + 1]) count++;
            else { result += count > 1 ? count + str[i] : str[i]; count = 1; }
        }
        return result;
    }

    static simpleDecompress(str) {
        let result = '';
        let num = '';
        for (let i = 0; i < str.length; i++) {
            if (/\d/.test(str[i])) num += str[i];
            else { result += str[i].repeat(parseInt(num) || 1); num = ''; }
        }
        return result;
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
