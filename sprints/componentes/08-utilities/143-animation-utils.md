# FiscalUI Framework

## Documento 143 — Animation Utils

**Nível 8 — Utilities**

**Versão 1.0**

Utilitários de animação: easings, keyframes, transições, requestAnimationFrame helpers.

---

```js
class AnimationUtils {
    static easings = {
        linear: t => t,
        easeInQuad: t => t * t,
        easeOutQuad: t => t * (2 - t),
        easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
        easeInCubic: t => t * t * t,
        easeOutCubic: t => (--t) * t * t + 1,
        easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
        easeInElastic: t => t === 0 ? 0 : t === 1 ? 1 : -Math.pow(2, 10 * t - 10) * Math.sin((t * 10 - 10.75) * (2 * Math.PI) / 3),
        easeOutElastic: t => t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI) / 3) + 1,
        easeInBounce: t => { const b = t => { let t2 = 7.5625, d = 2.75; if (t < 1 / d) return t2 * t * t; else if (t < 2 / d) return t2 * (t -= 1.5 / d) * t + 0.75; else if (t < 2.5 / d) return t2 * (t -= 2.25 / d) * t + 0.9375; else return t2 * (t -= 2.625 / d) * t + 0.984375; }; return 1 - b(1 - t); },
        easeOutBounce: t => { const t2 = 7.5625, d = 2.75; if (t < 1 / d) return t2 * t * t; else if (t < 2 / d) return t2 * (t -= 1.5 / d) * t + 0.75; else if (t < 2.5 / d) return t2 * (t -= 2.25 / d) * t + 0.9375; else return t2 * (t -= 2.625 / d) * t + 0.984375; }
    };

    static animate(options) {
        const {
            from = 0, to = 1, duration = 300, easing = 'easeOutQuad',
            onUpdate, onComplete
        } = options;

        const easeFn = typeof easing === 'function' ? easing : AnimationUtils.easings[easing] || AnimationUtils.easings.easeOutQuad;
        const start = performance.now();

        const frame = (now) => {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const value = from + (to - from) * easeFn(progress);
            onUpdate?.(value, progress);
            if (progress < 1) requestAnimationFrame(frame);
            else onComplete?.();
        };

        requestAnimationFrame(frame);
        return { cancel: () => {} };
    }

    static fadeIn(el, duration = 300) {
        el.style.opacity = '0';
        el.style.display = '';
        return AnimationUtils.animate({
            from: 0, to: 1, duration,
            onUpdate: (v) => el.style.opacity = v
        });
    }

    static fadeOut(el, duration = 300) {
        return AnimationUtils.animate({
            from: 1, to: 0, duration,
            onUpdate: (v) => el.style.opacity = v,
            onComplete: () => el.style.display = 'none'
        });
    }

    static slideDown(el, duration = 300) {
        const height = el.scrollHeight;
        el.style.overflow = 'hidden';
        el.style.maxHeight = '0';
        return AnimationUtils.animate({
            from: 0, to: height, duration,
            onUpdate: (v) => el.style.maxHeight = v + 'px',
            onComplete: () => { el.style.maxHeight = ''; el.style.overflow = ''; }
        });
    }

    static slideUp(el, duration = 300) {
        const height = el.scrollHeight;
        el.style.maxHeight = height + 'px';
        el.style.overflow = 'hidden';
        return AnimationUtils.animate({
            from: height, to: 0, duration,
            onUpdate: (v) => el.style.maxHeight = v + 'px',
            onComplete: () => { el.style.maxHeight = '0'; el.style.display = 'none'; }
        });
    }

    static slideToggle(el, duration = 300) {
        if (el.style.display === 'none' || el.style.maxHeight === '0px') {
            el.style.display = '';
            return AnimationUtils.slideDown(el, duration);
        }
        return AnimationUtils.slideUp(el, duration);
    }

    static wait(ms) { return new Promise(r => setTimeout(r, ms)); }

    static raf() { return new Promise(resolve => requestAnimationFrame(resolve)); }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |
