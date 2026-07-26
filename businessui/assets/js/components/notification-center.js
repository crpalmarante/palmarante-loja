(function () {
  'use strict';

  const BusinessUI = window.BusinessUI || {};

  BusinessUI.notifications = {
    apiUrl: 'http://localhost:8010/api/notifications',
    tasksApiUrl: 'http://localhost:8010/api/tasks',
    approvalsApiUrl: 'http://localhost:8010/api/approvals',
    alertsApiUrl: 'http://localhost:8010/api/alerts',
    userId: 'user-001',
    pollInterval: null,

    init(options) {
      if (options) Object.assign(this, options);
      this._buildBell();
      this._buildNotificationCenter();
      this._bindEvents();
      this._poll();
      this.pollInterval = setInterval(() => this._poll(), 30000);
    },

    _buildBell() {
      const bell = document.querySelector('.bu-topbar-btn-notif');
      if (!bell) return;
      const badge = bell.querySelector('.bu-topbar-badge');
      this.bell = bell;
      this.badge = badge;
    },

    _buildNotificationCenter() {
      if (document.getElementById('buNotifCenter')) return;
      const div = document.createElement('div');
      div.id = 'buNotifCenter';
      div.className = 'bu-dialog-backdrop';
      div.innerHTML = `
        <div class="bu-dialog bu-dialog-xl bu-notif-dialog" style="max-width:680px;">
          <div class="bu-dialog-header">
            <h3>Central de Notificações</h3>
            <div style="display:flex;gap:var(--bu-space-3);align-items:center;">
              <button class="bu-btn bu-btn-sm bu-btn-ghost" onclick="BusinessUI.notifications.markAllRead()">Marcar tudo lido</button>
              <button class="bu-dialog-close" onclick="this.closest('.bu-dialog-backdrop').classList.remove('open')">✕</button>
            </div>
          </div>
          <div class="bu-notif-center-tabs" style="display:flex;gap:0;border-bottom:var(--bu-border-thin) solid var(--bu-border);padding:0 var(--bu-space-7);">
            <button class="bu-notif-tab active" data-tab="notifications">Notificações</button>
            <button class="bu-notif-tab" data-tab="tasks">Tarefas</button>
            <button class="bu-notif-tab" data-tab="approvals">Aprovações</button>
            <button class="bu-notif-tab" data-tab="alerts">Alertas</button>
          </div>
          <div class="bu-dialog-body" style="max-height:60vh;overflow-y:auto;padding:0;">
            <div class="bu-notif-panel active" id="buNotifPanel-notifications">
              <div class="bu-notif-loading">Carregando...</div>
            </div>
            <div class="bu-notif-panel" id="buNotifPanel-tasks">
              <div class="bu-notif-loading">Carregando...</div>
            </div>
            <div class="bu-notif-panel" id="buNotifPanel-approvals">
              <div class="bu-notif-loading">Carregando...</div>
            </div>
            <div class="bu-notif-panel" id="buNotifPanel-alerts">
              <div class="bu-notif-loading">Carregando...</div>
            </div>
          </div>
        </div>`;
      document.body.appendChild(div);

      div.querySelectorAll('.bu-notif-tab').forEach(tab => {
        tab.addEventListener('click', () => {
          div.querySelectorAll('.bu-notif-tab').forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          div.querySelectorAll('.bu-notif-panel').forEach(p => p.classList.remove('active'));
          const panel = document.getElementById('buNotifPanel-' + tab.dataset.tab);
          if (panel) panel.classList.add('active');
          this._loadTab(tab.dataset.tab);
        });
      });
    },

    _bindEvents() {
      if (this.bell) {
        this.bell.addEventListener('click', (e) => {
          e.stopPropagation();
          const dropdown = document.getElementById('buNotifDropdown');
          if (dropdown && dropdown.classList.contains('open')) {
            this._closeDropdown();
          } else {
            this._openDropdown();
          }
        });
      }
      document.addEventListener('click', (e) => {
        if (!e.target.closest('#buNotifDropdown') && !e.target.closest('.bu-topbar-btn-notif')) {
          this._closeDropdown();
        }
      });
    },

    _poll() {
      this._updateBadge();
    },

    async _updateBadge() {
      try {
        const r = await fetch(`${this.apiUrl}/unread-count?user_id=${this.userId}`);
        const data = await r.json();
        const count = data?.data?.count || 0;
        if (this.badge) {
          if (count > 0) {
            this.badge.textContent = count > 99 ? '99+' : count;
            this.badge.style.display = 'flex';
          } else {
            this.badge.style.display = 'none';
          }
        }
      } catch (e) { /* ignore */ }
    },

    async _openDropdown() {
      let dropdown = document.getElementById('buNotifDropdown');
      if (!dropdown) {
        dropdown = document.createElement('div');
        dropdown.id = 'buNotifDropdown';
        dropdown.className = 'bu-notif-dropdown';
        document.body.appendChild(dropdown);
      }
      dropdown.classList.add('open');
      this._loadDropdown(dropdown);
    },

    _closeDropdown() {
      const dropdown = document.getElementById('buNotifDropdown');
      if (dropdown) dropdown.classList.remove('open');
    },

    async _loadDropdown(container) {
      container.innerHTML = '<div class="bu-notif-loading" style="padding:var(--bu-space-7);text-align:center;">Carregando...</div>';
      try {
        const [notifRes, taskRes, alertRes, approvalRes] = await Promise.all([
          fetch(`${this.apiUrl}?user_id=${this.userId}&unread_only=true&limit=5`),
          fetch(`${this.tasksApiUrl}/pending?user_id=${this.userId}`),
          fetch(`${this.alertsApiUrl}?user_id=${this.userId}`),
          fetch(`${this.approvalsApiUrl}/pending?user_id=${this.userId}`),
        ]);
        const notifications = (await notifRes.json())?.data || [];
        const tasks = (await taskRes.json())?.data || [];
        const alerts = (await alertRes.json())?.data || [];
        const approvals = (await approvalRes.json())?.data || [];

        let html = '<div class="bu-notif-dropdown-header"><span>Notificações</span><button class="bu-btn bu-btn-sm bu-btn-ghost" onclick="BusinessUI.notifications.openCenter()">Ver todas</button></div>';
        if (!notifications.length && !tasks.length && !alerts.length && !approvals.length) {
          html += '<div class="bu-notif-empty">Nenhuma notificação pendente</div>';
        } else {
          if (notifications.length) {
            html += '<div class="bu-notif-group-label">📬 Não lidas</div>';
            notifications.forEach(n => {
              html += `<div class="bu-notif-item" onclick="BusinessUI.notifications.markRead('${n.id}');${n.action_url ? `BusinessUI._switchTab && BusinessUI._switchTab('${n.entity_type}')` : ''}">
                <div class="bu-notif-item-icon">${n.icon || '📄'}</div>
                <div class="bu-notif-item-content">
                  <div class="bu-notif-item-title">${n.title}</div>
                  <div class="bu-notif-item-meta">${n.message || ''}</div>
                </div>
                <span class="bu-notif-item-time">${this._timeAgo(n.created_at)}</span>
              </div>`;
            });
          }
          if (tasks.length) {
            html += '<div class="bu-notif-group-label">✅ Tarefas pendentes</div>';
            tasks.slice(0, 3).forEach(t => {
              html += `<div class="bu-notif-item">
                <div class="bu-notif-item-icon">📋</div>
                <div class="bu-notif-item-content">
                  <div class="bu-notif-item-title">${t.title}</div>
                  <div class="bu-notif-item-meta">${t.overdue ? '🔴 Atrasada' : `Prioridade: ${t.priority}`}</div>
                </div>
                <span class="bu-notif-item-time">${this._timeAgo(t.created_at)}</span>
              </div>`;
            });
          }
          if (approvals.length) {
            html += '<div class="bu-notif-group-label">⏳ Aprovações pendentes</div>';
            approvals.slice(0, 3).forEach(a => {
              html += `<div class="bu-notif-item">
                <div class="bu-notif-item-icon">✋</div>
                <div class="bu-notif-item-content">
                  <div class="bu-notif-item-title">${a.title}</div>
                  <div class="bu-notif-item-meta">${a.overdue ? '🔴 Urgente' : `Prazo: ${a.deadline ? new Date(a.deadline).toLocaleDateString('pt-BR') : '—'}`}</div>
                </div>
              </div>`;
            });
          }
          if (alerts.length) {
            html += '<div class="bu-notif-group-label">⚠️ Alertas ativos</div>';
            alerts.slice(0, 2).forEach(a => {
              html += `<div class="bu-notif-item bu-notif-item-alert">
                <div class="bu-notif-item-icon">${a.severity === 'critical' ? '🔴' : '⚠️'}</div>
                <div class="bu-notif-item-content">
                  <div class="bu-notif-item-title">${a.title}</div>
                  <div class="bu-notif-item-meta">${a.message || ''}</div>
                </div>
              </div>`;
            });
          }
        }
        html += '<div class="bu-notif-dropdown-footer"><button class="bu-btn bu-btn-sm bu-btn-primary" onclick="BusinessUI.notifications.openCenter()">Abrir Central</button></div>';
        container.innerHTML = html;
      } catch (e) {
        container.innerHTML = '<div class="bu-notif-empty">Erro ao carregar notificações</div>';
      }
    },

    async _loadTab(tab) {
      const panel = document.getElementById('buNotifPanel-' + tab);
      if (!panel || panel.dataset.loaded) return;
      panel.dataset.loaded = 'true';
      panel.innerHTML = '<div class="bu-notif-loading">Carregando...</div>';
      try {
        if (tab === 'notifications') {
          const r = await fetch(`${this.apiUrl}?user_id=${this.userId}&limit=50`);
          const items = (await r.json())?.data || [];
          if (!items.length) { panel.innerHTML = '<div class="bu-notif-empty" style="padding:var(--bu-space-7);">Nenhuma notificação</div>'; return; }
          let html = '';
          items.forEach(n => {
            html += `<div class="bu-notif-item ${n.read ? 'bu-notif-item-read' : ''}" onclick="BusinessUI.notifications.markRead('${n.id}')">
              <div class="bu-notif-item-icon">${n.icon || '📄'}</div>
              <div class="bu-notif-item-content">
                <div class="bu-notif-item-title">${n.title}</div>
                <div class="bu-notif-item-meta">${n.message || ''}</div>
              </div>
              <div style="display:flex;flex-direction:column;align-items:flex-end;gap:2px;">
                <span class="bu-notif-item-time">${this._timeAgo(n.created_at)}</span>
                ${n.read ? '' : '<span class="bu-badge bu-badge-primary" style="font-size:8px;width:8px;height:8px;padding:0;border-radius:50%;"></span>'}
              </div>
            </div>`;
          });
          panel.innerHTML = html;
        } else if (tab === 'tasks') {
          const r = await fetch(`${this.tasksApiUrl}?user_id=${this.userId}`);
          const items = (await r.json())?.data || [];
          if (!items.length) { panel.innerHTML = '<div class="bu-notif-empty" style="padding:var(--bu-space-7);">Nenhuma tarefa</div>'; return; }
          let html = '';
          items.forEach(t => {
            const statusIcons = { pending: '⏳', in_progress: '🔄', completed: '✅', cancelled: '❌' };
            html += `<div class="bu-notif-item">
              <div class="bu-notif-item-icon">${statusIcons[t.status] || '📋'}</div>
              <div class="bu-notif-item-content">
                <div class="bu-notif-item-title">${t.title}</div>
                <div class="bu-notif-item-meta">${t.category ? t.category + ' · ' : ''}${t.overdue ? '🔴 Atrasada' : t.due_date ? '📅 ' + new Date(t.due_date).toLocaleDateString('pt-BR') : 'Sem prazo'}</div>
              </div>
              <div>
                <span class="bu-badge bu-badge-${t.status === 'completed' ? 'success' : t.status === 'in_progress' ? 'info' : t.status === 'cancelled' ? 'neutral' : 'warning'}">${t.status.replace('_', ' ')}</span>
              </div>
            </div>`;
          });
          panel.innerHTML = html;
        } else if (tab === 'approvals') {
          const r = await fetch(`${this.approvalsApiUrl}/pending?user_id=${this.userId}`);
          const items = (await r.json())?.data || [];
          if (!items.length) { panel.innerHTML = '<div class="bu-notif-empty" style="padding:var(--bu-space-7);">Nenhuma aprovação pendente</div>'; return; }
          let html = '';
          items.forEach(a => {
            html += `<div class="bu-notif-item ${a.overdue ? 'bu-notif-item-alert' : ''}">
              <div class="bu-notif-item-icon">✋</div>
              <div class="bu-notif-item-content">
                <div class="bu-notif-item-title">${a.title}</div>
                <div class="bu-notif-item-meta">${a.target_type} · ${a.overdue ? '🔴 Atrasado' : a.deadline ? '📅 ' + new Date(a.deadline).toLocaleDateString('pt-BR') : 'Sem prazo'}</div>
              </div>
              <div style="display:flex;gap:var(--bu-space-2);">
                <button class="bu-btn bu-btn-sm bu-btn-success" onclick="BusinessUI.notifications._approve('${a.id}')">✓</button>
                <button class="bu-btn bu-btn-sm bu-btn-danger" onclick="BusinessUI.notifications._reject('${a.id}')">✕</button>
              </div>
            </div>`;
          });
          panel.innerHTML = html;
        } else if (tab === 'alerts') {
          const r = await fetch(`${this.alertsApiUrl}?user_id=${this.userId}`);
          const items = (await r.json())?.data || [];
          if (!items.length) { panel.innerHTML = '<div class="bu-notif-empty" style="padding:var(--bu-space-7);">Nenhum alerta</div>'; return; }
          let html = '';
          items.forEach(a => {
            const sevIcons = { critical: '🔴', warning: '⚠️', info: 'ℹ️' };
            html += `<div class="bu-notif-item ${a.severity === 'critical' ? 'bu-notif-item-alert' : ''}">
              <div class="bu-notif-item-icon">${sevIcons[a.severity] || 'ℹ️'}</div>
              <div class="bu-notif-item-content">
                <div class="bu-notif-item-title">${a.title}</div>
                <div class="bu-notif-item-meta">${a.message || ''}</div>
              </div>
              ${a.acknowledged ? '<span class="bu-badge bu-badge-neutral">visto</span>' : `<button class="bu-btn bu-btn-sm" onclick="BusinessUI.notifications._acknowledgeAlert('${a.id}', this)">OK</button>`}
            </div>`;
          });
          panel.innerHTML = html;
        }
      } catch (e) {
        panel.innerHTML = '<div class="bu-notif-empty" style="padding:var(--bu-space-7);">Erro ao carregar</div>';
      }
    },

    openCenter() {
      this._closeDropdown();
      const dialog = document.getElementById('buNotifCenter');
      if (dialog) dialog.classList.add('open');
      document.querySelectorAll('.bu-notif-panel').forEach(p => { p.dataset.loaded = ''; p.innerHTML = '<div class="bu-notif-loading">Carregando...</div>'; });
      this._loadTab('notifications');
    },

    async markRead(id) {
      try {
        await fetch(`${this.apiUrl}/${id}/read`, { method: 'POST' });
        this._updateBadge();
      } catch (e) { /* ignore */ }
    },

    async markAllRead() {
      try {
        await fetch(`${this.apiUrl}/read-all?user_id=${this.userId}`, { method: 'POST' });
        this._updateBadge();
        document.querySelectorAll('#buNotifPanel-notifications .bu-notif-item').forEach(el => el.classList.add('bu-notif-item-read'));
      } catch (e) { /* ignore */ }
    },

    async _approve(id) {
      try {
        await fetch(`${this.approvalsApiUrl}/${id}/approve`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: this.userId, reason: 'Aprovado' }),
        });
        document.getElementById('buNotifPanel-approvals').dataset.loaded = '';
        this._loadTab('approvals');
        this._updateBadge();
      } catch (e) { /* ignore */ }
    },

    async _reject(id) {
      try {
        await fetch(`${this.approvalsApiUrl}/${id}/reject`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: this.userId, reason: 'Recusado' }),
        });
        document.getElementById('buNotifPanel-approvals').dataset.loaded = '';
        this._loadTab('approvals');
        this._updateBadge();
      } catch (e) { /* ignore */ }
    },

    async _acknowledgeAlert(id, btn) {
      try {
        await fetch(`${this.alertsApiUrl}/${id}/acknowledge`, { method: 'POST' });
        btn.closest('.bu-notif-item')?.remove();
      } catch (e) { /* ignore */ }
    },

    _timeAgo(iso) {
      if (!iso) return '';
      const diff = Date.now() - new Date(iso).getTime();
      const mins = Math.floor(diff / 60000);
      if (mins < 1) return 'agora';
      if (mins < 60) return `${mins}min`;
      const hours = Math.floor(mins / 60);
      if (hours < 24) return `${hours}h`;
      const days = Math.floor(hours / 24);
      if (days < 30) return `${days}d`;
      return new Date(iso).toLocaleDateString('pt-BR');
    },
  };

  window.BusinessUI = BusinessUI;
})();
