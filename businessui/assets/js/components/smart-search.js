(function () {
  'use strict';

  const BusinessUI = window.BusinessUI || {};

  BusinessUI.smartSearch = {
    apiUrl: '/api/search',
    minChars: 2,
    debounceMs: 300,
    timer: null,
    selectedIndex: -1,

    init(options) {
      if (options && options.apiUrl) this.apiUrl = options.apiUrl;
      if (options && options.minChars !== undefined) this.minChars = options.minChars;
      this._build();
      this._bindEvents();
    },

    _build() {
      const container = document.querySelector('.bu-topbar-search');
      if (!container) return;
      const input = container.querySelector('.bu-input');
      if (!input) return;
      input.setAttribute('autocomplete', 'off');
      input.setAttribute('data-smart-search', 'true');
      const dropdown = document.createElement('div');
      dropdown.className = 'bu-smart-search-dropdown';
      dropdown.id = 'smartSearchDropdown';
      container.appendChild(dropdown);
      this.input = input;
      this.dropdown = dropdown;
    },

    _bindEvents() {
      const input = this.input;
      input.addEventListener('input', () => {
        clearTimeout(this.timer);
        this.timer = setTimeout(() => this._search(), this.debounceMs);
      });
      input.addEventListener('focus', () => {
        if (input.value.length >= this.minChars) this._search();
      });
      input.addEventListener('keydown', (e) => this._keydown(e));
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.bu-topbar-search')) this._close();
      });
    },

    async _search() {
      const q = this.input.value.trim();
      if (q.length < this.minChars) { this._close(); return; }
      this.selectedIndex = -1;
      this.dropdown.innerHTML = `<div class="bu-smart-search-loading"><div class="bu-spinner"></div> Buscando...</div>`;
      this.dropdown.classList.add('open');
      try {
        const res = await fetch(`${this.apiUrl}?q=${encodeURIComponent(q)}&limit=5`);
        const data = await res.json();
        this._render(data.data || data);
      } catch (e) {
        this.dropdown.innerHTML = `<div class="bu-smart-search-empty">Erro ao buscar</div>`;
      }
    },

    _render(results) {
      const items = results?.items || results || [];
      if ((Array.isArray(items) && items.length === 0) || (typeof items === 'object' && Object.keys(items).length === 0)) {
        this.dropdown.innerHTML = `<div class="bu-smart-search-empty">Nenhum resultado encontrado</div>`;
        return;
      }
      let html = '';
      if (items.orders?.length || items.products?.length || items.customers?.length || items.quotations?.length || items.purchase_orders?.length || items.suppliers?.length) {
        const groups = [
          { key: 'products', icon: '📦', label: 'Produtos' },
          { key: 'orders', icon: '📄', label: 'Pedidos de Venda' },
          { key: 'purchase_orders', icon: '📋', label: 'Pedidos de Compra' },
          { key: 'quotations', icon: '💰', label: 'Cotações' },
          { key: 'customers', icon: '👥', label: 'Clientes' },
          { key: 'suppliers', icon: '🏭', label: 'Fornecedores' },
          { key: 'contracts', icon: '📑', label: 'Contratos' },
        ];
        groups.forEach(g => {
          const list = items[g.key];
          if (!list || !list.length) return;
          html += `<div class="bu-smart-search-group"><div class="bu-smart-search-group-label">${g.icon} ${g.label} (${list.length})</div>`;
          list.forEach((item, idx) => {
            const title = item.title || item.name || item.item_name || '';
            const subtitle = item.code || item.status || item.document_number || item.email || '';
            const type = item.type || g.key;
            html += `<div class="bu-smart-search-item" data-id="${item.id || item.item_id || ''}" data-type="${type}" onclick="BusinessUI.smartSearch._navigate('${type}','${item.id || item.item_id || ''}')">
              <div class="bu-smart-search-item-title">${title}</div>
              ${subtitle ? `<div class="bu-smart-search-item-sub">${subtitle}</div>` : ''}
            </div>`;
          });
          html += `</div>`;
        });
      } else if (Array.isArray(items)) {
        items.forEach(item => {
          const title = item.title || item.name || item.item_name || item.id || '';
          html += `<div class="bu-smart-search-item" onclick="BusinessUI.smartSearch._navigate('result','${item.id||''}')">
            <div class="bu-smart-search-item-title">${title}</div>
          </div>`;
        });
      }
      if (!html) { this.dropdown.innerHTML = `<div class="bu-smart-search-empty">Nenhum resultado</div>`; return; }
      this.dropdown.innerHTML = html;
      this.dropdown.querySelectorAll('.bu-smart-search-item').forEach((el, i) => {
        el.addEventListener('mouseenter', () => { this.selectedIndex = i; this._highlight(); });
      });
    },

    _highlight() {
      this.dropdown.querySelectorAll('.bu-smart-search-item').forEach((el, i) => {
        el.classList.toggle('selected', i === this.selectedIndex);
      });
    },

    _keydown(e) {
      const items = this.dropdown.querySelectorAll('.bu-smart-search-item');
      if (!items.length) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); this.selectedIndex = Math.min(this.selectedIndex + 1, items.length - 1); this._highlight(); this._scrollIntoView(items[this.selectedIndex]); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); this.selectedIndex = Math.max(this.selectedIndex - 1, 0); this._highlight(); this._scrollIntoView(items[this.selectedIndex]); }
      else if (e.key === 'Enter' && this.selectedIndex >= 0) { e.preventDefault(); items[this.selectedIndex].click(); }
      else if (e.key === 'Escape') { this._close(); }
    },

    _scrollIntoView(el) {
      if (el) el.scrollIntoView({ block: 'nearest' });
    },

    _navigate(type, id) {
      this._close();
      const routes = {
        'product': () => window.location.href = `/?tab=catalog&id=${id}`,
        'order': () => BusinessUI._switchTab && BusinessUI._switchTab('orders'),
        'purchase_order': () => BusinessUI._switchTab && BusinessUI._switchTab('orders'),
        'customer': () => BusinessUI._switchTab && BusinessUI._switchTab('customers'),
        'supplier': () => BusinessUI._switchTab && BusinessUI._switchTab('suppliers'),
        'quotation': () => BusinessUI._switchTab && BusinessUI._switchTab('comparison'),
        'contract': () => BusinessUI._switchTab && BusinessUI._switchTab('contracts'),
      };
      const handler = routes[type];
      if (handler) handler();
      else if (window.handleSmartSearch) window.handleSmartSearch(type, id);
    },

    _close() {
      this.dropdown.classList.remove('open');
      this.selectedIndex = -1;
    }
  };

  window.BusinessUI = BusinessUI;
})();
