<template>
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <h2 v-if="!sidebarCollapsed">Fluxor</h2>
          <span v-else>F</span>
        </div>
        <button @click="toggleSidebar" class="sidebar-toggle">
          <i class="icon-menu"></i>
        </button>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <i class="icon-dashboard"></i>
          <span v-if="!sidebarCollapsed">Dashboard</span>
        </router-link>
        
        <router-link to="/users" class="nav-item" active-class="active">
          <i class="icon-users"></i>
          <span v-if="!sidebarCollapsed">Users</span>
        </router-link>
        
        <router-link to="/wallets" class="nav-item" active-class="active">
          <i class="icon-wallet"></i>
          <span v-if="!sidebarCollapsed">Wallets</span>
        </router-link>
        
        <router-link to="/trading" class="nav-item" active-class="active">
          <i class="icon-trading"></i>
          <span v-if="!sidebarCollapsed">Trading</span>
        </router-link>
        
        <router-link to="/transactions" class="nav-item" active-class="active">
          <i class="icon-transactions"></i>
          <span v-if="!sidebarCollapsed">Transactions</span>
        </router-link>
        
        <router-link to="/reports" class="nav-item" active-class="active">
          <i class="icon-reports"></i>
          <span v-if="!sidebarCollapsed">Reports</span>
        </router-link>
        
        <router-link to="/settings" class="nav-item" active-class="active">
          <i class="icon-settings"></i>
          <span v-if="!sidebarCollapsed">Settings</span>
        </router-link>
      </nav>
    </aside>
    
    <!-- Main Content -->
    <div class="main-content">
      <!-- Header -->
      <header class="header">
        <div class="header-left">
          <h1 class="page-title">{{ pageTitle }}</h1>
        </div>
        
        <div class="header-right">
          <div class="user-menu">
            <div class="user-info">
              <span class="user-name">{{ userDisplayName }}</span>
              <span class="user-role">{{ userRole }}</span>
            </div>
            <div class="user-avatar">
              {{ userInitials }}
            </div>
            <div class="user-dropdown">
              <button @click="showUserMenu = !showUserMenu" class="dropdown-toggle">
                <i class="icon-chevron-down"></i>
              </button>
              <div v-if="showUserMenu" class="dropdown-menu">
                <a href="#" @click="logout" class="dropdown-item">
                  <i class="icon-logout"></i>
                  Logout
                </a>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Page Content -->
      <main class="page-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const sidebarCollapsed = ref(false)
const showUserMenu = ref(false)

const pageTitle = computed(() => {
  const routeName = route.name as string
  if (!routeName) return 'Dashboard'
  
  const titles: Record<string, string> = {
    'dashboard': 'Dashboard',
    'users': 'User Management',
    'wallets': 'Wallet Management',
    'trading': 'Trading Control',
    'transactions': 'Transactions',
    'reports': 'Reports',
    'settings': 'Settings'
  }
  
  return titles[routeName] || routeName.charAt(0).toUpperCase() + routeName.slice(1)
})

const userDisplayName = computed(() => {
  if (!authStore.user) return 'Admin'
  return authStore.user.firstName && authStore.user.lastName 
    ? `${authStore.user.firstName} ${authStore.user.lastName}`
    : authStore.user.username || authStore.user.email
})

const userRole = computed(() => {
  if (!authStore.user) return 'Admin'
  if (authStore.user.role === 'admin') return 'Super Admin'
  return 'Admin'
})

const userInitials = computed(() => {
  if (!authStore.user) return 'A'
  const name = userDisplayName.value
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
})

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}

const handleClickOutside = (event: Event) => {
  const target = event.target as Element
  if (!target.closest('.user-menu')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
  background: var(--bg-primary);
}

.sidebar {
  width: 280px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo h2 {
  color: var(--primary-color);
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.logo span {
  color: var(--primary-color);
  font-size: 24px;
  font-weight: bold;
}

.sidebar-toggle {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.sidebar-toggle:hover {
  background: var(--bg-tertiary);
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--bg-tertiary);
  color: var(--primary-color);
  border-left-color: var(--primary-color);
}

.nav-item i {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  font-size: 18px;
}

.sidebar-collapsed .nav-item {
  justify-content: center;
  padding: 12px;
}

.sidebar-collapsed .nav-item i {
  margin-right: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 0 24px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 14px;
}

.user-role {
  color: var(--text-secondary);
  font-size: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  color: var(--text-dark);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.dropdown-toggle {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.dropdown-toggle:hover {
  background: var(--bg-tertiary);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  min-width: 150px;
  z-index: 1000;
  margin-top: 8px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: var(--text-primary);
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background: var(--bg-tertiary);
}

.dropdown-item i {
  margin-right: 8px;
  width: 16px;
}

.page-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: var(--bg-primary);
}

/* Icon placeholders - replace with actual icon font */
.icon-menu::before { content: '☰'; }
.icon-dashboard::before { content: '📊'; }
.icon-users::before { content: '👥'; }
.icon-wallet::before { content: '💰'; }
.icon-trading::before { content: '📈'; }
.icon-transactions::before { content: '💳'; }
.icon-reports::before { content: '📋'; }
.icon-settings::before { content: '⚙️'; }
.icon-chevron-down::before { content: '▼'; }
.icon-logout::before { content: '🚪'; }
</style>
