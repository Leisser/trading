import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DashboardLayout from '../components/DashboardLayout.vue'
import DashboardView from '../views/SimpleDashboard.vue'
import LoginForm from '../components/LoginForm.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginForm,
      meta: { requiresGuest: true }
    },
    {
      path: '/',
      component: DashboardLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardView,
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('../views/UsersView.vue'),
          meta: { requiresSuperAdmin: true }
        },
        {
          path: 'wallets',
          name: 'wallets',
          component: () => import('../views/WalletManagement.vue'),
        },
        {
          path: 'trading',
          name: 'trading',
          component: () => import('../views/TradingControlView.vue'),
        },
        {
          path: 'transactions',
          name: 'transactions',
          component: () => import('../views/TransactionView.vue'),
        },
        {
          path: 'cryptocurrencies',
          name: 'cryptocurrencies',
          component: () => import('../views/CryptocurrenciesView.vue'),
        },
        {
          path: 'reports',
          name: 'reports',
          component: () => import('../views/ReportsView.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/SettingsView.vue'),
        },
      ],
    },
  ],
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Initialize auth store if not already done
  if (!authStore.isAuthenticated && localStorage.getItem('auth_token')) {
    await authStore.initialize()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check if route requires admin privileges
  if (to.meta.requiresAdmin && !authStore.isAdmin && !authStore.isManager) {
    next('/login')
    return
  }

  // Check if route requires super admin privileges
  if (to.meta.requiresSuperAdmin && !authStore.isAdmin) {
    next('/')
    return
  }

  // Redirect authenticated users away from login
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router
