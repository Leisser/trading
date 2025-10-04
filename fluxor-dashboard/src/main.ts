import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

// Import views
import SimpleDashboard from './views/SimpleDashboard.vue'

// Router configuration
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: SimpleDashboard
  },
  {
    path: '/dashboard',
    name: 'DashboardHome',
    component: SimpleDashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create Vue app
const app = createApp(App)
app.use(router)
app.mount('#app')
