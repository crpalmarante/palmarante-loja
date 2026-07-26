# FiscalUI Framework

## Documento 144 — Clipboard

**Nível 8 — Utilities**

**Versão 1.0**

Utilitário de clipboard com fallback para document.execCommand e suporte a leitura/escrita.

---

```js
class Clipboard {
    static async copy(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch {
            // Fallback para navegadores antigos
            return Clipboard._fallbackCopy(text);
        }
    }

    static async cut(input) {
        try {
            input.select();
            document.execCommand('cut');
            return true;
        } catch {
            return false;
        }
    }

    static async read() {
        try {
            return await navigator.clipboard.readText();
        } catch {
            return null;
        }
    }

    static async copyElement(el) {
        try {
            const range = document.createRange();
            const selection = window.getSelection();
            range.selectNodeContents(el);
            selection.removeAllRanges();
            selection.addRange(range);
            const success = document.execCommand('copy');
            selection.removeAllRanges();
            return success;
        } catch {
            return false;
        }
    }

    static async copyImage(blob) {
        try {
            await navigator.clipboard.write([new ClipboardItem({ [blob.type]: blob })]);
            return true;
        } catch {
            return false;
        }
    }

    static _fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            const success = document.execCommand('copy');
            document.body.removeChild(textarea);
            return success;
        } catch {
            document.body.removeChild(textarea);
            return false;
        }
    }

    static onCopy(el, callback) {
        el.addEventListener('copy', (e) => {
            callback(e);
        });
    }

    static onPaste(el, callback) {
        el.addEventListener('paste', (e) => {
            callback(e);
        });
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
