# FiscalUI Framework

## Documento 150 — Export Engine

**Nível 8 — Utilities**

**Versão 1.0**

Motor de exportação de dados: CSV, JSON, XML, XLS (CSV formatado), PDF, impressão. Suporta formatação de dados fiscais.

---

```js
class ExportEngine {
    constructor(options = {}) {
        this.filename = options.filename || 'export';
        this.separator = options.separator || ';';
        this.decimal = options.decimal || ',';
    }

    csv(data, options = {}) {
        const filename = options.filename || this.filename;
        const sep = options.separator || this.separator;
        const rows = [];

        if (options.header) rows.push(options.header.join(sep));

        for (const row of data) {
            const values = options.columns
                ? options.columns.map(c => this._formatCell(row[c], sep))
                : Object.values(row).map(v => this._formatCell(v, sep));
            rows.push(values.join(sep));
        }

        const content = '\uFEFF' + rows.join('\n'); // BOM para Excel
        this._download(content, `${filename}.csv`, 'text/csv;charset=utf-8');
    }

    json(data, options = {}) {
        const filename = options.filename || this.filename;
        const pretty = options.pretty !== false;
        const content = pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
        this._download(content, `${filename}.json`, 'application/json;charset=utf-8');
    }

    xml(data, options = {}) {
        const filename = options.filename || this.filename;
        const root = options.root || 'data';
        const item = options.item || 'item';

        let content = `<?xml version="1.0" encoding="UTF-8"?>\n<${root}>\n`;
        for (const row of data) {
            content += `  <${item}>\n`;
            for (const [key, value] of Object.entries(row)) {
                content += `    <${key}>${this._escapeXml(String(value))}</${key}>\n`;
            }
            content += `  </${item}>\n`;
        }
        content += `</${root}>`;

        this._download(content, `${filename}.xml`, 'application/xml;charset=utf-8');
    }

    xls(data, options = {}) {
        // Gera HTML formatado que o Excel abre como planilha
        const filename = options.filename || this.filename;
        const header = options.header || Object.keys(data[0] || {});

        let html = '<html><head><meta charset="UTF-8"><table>';
        html += '<tr>' + header.map(h => `<th>${h}</th>`).join('') + '</tr>\n';
        for (const row of data) {
            html += '<tr>' + header.map(h => `<td>${row[h] ?? ''}</td>`).join('') + '</tr>\n';
        }
        html += '</table></html>';

        this._download(html, `${filename}.xls`, 'application/vnd.ms-excel;charset=utf-8');
    }

    async pdf(element, options = {}) {
        const filename = options.filename || this.filename;
        const printService = options.printService || new PrintService();
        await printService.print(element, { title: filename, ...options });
    }

    print(data, options = {}) {
        const title = options.title || this.filename;
        const table = document.createElement('table');
        table.style.cssText = 'width:100%;border-collapse:collapse;font-family:sans-serif;font-size:12px';

        const header = options.header || Object.keys(data[0] || {});
        const thead = table.createTHead();
        const hr = thead.insertRow();
        header.forEach(h => {
            const th = document.createElement('th');
            th.textContent = h;
            th.style.cssText = 'border:1px solid #ccc;padding:8px;background:#f5f5f5;text-align:left';
            hr.appendChild(th);
        });

        const tbody = table.createTBody();
        for (const row of data) {
            const tr = tbody.insertRow();
            header.forEach(h => {
                const td = tr.insertCell();
                td.textContent = row[h] ?? '';
                td.style.cssText = 'border:1px solid #ccc;padding:6px';
            });
        }

        const win = window.open('', '_blank');
        win.document.write(`<html><head><title>${title}</title></head><body>`);
        win.document.write(table.outerHTML);
        win.document.write('</body></html>');
        win.document.close();
        win.print();
    }

    _formatCell(value, sep) {
        const str = value === null || value === undefined ? '' : String(value);
        if (str.includes(sep) || str.includes('"') || str.includes('\n')) {
            return `"${str.replace(/"/g, '""')}"`;
        }
        return str;
    }

    _escapeXml(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');
    }

    _download(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
