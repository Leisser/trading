<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Loading overlay -->
    <Loading 
      v-model:active="isLoading" 
      :can-cancel="false"
      :is-full-page="true"
      color="#3b82f6"
      loader="spinner"
      :opacity="0.8"
      :z-index="9999"
    />
    
    <!-- Authentication Layout -->
    <template v-if="isAuthRoute">
      <div class="min-h-screen flex">
        <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
          <div class="mx-auto w-full max-w-sm lg:w-96">
            <router-view />
          </div>
        </div>
        <div class="hidden lg:block relative w-0 flex-1">
          <div class="absolute inset-0 bg-gradient-to-br from-primary-600 to-primary-800">
            <div class="absolute inset-0 bg-black opacity-20"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-center text-white">
                <h1 class="text-4xl font-bold mb-4">Fluxor Trading</h1>
                <p class="text-xl opacity-90">Advanced Cryptocurrency Trading Platform</p>
                <div class="mt-8 grid grid-cols-2 gap-4 text-sm">
                  <div class="bg-white bg-opacity-10 p-4 rounded-lg backdrop-filter backdrop-blur-lg">
                    <div class="text-2xl font-bold">₿ 45,230</div>
                    <div class="opacity-80">Bitcoin</div>
                  </div>
                  <div class="bg-white bg-opacity-10 p-4 rounded-lg backdrop-filter backdrop-blur-lg">
                    <div class="text-2xl font-bold">Ξ 2,840</div>
                    <div class="opacity-80">Ethereum</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <!-- Main Application Layout -->
    <template v-else>
      <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
        <!-- Sidebar -->
        <Sidebar 
          v-if="authStore.isAuthenticated"
          :is-open="sidebarOpen"
          @toggle="toggleSidebar"
        />
        
        <!-- Main Content -->
        <div class="flex-1 flex flex-col overflow-hidden">
          <!-- Header -->
          <Header 
            v-if="authStore.isAuthenticated"
            @toggle-sidebar="toggleSidebar"
            @toggle-theme="toggleTheme"
          />
          
          <!-- Main Content Area -->
          <main class="flex-1 relative overflow-y-auto focus:outline-none">
            <div class="py-6">
              <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                <router-view v-slot="{ Component, route }">
                  <transition name="fade" mode="out-in">
                    <component 
                      :is="Component" 
                      :key="route.path"
                    />
                  </transition>
                </router-view>
              </div>
            </div>
          </main>
        </div>
      </div>
      
      <!-- Connection Status -->
      <ConnectionStatus />
      
      <!-- Notification Center -->
      <NotificationCenter />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWebSocketStore } from '@/stores/websocket'
import { useTheme } from '@/composables/useTheme'
import Loading from 'vue-loading-overlay'

// Components (these will be created)
import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'
import ConnectionStatus from '@/components/common/ConnectionStatus.vue'
import NotificationCenter from '@/components/common/NotificationCenter.vue'

// Stores
const authStore = useAuthStore()
const wsStore = useWebSocketStore()

// Theme
const { toggleTheme } = useTheme()

// Route
const route = useRoute()

// State
const isLoading = ref(false)
const sidebarOpen = ref(true)

// Computed
const isAuthRoute = computed(() => {
  return route.path.startsWith('/login') || 
         route.path.startsWith('/register') || 
         route.path.startsWith('/forgot-password')
})

// Methods
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// Lifecycle
onMounted(async () => {
  // Initialize theme
  const theme = localStorage.getItem('theme') || 'light'
  document.documentElement.classList.toggle('dark', theme === 'dark')
  
  // Check authentication
  if (authStore.token && !authStore.isAuthenticated) {
    isLoading.value = true
    try {
      await authStore.fetchUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
      authStore.logout()
    } finally {
      isLoading.value = false
    }
  }
  
  // Initialize WebSocket connection if authenticated
  if (authStore.isAuthenticated) {
    wsStore.connect()
  }
})
</script>

<style>
/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Sidebar animations */
.sidebar-enter-active, .sidebar-leave-active {
  transition: transform 0.3s ease;
}

.sidebar-enter-from, .sidebar-leave-to {
  transform: translateX(-100%);
}

/* Loading spinner customization */
.vld-overlay .vld-icon {
  color: var(--color-primary) !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: theme('colors.gray.100');
}

.dark ::-webkit-scrollbar-track {
  background: theme('colors.gray.800');
}

::-webkit-scrollbar-thumb {
  background: theme('colors.gray.400');
  border-radius: 4px;
}

.dark ::-webkit-scrollbar-thumb {
  background: theme('colors.gray.600');
}

::-webkit-scrollbar-thumb:hover {
  background: theme('colors.gray.500');
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: theme('colors.gray.500');
}
</style>