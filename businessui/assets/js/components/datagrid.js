/* ══════════════════════════════════════════════════════════════
   BusinessUI — DataGrid Component
   v1.0.0
   ─────────────────────────────────────────────────────────────
   Componente mais importante do sistema.
   ══════════════════════════════════════════════════════════════ */

class DataGrid {
  constructor(container, options) {
    this.container = typeof container === 'string'
      ? document.querySelector(container)
      : container;

    this.options = Object.assign({
      columns: [],
      data: [],
      pageSize: 10,
      pageSizes: [10, 25, 50, 100],
      selectable: false,
      searchable: true,
      sortable: true,
      actions: [],
      emptyText: 'Nenhum registro encontrado.',
      emptyHint: 'Tente ajustar os filtros ou cadastrar um novo registro.',
      onRowClick: null,
      onSelectionChange: null,
      onPageChange: null,
      onSort: null,
      onSearch: null,
      onAction: null,
      rowClass: null
    }, options);

    this.state = {
      data: [],
      filtered: [],
      page: 1,
      pageSize: this.options.pageSize,
      search: '',
      sortField: null,
      sortDir: 'asc',
      selected: new Set(),
      loading: false
    };

    this.el = null;
    this.render();
    this.load(this.options.data);
  }

  /* ── Render ──────────────────────────────────────────── */
  render() {
    this.el = document.createElement('div');
    this.el.className = 'bu-datagrid';
    this.el.innerHTML = `
      <div class="bu-datagrid-toolbar">
        ${this.options.searchable ? `
          <div class="bu-datagrid-search">
            <span class="bu-datagrid-search-icon">🔍</span>
            <input class="bu-input bu-input-sm" placeholder="Pesquisar..." data-dg-search>
          </div>
        ` : ''}
        <span class="bu-datagrid-info" data-dg-info></span>
        <div class="bu-datagrid-actions" data-dg-actions></div>
      </div>
      <div class="bu-datagrid-wrapper">
        <table class="bu-datagrid-table">
          <thead><tr data-dg-header></tr></thead>
          <tbody data-dg-body></tbody>
        </table>
        <div class="bu-datagrid-loading" data-dg-loading style="display:none;">
          <div class="bu-datagrid-spinner"></div>
          Carregando...
        </div>
        <div class="bu-datagrid-empty" data-dg-empty style="display:none;">
          <div class="bu-datagrid-empty-icon">📋</div>
          <div class="bu-datagrid-empty-text">${this.options.emptyText}</div>
          <div class="bu-datagrid-empty-hint">${this.options.emptyHint}</div>
        </div>
      </div>
      <div class="bu-datagrid-pagination" data-dg-pagination></div>
    `;
    this.container.appendChild(this.el);

    this.cache = {
      search: this.el.querySelector('[data-dg-search]'),
      info: this.el.querySelector('[data-dg-info]'),
      header: this.el.querySelector('[data-dg-header]'),
      body: this.el.querySelector('[data-dg-body]'),
      loading: this.el.querySelector('[data-dg-loading]'),
      empty: this.el.querySelector('[data-dg-empty]'),
      pagination: this.el.querySelector('[data-dg-pagination]'),
      actions: this.el.querySelector('[data-dg-actions]')
    };

    this.renderHeader();
    this.renderActions();
    this.bindEvents();
  }

  /* ── Header ──────────────────────────────────────────── */
  renderHeader() {
    const cols = this.getColumns();
    let html = '';

    if (this.options.selectable) {
      html += '<th class="bu-datagrid-checkbox-col"><input type="checkbox" class="bu-datagrid-checkbox" data-dg-select-all></th>';
    }

    cols.forEach(col => {
      const sortable = this.options.sortable && col.sortable !== false;
      const sorted = this.state.sortField === col.field;
      const icon = sorted ? (this.state.sortDir === 'asc' ? '▲' : '▼') : '⇅';
      html += `<th class="${sortable ? 'sortable' : ''} ${sorted ? 'sorted' : ''}" data-field="${col.field}" ${col.width ? `style="width:${col.width}"` : ''}>
        <div class="bu-datagrid-th-content">
          <span>${col.label || col.field}</span>
          ${sortable ? `<span class="bu-datagrid-sort-icon">${icon}</span>` : ''}
        </div>
      </th>`;
    });

    if (this.options.actions.length) {
      html += '<th class="bu-datagrid-actions-col"></th>';
    }

    this.cache.header.innerHTML = html;
  }

