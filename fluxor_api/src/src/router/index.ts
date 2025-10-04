import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy-loaded components
const Dashboard = () => import('@/views/Dashboard.vue')
const Trading = () => import('@/views/Trading.vue')
const Portfolio = () => import('@/views/Portfolio.vue')
const History = () => import('@/views/History.vue')
const Settings = () => import('@/views/Settings.vue')
const Login = () => import('@/views/auth/Login.vue')
const Register = () => import('@/views/auth/Register.vue')
const ForgotPassword = () => import('@/views/auth/ForgotPassword.vue')
const Profile = () => import('@/views/Profile.vue')
const Security = () => import('@/views/Security.vue')
const ApiKeys = () => import('@/views/ApiKeys.vue')

const routes: Array<RouteRecordRaw> = [
  // Authentication routes
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { 
      requiresAuth: false,
      title: 'Login - Fluxor Trading'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { 
      requiresAuth: false,
      title: 'Register - Fluxor Trading'
    }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { 
      requiresAuth: false,
      title: 'Forgot Password - Fluxor Trading'
    }
  },
  
  // Main application routes
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { 
      requiresAuth: true,
      title: 'Dashboard - Fluxor Trading'
    }
  },
  {
    path: '/trading',
    name: 'Trading',
    component: Trading,
    meta: { 
      requiresAuth: true,
      title: 'Trading - Fluxor Trading'
    }
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: Portfolio,
    meta: { 
      requiresAuth: true,
      title: 'Portfolio - Fluxor Trading'
    }
  },
  {
    path: '/history',
    name: 'History',
    component: History,
    meta: { 
      requiresAuth: true,
      title: 'Trade History - Fluxor Trading'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { 
      requiresAuth: true,
      title: 'Profile - Fluxor Trading'
    }
  },
  {
    path: '/security',
    name: 'Security',
    component: Security,
    meta: { 
      requiresAuth: true,
      title: 'Security Settings - Fluxor Trading'
    }
  },
  {
    path: '/api-keys',
    name: 'ApiKeys',
    component: ApiKeys,
    meta: { 
      requiresAuth: true,
      title: 'API Keys - Fluxor Trading'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { 
      requiresAuth: true,
      title: 'Settings - Fluxor Trading'
    }
  },
  
  // Catch-all redirect
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title as string
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Check if we have a token but haven't fetched user yet
      if (authStore.token) {
        try {
          await authStore.fetchUser()
          next()
        } catch (error) {
          console.error('Authentication failed:', error)
          authStore.logout()
          next({ name: 'Login', query: { redirect: to.fullPath } })
        }
      } else {
        next({ name: 'Login', query: { redirect: to.fullPath } })
      }
    } else {
      next()
    }
  } else {
    // If user is authenticated and trying to access auth routes, redirect to dashboard
    if (authStore.isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
      next({ name: 'Dashboard' })
    } else {
      next()
    }
  }
})

export default router