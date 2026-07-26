export function createElement(tag, attrs = {}, children = []) {
    const el = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
        if (key === 'className') el.className = value;
        else if (key === 'dataset') Object.assign(el.dataset, value);
        else if (key.startsWith('on')) el.addEventListener(key.slice(2).toLowerCase(), value);
        else if (key === 'style' && typeof value === 'object') Object.assign(el.style, value);
        else el.setAttribute(key, value);
    }
    for (const child of children) {
        if (typeof child === 'string') el.appendChild(document.createTextNode(child));
        else if (child instanceof Node) el.appendChild(child);
    }
    return el;
}

export function removeElement(el) {
    if (el?.parentNode) el.parentNode.removeChild(el);
}

export function emptyElement(el) {
    while (el?.firstChild) el.removeChild(el.firstChild);
}

export function getElement(selector, context = document) {
    return typeof selector === 'string' ? context.querySelector(selector) : selector;
}

export function getElements(selector, context = document) {
    return Array.from(typeof selector === 'string' ? context.querySelectorAll(selector) : selector || []);
}

export function insertAfter(newEl, referenceEl) {
    referenceEl.parentNode?.insertBefore(newEl, referenceEl.nextSibling);
}

export function insertBefore(newEl, referenceEl) {
    referenceEl.parentNode?.insertBefore(newEl, referenceEl);
}

export function hasClass(el, className) {
    return el?.classList.contains(className) || false;
}

export function addClass(el, ...classes) {
    el?.classList.add(...classes);
}

export function removeClass(el, ...classes) {
    el?.classList.remove(...classes);
}

export function toggleClass(el, className) {
    el?.classList.toggle(className);
}

export function setAttributes(el, attrs) {
    for (const [key, value] of Object.entries(attrs)) el?.setAttribute(key, value);
}

export function removeAttributes(el, ...attrs) {
    for (const attr of attrs) el?.removeAttribute(attr);
}

export function matches(el, selector) {
    return el?.matches(selector) || false;
}

export function closest(el, selector) {
    return el?.closest(selector) || null;
}

export function getData(el, key) {
    return el?.dataset[key];
}

export function setData(el, key, value) {
    if (el) el.dataset[key] = value;
}

export function on(el, event, selector, callback) {
    if (typeof selector === 'function') {
        callback = selector;
        selector = null;
    }
    const handler = selector
        ? (e) => { if (e.target?.matches(selector)) callback(e); }
        : callback;
    el?.addEventListener(event, handler);
    return () => el?.removeEventListener(event, handler);
}

export function off(el, event, handler) {
    el?.removeEventListener(event, handler);
}

export function trigger(el, event, detail = {}) {
    el?.dispatchEvent(new CustomEvent(event, { detail, bubbles: true, cancelable: true }));
}

export function getRect(el) {
    return el?.getBoundingClientRect() || { top: 0, right: 0, bottom: 0, left: 0, width: 0, height: 0 };
}

export function isVisible(el) {
    return el && el.offsetParent !== null;
}
