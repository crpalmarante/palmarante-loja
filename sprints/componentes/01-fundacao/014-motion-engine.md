# FiscalUI Framework

## Documento 014 — Motion Engine

**Versão 1.0**

Este documento define o sistema de animações e transições do FiscalUI. Curvas de easing, durações, animações pré-definidas, transições de estado, e suporte a reduced motion. Toda animação no FiscalUI passa pelo Motion Engine.

---

# Índice

1. Introdução
2. Filosofia
3. Arquitetura
4. API Pública
5. Curvas de Easing
6. Durações
7. Animações Pré-definidas
8. Transições de Estado
9. Animações de Entrada/Saída
10. Animação de Listas (Stagger)
11. Scroll Animation
12. CSS vs JS Animation
13. Reduced Motion
14. Performance
15. Integração com EventBus
16. Testes
17. Boas Práticas

---

# 1. Introdução

## 1.1 Propósito

O Motion Engine gerencia toda animação e transição no FiscalUI. Ele define o sistema de timing, easing, e animações pré-definidas que todos os componentes usam, garantindo consistência visual e performance.

---

# 2. Filosofia

```
1. CSS transitions > CSS animations > JS animations
2. Toda animação deve ter propósito (não animar por animar)
3. Toda animação deve respeitar prefers-reduced-motion
4. Durações consistentes em todo o sistema
5. Easing consistente em todo o sistema
6. Animações nunca devem bloquear interação do usuário
```

---

# 3. Arquitetura

```
Motion Engine
    │
    ├── Easing: ease-in-out, ease-out, ease-in, linear, custom
    ├── Duration: instant, fast, normal, slow, very-slow
    ├── Animations: fade, slide, scale, rotate, shake
    ├── Transitions: enter, leave, move, state
    └── Controls: play, pause, reverse, cancel
```

---

# 4. API Pública

```js
class MotionEngine {
    constructor(framework = null) {
        this.framework = framework;
        this._easing = {
            'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
            'ease-out':    'cubic-bezier(0, 0, 0.2, 1)',
            'ease-in':     'cubic-bezier(0.4, 0, 1, 1)',
            'linear':      'linear',
            'snap':        'cubic-bezier(0, 1, 0, 1)',
            'bounce':      'cubic-bezier(0.68, -0.55, 0.27, 1.55)'
        };
        this._durations = {
            'instant':   0,
            'fast':      150,
            'normal':    300,
            'slow':      500,
            'very-slow': 800
        };
    }

    get easing() { return { ...this._easing }; }
    get durations() { return { ...this._durations }; }

    animate(element, keyframes, options = {}) {
        if (!element || this.reducedMotion) return { play: () => {}, cancel: () => {} };

        const anim = element.animate(keyframes, {
            duration: options.duration || this._durations.normal,
            easing: this._resolveEasing(options.easing || 'ease-in-out'),
            fill: options.fill || 'both',
            ...options
        });

        return anim;
    }

    transition(element, property, from, to, options = {}) {
        if (!element) return;

        const duration = options.duration || this._durations.normal;
        const easing = this._resolveEasing(options.easing || 'ease-in-out');

        element.style.transition = `${property} ${duration}ms ${easing}`;
        element.style[property] = to;

        const onEnd = () => {
            element.style.transition = '';
            element.removeEventListener('transitionend', onEnd);
            options.onFinish?.();
        };
        element.addEventListener('transitionend', onEnd);
    }

    fadeIn(element, options = {}) {
        return this.animate(element, [
            { opacity: 0 },
            { opacity: 1 }
        ], { duration: options.duration || this._durations.normal, easing: 'ease-out', ...options });
    }

    fadeOut(element, options = {}) {
        return this.animate(element, [
            { opacity: 1 },
            { opacity: 0 }
        ], { duration: options.duration || this._durations.normal, easing: 'ease-in', ...options });
    }

    slideIn(element, direction = 'left', options = {}) {
        const offset = direction === 'left' ? '-30px' : direction === 'right' ? '30px' : direction === 'top' ? '-30px' : '30px';
        const axis = direction === 'left' || direction === 'right' ? 'translateX' : 'translateY';

        return this.animate(element, [
            { transform: `${axis}(${offset})`, opacity: 0 },
            { transform: `${axis}(0)`, opacity: 1 }
        ], options);
    }

    slideOut(element, direction = 'left', options = {}) {
        const offset = direction === 'left' ? '-30px' : direction === 'right' ? '30px' : direction === 'top' ? '-30px' : '30px';
        const axis = direction === 'left' || direction === 'right' ? 'translateX' : 'translateY';

        return this.animate(element, [
            { transform: `${axis}(0)`, opacity: 1 },
            { transform: `${axis}(${offset})`, opacity: 0 }
        ], options);
    }

    scaleIn(element, options = {}) {
        return this.animate(element, [
            { transform: 'scale(0.9)', opacity: 0 },
            { transform: 'scale(1)', opacity: 1 }
        ], { duration: this._durations.normal, easing: 'ease-out', ...options });
    }

    stagger(elements, animationFn, options = {}) {
        const delay = options.staggerDelay || 50;

        return elements.map((el, i) => {
            return animationFn(el, { ...options, delay: (options.delay || 0) + (i * delay) });
        });
    }

    get reducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    _resolveEasing(easing) {
        return this._easing[easing] || easing;
    }
}
```

