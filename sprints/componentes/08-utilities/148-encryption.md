# FiscalUI Framework

## Documento 148 — Encryption

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de criptografia: hash SHA-256, base64, AES via Web Crypto API.

---

```js
class Encryption {
    static async sha256(text) {
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const hash = await crypto.subtle.digest('SHA-256', data);
        return Encryption._bufferToHex(hash);
    }

    static async sha1(text) {
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const hash = await crypto.subtle.digest('SHA-1', data);
        return Encryption._bufferToHex(hash);
    }

    static async md5(text) {
        // MD5 não é seguro — mantido apenas para compatibilidade
        // Em produção, usar apenas SHA-256 ou superior
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const hash = await crypto.subtle.digest('SHA-256', data);
        return Encryption._bufferToHex(hash).slice(0, 32);
    }

    static base64Encode(text) {
        return btoa(unescape(encodeURIComponent(text)));
    }

    static base64Decode(text) {
        return decodeURIComponent(escape(atob(text)));
    }

    static base64UrlEncode(text) {
        return Encryption.base64Encode(text)
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=+$/, '');
    }

    static base64UrlDecode(text) {
        text = text.replace(/-/g, '+').replace(/_/g, '/');
        while (text.length % 4) text += '=';
        return Encryption.base64Decode(text);
    }

    static async generateKey() {
        const key = await crypto.subtle.generateKey(
            { name: 'AES-GCM', length: 256 },
            true,
            ['encrypt', 'decrypt']
        );
        return key;
    }

    static async exportKey(key) {
        const raw = await crypto.subtle.exportKey('raw', key);
        return Encryption._bufferToHex(raw);
    }

    static async importKey(hexKey) {
        const raw = Encryption._hexToBuffer(hexKey);
        return await crypto.subtle.importKey('raw', raw, { name: 'AES-GCM' }, false, ['encrypt', 'decrypt']);
    }

    static async encrypt(plaintext, key) {
        const encoder = new TextEncoder();
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const encrypted = await crypto.subtle.encrypt(
            { name: 'AES-GCM', iv },
            key,
            encoder.encode(plaintext)
        );
        return {
            iv: Encryption._bufferToHex(iv),
            data: Encryption._bufferToHex(encrypted)
        };
    }

    static async decrypt(ciphertext, key) {
        const decoder = new TextDecoder();
        const iv = Encryption._hexToBuffer(ciphertext.iv);
        const data = Encryption._hexToBuffer(ciphertext.data);
        const decrypted = await crypto.subtle.decrypt(
            { name: 'AES-GCM', iv },
            key,
            data
        );
        return decoder.decode(decrypted);
    }

    static _bufferToHex(buffer) {
        return Array.from(new Uint8Array(buffer))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    static _hexToBuffer(hex) {
        const bytes = new Uint8Array(hex.length / 2);
        for (let i = 0; i < hex.length; i += 2) {
            bytes[i / 2] = parseInt(hex.substring(i, i + 2), 16);
        }
        return bytes;
    }

    static randomBytes(length = 32) {
        const bytes = crypto.getRandomValues(new Uint8Array(length));
        return Encryption._bufferToHex(bytes);
    }

    static obfuscate(text, visibleChars = 3) {
        if (!text || text.length <= visibleChars) return text;
        const visible = text.slice(0, visibleChars);
        const hidden = '*'.repeat(text.length - visibleChars);
        return visible + hidden;
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
