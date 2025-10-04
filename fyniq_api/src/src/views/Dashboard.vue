<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Trading Dashboard</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Welcome back, {{ authStore.user?.full_name }}
        </p>
      </div>
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          @click="refreshData"
          :disabled="isLoading"
          class="btn-secondary"
        >
          <ArrowPathIcon class="h-4 w-4 mr-2" :class="{ 'animate-spin': isLoading }" />
          Refresh
        </button>
        <router-link to="/trade" class="btn-primary">
          <PlusIcon class="h-4 w-4 mr-2" />
          New Trade
        </router-link>
      </div>
    </div>

    <!-- Account Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Portfolio Value -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="p-3 bg-primary-100 rounded-lg">
              <CurrencyDollarIcon class="h-6 w-6 text-primary-600" />
            </div>
          </div>
          <div class="ml-4 flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              Portfolio Value
            </p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {{ formatCurrency(portfolioStats.totalValue) }}
            </p>
            <p class="text-sm" :class="portfolioStats.totalChange >= 0 ? 'text-green-600' : 'text-red-600'">
              <span class="flex items-center">
                <ArrowUpIcon v-if="portfolioStats.totalChange >= 0" class="h-3 w-3 mr-1" />
                <ArrowDownIcon v-else class="h-3 w-3 mr-1" />
                {{ formatCurrency(portfolioStats.totalChange) }} ({{ formatPercentage(portfolioStats.totalChangePercent) }})
              </span>
            </p>
          </div>
        </div>
      </div>

      <!-- Available Cash -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="p-3 bg-green-100 rounded-lg">
              <BanknotesIcon class="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div class="ml-4 flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              Available Cash
            </p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {{ formatCurrency(portfolioStats.availableCash) }}
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Ready to trade
            </p>
          </div>
        </div>
      </div>

      <!-- Today's P&L -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="p-3" :class="portfolioStats.todayPnL >= 0 ? 'bg-green-100' : 'bg-red-100'">
              <TrendingUpIcon v-if="portfolioStats.todayPnL >= 0" class="h-6 w-6 text-green-600" />
              <TrendingDownIcon v-else class="h-6 w-6 text-red-600" />
            </div>
          </div>
          <div class="ml-4 flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              Today's P&L
            </p>
            <p class="text-2xl font-semibold" :class="portfolioStats.todayPnL >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ formatCurrency(portfolioStats.todayPnL) }}
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ formatPercentage(portfolioStats.todayPnLPercent) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Open Positions -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="p-3 bg-blue-100 rounded-lg">
              <ChartBarIcon class="h-6 w-6 text-blue-600" />
            </div>
          </div>
          <div class="ml-4 flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              Open Positions
            </p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {{ positions.length }}
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Active trades
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts and Market Data -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Portfolio Performance Chart -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Portfolio Performance</h3>
          <div class="flex space-x-1">
            <button
              v-for="period in chartPeriods"
              :key="period.value"
              @click="selectedPeriod = period.value"
              :class="[
                'px-3 py-1 text-xs font-medium rounded-md',
                selectedPeriod === period.value
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              {{ period.label }}
            </button>
          </div>
        </div>
        <div class="h-64">
          <PortfolioChart
            :data="chartData"
            :period="selectedPeriod"
            @loading="(loading) => chartLoading = loading"
          />
        </div>
      </div>

        <!-- Market Data -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Market Data</h3>
            <button
              @click="refreshMarketData"
              class="text-sm text-primary-600 hover:text-primary-500"
            >
              Refresh
            </button>
          </div>
          <div class="space-y-3">
            <!-- Show market data if available -->
            <div v-if="marketData" class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700">
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div v-for="(value, key) in marketData" :key="key" class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400 capitalize">{{ key.replace('_', ' ') }}:</span>
                  <span class="font-medium text-gray-900 dark:text-white">
                    {{ typeof value === 'number' ? formatCurrency(value) : value }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Show crypto positions as market items -->
            <div
              v-for="position in positions.slice(0, 4)"
              :key="position.symbol"
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center">
                    <span class="text-xs font-bold text-gray-600 dark:text-gray-300">
                      {{ position.symbol?.charAt(0) || 'C' }}
                    </span>
                  </div>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ position.symbol || 'Unknown' }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ position.name || 'Cryptocurrency' }}
                  </p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ formatCurrency(position.currentValue || 0) }}
                </p>
                <p class="text-xs" :class="(position.unrealizedPnLPercent || 0) >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ formatPercentage(position.unrealizedPnLPercent || 0) }}
                </p>
              </div>
            </div>
            
            <!-- Empty state -->
            <div v-if="!marketData && positions.length === 0" class="text-center py-8">
              <p class="text-gray-500 dark:text-gray-400">No market data available</p>
              <button
                @click="refreshMarketData"
                class="mt-2 text-sm text-primary-600 hover:text-primary-500"
              >
                Try loading data
              </button>
            </div>
          </div>
        </div>
    </div>

    <!-- Recent Activity and Positions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Trades -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Recent Trades</h3>
          <router-link
            to="/history"
            class="text-sm text-primary-600 hover:text-primary-500"
          >
            View all
          </router-link>
        </div>
        <div class="space-y-3">
          <div
            v-for="trade in recentTrades"
            :key="trade.id"
            class="flex items-center justify-between p-3 rounded-lg border border-gray-200 dark:border-gray-600"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div
                  class="px-2 py-1 rounded text-xs font-medium"
                  :class="trade.side === 'buy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                >
                  {{ trade.side.toUpperCase() }}
                </div>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ trade.symbol }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ trade.quantity }} shares @ {{ formatCurrency(trade.price) }}
                </p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                {{ formatCurrency(trade.total) }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatDate(trade.timestamp) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Positions -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Current Positions</h3>
          <router-link
            to="/positions"
            class="text-sm text-primary-600 hover:text-primary-500"
          >
            View all
          </router-link>
        </div>
        <div class="space-y-3">
          <div
            v-for="position in positions.slice(0, 5)"
            :key="position.symbol"
            class="flex items-center justify-between p-3 rounded-lg border border-gray-200 dark:border-gray-600"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center">
                  <span class="text-xs font-bold text-gray-600 dark:text-gray-300">
                    {{ position.symbol.charAt(0) }}
                  </span>
                </div>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ position.symbol }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">
                  {{ position.quantity }} shares
                </p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                {{ formatCurrency(position.currentValue) }}
              </p>
              <p class="text-xs" :class="position.unrealizedPnL >= 0 ? 'text-green-600' : 'text-red-600'">
                {{ position.unrealizedPnL >= 0 ? '+' : '' }}{{ formatCurrency(position.unrealizedPnL) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="card">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <router-link
          to="/trade"
          class="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-colors"
        >
          <PlusIcon class="h-6 w-6 text-primary-600 mr-3" />
          <span class="text-sm font-medium text-gray-900 dark:text-white">Place Order</span>
        </router-link>
        
        <router-link
          to="/positions"
          class="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-colors"
        >
          <ChartBarIcon class="h-6 w-6 text-primary-600 mr-3" />
          <span class="text-sm font-medium text-gray-900 dark:text-white">View Positions</span>
        </router-link>
        
        <router-link
          to="/history"
          class="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-colors"
        >
          <ClockIcon class="h-6 w-6 text-primary-600 mr-3" />
          <span class="text-sm font-medium text-gray-900 dark:text-white">Trade History</span>
        </router-link>
        
        <router-link
          to="/settings"
          class="flex items-center p-4 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-primary-300 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-colors"
        >
          <Cog6ToothIcon class="h-6 w-6 text-primary-600 mr-3" />
          <span class="text-sm font-medium text-gray-900 dark:text-white">Settings</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/services/api'
import PortfolioChart from '@/components/PortfolioChart.vue'
import { useNotifications } from '@/utils/notifications'
import {
  ArrowPathIcon,
  PlusIcon,
  CurrencyDollarIcon,
  BanknotesIcon,
  TrendingUpIcon,
  TrendingDownIcon,
  ChartBarIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  ClockIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'

// Stores and composables
const authStore = useAuthStore()
const { showNotification } = useNotifications()

// State
const isLoading = ref(false)
const chartLoading = ref(false)
const selectedPeriod = ref('1D')

const chartPeriods = [
  { label: '1D', value: '1D' },
  { label: '1W', value: '1W' },
  { label: '1M', value: '1M' },
  { label: '3M', value: '3M' },
  { label: '1Y', value: '1Y' }
]

// API Data State
const walletData = ref<any>(null)
const portfolioStats = reactive({
  totalValue: 0,
  availableCash: 0,
  todayPnL: 0,
  todayPnLPercent: 0,
  totalChange: 0,
  totalChangePercent: 0
})

const positions = ref<any[]>([])
const recentTrades = ref<any[]>([])
const marketData = ref<any>(null)
const tradingStats = ref<any>(null)
const chartData = ref([])

// Methods
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const formatPercentage = (percentage: number) => {
  return `${percentage >= 0 ? '+' : ''}${percentage.toFixed(2)}%`
}

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  }).format(date)
}

