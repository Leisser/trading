import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '../components/DashboardLayout.vue'
import DashboardView from '../views/SimpleDashboard.vue'
import CryptocurrenciesView from '../views/CryptocurrenciesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DashboardLayout,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardView,
        },
        {
          path: 'cryptocurrencies',
          name: 'cryptocurrencies',
          component: CryptocurrenciesView,
        },
        {
          path: 'trading',
          name: 'trading',
          component: () => import('../views/TradingControlView.vue'),
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('../views/UsersView.vue'),
        },
        {
          path: 'reports',
          name: 'reports',
          component: () => import('../views/ReportsView.vue'),
        },
        {
          path: 'security',
          name: 'security',
          component: () => import('../views/SecurityView.vue'),
        },
        {
          path: 'system',
          name: 'system',
          component: () => import('../views/SystemView.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/SettingsView.vue'),
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
  ],
})

export default router
