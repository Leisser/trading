<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Positions</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Current holdings and performance
        </p>
      </div>
      <div class="mt-4 sm:mt-0 flex items-center space-x-3">
        <button
          @click="refreshPositions"
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

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
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
              Total Value
            </p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">
              {{ formatCurrency(portfolioSummary.totalValue) }}
            </p>
            <p class="text-sm" :class="portfolioSummary.totalPnL >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ portfolioSummary.totalPnL >= 0 ? '+' : '' }}{{ formatCurrency(portfolioSummary.totalPnL) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Total P&L -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="p-3" :class="portfolioSummary.totalPnLPercent >= 0 ? 'bg-green-100' : 'bg-red-100'">
              <TrendingUpIcon v-if="portfolioSummary.totalPnLPercent >= 0" class="h-6 w-6 text-green-600" />
              <TrendingDownIcon v-else class="h-6 w-6 text-red-600" />
            </div>
          </div>
          <div class="ml-4 flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              Total Return
            </p>
            <p class="text-2xl font-semibold" :class="portfolioSummary.totalPnLPercent >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ formatPercentage(portfolioSummary.totalPnLPercent) }}
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              All time
            </p>
          </div>
        </div>
      </div>

      <!-- Day P&L -->
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="p-3" :class="portfolioSummary.dayPnL >= 0 ? 'bg-green-100' : 'bg-red-100'">
              <ArrowUpIcon v-if="portfolioSummary.dayPnL >= 0" class="h-6 w-6 text-green-600" />
              <ArrowDownIcon v-else class="h-6 w-6 text-red-600" />
            </div>
          </div>
          <div class="ml-4 flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
              Day P&L
            </p>
            <p class="text-2xl font-semibold" :class="portfolioSummary.dayPnL >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ formatCurrency(portfolioSummary.dayPnL) }}
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ formatPercentage(portfolioSummary.dayPnLPercent) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-4">
        <div class="relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search positions..."
            class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        
        <select
          v-model="sortBy"
          class="form-select min-w-[120px]"
        >
          <option value="symbol">Symbol</option>
          <option value="value">Value</option>
          <option value="pnl">P&L</option>
          <option value="pnlPercent">P&L %</option>
          <option value="quantity">Quantity</option>
        </select>
        
        <button
          @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
          class="p-2 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          <ArrowUpIcon v-if="sortOrder === 'asc'" class="h-4 w-4 text-gray-600 dark:text-gray-400" />
          <ArrowDownIcon v-else class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
      </div>
      
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-500 dark:text-gray-400">Show:</span>
        <button
          v-for="filter in positionFilters"
          :key="filter.value"
          @click="activeFilter = filter.value"
          :class="[
            'px-3 py-1 text-sm rounded-md transition-colors',
            activeFilter === filter.value
              ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
              : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
          ]"
        >
          {{ filter.label }}
        </button>
      </div>
    </div>

    <!-- Positions Table -->
    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-600">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Symbol
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Quantity
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Avg. Cost
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Current Price
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Market Value
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                P&L
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Day P&L
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-600">
            <tr
              v-for="position in filteredAndSortedPositions"
              :key="position.symbol"
              class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 w-10 h-10">
                    <div class="w-10 h-10 bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center">
                      <span class="text-sm font-bold text-gray-600 dark:text-gray-300">
                        {{ position.symbol.charAt(0) }}
                      </span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">
                      {{ position.symbol }}
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      {{ position.name }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ position.quantity.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ formatCurrency(position.avgCost) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">
                  {{ formatCurrency(position.currentPrice) }}
                </div>
                <div class="text-sm" :class="position.priceChange >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ position.priceChange >= 0 ? '+' : '' }}{{ formatCurrency(position.priceChange) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ formatCurrency(position.marketValue) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium" :class="position.unrealizedPnL >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ position.unrealizedPnL >= 0 ? '+' : '' }}{{ formatCurrency(position.unrealizedPnL) }}
                </div>
                <div class="text-sm" :class="position.unrealizedPnLPercent >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ formatPercentage(position.unrealizedPnLPercent) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium" :class="position.dayPnL >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ position.dayPnL >= 0 ? '+' : '' }}{{ formatCurrency(position.dayPnL) }}
                </div>
                <div class="text-sm" :class="position.dayPnLPercent >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ formatPercentage(position.dayPnLPercent) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button
                  @click="showTradeModal(position, 'buy')"
                  class="text-green-600 hover:text-green-900 dark:hover:text-green-400"
                >
                  Buy
                </button>
                <button
                  @click="showTradeModal(position, 'sell')"
                  class="text-red-600 hover:text-red-900 dark:hover:text-red-400"
                >
                  Sell
                </button>
                <button
                  @click="viewDetails(position)"
                  class="text-primary-600 hover:text-primary-900 dark:hover:text-primary-400"
                >
                  Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- Empty State -->
        <div v-if="filteredAndSortedPositions.length === 0" class="text-center py-12">
          <ChartBarIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No positions found</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {{ searchQuery ? 'Try adjusting your search terms.' : 'Start trading to see your positions here.' }}
          </p>
          <div class="mt-6">
            <router-link to="/trade" class="btn-primary">
              <PlusIcon class="h-4 w-4 mr-2" />
              Start Trading
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Trade Modal -->
    <div
      v-if="showQuickTrade"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click="closeTradeModal"
    >
      <div
        class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6"
        @click.stop
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            {{ quickTradeAction === 'buy' ? 'Buy' : 'Sell' }} {{ selectedPosition?.symbol }}
          </h3>
          <button
            @click="closeTradeModal"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <form @submit.prevent="executeQuickTrade" class="space-y-4">
          <div>
            <label class="form-label">Quantity</label>
            <input
              v-model.number="quickTradeQuantity"
              type="number"
              :max="quickTradeAction === 'sell' ? selectedPosition?.quantity : undefined"
              min="1"
              class="form-input"
              placeholder="Number of shares"
              required
            />
            <p v-if="quickTradeAction === 'sell'" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Available: {{ selectedPosition?.quantity }} shares
            </p>
          </div>
          
          <div>
            <label class="form-label">Order Type</label>
            <select v-model="quickTradeOrderType" class="form-select">
              <option value="market">Market Order</option>
              <option value="limit">Limit Order</option>
            </select>
          </div>
          
          <div v-if="quickTradeOrderType === 'limit'">
            <label class="form-label">Limit Price</label>
            <input
              v-model.number="quickTradePrice"
              type="number"
              step="0.01"
              class="form-input"
              :placeholder="selectedPosition ? formatCurrency(selectedPosition.currentPrice) : '0.00'"
              required
            />
          </div>
          
          <div class="border-t border-gray-200 dark:border-gray-600 pt-4">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">Estimated Total:</span>
              <span class="font-medium text-gray-900 dark:text-white">
                {{ formatCurrency(estimatedTradeTotal) }}
              </span>
            </div>
          </div>
          
          <div class="flex space-x-3 pt-4">
            <button
              type="button"
              @click="closeTradeModal"
              class="flex-1 btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="!quickTradeQuantity || isTrading"
              :class="[
                'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
                quickTradeAction === 'buy'
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-red-600 hover:bg-red-700 text-white',
                (!quickTradeQuantity || isTrading) && 'opacity-50 cursor-not-allowed'
              ]"
            >
              {{ isTrading ? 'Placing...' : (quickTradeAction === 'buy' ? 'Buy' : 'Sell') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotifications } from '@/utils/notifications'
import {
  ArrowPathIcon,
  PlusIcon,
  CurrencyDollarIcon,
  TrendingUpIcon,
  TrendingDownIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  MagnifyingGlassIcon,
  ChartBarIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// Composables
const router = useRouter()
const { showNotification } = useNotifications()

// State
const isLoading = ref(false)
const isTrading = ref(false)
const searchQuery = ref('')
const sortBy = ref('symbol')
const sortOrder = ref<'asc' | 'desc'>('asc')
const activeFilter = ref('all')
const showQuickTrade = ref(false)
const selectedPosition = ref<any>(null)
const quickTradeAction = ref<'buy' | 'sell'>('buy')
const quickTradeQuantity = ref<number | null>(null)
const quickTradeOrderType = ref('market')
const quickTradePrice = ref<number | null>(null)

const positionFilters = [
  { label: 'All', value: 'all' },
  { label: 'Profitable', value: 'profitable' },
  { label: 'Losing', value: 'losing' },
  { label: 'Large', value: 'large' }
]

// Mock data
const positions = ref([
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    quantity: 100,
    avgCost: 151.20,
    currentPrice: 154.30,
    priceChange: 2.45,
    marketValue: 15430,
    unrealizedPnL: 310,
    unrealizedPnLPercent: 2.05,
    dayPnL: 245,
    dayPnLPercent: 1.61,
    costBasis: 15120
  },
  {
    symbol: 'GOOGL',
    name: 'Alphabet Inc.',
    quantity: 50,
    avgCost: 135.40,
    currentPrice: 132.50,
    priceChange: -1.25,
    marketValue: 6625,
    unrealizedPnL: -145,
    unrealizedPnLPercent: -2.14,
    dayPnL: -62.50,
    dayPnLPercent: -0.93,
    costBasis: 6770
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corporation',
    quantity: 75,
    avgCost: 338.80,
    currentPrice: 342.15,
    priceChange: 4.82,
    marketValue: 25661.25,
    unrealizedPnL: 251.25,
    unrealizedPnLPercent: 0.99,
    dayPnL: 361.50,
    dayPnLPercent: 1.43,
    costBasis: 25410
  },
  {
    symbol: 'TSLA',
    name: 'Tesla Inc.',
    quantity: 25,
    avgCost: 248.90,
    currentPrice: 245.67,
    priceChange: -5.23,
    marketValue: 6141.75,
    unrealizedPnL: -80.75,
    unrealizedPnLPercent: -1.30,
    dayPnL: -130.75,
    dayPnLPercent: -2.09,
    costBasis: 6222.50
  }
])

const portfolioSummary = computed(() => {
  const totalValue = positions.value.reduce((sum, pos) => sum + pos.marketValue, 0)
  const totalCostBasis = positions.value.reduce((sum, pos) => sum + pos.costBasis, 0)
  const totalPnL = totalValue - totalCostBasis
  const totalPnLPercent = totalCostBasis > 0 ? (totalPnL / totalCostBasis) * 100 : 0
  const dayPnL = positions.value.reduce((sum, pos) => sum + pos.dayPnL, 0)
  const dayPnLPercent = positions.value.reduce((sum, pos) => sum + pos.dayPnLPercent, 0) / positions.value.length

  return {
    totalValue,
    totalPnL,
    totalPnLPercent,
    dayPnL,
    dayPnLPercent
  }
})

const filteredAndSortedPositions = computed(() => {
  let filtered = positions.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(pos => 
      pos.symbol.toLowerCase().includes(query) || 
      pos.name.toLowerCase().includes(query)
    )
  }

  // Apply category filter
  switch (activeFilter.value) {
    case 'profitable':
      filtered = filtered.filter(pos => pos.unrealizedPnL > 0)
      break
    case 'losing':
      filtered = filtered.filter(pos => pos.unrealizedPnL < 0)
      break
    case 'large':
      filtered = filtered.filter(pos => pos.marketValue > 10000)
      break
  }

  // Apply sorting
  filtered.sort((a, b) => {
    let aVal: any, bVal: any
    
    switch (sortBy.value) {
      case 'symbol':
        aVal = a.symbol
        bVal = b.symbol
        break
      case 'value':
        aVal = a.marketValue
        bVal = b.marketValue
        break
      case 'pnl':
        aVal = a.unrealizedPnL
        bVal = b.unrealizedPnL
        break
      case 'pnlPercent':
        aVal = a.unrealizedPnLPercent
        bVal = b.unrealizedPnLPercent
        break
      case 'quantity':
        aVal = a.quantity
        bVal = b.quantity
        break
      default:
        aVal = a.symbol
        bVal = b.symbol
    }

    if (typeof aVal === 'string') {
      return sortOrder.value === 'asc' 
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal)
    } else {
      return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal
    }
  })

  return filtered
})

