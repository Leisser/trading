import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

// Import views
import FirebaseLogin from './views/FirebaseLogin.vue'
import DashboardLogin from './views/DashboardLogin.vue'
import HomePage from './views/HomePage.vue'

// Router configuration
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: FirebaseLogin
  },
  {
    path: '/register',
    name: 'Register',
    component: FirebaseLogin,
    query: { mode: 'register' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardLogin
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
