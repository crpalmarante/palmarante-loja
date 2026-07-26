# FiscalUI Framework

## Documento 126 — Print

**Nível 7 — Services**

**Versão 1.0**

Serviço de impressão com preview, formatação de relatórios e seleção de áreas de impressão.

---

```js
class PrintService {
    constructor() {
        this._styles = '';
        this._printRoot = null;
    }

    async print(elementOrSelector, options = {}) {
        const el = typeof elementOrSelector === 'string' ? document.querySelector(elementOrSelector) : elementOrSelector;
        if (!el) throw new Error('Elemento não encontrado');

        const title = options.title || document.title || 'FiscalUI Print';
        const margin = options.margin || '15mm';
        const orientation = options.orientation || 'portrait'; // portrait, landscape

        const clone = el.cloneNode(true);
        this._preprocess(clone);

        const frame = document.createElement('iframe');
        frame.style.cssText = 'position:fixed;top:0;left:-9999px;width:1px;height:1px';
        document.body.appendChild(frame);

        const doc = frame.contentWindow.document;
        doc.write(`
            <!DOCTYPE html>
            <html><head>
                <title>${title}</title>
                <style>
                    @page { margin: ${margin}; size: ${orientation}; }
                    body { font-family: ${getComputedStyle(document.body).fontFamily || 'sans-serif'}; }
                    ${this._styles}
                    ${options.styles || ''}
                    .ui-print-hide { display: none !important; }
                </style>
            </head><body>${clone.outerHTML}</body></html>
        `);
        doc.close();

        await new Promise(r => frame.onload = r);

        frame.contentWindow.focus();
        frame.contentWindow.print();
        setTimeout(() => document.body.removeChild(frame), 1000);
    }

    _preprocess(el) {
        el.querySelectorAll('[data-print-hide]').forEach(n => n.classList.add('ui-print-hide'));
        el.querySelectorAll('[data-print-show]').forEach(n => n.style.display = '');
    }

    addGlobalStyles(css) { this._styles += css; }

    getPaperSizes() {
        return [
            { id: 'a4', label: 'A4', width: 210, height: 297 },
            { id: 'letter', label: 'Carta', width: 216, height: 279 },
            { id: 'legal', label: 'Ofício', width: 216, height: 356 }
        ];
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