  /* ── Body ────────────────────────────────────────────── */
  renderBody() {
    const cols = this.getColumns();
    const rows = this.getPageData();
    let html = '';

    if (!rows.length) {
      this.cache.body.innerHTML = '';
      this.cache.empty.style.display = 'flex';
      return;
    }
    this.cache.empty.style.display = 'none';

    rows.forEach((row, idx) => {
      const uid = row._uid != null ? row._uid : (row.id || idx);
      const selected = this.state.selected.has(uid);
      const extraClass = typeof this.options.rowClass === 'function' ? ' ' + this.options.rowClass(row) : '';

      html += `<tr class="${selected ? 'selected' : ''}${extraClass}" data-uid="${uid}">`;

      if (this.options.selectable) {
        html += `<td class="bu-datagrid-checkbox-col"><input type="checkbox" class="bu-datagrid-checkbox" ${selected ? 'checked' : ''} data-dg-select></td>`;
      }

      cols.forEach(col => {
        const val = row[col.field];
        const display = col.formatter ? col.formatter(val, row) : (val != null ? val : '-');
        html += `<td data-label="${col.label || col.field}">${display}</td>`;
      });

      if (this.options.actions.length) {
        html += '<td class="bu-datagrid-actions-col">';
        this.options.actions.forEach((act, ai) => {
          html += `<button class="bu-btn bu-btn-ghost bu-btn-sm bu-btn-icon" data-dg-action="${ai}" title="${act.label || ''}">${act.icon || '⋯'}</button>`;
        });
        html += '</td>';
      }

      html += '</tr>';
    });

    this.cache.body.innerHTML = html;
    this.updateInfo();
    this.renderPagination();
  }

  /* ── Pagination ──────────────────────────────────────── */
  renderPagination() {
    const total = this.state.filtered.length;
    const pages = Math.ceil(total / this.state.pageSize) || 1;
    const page = Math.min(this.state.page, pages);
    this.state.page = page;

    if (total === 0) {
      this.cache.pagination.innerHTML = '';
      return;
    }

    let html = `
      <div class="bu-datagrid-pagination-info">
        ${(page - 1) * this.state.pageSize + 1}–${Math.min(page * this.state.pageSize, total)} de ${total}
      </div>
      <div class="bu-datagrid-pagination-pages">
        <button class="bu-datagrid-page-btn" data-dg-page="prev" ${page <= 1 ? 'disabled' : ''}>‹</button>`;

    const maxBtns = 5;
    let start = Math.max(1, page - Math.floor(maxBtns / 2));
    let end = Math.min(pages, start + maxBtns - 1);
    if (end - start < maxBtns - 1) start = Math.max(1, end - maxBtns + 1);

    if (start > 1) {
      html += `<button class="bu-datagrid-page-btn" data-dg-page="1">1</button>`;
      if (start > 2) html += `<span style="color:var(--bu-text-muted);padding:0 var(--bu-space-1);">…</span>`;
    }

    for (let i = start; i <= end; i++) {
      html += `<button class="bu-datagrid-page-btn ${i === page ? 'active' : ''}" data-dg-page="${i}">${i}</button>`;
    }

    if (end < pages) {
      if (end < pages - 1) html += `<span style="color:var(--bu-text-muted);padding:0 var(--bu-space-1);">…</span>`;
      html += `<button class="bu-datagrid-page-btn" data-dg-page="${pages}">${pages}</button>`;
    }

    html += `
        <button class="bu-datagrid-page-btn" data-dg-page="next" ${page >= pages ? 'disabled' : ''}>›</button>
      </div>
      <div class="bu-datagrid-page-size">
        <span>Por página:</span>
        <select class="bu-select" data-dg-page-size>
          ${this.options.pageSizes.map(s => `<option value="${s}" ${s === this.state.pageSize ? 'selected' : ''}>${s}</option>`).join('')}
        </select>
      </div>`;

    this.cache.pagination.innerHTML = html;
  }

