# FiscalUI Framework

## Documento 129 — WebSocket

**Nível 7 — Services**

**Versão 1.0**

Serviço de WebSocket com reconexão automática, heartbeat e fila de mensagens.

---

```js
class WebSocketService {
    constructor(options = {}) {
        this.url = options.url || '';
        this.reconnectInterval = options.reconnectInterval || 3000;
        this.maxReconnects = options.maxReconnects || 10;
        this.heartbeatInterval = options.heartbeatInterval || 30000;
        this._ws = null;
        this._reconnectCount = 0;
        this._listeners = new Map();
        this._queue = [];
        this._connected = false;
        this._heartbeatTimer = null;
        this._intentionalClose = false;
    }

    connect(url) {
        if (url) this.url = url;
        if (!this.url) throw new Error('WebSocket URL não definida');
        this._intentionalClose = false;

        this._ws = new WebSocket(this.url);
        this._ws.onopen = () => {
            this._connected = true;
            this._reconnectCount = 0;
            this._flushQueue();
            this._startHeartbeat();
            this._emit('open');
        };
        this._ws.onmessage = (e) => {
            try { const data = JSON.parse(e.data); this._emit('message', data); } catch { this._emit('message', e.data); }
        };
        this._ws.onclose = (e) => {
            this._connected = false;
            this._stopHeartbeat();
            this._emit('close', e);
            if (!this._intentionalClose && this._reconnectCount < this.maxReconnects) this._reconnect();
        };
        this._ws.onerror = (err) => this._emit('error', err);
    }

    disconnect() {
        this._intentionalClose = true;
        this._reconnectCount = this.maxReconnects;
        this._ws?.close();
        this._ws = null;
    }

    send(data) {
        const msg = typeof data === 'string' ? data : JSON.stringify(data);
        if (this._connected && this._ws?.readyState === WebSocket.OPEN) {
            this._ws.send(msg);
        } else {
            this._queue.push(msg);
        }
    }

    on(event, callback) {
        if (!this._listeners.has(event)) this._listeners.set(event, []);
        this._listeners.get(event).push(callback);
        return () => this.off(event, callback);
    }

    off(event, callback) {
        const list = this._listeners.get(event);
        if (list) this._listeners.set(event, list.filter(cb => cb !== callback));
    }

    isConnected() { return this._connected; }

    _emit(event, data) {
        (this._listeners.get(event) || []).forEach(cb => cb(data));
    }

    _reconnect() {
        this._reconnectCount++;
        setTimeout(() => this.connect(), this.reconnectInterval);
    }

    _flushQueue() {
        while (this._queue.length) this.send(this._queue.shift());
    }

    _startHeartbeat() {
        this._heartbeatTimer = setInterval(() => {
            if (this._connected) this.send({ type: 'ping' });
        }, this.heartbeatInterval);
    }

    _stopHeartbeat() {
        if (this._heartbeatTimer) { clearInterval(this._heartbeatTimer); this._heartbeatTimer = null; }
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
