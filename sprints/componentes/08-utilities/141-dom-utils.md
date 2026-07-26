# FiscalUI Framework

## Documento 141 — DOM Utils

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de manipulação do DOM: criação de elementos, queries, posicionamento, eventos, scroll.

---

```js
class DOMUtils {
    static create(tag, attrs = {}, children = []) {
        const el = document.createElement(tag);
        for (const [key, value] of Object.entries(attrs)) {
            if (key === 'className') el.className = value;
            else if (key === 'style' && typeof value === 'object') Object.assign(el.style, value);
            else if (key.startsWith('on')) el.addEventListener(key.slice(2), value);
            else if (key === 'dataset') Object.assign(el.dataset, value);
            else el.setAttribute(key, value);
        }
        for (const child of children) {
            if (typeof child === 'string') el.appendChild(document.createTextNode(child));
            else el.appendChild(child);
        }
        return el;
    }

    static qs(selector, context = document) { return context.querySelector(selector); }
    static qsa(selector, context = document) { return Array.from(context.querySelectorAll(selector)); }

    static on(el, event, handler, options = {}) {
        el.addEventListener(event, handler, options);
        return () => el.removeEventListener(event, handler, options);
    }

    static once(el, event) {
        return new Promise(resolve => el.addEventListener(event, resolve, { once: true }));
    }

    static delegate(parent, selector, event, handler) {
        parent.addEventListener(event, (e) => {
            const target = e.target.closest(selector);
            if (target && parent.contains(target)) handler(e, target);
        });
    }

    static ready(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    static offset(el) {
        const rect = el.getBoundingClientRect();
        return { top: rect.top + window.scrollY, left: rect.left + window.scrollX, width: rect.width, height: rect.height };
    }

    static position(el) {
        const rect = el.getBoundingClientRect();
        return { top: rect.top, left: rect.left, width: rect.width, height: rect.height };
    }

    static scrollTo(el, options = {}) {
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest', ...options });
    }

    static scrollToTop(options = {}) {
        window.scrollTo({ top: 0, behavior: 'smooth', ...options });
    }

    static insertAfter(newEl, refEl) {
        refEl.parentNode.insertBefore(newEl, refEl.nextSibling);
    }

    static wrap(el, wrapper) {
        el.parentNode.insertBefore(wrapper, el);
        wrapper.appendChild(el);
        return wrapper;
    }

    static remove(el) { el?.parentNode?.removeChild(el); }

    static empty(el) { while (el.firstChild) el.removeChild(el.firstChild); }

    static show(el) { el.style.display = ''; }
    static hide(el) { el.style.display = 'none'; }
    static toggle(el) { el.style.display = el.style.display === 'none' ? '' : 'none'; }

    static hasClass(el, cls) { return el.classList.contains(cls); }
    static addClass(el, cls) { el.classList.add(cls); }
    static removeClass(el, cls) { el.classList.remove(cls); }
    static toggleClass(el, cls) { el.classList.toggle(cls); }

    static outerWidth(el, includeMargin = false) {
        let width = el.offsetWidth;
        if (includeMargin) {
            const style = getComputedStyle(el);
            width += parseInt(style.marginLeft) + parseInt(style.marginRight);
        }
        return width;
    }

    static outerHeight(el, includeMargin = false) {
        let height = el.offsetHeight;
        if (includeMargin) {
            const style = getComputedStyle(el);
            height += parseInt(style.marginTop) + parseInt(style.marginBottom);
        }
        return height;
    }

    static matches(el, selector) { return el.matches(selector); }
    static closest(el, selector) { return el.closest(selector); }

    static siblings(el) {
        return Array.from(el.parentNode.children).filter(child => child !== el);
    }

    static prev(el) { return el.previousElementSibling; }
    static next(el) { return el.nextElementSibling; }
    static parent(el) { return el.parentElement; }
    static children(el) { return Array.from(el.children); }

    static fragment(...elements) {
        const f = document.createDocumentFragment();
        elements.forEach(e => f.appendChild(e));
        return f;
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
