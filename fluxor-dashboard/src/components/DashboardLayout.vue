<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <div class="flex">
      <!-- Mobile sidebar overlay -->
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 z-40 lg:hidden"
        @click="sidebarOpen = false"
      >
        <div class="fixed inset-0 bg-gray-600 bg-opacity-75"></div>
      </div>

      <!-- Sidebar component -->
      <div
        :class="[
          'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        ]"
      >
        <div class="flex items-center justify-center h-16 bg-primary-600">
          <h1 class="text-xl font-bold text-white">Fluxor Dashboard</h1>
        </div>

        <nav class="mt-8">
          <div class="px-4">
            <ul class="space-y-2">
              <li v-for="item in navigation" :key="item.name">
                <router-link
                  :to="item.href"
                  :class="[
                    $route.path === item.href
                      ? 'sidebar-link-active'
                      : 'sidebar-link-inactive'
                  ]"
                >
                  <component :is="item.icon" class="h-5 w-5 mr-3" />
                  {{ item.name }}
                  <span v-if="item.badge" :class="item.badge.class" class="ml-auto">
                    {{ item.badge.text }}
                  </span>
                </router-link>
              </li>
            </ul>
          </div>
        </nav>

        <!-- User Profile Section -->
        <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 rounded-full bg-primary-200 flex items-center justify-center">
                <UserIcon class="h-5 w-5 text-primary-600" />
              </div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-700">{{ user.name }}</p>
              <p class="text-xs text-gray-500">{{ user.role }}</p>
            </div>
            <button
              @click="logout"
              class="ml-auto text-gray-400 hover:text-gray-600"
              title="Logout"
            >
              <ArrowRightOnRectangleIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <header class="bg-white shadow-sm border-b border-gray-200">
        <div class="flex items-center justify-between h-16 px-4">
          <div class="flex items-center">
            <button
              @click="sidebarOpen = !sidebarOpen"
              class="text-gray-500 hover:text-gray-700 lg:hidden"
            >
              <Bars3Icon class="h-6 w-6" />
            </button>
            <div class="ml-4 lg:ml-0">
              <h2 class="text-lg font-semibold text-gray-900">{{ pageTitle }}</h2>
              <p v-if="pageSubtitle" class="text-sm text-gray-500">{{ pageSubtitle }}</p>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <!-- Search -->
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search..."
                class="pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                v-model="searchQuery"
              />
            </div>

            <!-- Notifications -->
            <button class="relative text-gray-400 hover:text-gray-600">
              <BellIcon class="h-6 w-6" />
              <span v-if="notifications.length > 0" class="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                {{ notifications.length }}
              </span>
            </button>

            <!-- Settings -->
            <router-link
              to="/settings"
              class="text-gray-400 hover:text-gray-600"
            >
              <CogIcon class="h-6 w-6" />
            </router-link>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto">
        <div class="p-6">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Bars3Icon,
  BellIcon,
  CogIcon,
  MagnifyingGlassIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  HomeIcon,
  CurrencyDollarIcon,
  UsersIcon,
  ChartBarIcon,
  DocumentTextIcon,
  ShieldCheckIcon,
  ServerIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

// State
const sidebarOpen = ref(false)
const searchQuery = ref('')
const notifications = ref([
  { id: 1, message: 'New cryptocurrency added', type: 'info' },
  { id: 2, message: 'Trading volume alert', type: 'warning' }
])

// Navigation items
const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Cryptocurrencies', href: '/cryptocurrencies', icon: CurrencyDollarIcon, badge: { text: 'New', class: 'badge-success' } },
  { name: 'Trading', href: '/trading', icon: ChartBarIcon },
  { name: 'Users', href: '/users', icon: UsersIcon },
  { name: 'Reports', href: '/reports', icon: DocumentTextIcon },
  { name: 'Security', href: '/security', icon: ShieldCheckIcon },
  { name: 'System', href: '/system', icon: ServerIcon }
]

// User data
const user = ref({
  name: 'Admin User',
  role: 'System Administrator',
  avatar: null
})

// Computed properties
const pageTitle = computed(() => {
  const currentRoute = navigation.find(item => item.href === route.path)
  return currentRoute?.name || 'Dashboard'
})

const pageSubtitle = computed(() => {
  // Add dynamic subtitle based on route
  switch (route.path) {
    case '/':
      return 'Overview of your trading platform'
    case '/cryptocurrencies':
      return 'Manage cryptocurrencies and trading pairs'
    case '/users':
      return 'User management and permissions'
    case '/trading':
      return 'Trading activities and analytics'
    case '/reports':
      return 'Financial and performance reports'
    case '/security':
      return 'Security settings and logs'
    case '/system':
      return 'System configuration and maintenance'
    default:
      return null
  }
})

// Methods
const logout = () => {
  // Handle logout logic
  router.push('/login')
}
</script>