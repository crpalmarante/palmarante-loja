# FiscalUI Framework

## Documento 142 — CSS Utils

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de manipulação de CSS via JS: estilos computados, animações, variáveis CSS, breakpoints.

---

```js
class CSSUtils {
    static getStyle(el, property) {
        return getComputedStyle(el).getPropertyValue(property).trim();
    }

    static setStyle(el, property, value) {
        el.style.setProperty(property, value);
    }

    static setStyles(el, styles) {
        Object.assign(el.style, styles);
    }

    static getCSSVar(name, el = document.documentElement) {
        return getComputedStyle(el).getPropertyValue(name).trim();
    }

    static setCSSVar(name, value, el = document.documentElement) {
        el.style.setProperty(name, value);
    }

    static removeCSSClass(className) {
        document.querySelectorAll(`.${className}`).forEach(el => el.classList.remove(className));
    }

    static addCSSClass(className, el = document.documentElement) {
        el.classList.add(className);
    }

    static injectCSS(css, id = null) {
        const style = document.createElement('style');
        if (id) style.id = id;
        style.textContent = css;
        document.head.appendChild(style);
        return style;
    }

    static removeCSS(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    static getColorScheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    static onColorSchemeChange(callback) {
        const mq = window.matchMedia('(prefers-color-scheme: dark)');
        mq.addEventListener('change', (e) => callback(e.matches ? 'dark' : 'light'));
    }

    static getBreakpoint() {
        const width = window.innerWidth;
        if (width < 576) return 'xs';
        if (width < 768) return 'sm';
        if (width < 992) return 'md';
        if (width < 1200) return 'lg';
        if (width < 1400) return 'xl';
        return 'xxl';
    }

    static onBreakpointChange(callback) {
        let current = CSSUtils.getBreakpoint();
        const handler = () => {
            const bp = CSSUtils.getBreakpoint();
            if (bp !== current) { callback(bp, current); current = bp; }
        };
        window.addEventListener('resize', handler);
        return () => window.removeEventListener('resize', handler);
    }

    static transitionEnd(el) {
        return new Promise(resolve => {
            el.addEventListener('transitionend', resolve, { once: true });
        });
    }

    static animationEnd(el) {
        return new Promise(resolve => {
            el.addEventListener('animationend', resolve, { once: true });
        });
    }

    static hasOverflow(el) {
        return el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight;
    }

    static getScrollbarWidth() {
        const outer = document.createElement('div');
        outer.style.cssText = 'visibility:hidden;overflow:scroll;position:absolute;top:-9999px';
        document.body.appendChild(outer);
        const inner = document.createElement('div');
        outer.appendChild(inner);
        const width = outer.offsetWidth - inner.offsetWidth;
        outer.remove();
        return width;
    }

    static isVisible(el) {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
    }

    static viewport() {
        return { width: window.innerWidth, height: window.innerHeight };
    }

    static documentSize() {
        return { width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight };
    }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