const estimatedTradeTotal = computed(() => {
  if (!quickTradeQuantity.value || !selectedPosition.value) return 0
  
  const price = quickTradeOrderType.value === 'market' 
    ? selectedPosition.value.currentPrice
    : quickTradePrice.value || selectedPosition.value.currentPrice
    
  return quickTradeQuantity.value * price
})

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

const refreshPositions = async () => {
  isLoading.value = true
  try {
    // Mock API call - replace with real implementation
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update mock prices (simulate real-time updates)
    positions.value.forEach(pos => {
      const change = (Math.random() - 0.5) * 5
      pos.currentPrice += change
      pos.priceChange += change
      pos.marketValue = pos.quantity * pos.currentPrice
      pos.unrealizedPnL = pos.marketValue - pos.costBasis
      pos.unrealizedPnLPercent = (pos.unrealizedPnL / pos.costBasis) * 100
      pos.dayPnL += change * pos.quantity
      pos.dayPnLPercent = (pos.dayPnL / pos.costBasis) * 100
    })
    
    showNotification({
      type: 'success',
      title: 'Positions Updated',
      message: 'Position data has been refreshed successfully.'
    })
  } catch (error) {
    console.error('Error refreshing positions:', error)
    showNotification({
      type: 'error',
      title: 'Refresh Failed',
      message: 'Failed to refresh position data. Please try again.'
    })
  } finally {
    isLoading.value = false
  }
}

