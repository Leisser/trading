<template>
  <div class="space-y-4">
    <!-- Header with Controls -->
    <div class="flex justify-between items-center">
      <div>
        <h3 class="text-lg font-medium text-gray-900 flex items-center">
          ⚡ Active Trades Monitor
          <span class="ml-2 badge-primary">{{ activeTrades.length }}</span>
        </h3>
        <p class="text-sm text-gray-600">Real-time monitoring of controlled trades</p>
      </div>
      <div class="flex space-x-2">
        <button @click="toggleAutoRefresh" :class="autoRefresh ? 'btn-success' : 'btn-secondary'" class="text-sm">
          {{ autoRefresh ? '⏸️ Pause' : '▶️ Auto-refresh' }}
        </button>
        <button @click="refreshTrades" :disabled="loading" class="btn-primary text-sm">
          🔄 Refresh
        </button>
      </div>
    </div>

    <!-- Filter Controls -->
    <div class="bg-white p-4 rounded-lg shadow-sm border">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Trading Pair</label>
          <select v-model="filters.pair" @change="applyFilters" class="input-field">
            <option value="">All Pairs</option>
            <option v-for="pair in availablePairs" :key="pair" :value="pair">{{ pair }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Outcome Control</label>
          <select v-model="filters.controlled" @change="applyFilters" class="input-field">
            <option value="">All Trades</option>
            <option value="true">Controlled Only</option>
            <option value="false">Natural Only</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select v-model="filters.status" @change="applyFilters" class="input-field">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="expiring">Expiring Soon</option>
            <option value="pending">Pending Close</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">User Type</label>
          <select v-model="filters.userType" @change="applyFilters" class="input-field">
            <option value="">All Users</option>
            <option value="new">New Users</option>
            <option value="vip">VIP Users</option>
            <option value="regular">Regular Users</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Active Trades Table -->
    <div class="card">
      <div class="overflow-x-auto">
        <table class="table">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-header">Trade ID</th>
              <th class="table-header">Time</th>
              <th class="table-header">User</th>
              <th class="table-header">Pair</th>
              <th class="table-header">Amount</th>
              <th class="table-header">Controlled Outcome</th>
              <th class="table-header">Current P&L</th>
              <th class="table-header">Time Remaining</th>
              <th class="table-header">Status</th>
              <th class="table-header">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="10" class="table-cell text-center py-8">
                <div class="loading-spinner mx-auto"></div>
                <p class="text-sm text-gray-500 mt-2">Loading active trades...</p>
              </td>
            </tr>
            <tr v-else-if="filteredTrades.length === 0">
              <td colspan="10" class="table-cell text-center py-8 text-gray-500">
                No active trades found
              </td>
            </tr>
            <tr v-else v-for="trade in filteredTrades" :key="trade.id" 
                class="hover:bg-gray-50" :class="getTradeRowClass(trade)">
              <td class="table-cell font-mono text-sm">{{ trade.id }}</td>
              <td class="table-cell">{{ formatTime(trade.startTime) }}</td>
              <td class="table-cell">
                <div class="flex items-center space-x-2">
                  <span class="font-medium">{{ trade.username }}</span>
                  <span v-if="trade.userType === 'vip'" class="badge-warning">VIP</span>
                  <span v-if="trade.userType === 'new'" class="badge-info">NEW</span>
                </div>
              </td>
              <td class="table-cell font-medium">{{ trade.pair }}</td>
              <td class="table-cell">${{ formatCurrency(trade.amount) }}</td>
              <td class="table-cell">
                <div v-if="trade.controlledOutcome" class="flex items-center space-x-2">
                  <span :class="trade.controlledOutcome.outcome === 'profit' ? 'text-success-600' : 'text-danger-600'">
                    {{ trade.controlledOutcome.outcome === 'profit' ? '+' : '-' }}{{ trade.controlledOutcome.percentage }}%
                  </span>
                  <span class="badge-primary">CTRL</span>
                </div>
                <span v-else class="text-gray-400 text-sm">Natural</span>
              </td>
              <td class="table-cell">
                <span :class="trade.currentPnL >= 0 ? 'text-success-600' : 'text-danger-600'" class="font-medium">
                  {{ trade.currentPnL >= 0 ? '+' : '' }}${{ formatCurrency(Math.abs(trade.currentPnL)) }}
                </span>
              </td>
              <td class="table-cell">
                <div class="text-sm">
                  <div :class="getTimeRemainingClass(trade.timeRemaining)">
                    {{ formatTimeRemaining(trade.timeRemaining) }}
                  </div>
                  <div class="text-xs text-gray-400">
                    {{ formatDuration(trade.duration, trade.durationUnit) }} total
                  </div>
                </div>
              </td>
              <td class="table-cell">
                <span :class="getStatusClass(trade.status)">
                  {{ trade.status }}
                </span>
              </td>
              <td class="table-cell">
                <div class="flex space-x-1">
                  <button v-if="trade.controlledOutcome" 
                          @click="modifyOutcome(trade)"
                          class="text-primary-600 hover:text-primary-800 text-xs">
                    ✏️ Modify
                  </button>
                  <button @click="closeTrade(trade.id)"
                          class="text-warning-600 hover:text-warning-800 text-xs">
                    🏁 Close
                  </button>
                  <button @click="viewDetails(trade)"
                          class="text-gray-600 hover:text-gray-800 text-xs">
                    👁️ View
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Trade Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Total Active</p>
            <p class="text-2xl font-bold text-gray-900">{{ tradeStats.total }}</p>
          </div>
          <div class="text-primary-500">⚡</div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Controlled</p>
            <p class="text-2xl font-bold text-success-600">{{ tradeStats.controlled }}</p>
          </div>
          <div class="text-success-500">🎯</div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Avg. P&L</p>
            <p class="text-2xl font-bold" :class="tradeStats.avgPnL >= 0 ? 'text-success-600' : 'text-danger-600'">
              {{ tradeStats.avgPnL >= 0 ? '+' : '' }}${{ formatCurrency(Math.abs(tradeStats.avgPnL)) }}
            </p>
          </div>
          <div class="text-warning-500">📊</div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Success Rate</p>
            <p class="text-2xl font-bold text-primary-600">{{ tradeStats.successRate }}%</p>
          </div>
          <div class="text-primary-500">🎯</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'

// Props
interface Props {
  refreshInterval?: number
  maxTrades?: number
}

const props = withDefaults(defineProps<Props>(), {
  refreshInterval: 5000,
  maxTrades: 100
})

// State
const loading = ref(false)
const autoRefresh = ref(true)
let refreshTimer: number | null = null

const filters = reactive({
  pair: '',
  controlled: '',
  status: '',
  userType: ''
})

// Sample data
const activeTrades = ref([
  {
    id: 'T001',
    startTime: new Date(Date.now() - 45000),
    username: 'alice_trader',
    userType: 'vip',
    pair: 'BTC/USD',
    amount: 500.00,
    controlledOutcome: {
      outcome: 'profit',
      percentage: 85,
      priority: 'high'
    },
    currentPnL: 425.00,
    timeRemaining: 75000, // milliseconds
    duration: 2,
    durationUnit: 'minutes',
    status: 'active'
  },
  {
    id: 'T002',
    startTime: new Date(Date.now() - 25000),
    username: 'bob_crypto',
    userType: 'new',
    pair: 'ETH/USD',
    amount: 300.00,
    controlledOutcome: {
      outcome: 'loss',
      percentage: 40,
      priority: 'medium'
    },
    currentPnL: -120.00,
    timeRemaining: 20000,
    duration: 45,
    durationUnit: 'seconds',
    status: 'expiring'
  },
  {
    id: 'T003',
    startTime: new Date(Date.now() - 120000),
    username: 'charlie_btc',
    userType: 'regular',
    pair: 'ADA/USD',
    amount: 200.00,
    controlledOutcome: null,
    currentPnL: 15.50,
    timeRemaining: 2880000,
    duration: 1,
    durationUnit: 'hours',
    status: 'active'
  }
])

const availablePairs = ['BTC/USD', 'ETH/USD', 'ADA/USD', 'DOT/USD', 'SOL/USD']

// Computed
const filteredTrades = computed(() => {
  let filtered = [...activeTrades.value]

  if (filters.pair) {
    filtered = filtered.filter(trade => trade.pair === filters.pair)
  }

  if (filters.controlled) {
    const isControlled = filters.controlled === 'true'
    filtered = filtered.filter(trade => !!trade.controlledOutcome === isControlled)
  }

  if (filters.status) {
    filtered = filtered.filter(trade => trade.status === filters.status)
  }

  if (filters.userType) {
    filtered = filtered.filter(trade => trade.userType === filters.userType)
  }

  return filtered.slice(0, props.maxTrades)
})

const tradeStats = computed(() => {
  const trades = filteredTrades.value
  return {
    total: trades.length,
    controlled: trades.filter(t => t.controlledOutcome).length,
    avgPnL: trades.reduce((sum, t) => sum + t.currentPnL, 0) / (trades.length || 1),
    successRate: Math.round((trades.filter(t => t.currentPnL > 0).length / (trades.length || 1)) * 100)
  }
})

// Methods
const formatCurrency = (amount: number): string => {
  return amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString()
}

const formatTimeRemaining = (milliseconds: number): string => {
  const seconds = Math.floor(milliseconds / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  
  if (hours > 0) return `${hours}h ${minutes % 60}m`
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`
  return `${seconds}s`
}

const formatDuration = (duration: number, unit: string): string => {
  return `${duration} ${unit}`
}

const getTimeRemainingClass = (milliseconds: number): string => {
  const minutes = milliseconds / (1000 * 60)
  if (minutes <= 1) return 'text-danger-600 font-medium'
  if (minutes <= 5) return 'text-warning-600'
  return 'text-gray-900'
}

const getStatusClass = (status: string): string => {
  const classes = {
    active: 'badge-success',
    expiring: 'badge-warning',
    pending: 'badge-info'
  }
  return classes[status as keyof typeof classes] || 'badge-secondary'
}

const getTradeRowClass = (trade: any): string => {
  if (trade.status === 'expiring') return 'bg-warning-50 border-l-4 border-warning-400'
  if (trade.controlledOutcome && trade.controlledOutcome.priority === 'high') return 'bg-primary-50 border-l-4 border-primary-400'
  return ''
}

const applyFilters = () => {
  // Filters are reactive, so the computed property will update automatically
}

const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  if (autoRefresh.value) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

const refreshTrades = async () => {
  loading.value = true
  try {
    // TODO: API call to get active trades
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Simulate real-time updates
    activeTrades.value.forEach(trade => {
      // Update time remaining
      trade.timeRemaining = Math.max(0, trade.timeRemaining - 5000)
      
      // Update current P&L with some randomness
      const volatility = Math.random() * 0.1 - 0.05 // -5% to +5%
      trade.currentPnL += trade.amount * volatility
      
      // Update status based on time remaining
      if (trade.timeRemaining <= 60000) { // 1 minute
        trade.status = 'expiring'
      } else if (trade.timeRemaining <= 0) {
        trade.status = 'pending'
      }
    })
  } finally {
    loading.value = false
  }
}

const startAutoRefresh = () => {
  if (refreshTimer) return
  refreshTimer = setInterval(() => {
    if (!loading.value) {
      refreshTrades()
    }
  }, props.refreshInterval)
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

const modifyOutcome = (trade: any) => {
  console.log('Modify outcome for trade:', trade.id)
  // TODO: Open modify outcome modal
}

const closeTrade = (tradeId: string) => {
  if (confirm(`Are you sure you want to manually close trade ${tradeId}?`)) {
    // TODO: API call to close trade
    const index = activeTrades.value.findIndex(t => t.id === tradeId)
    if (index > -1) {
      activeTrades.value.splice(index, 1)
    }
  }
}

const viewDetails = (trade: any) => {
  console.log('View details for trade:', trade.id)
  // TODO: Open trade details modal
}

// Lifecycle
onMounted(() => {
  refreshTrades()
  if (autoRefresh.value) {
    startAutoRefresh()
  }
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>