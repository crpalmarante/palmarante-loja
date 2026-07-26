# FiscalUI Framework

## Documento 146 — Barcode

**Nível 8 — Utilities**

**Versão 1.0**

Gerador de código de barras (EAN-13, CODE-128, EAN-8, UPC-A) via canvas, sem dependências.

---

```js
class Barcode {
    constructor(options = {}) {
        this.width = options.width || 300;
        this.height = options.height || 100;
        this.color = options.color || '#000000';
        this.bgColor = options.bgColor || '#ffffff';
        this.displayValue = options.displayValue !== false;
    }

    generate(text, format = 'ean13') {
        const canvas = document.createElement('canvas');
        canvas.width = this.width;
        canvas.height = this.height;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = this.bgColor;
        ctx.fillRect(0, 0, this.width, this.height);

        const digits = text.replace(/\D/g, '');
        const totalBars = digits.length * 2 + 4; // margens + dados
        const barWidth = Math.floor((this.width - 20) / totalBars);
        const startX = 10;

        ctx.fillStyle = this.color;
        // Simulação: barras baseadas nos dígitos
        for (let i = 0; i < digits.length; i++) {
            const d = parseInt(digits[i]);
            for (let b = 0; b < 2; b++) {
                const x = startX + (i * 2 + b) * barWidth;
                if ((d + b) % 2 === 0) {
                    ctx.fillRect(x, 5, barWidth - 1, this.height - 30);
                }
            }
        }

        if (this.displayValue) {
            ctx.fillStyle = this.color;
            ctx.font = '12px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(text, this.width / 2, this.height - 5);
        }

        return canvas;
    }

    generateDataURL(text, format = 'ean13') {
        return this.generate(text, format).toDataURL('image/png');
    }

    download(text, format = 'ean13', filename = 'barcode.png') {
        const link = document.createElement('a');
        link.download = filename;
        link.href = this.generateDataURL(text, format);
        link.click();
    }
}
```

> **Nota:** Implementação completa exige codificação específica para cada formato (EAN-13 checksum, CODE-128 charset, etc.). O código acima é um placeholder funcional.

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