const showTradeModal = (position: any, action: 'buy' | 'sell') => {
  selectedPosition.value = position
  quickTradeAction.value = action
  quickTradeQuantity.value = null
  quickTradeOrderType.value = 'market'
  quickTradePrice.value = null
  showQuickTrade.value = true
}

const closeTradeModal = () => {
  showQuickTrade.value = false
  selectedPosition.value = null
  quickTradeQuantity.value = null
  quickTradePrice.value = null
}

const executeQuickTrade = async () => {
  if (!selectedPosition.value || !quickTradeQuantity.value) return

  isTrading.value = true

  try {
    // Mock API call - replace with real implementation
    await new Promise(resolve => setTimeout(resolve, 2000))

    const action = quickTradeAction.value.toUpperCase()
    const symbol = selectedPosition.value.symbol
    const quantity = quickTradeQuantity.value

    showNotification({
      type: 'success',
      title: 'Order Placed',
      message: `${action} order for ${quantity} shares of ${symbol} has been placed successfully.`
    })

    closeTradeModal()
    await refreshPositions()

  } catch (error) {
    console.error('Error executing trade:', error)
    showNotification({
      type: 'error',
      title: 'Order Failed',
      message: 'Failed to place order. Please try again.'
    })
  } finally {
    isTrading.value = false
  }
}

const viewDetails = (position: any) => {
  // Navigate to detailed position view or show modal
  router.push(`/positions/${position.symbol}`)
}

// Lifecycle
onMounted(() => {
  refreshPositions()
})
</script>