<!-- SideMenuDashboard.vue -->
<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="brand">
        <div class="brand-icon">R</div>
        <span>Reflectly</span>
        <button class="expand-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
      </div>

      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        <input
          type="text"
          class="search-input"
          placeholder="Search"
          v-model="searchQuery"
        >
        <span class="search-shortcut">⌘K</span>
      </div>
    </div>

    <nav class="nav-section">
      <a
        v-for="item in menuItems"
        :key="item.id"
        :class="['nav-item', { active: item.active, expanded: item.expanded, 'has-submenu': item.submenu }]"
        @click="handleNavClick(item)"
      >
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path :d="item.iconPath"></path>
        </svg>
        <span>{{ item.label }}</span>
        <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
        <svg v-if="item.submenu" class="nav-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </a>

      <div v-if="expandedMenu" class="submenu">
        <a
          v-for="subitem in getSubmenuItems(expandedMenu)"
          :key="subitem.id"
          class="submenu-item"
          @click="handleSubmenuClick(subitem)"
        >
          {{ subitem.label }}
          <svg v-if="subitem.hasAction" class="submenu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="1"></circle>
            <circle cx="19" cy="12" r="1"></circle>
            <circle cx="5" cy="12" r="1"></circle>
          </svg>
        </a>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="support-section">
        <div class="support-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
        </div>
        <div>
          <div class="support-title">Need support?</div>
          <div class="support-text">Get in touch with our agents</div>
        </div>
      </div>
      <button class="contact-btn">Contact us</button>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'SideMenuDashboard',
  data() {
    return {
      searchQuery: '',
      expandedMenu: null,
      menuItems: [
        {
          id: 'dashboard',
          label: 'Dashboard',
          active: true,
          iconPath: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'
        },
        {
          id: 'calendar',
          label: 'Calendar',
          active: false,
          iconPath: 'M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V6a2 2 0 00-2-2zm0 16H5V10h14v10z'
        },
        {
          id: 'updates',
          label: 'Updates',
          active: false,
          badge: '3',
          iconPath: 'M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0'
        },
        {
          id: 'messages',
          label: 'Messages',
          active: false,
          iconPath: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'
        },
        {
          id: 'mail',
          label: 'Mail',
          active: false,
          iconPath: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z M22 6l-10 7L2 6'
        },
        {
          id: 'workspace',
          label: 'Workspace',
          active: false,
          submenu: true,
          expanded: false,
          iconPath: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z'
        },
        {
          id: 'settings',
          label: 'Settings',
          active: false,
          submenu: true,
          expanded: false,
          iconPath: 'M12 15a3 3 0 100-6 3 3 0 000 6z M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z'
        },
        {
          id: 'account',
          label: 'Account',
          active: false,
          iconPath: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2 M12 11a4 4 0 100-8 4 4 0 000 8z'
        }
      ],
      submenus: {
        workspace: [
          { id: 'overview', label: 'Overview', hasAction: true },
          { id: 'settings', label: 'Settings', hasAction: false },
          { id: 'members', label: 'Members', hasAction: false },
          { id: 'integrations', label: 'Integrations', hasAction: false }
        ],
        settings: [
          { id: 'general', label: 'General', hasAction: false },
          { id: 'security', label: 'Security', hasAction: false },
          { id: 'notifications', label: 'Notifications', hasAction: false },
          { id: 'billing', label: 'Billing', hasAction: false }
        ]
      }
    }
  },
  methods: {
    handleNavClick(item) {
      if (item.submenu) {
        if (this.expandedMenu === item.id) {
          this.expandedMenu = null;
          item.expanded = false;
        } else {
          this.menuItems.forEach(m => m.expanded = false);
          this.expandedMenu = item.id;
          item.expanded = true;
        }
      } else {
        this.menuItems.forEach(m => m.active = false);
        item.active = true;
        this.$emit('navigate', item.id);
      }
    },
    handleSubmenuClick(subitem) {
      this.$emit('submenu-navigate', subitem.id);
    },
    getSubmenuItems(menuId) {
      return this.submenus[menuId] || [];
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  background: #1a1d23;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #2a2d35;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: #667eea;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.expand-btn {
  margin-left: auto;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.expand-btn:hover {
  background: #2a2d35;
  color: #fff;
}

.expand-btn svg {
  width: 16px;
  height: 16px;
}

.search-box {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 10px 36px 10px 36px;
  background: #0f1115;
  border: 1px solid #2a2d35;
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: #667eea;
  background: #14161b;
}

.search-input::placeholder {
  color: #6b7280;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  width: 16px;
  height: 16px;
}

.search-shortcut {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  font-size: 12px;
  background: #2a2d35;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;
}

.nav-section {
  padding: 12px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  color: #9ca3af;
  text-decoration: none;
  border-radius: 8px;
  margin-bottom: 2px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  position: relative;
}

.nav-item:hover {
  background: #2a2d35;
  color: #fff;
}

.nav-item.active {
  background: #667eea;
  color: #fff;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-badge {
  margin-left: auto;
  background: #667eea;
  color: #fff;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 600;
}

.nav-arrow {
  width: 16px;
  height: 16px;
  margin-left: auto;
  transition: transform 0.2s;
}

.nav-item.expanded .nav-arrow {
  transform: rotate(180deg);
}

.submenu {
  background: #14161b;
  border-radius: 8px;
  padding: 8px;
  margin: 8px 0 12px 0;
  border: 1px solid #2a2d35;
}

.submenu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  color: #9ca3af;
  text-decoration: none;
  border-radius: 6px;
  margin-bottom: 2px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.submenu-item:hover {
  background: #1a1d23;
  color: #fff;
}

.submenu-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #2a2d35;
}

.support-section {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.support-icon {
  width: 40px;
  height: 40px;
  background: #2a2d35;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.support-icon svg {
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.support-title {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
}

.support-text {
  color: #6b7280;
  font-size: 12px;
}

.contact-btn {
  width: 100%;
  padding: 10px;
  background: #2a2d35;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.contact-btn:hover {
  background: #3a3d45;
}
</style>