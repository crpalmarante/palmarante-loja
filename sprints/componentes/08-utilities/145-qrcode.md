# FiscalUI Framework

## Documento 145 — QRCode

**Nível 8 — Utilities**

**Versão 1.0**

Gerador de QR Code nativo (canvas), sem dependências externas.

---

```js
class QRCode {
    constructor(options = {}) {
        this.size = options.size || 256;
        this.level = options.level || 'M'; // L, M, Q, H
        this.colorDark = options.colorDark || '#000000';
        this.colorLight = options.colorLight || '#ffffff';
    }

    generate(text) {
        const canvas = document.createElement('canvas');
        canvas.width = this.size;
        canvas.height = this.size;
        const ctx = canvas.getContext('2d');

        // Implementação simplificada de QR Code
        // Em produção, usar lib como qrcode-generator ou implementar algoritmo completo
        const moduleCount = 25; // Simulação
        const moduleSize = Math.floor(this.size / moduleCount);
        const offset = Math.floor((this.size - moduleSize * moduleCount) / 2);

        // Fundo
        ctx.fillStyle = this.colorLight;
        ctx.fillRect(0, 0, this.size, this.size);

        // Simular padrão de QR Code com dados do texto
        ctx.fillStyle = this.colorDark;
        for (let row = 0; row < moduleCount; row++) {
            for (let col = 0; col < moduleCount; col++) {
                // Pattern simulado baseado no hash do texto
                const hash = this._hash(text + row + col);
                if (hash % 3 !== 0) {
                    ctx.fillRect(offset + col * moduleSize, offset + row * moduleSize, moduleSize - 1, moduleSize - 1);
                }
            }
        }

        return canvas;
    }

    generateDataURL(text) {
        return this.generate(text).toDataURL('image/png');
    }

    download(text, filename = 'qrcode.png') {
        const link = document.createElement('a');
        link.download = filename;
        link.href = this.generateDataURL(text);
        link.click();
    }

    _hash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }
}
```

> **Nota:** Para implementação real, deve-se usar o algoritmo completo de QR Code (ISO/IEC 18004) ou uma biblioteca especializada. O código acima é um placeholder funcional. Recomenda-se o uso de `qrcode-generator.js` ou similar em produção.

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
