<template>
  <div class="space-y-6">
    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CurrencyDollarIcon class="h-8 w-8 text-success-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Portfolio Value</dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">
                    ${{ formatCurrency(stats.totalPortfolioValue) }}
                  </div>
                  <div class="ml-2 flex items-baseline text-sm font-semibold text-success-600">
                    <ArrowTrendingUpIcon class="h-3 w-3 mr-1" />
                    {{ stats.portfolioChange }}%
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ChartBarIcon class="h-8 w-8 text-primary-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Active Trades</dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">{{ stats.activeTrades }}</div>
                  <div class="ml-2 flex items-baseline text-sm font-semibold text-primary-600">
                    +{{ stats.newTradesToday }} today
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <UsersIcon class="h-8 w-8 text-warning-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Active Users</dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">{{ stats.activeUsers.toLocaleString() }}</div>
                  <div class="ml-2 flex items-baseline text-sm font-semibold text-warning-600">
                    {{ stats.userGrowth }}% growth
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ServerIcon class="h-8 w-8 text-danger-600" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">System Health</dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">{{ stats.systemHealth }}%</div>
                  <div class="ml-2">
                    <span class="badge-success">Healthy</span>
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Trading Volume Chart -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Trading Volume (24h)</h3>
        </div>
        <div class="card-body">
          <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div class="text-center">
              <ChartBarIcon class="h-12 w-12 text-gray-400 mx-auto mb-2" />
              <p class="text-sm text-gray-500">Chart will be implemented with Chart.js</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Cryptocurrencies -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Top Performing Cryptocurrencies</h3>
        </div>
        <div class="card-body">
          <div class="space-y-3">
            <div 
              v-for="crypto in topCryptocurrencies" 
              :key="crypto.symbol"
              class="flex items-center justify-between"
            >
              <div class="flex items-center">
                <div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center mr-3">
                  <span class="text-xs font-bold text-gray-600">{{ crypto.symbol }}</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ crypto.name }}</p>
                  <p class="text-xs text-gray-500">${{ crypto.price }}</p>
                </div>
              </div>
              <div class="text-right">
                <p :class="crypto.change >= 0 ? 'text-success-600' : 'text-danger-600'" class="text-sm font-medium">
                  {{ crypto.change >= 0 ? '+' : '' }}{{ crypto.change }}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Trades -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Recent Trades</h3>
        </div>
        <div class="card-body">
          <div class="space-y-3">
            <div v-for="trade in recentTrades" :key="trade.id" class="flex items-center justify-between py-2">
              <div>
                <p class="text-sm font-medium text-gray-900">{{ trade.pair }}</p>
                <p class="text-xs text-gray-500">{{ formatTime(trade.timestamp) }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900">${{ trade.amount }}</p>
                <p :class="trade.type === 'buy' ? 'text-success-600' : 'text-danger-600'" class="text-xs">
                  {{ trade.type.toUpperCase() }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Alerts -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">System Alerts</h3>
        </div>
        <div class="card-body">
          <div class="space-y-3">
            <div v-for="alert in systemAlerts" :key="alert.id" class="flex items-start">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon 
                  :class="alert.severity === 'high' ? 'text-danger-500' : alert.severity === 'medium' ? 'text-warning-500' : 'text-primary-500'"
                  class="h-5 w-5 mt-0.5"
                />
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900">{{ alert.title }}</p>
                <p class="text-xs text-gray-500">{{ alert.message }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ formatTime(alert.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Quick Actions</h3>
        </div>
        <div class="card-body">
          <div class="space-y-3">
            <router-link 
              to="/cryptocurrencies" 
              class="block p-3 rounded-md border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center">
                <CurrencyDollarIcon class="h-5 w-5 text-primary-600 mr-3" />
                <span class="text-sm font-medium text-gray-900">Manage Cryptocurrencies</span>
              </div>
            </router-link>
            
            <router-link 
              to="/trading" 
              class="block p-3 rounded-md border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center">
                <ChartBarIcon class="h-5 w-5 text-success-600 mr-3" />
                <span class="text-sm font-medium text-gray-900">Trading Dashboard</span>
              </div>
            </router-link>
            
            <router-link 
              to="/users" 
              class="block p-3 rounded-md border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center">
                <UsersIcon class="h-5 w-5 text-warning-600 mr-3" />
                <span class="text-sm font-medium text-gray-900">User Management</span>
              </div>
            </router-link>
            
            <router-link 
              to="/reports" 
              class="block p-3 rounded-md border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center">
                <DocumentTextIcon class="h-5 w-5 text-primary-600 mr-3" />
                <span class="text-sm font-medium text-gray-900">Generate Reports</span>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Trades Monitor -->
    <div class="mt-8">
      <ActiveTradesMonitor :refresh-interval="10000" :max-trades="5" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'
import {
  CurrencyDollarIcon,
  ChartBarIcon,
  UsersIcon,
  ServerIcon,
  ArrowTrendingUpIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'
import ActiveTradesMonitor from '@/components/ActiveTradesMonitor.vue'

// Sample data
const stats = ref({
  totalPortfolioValue: 2845672,
  portfolioChange: 12.5,
  activeTrades: 1247,
  newTradesToday: 89,
  activeUsers: 15673,
  userGrowth: 8.2,
  systemHealth: 99.2
})

const topCryptocurrencies = ref([
  { symbol: 'BTC', name: 'Bitcoin', price: '45,234.56', change: 5.2 },
  { symbol: 'ETH', name: 'Ethereum', price: '3,187.92', change: 3.8 },
  { symbol: 'ADA', name: 'Cardano', price: '0.89', change: -2.1 },
  { symbol: 'DOT', name: 'Polkadot', price: '23.45', change: 7.3 },
  { symbol: 'SOL', name: 'Solana', price: '112.78', change: -1.5 }
])

const recentTrades = ref([
  { id: 1, pair: 'BTC/USD', amount: '12,450', type: 'buy', timestamp: new Date(Date.now() - 300000) },
  { id: 2, pair: 'ETH/USD', amount: '8,920', type: 'sell', timestamp: new Date(Date.now() - 600000) },
  { id: 3, pair: 'ADA/USD', amount: '3,456', type: 'buy', timestamp: new Date(Date.now() - 900000) },
  { id: 4, pair: 'DOT/USD', amount: '5,678', type: 'sell', timestamp: new Date(Date.now() - 1200000) }
])

const systemAlerts = ref([
  { 
    id: 1, 
    title: 'High Trading Volume', 
    message: 'Bitcoin trading volume increased by 45% in the last hour',
    severity: 'medium',
    timestamp: new Date(Date.now() - 1800000)
  },
  { 
    id: 2, 
    title: 'System Update Available', 
    message: 'New system update available for improved performance',
    severity: 'low',
    timestamp: new Date(Date.now() - 3600000)
  },
  { 
    id: 3, 
    title: 'Price Alert', 
    message: 'Ethereum reached target price of $3,200',
    severity: 'high',
    timestamp: new Date(Date.now() - 7200000)
  }
])

// Helper functions
const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

const formatTime = (date: Date): string => {
  return formatDistanceToNow(date, { addSuffix: true })
}

// Lifecycle
onMounted(() => {
  // Load dashboard data
  console.log('Dashboard mounted - load real data from API here')
})
</script>