  /* ── Actions toolbar ─────────────────────────────────── */
  renderActions() {
    this.cache.actions.innerHTML = '';
  }

  /* ── Events ──────────────────────────────────────────── */
  bindEvents() {
    const self = this;

    // Search
    if (this.cache.search) {
      let timer;
      this.cache.search.addEventListener('input', function () {
        clearTimeout(timer);
        timer = setTimeout(() => {
          self.search(this.value);
          if (self.options.onSearch) self.options.onSearch(this.value);
        }, 250);
      });
    }

    // Header sort
    this.cache.header.addEventListener('click', function (e) {
      const th = e.target.closest('th');
      if (!th || !th.classList.contains('sortable')) return;
      const field = th.dataset.field;
      if (!field) return;
      const dir = (self.state.sortField === field && self.state.sortDir === 'asc') ? 'desc' : 'asc';
      self.sort(field, dir);
    });

    // Body events (click, select, action)
    this.cache.body.addEventListener('click', function (e) {
      const tr = e.target.closest('tr');
      if (!tr) return;

      // Action button
      const actBtn = e.target.closest('[data-dg-action]');
      if (actBtn) {
        const idx = parseInt(actBtn.dataset.dgAction);
        const uid = parseInt(tr.dataset.uid);
        const row = self.state.filtered.find(r => (r._uid != null ? r._uid : (r.id || self.state.filtered.indexOf(r))) === uid);
        if (row && self.options.actions[idx]) {
          self.options.actions[idx].action(row, idx);
          if (self.options.onAction) self.options.onAction(row, idx);
        }
        return;
      }

      // Select
      const cb = e.target.closest('[data-dg-select]');
      if (cb) {
        self.toggleSelect(tr.dataset.uid);
        return;
      }

      // Select all
      const allCb = e.target.closest('[data-dg-select-all]');
      if (allCb) {
        self.selectAll(allCb.checked);
        return;
      }

      // Row click
      if (self.options.onRowClick) {
        const uid = parseInt(tr.dataset.uid);
        const row = self.state.filtered.find(r => (r._uid != null ? r._uid : (r.id || self.state.filtered.indexOf(r))) === uid);
        if (row) self.options.onRowClick(row);
      }
    });

    // Pagination events
    this.cache.pagination.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-dg-page]');
      if (!btn || btn.disabled) return;
      const val = btn.dataset.dgPage;
      if (val === 'prev') self.prevPage();
      else if (val === 'next') self.nextPage();
      else self.goToPage(parseInt(val));
    });

    this.cache.pagination.addEventListener('change', function (e) {
      const sel = e.target.closest('[data-dg-page-size]');
      if (sel) {
        self.state.pageSize = parseInt(sel.value);
        self.state.page = 1;
        self.renderBody();
        if (self.options.onPageChange) self.options.onPageChange(self.state.page, self.state.pageSize);
      }
    });
  }

  /* ── Core methods ────────────────────────────────────── */
  load(data) {
    this.state.data = data.map((row, i) => {
      if (row._uid == null) row._uid = row.id || i;
      return row;
    });
    this.state.page = 1;
    this.state.search = '';
    this.state.sortField = null;
    this.state.sortDir = 'asc';
    this.state.selected = new Set();
    this.filter();
  }

  reload() {
    this.filter();
  }

  search(query) {
    this.state.search = query.toLowerCase().trim();
    this.state.page = 1;
    this.filter();
  }

  sort(field, dir) {
    this.state.sortField = field;
    this.state.sortDir = dir || 'asc';
    this.renderHeader();
    this.filter();
  }

  goToPage(page) {
    const max = Math.ceil(this.state.filtered.length / this.state.pageSize) || 1;
    this.state.page = Math.max(1, Math.min(page, max));
    this.renderBody();
    if (this.options.onPageChange) this.options.onPageChange(this.state.page, this.state.pageSize);
  }

  prevPage() { if (this.state.page > 1) this.goToPage(this.state.page - 1); }
  nextPage() { this.goToPage(this.state.page + 1); }

  getSelected() {
    const selected = [];
    this.state.filtered.forEach(row => {
      const uid = row._uid != null ? row._uid : (row.id || this.state.filtered.indexOf(row));
      if (this.state.selected.has(uid)) selected.push(row);
    });
    return selected;
  }

  selectAll(checked) {
    const rows = this.getPageData();
    if (checked) {
      rows.forEach(row => {
        const uid = row._uid != null ? row._uid : (row.id || this.state.filtered.indexOf(row));
        this.state.selected.add(uid);
      });
    } else {
      rows.forEach(row => {
        const uid = row._uid != null ? row._uid : (row.id || this.state.filtered.indexOf(row));
        this.state.selected.delete(uid);
      });
    }
    this.renderBody();
    if (this.options.onSelectionChange) this.options.onSelectionChange(this.getSelected());
  }

  toggleSelect(uid) {
    uid = parseInt(uid);
    if (this.state.selected.has(uid)) this.state.selected.delete(uid);
    else this.state.selected.add(uid);
    this.renderBody();
    if (this.options.onSelectionChange) this.options.onSelectionChange(this.getSelected());
  }

  /* ── Internal ────────────────────────────────────────── */
  getColumns() {
    return this.options.columns;
  }

  filter() {
    let data = this.state.data;

    if (this.state.search) {
      const q = this.state.search;
      data = data.filter(row => {
        return this.options.columns.some(col => {
          const val = row[col.field];
          return val != null && String(val).toLowerCase().includes(q);
        });
      });
    }

    if (this.state.sortField) {
      const field = this.state.sortField;
      const dir = this.state.sortDir === 'asc' ? 1 : -1;
      data = [...data].sort((a, b) => {
        const va = a[field], vb = b[field];
        if (va == null) return 1;
        if (vb == null) return -1;
        if (typeof va === 'number' && typeof vb === 'number') return (va - vb) * dir;
        return String(va).localeCompare(String(vb), 'pt-BR') * dir;
      });
    }

    this.state.filtered = data;
    this.state.page = 1;
    this.renderBody();
  }

  getPageData() {
    const start = (this.state.page - 1) * this.state.pageSize;
    return this.state.filtered.slice(start, start + this.state.pageSize);
  }

  updateInfo() {
    const total = this.state.filtered.length;
    const sel = this.state.selected.size;
    const parts = [];
    if (sel > 0) parts.push(`${sel} selecionado${sel > 1 ? 's' : ''}`);
    if (this.cache.search && this.cache.search.value) parts.push(`filtrados: ${total}`);
    this.cache.info.textContent = parts.length ? parts.join(' · ') : (total > 0 ? `${total} registro${total > 1 ? 's' : ''}` : '');
  }

  setLoading(on) {
    this.state.loading = on;
    this.cache.loading.style.display = on ? 'flex' : 'none';
    if (on) {
      this.cache.body.innerHTML = '';
      this.cache.empty.style.display = 'none';
    }
    if (!on) this.renderBody();
  }

  destroy() {
    if (this.el && this.el.parentElement) {
      this.el.parentElement.removeChild(this.el);
    }
  }
}
