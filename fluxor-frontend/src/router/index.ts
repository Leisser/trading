import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import FirebaseLoginView from '../views/FirebaseLogin.vue'
import DashboardLoginView from '../views/DashboardLogin.vue'
import DashboardView from '../views/DashboardView.vue'
import AdminView from '../views/AdminView.vue'
import ProfileView from '../views/ProfileView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import LiveTradeView from '../views/LiveTradeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
        {
          path: '/login',
          name: 'login',
          component: FirebaseLoginView,
          meta: { requiresGuest: true },
        },
        {
          path: '/register',
          name: 'register',
          component: FirebaseLoginView,
          meta: { requiresGuest: true },
          beforeEnter: (to) => {
            to.query.mode = 'register'
          }
        },
    {
      path: '/firebase-login',
      name: 'firebase-login',
      component: FirebaseLoginView,
      meta: { requiresGuest: true },
    },
    {
      path: '/dashboard-login',
      name: 'dashboard-login',
      component: DashboardLoginView,
      meta: { requiresGuest: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/live-trade',
      name: 'live-trade',
      component: LiveTradeView,
      meta: { requiresAuth: true },
    },
  ],
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check if we have stored tokens but user is not authenticated (initial load)
  if (!authStore.isAuthenticated) {
    try {
      console.log('Restoring authentication from storage...')
      // Load tokens and fetch user data
      await authStore.loadTokens()
      console.log('Authentication restored from storage')
    } catch (error) {
      console.error('Failed to restore authentication:', error)
      // Clear invalid tokens
      await authStore.logout()
    }
  }

  // If user is authenticated and trying to access home/login/register, redirect to dashboard
  if (
    authStore.isAuthenticated &&
    (to.path === '/' || to.path === '/login' || to.path === '/register')
  ) {
    next('/dashboard')
  }
  // If route requires auth and user is not authenticated, redirect to login
  else if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  }
  // If route requires guest (login/register) and user is authenticated, redirect to dashboard
  else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
  }
  // If route requires admin and user is not admin, redirect to dashboard
  else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/dashboard')
  }
  // Otherwise, allow navigation
  else {
    next()
  }
})

export default router
