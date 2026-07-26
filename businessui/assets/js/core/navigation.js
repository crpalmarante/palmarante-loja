/* ══════════════════════════════════════════════════════════════
   BusinessUI — Navigation Core
   v1.0.0
   ══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const BusinessUI = window.BusinessUI || {};

  /* ── Sidebar Collapse ─────────────────────────────────── */
  BusinessUI.sidebar = {
    toggle() {
      document.querySelector('.bu-sidebar').classList.toggle('collapsed');
    },
    collapse() {
      document.querySelector('.bu-sidebar').classList.add('collapsed');
    },
    expand() {
      document.querySelector('.bu-sidebar').classList.remove('collapsed');
    }
  };

  /* ── Submenu Toggle ────────────────────────────────────── */
  BusinessUI.submenu = {
    toggle(el) {
      el.classList.toggle('open');
      const sub = el.nextElementSibling;
      if (sub && sub.classList.contains('bu-submenu')) {
        sub.classList.toggle('open');
      }
    },
    open(el) {
      el.classList.add('open');
      const sub = el.nextElementSibling;
      if (sub && sub.classList.contains('bu-submenu')) {
        sub.classList.add('open');
      }
    },
    close(el) {
      el.classList.remove('open');
      const sub = el.nextElementSibling;
      if (sub && sub.classList.contains('bu-submenu')) {
        sub.classList.remove('open');
      }
    }
  };

  /* ── Tabs ─────────────────────────────────────────────── */
  BusinessUI.tabs = {
    switch(tabEl, tabId) {
      const container = tabEl.closest('.bu-tabs') || tabEl.parentElement;
      const parent = container.parentElement;
      container.querySelectorAll('.bu-tab').forEach(t => t.classList.remove('active'));
      tabEl.classList.add('active');
      parent.querySelectorAll('.bu-tab-content').forEach(t => t.classList.remove('active'));
      const target = parent.querySelector('#' + tabId) || document.getElementById(tabId);
      if (target) target.classList.add('active');
    }
  };

  /* ── Dialog ───────────────────────────────────────────── */
  BusinessUI.dialog = {
    open(id) {
      document.getElementById(id).classList.add('open');
    },
    close(el) {
      const backdrop = el.closest('.bu-dialog-backdrop');
      if (backdrop) backdrop.classList.remove('open');
    },
    closeAll() {
      document.querySelectorAll('.bu-dialog-backdrop.open').forEach(d => d.classList.remove('open'));
    }
  };

  /* ── Toast ────────────────────────────────────────────── */
  BusinessUI.toast = {
    show(message, type, duration) {
      type = type || 'info';
      duration = duration || 4000;
      const container = document.querySelector('.bu-toast-container');
      if (!container) return;
      const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
      const toast = document.createElement('div');
      toast.className = 'bu-toast bu-toast-' + type;
      toast.innerHTML =
        '<span class="bu-toast-icon">' + (icons[type] || 'ℹ') + '</span>' +
        '<span class="bu-toast-message">' + message + '</span>' +
        '<button class="bu-toast-close" onclick="this.parentElement.remove()">✕</button>';
      container.appendChild(toast);
      setTimeout(() => { if (toast.parentElement) toast.remove(); }, duration);
    }
  };

  /* ── Clock ────────────────────────────────────────────── */
  BusinessUI.clock = {
    start(selector) {
      const el = document.querySelector(selector || '#clock');
      if (!el) return;
      function tick() {
        el.textContent = new Date().toLocaleString('pt-BR');
      }
      tick();
      setInterval(tick, 1000);
    }
  };

  window.BusinessUI = BusinessUI;
})();