## 4.1 Resumo da API

| Método | Descrição |
|--------|-----------|
| `animate(element, keyframes, opts)` | Animação via Web Animations API |
| `transition(element, prop, from, to, opts)` | Transição CSS |
| `fadeIn(element, opts)` | Fade in |
| `fadeOut(element, opts)` | Fade out |
| `slideIn(element, dir, opts)` | Slide in (left, right, top, bottom) |
| `slideOut(element, dir, opts)` | Slide out |
| `scaleIn(element, opts)` | Scale in |
| `stagger(elements, fn, opts)` | Animação em sequência |

---

# 5. Curvas de Easing

```js
'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)'   // Entrada/saída suave
'ease-out':    'cubic-bezier(0, 0, 0.2, 1)'      // Saída suave (mais natural)
'ease-in':     'cubic-bezier(0.4, 0, 1, 1)'      // Entrada suave
'linear':      'linear'                           // Constante
'snap':        'cubic-bezier(0, 1, 0, 1)'         // Instantâneo
'bounce':      'cubic-bezier(0.68, -0.55, 0.27, 1.55)' // Efeito bounce
```

---

# 6. Durações

```js
'instant':   0     // Sem animação (mudança imediata)
'fast':      150   // Hover, feedback rápido
'normal':    300   // Transições padrão
'slow':      500   // Modais, páginas
'very-slow': 800   // Animações de destaque
```

---

# 7. Animações Pré-definidas

## 7.1 CSS Classes

```css
.ui-fade-enter {
    opacity: 0;
}
.ui-fade-enter-active {
    opacity: 1;
    transition: opacity var(--motion-normal) var(--ease-out);
}

.ui-slide-left-enter {
    transform: translateX(-30px);
    opacity: 0;
}
.ui-slide-left-enter-active {
    transform: translateX(0);
    opacity: 1;
    transition: all var(--motion-normal) var(--ease-out);
}

.ui-scale-enter {
    transform: scale(0.95);
    opacity: 0;
}
.ui-scale-enter-active {
    transform: scale(1);
    opacity: 1;
    transition: all var(--motion-normal) var(--ease-out);
}
```

## 7.2 Uso em Componentes

```js
class Modal extends UIComponent {
    open() {
        this.element.classList.add('ui-modal--open');
        FiscalUI.motion.fadeIn(this.element, { duration: 300 });
    }

    close() {
        FiscalUI.motion.fadeOut(this.element, { duration: 200 });
        setTimeout(() => this.destroy(), 200);
    }
}
```

---

# 8. Transições de Estado

```js
class AccordionItem {
    toggle(expanded) {
        const panel = this.element.querySelector('.ui-accordion__panel');

        if (expanded) {
            panel.style.height = '0';
            panel.style.display = 'block';
            const height = panel.scrollHeight;
            FiscalUI.motion.transition(panel, 'height', '0px', `${height}px`);
            panel.addEventListener('transitionend', () => {
                panel.style.height = 'auto';
            }, { once: true });
        } else {
            panel.style.height = `${panel.scrollHeight}px`;
            FiscalUI.motion.transition(panel, 'height', `${panel.scrollHeight}px`, '0px');
            panel.addEventListener('transitionend', () => {
                panel.style.display = 'none';
            }, { once: true });
        }
    }
}
```

---

# 9. Animações de Listas (Stagger)

```js
class NFETable extends UIComponent {
    onDataLoaded(items) {
        const rows = this.renderRows(items);

        FiscalUI.motion.stagger(rows, (row) => {
            return FiscalUI.motion.fadeIn(row, { duration: 200 });
        }, { staggerDelay: 30 });
    }
}
```

---

# 10. Reduced Motion

```js
class AnimatedComponent extends UIComponent {
    playAnimation() {
        if (FiscalUI.motion.reducedMotion) {
            this.element.style.opacity = '1';
            this.element.style.transform = 'none';
            return;
        }
        FiscalUI.motion.fadeIn(this.element);
    }
}
```

---

# 11. Performance

```
1. Use transform e opacity (GPU acelerado), nunca width/height/top/left
2. Prefira CSS transitions a JS animations
3. Evite animar muitos elementos simultaneamente (> 20)
4. Use will-change: transform em elementos animados
5. Respeite reduced motion
```

---

# 12. Testes

```js
describe('MotionEngine', () => {
    it('should fade in element', () => {
        const el = document.createElement('div');
        FiscalUI.motion.fadeIn(el);
        expect(el.getAnimations().length).toBe(1);
    });
});
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-24 | FiscalUI Team | Versão inicial — Motion Engine |