const refreshData = async () => {
  isLoading.value = true
  try {
    // Load wallet/portfolio data
    const walletResponse = await api.wallets.getWallet()
    walletData.value = walletResponse.data
    
    // Update portfolio stats from wallet data
    if (walletData.value) {
      portfolioStats.totalValue = parseFloat(walletData.value.balance || '0')
      portfolioStats.availableCash = parseFloat(walletData.value.balance || '0')
      // Calculate P&L if historical data is available
      portfolioStats.todayPnL = 0 // Will be calculated from trades
      portfolioStats.todayPnLPercent = 0
      portfolioStats.totalChange = 0
      portfolioStats.totalChangePercent = 0
    }
    
    // Load recent trades
    const tradesResponse = await api.trades.getTrades({ limit: 5, ordering: '-created_at' })
    recentTrades.value = tradesResponse.data.results || tradesResponse.data
    
    // Load trading statistics
    try {
      const statsResponse = await api.trades.getTradingStats()
      tradingStats.value = statsResponse.data
      
      // Update portfolio stats from trading stats
      if (tradingStats.value) {
        portfolioStats.todayPnL = tradingStats.value.today_pnl || 0
        portfolioStats.todayPnLPercent = tradingStats.value.today_pnl_percent || 0
        portfolioStats.totalChange = tradingStats.value.total_pnl || 0
        portfolioStats.totalChangePercent = tradingStats.value.total_pnl_percent || 0
      }
    } catch (error) {
      console.log('Trading stats not available:', error)
    }
    
    // Load crypto wallets as positions
    try {
      const walletsResponse = await api.wallets.getCryptoWallets()
      positions.value = (walletsResponse.data.results || walletsResponse.data).map((wallet: any) => ({
        symbol: wallet.currency?.symbol || wallet.currency,
        name: wallet.currency?.name || wallet.currency,
        quantity: parseFloat(wallet.balance || '0'),
        currentValue: parseFloat(wallet.balance_usd || '0'),
        unrealizedPnL: parseFloat(wallet.unrealized_pnl || '0'),
        unrealizedPnLPercent: parseFloat(wallet.unrealized_pnl_percent || '0')
      }))
    } catch (error) {
      console.log('Crypto wallets not available:', error)
      positions.value = []
    }
    
  } catch (error: any) {
    console.error('Error refreshing data:', error)
    showNotification({
      type: 'error',
      title: 'Data Load Error',
      message: error.response?.data?.detail || 'Failed to load dashboard data. Please try again.'
    })
  } finally {
    isLoading.value = false
  }
}

const refreshMarketData = async () => {
  try {
    // Load market data from trading engine
    const marketResponse = await api.trading.getMarketData()
    marketData.value = marketResponse.data
    
    // Load price feed for popular crypto pairs
    try {
      const priceFeedResponse = await api.trading.getPriceFeed()
      if (priceFeedResponse.data) {
        // Update market data with latest prices
        console.log('Price feed data:', priceFeedResponse.data)
      }
    } catch (error) {
      console.log('Price feed not available:', error)
    }
    
  } catch (error: any) {
    console.error('Error refreshing market data:', error)
    showNotification({
      type: 'error',
      title: 'Market Data Error',
      message: 'Failed to refresh market data. Please try again.'
    })
  }
}

// Auto-refresh data
let refreshInterval: NodeJS.Timeout | null = null

onMounted(async () => {
  await refreshData()
  
  // Set up auto-refresh every 30 seconds
  refreshInterval = setInterval(refreshData, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>