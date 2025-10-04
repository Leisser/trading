import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast, { POSITION } from 'vue-toastification'
import LoadingOverlay from 'vue-loading-overlay'

import App from './App.vue'
import router from './router'

// Styles
import './assets/styles/main.css'
import 'vue-toastification/dist/index.css'
import 'vue-loading-overlay/dist/css/index.css'

// Create Vue app
const app = createApp(App)

// Pinia store
app.use(createPinia())

// Router
app.use(router)

// Toast notifications
app.use(Toast, {
  position: POSITION.TOP_RIGHT,
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
})

// Loading overlay
app.use(LoadingOverlay)

// Global properties
app.config.globalProperties.$api_url = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
app.config.globalProperties.$ws_url = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'

// Mount app
app.mount('#app')