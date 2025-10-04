<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Trade</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Place buy and sell orders
        </p>
      </div>
      <div class="mt-4 sm:mt-0 flex items-center space-x-3">
        <div class="flex items-center space-x-2 text-sm">
          <div class="flex items-center">
            <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
            <span class="text-gray-600 dark:text-gray-400">Market Open</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Order Form -->
      <div class="lg:col-span-1">
        <div class="card sticky top-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-medium text-gray-900 dark:text-white">Place Order</h2>
            <div class="flex rounded-lg bg-gray-100 dark:bg-gray-700 p-1">
              <button
                @click="orderSide = 'buy'"
                :class="[
                  'px-3 py-1 text-sm font-medium rounded-md transition-colors',
                  orderSide === 'buy' 
                    ? 'bg-green-600 text-white' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                ]"
              >
                Buy
              </button>
              <button
                @click="orderSide = 'sell'"
                :class="[
                  'px-3 py-1 text-sm font-medium rounded-md transition-colors',
                  orderSide === 'sell' 
                    ? 'bg-red-600 text-white' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                ]"
              >
                Sell
              </button>
            </div>
          </div>

          <form @submit.prevent="handlePlaceOrder" class="space-y-4">
            <!-- Symbol Search -->
            <div>
              <label for="symbol" class="form-label">Symbol</label>
              <div class="relative">
                <input
                  id="symbol"
                  v-model="orderForm.symbol"
                  type="text"
                  placeholder="Search symbol..."
                  class="form-input pr-10"
                  @input="searchSymbols"
                  @focus="showSymbolDropdown = true"
                  @blur="hideSymbolDropdown"
                />
                <MagnifyingGlassIcon class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
                
                <!-- Symbol dropdown -->
                <div
                  v-if="showSymbolDropdown && symbolResults.length > 0"
                  class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-md shadow-lg max-h-60 overflow-y-auto"
                >
                  <div
                    v-for="symbol in symbolResults"
                    :key="symbol.symbol"
                    @mousedown="selectSymbol(symbol)"
                    class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
                  >
                    <div class="flex items-center justify-between">
                      <div>
                        <div class="font-medium text-gray-900 dark:text-white">{{ symbol.symbol }}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400">{{ symbol.name }}</div>
                      </div>
                      <div class="text-right">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">
                          {{ formatCurrency(symbol.price) }}
                        </div>
                        <div class="text-xs" :class="symbol.change >= 0 ? 'text-green-600' : 'text-red-600'">
                          {{ symbol.change >= 0 ? '+' : '' }}{{ symbol.changePercent.toFixed(2) }}%
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <p v-if="errors.symbol" class="mt-1 text-sm text-red-600">{{ errors.symbol }}</p>
            </div>

            <!-- Order Type -->
            <div>
              <label for="orderType" class="form-label">Order Type</label>
              <select
                id="orderType"
                v-model="orderForm.orderType"
                class="form-select"
              >
                <option value="market">Market</option>
                <option value="limit">Limit</option>
                <option value="stop">Stop</option>
                <option value="stop_limit">Stop Limit</option>
              </select>
            </div>

            <!-- Quantity -->
            <div>
              <label for="quantity" class="form-label">Quantity</label>
              <input
                id="quantity"
                v-model.number="orderForm.quantity"
                type="number"
                min="1"
                step="1"
                class="form-input"
                placeholder="Number of shares"
              />
              <p v-if="errors.quantity" class="mt-1 text-sm text-red-600">{{ errors.quantity }}</p>
            </div>

            <!-- Price (for limit/stop orders) -->
            <div v-if="orderForm.orderType !== 'market'">
              <label for="price" class="form-label">
                {{ orderForm.orderType === 'limit' ? 'Limit Price' : 'Stop Price' }}
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span class="text-gray-500 dark:text-gray-400 text-sm">$</span>
                </div>
                <input
                  id="price"
                  v-model.number="orderForm.price"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input pl-7"
                  placeholder="0.00"
                />
              </div>
              <p v-if="errors.price" class="mt-1 text-sm text-red-600">{{ errors.price }}</p>
            </div>

            <!-- Stop Limit Price -->
            <div v-if="orderForm.orderType === 'stop_limit'">
              <label for="limitPrice" class="form-label">Limit Price</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span class="text-gray-500 dark:text-gray-400 text-sm">$</span>
                </div>
                <input
                  id="limitPrice"
                  v-model.number="orderForm.limitPrice"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input pl-7"
                  placeholder="0.00"
                />
              </div>
              <p v-if="errors.limitPrice" class="mt-1 text-sm text-red-600">{{ errors.limitPrice }}</p>
            </div>

            <!-- Time in Force -->
            <div>
              <label for="timeInForce" class="form-label">Time in Force</label>
              <select
                id="timeInForce"
                v-model="orderForm.timeInForce"
                class="form-select"
              >
                <option value="day">Day</option>
                <option value="gtc">Good Till Canceled</option>
                <option value="ioc">Immediate or Cancel</option>
                <option value="fok">Fill or Kill</option>
              </select>
            </div>

            <!-- Order Summary -->
            <div class="border-t border-gray-200 dark:border-gray-600 pt-4 space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Estimated Cost:</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ formatCurrency(estimatedCost) }}
                </span>
              </div>
              <div v-if="orderSide === 'buy'" class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Available Cash:</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ formatCurrency(availableCash) }}
                </span>
              </div>
              <div v-if="orderSide === 'sell' && selectedSymbol" class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Shares Owned:</span>
                <span class="font-medium text-gray-900 dark:text-white">
                  {{ getSharesOwned(selectedSymbol.symbol) }}
                </span>
              </div>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="!isFormValid || isSubmitting"
              :class="[
                'w-full py-3 px-4 rounded-md text-sm font-medium transition-colors',
                orderSide === 'buy'
                  ? 'bg-green-600 hover:bg-green-700 text-white'
                  : 'bg-red-600 hover:bg-red-700 text-white',
                (!isFormValid || isSubmitting) && 'opacity-50 cursor-not-allowed'
              ]"
            >
              <span v-if="isSubmitting" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Placing Order...
              </span>
              <span v-else>
                {{ orderSide === 'buy' ? 'Place Buy Order' : 'Place Sell Order' }}
              </span>
            </button>
          </form>
        </div>
      </div>

      <!-- Chart and Market Data -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Symbol Info -->
        <div v-if="selectedSymbol" class="card">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                {{ selectedSymbol.symbol }}
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ selectedSymbol.name }}
              </p>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ formatCurrency(selectedSymbol.price) }}
              </div>
              <div class="flex items-center" :class="selectedSymbol.change >= 0 ? 'text-green-600' : 'text-red-600'">
                <ArrowUpIcon v-if="selectedSymbol.change >= 0" class="h-4 w-4 mr-1" />
                <ArrowDownIcon v-else class="h-4 w-4 mr-1" />
                <span>{{ selectedSymbol.change >= 0 ? '+' : '' }}{{ formatCurrency(selectedSymbol.change) }}</span>
                <span class="ml-1">({{ selectedSymbol.changePercent.toFixed(2) }}%)</span>
              </div>
            </div>
          </div>
          
          <!-- Key Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <div class="text-gray-500 dark:text-gray-400">Open</div>
              <div class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(selectedSymbol.open) }}</div>
            </div>
            <div>
              <div class="text-gray-500 dark:text-gray-400">High</div>
              <div class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(selectedSymbol.high) }}</div>
            </div>
            <div>
              <div class="text-gray-500 dark:text-gray-400">Low</div>
              <div class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(selectedSymbol.low) }}</div>
            </div>
            <div>
              <div class="text-gray-500 dark:text-gray-400">Volume</div>
              <div class="font-medium text-gray-900 dark:text-white">{{ formatVolume(selectedSymbol.volume) }}</div>
            </div>
          </div>
        </div>

        <!-- Price Chart -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">
              {{ selectedSymbol?.symbol || 'Select Symbol' }} Chart
            </h3>
            <div class="flex space-x-1">
              <button
                v-for="period in chartPeriods"
                :key="period.value"
                @click="chartPeriod = period.value"
                :class="[
                  'px-3 py-1 text-xs font-medium rounded-md',
                  chartPeriod === period.value
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-500 hover:text-gray-700'
                ]"
              >
                {{ period.label }}
              </button>
            </div>
          </div>
          <div class="h-80">
            <TradingChart
              :symbol="selectedSymbol?.symbol"
              :period="chartPeriod"
              @loading="(loading) => chartLoading = loading"
            />
          </div>
        </div>

        <!-- Order Book & Recent Trades -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Order Book -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Order Book</h3>
            <div class="space-y-2">
              <div v-if="orderBook">
                <!-- Asks -->
                <div v-if="orderBook.asks" class="space-y-1">
                  <div class="text-xs font-medium text-red-600 uppercase tracking-wide">Ask</div>
                  <div
                    v-for="(ask, index) in orderBook.asks.slice(0, 5)"
                    :key="`ask-${index}`"
                    class="flex justify-between text-sm py-1"
                  >
                    <span class="text-red-600">{{ formatCurrency(ask.price || ask[0]) }}</span>
                    <span class="text-gray-600 dark:text-gray-400">{{ (ask.size || ask[1] || 0).toLocaleString() }}</span>
                  </div>
                </div>
                
                <!-- Spread -->
                <div class="border-t border-b border-gray-200 dark:border-gray-600 py-2 text-center">
                  <div class="text-xs text-gray-500 dark:text-gray-400">
                    {{ orderBook.spread ? `Spread: ${formatCurrency(orderBook.spread)}` : 'Order Book Data' }}
                  </div>
                </div>
                
                <!-- Bids -->
                <div v-if="orderBook.bids" class="space-y-1">
                  <div class="text-xs font-medium text-green-600 uppercase tracking-wide">Bid</div>
                  <div
                    v-for="(bid, index) in orderBook.bids.slice(0, 5)"
                    :key="`bid-${index}`"
                    class="flex justify-between text-sm py-1"
                  >
                    <span class="text-green-600">{{ formatCurrency(bid.price || bid[0]) }}</span>
                    <span class="text-gray-600 dark:text-gray-400">{{ (bid.size || bid[1] || 0).toLocaleString() }}</span>
                  </div>
                </div>
              </div>
              
              <!-- No data state -->
              <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
                <p>No order book data available</p>
                <p class="text-xs mt-1">Select a symbol to view order book</p>
              </div>
            </div>
          </div>

          <!-- Recent Trades -->
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent Trades</h3>
            <div class="space-y-2 max-h-64 overflow-y-auto">
              <div v-if="recentTrades.length > 0">
                <div
                  v-for="trade in recentTrades"
                  :key="trade.id || `${trade.price}-${trade.created_at}`"
                  class="flex justify-between items-center text-sm py-1"
                >
                  <span :class="trade.side === 'buy' ? 'text-green-600' : 'text-red-600'">
                    {{ formatCurrency(trade.price || 0) }}
                  </span>
                  <span class="text-gray-600 dark:text-gray-400">
                    {{ (trade.quantity || trade.size || 0).toLocaleString() }}
                  </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatTime(new Date(trade.created_at || trade.timestamp)) }}
                  </span>
                </div>
              </div>
              
              <!-- No data state -->
              <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
                <p>No recent trades</p>
                <p class="text-xs mt-1">Trade history will appear here</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useNotifications } from '@/utils/notifications'
import { api } from '@/services/api'
import TradingChart from '@/components/TradingChart.vue'
import {
  MagnifyingGlassIcon,
  ArrowUpIcon,
  ArrowDownIcon
} from '@heroicons/vue/24/outline'

// Composables
const router = useRouter()
const { showNotification } = useNotifications()

// State
const orderSide = ref<'buy' | 'sell'>('buy')
const showSymbolDropdown = ref(false)
const isSubmitting = ref(false)
const chartLoading = ref(false)
const chartPeriod = ref('1D')
const availableCash = ref(25430.50)

const chartPeriods = [
  { label: '1D', value: '1D' },
  { label: '5D', value: '5D' },
  { label: '1M', value: '1M' },
  { label: '3M', value: '3M' },
  { label: '1Y', value: '1Y' }
]

const orderForm = reactive({
  symbol: '',
  orderType: 'market',
  quantity: null as number | null,
  price: null as number | null,
  limitPrice: null as number | null,
  timeInForce: 'day'
})

const errors = reactive({
  symbol: '',
  quantity: '',
  price: '',
  limitPrice: ''
})

// API Data
const cryptocurrencies = ref<any[]>([])
const symbolResults = ref<any[]>([])
const selectedSymbol = ref<any>(null)
const orderBook = ref<any>(null)
const recentTrades = ref<any[]>([])
const positions = ref<any[]>([])
const priceFeed = ref<any>(null)

// Computed
const estimatedCost = computed(() => {
  if (!orderForm.quantity) return 0
  
  const price = orderForm.orderType === 'market' 
    ? selectedSymbol.value?.price || 0
    : orderForm.price || 0
    
  return orderForm.quantity * price
})

const isFormValid = computed(() => {
  return orderForm.symbol && 
         orderForm.quantity && 
         orderForm.quantity > 0 &&
         (orderForm.orderType === 'market' || (orderForm.price && orderForm.price > 0)) &&
         (orderForm.orderType !== 'stop_limit' || (orderForm.limitPrice && orderForm.limitPrice > 0))
})

// Methods
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const formatVolume = (volume: number) => {
  if (volume >= 1000000) {
    return `${(volume / 1000000).toFixed(1)}M`
  } else if (volume >= 1000) {
    return `${(volume / 1000).toFixed(1)}K`
  }
  return volume.toLocaleString()
}

const formatTime = (timestamp: Date) => {
  return timestamp.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const searchSymbols = async () => {
  if (orderForm.symbol.length >= 2) {
    try {
      const response = await api.trades.getCryptocurrencies()
      const cryptos = response.data.results || response.data
      
      symbolResults.value = cryptos
        .filter((crypto: any) => 
          crypto.symbol.toLowerCase().includes(orderForm.symbol.toLowerCase()) ||
          crypto.name.toLowerCase().includes(orderForm.symbol.toLowerCase())
        )
        .slice(0, 10) // Limit results
        .map((crypto: any) => ({
          symbol: crypto.symbol,
          name: crypto.name,
          price: parseFloat(crypto.current_price || '0'),
          change: parseFloat(crypto.price_change_24h || '0'),
          changePercent: parseFloat(crypto.price_change_percentage_24h || '0')
        }))
    } catch (error) {
      console.error('Error searching symbols:', error)
      symbolResults.value = []
    }
  } else {
    symbolResults.value = []
  }
}

const selectSymbol = (symbol: any) => {
  orderForm.symbol = symbol.symbol
  selectedSymbol.value = { ...symbol, open: 152.50, high: 155.20, low: 151.80, volume: 2450000 }
  showSymbolDropdown.value = false
  errors.symbol = ''
}

const hideSymbolDropdown = () => {
  setTimeout(() => {
    showSymbolDropdown.value = false
  }, 200)
}

const getSharesOwned = (symbol: string) => {
  const position = positions.value.find(p => p.symbol === symbol)
  return position?.quantity || 0
}

const validateForm = () => {
  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })

  let isValid = true

  if (!orderForm.symbol) {
    errors.symbol = 'Symbol is required'
    isValid = false
  }

  if (!orderForm.quantity || orderForm.quantity <= 0) {
    errors.quantity = 'Quantity must be greater than 0'
    isValid = false
  }

  if (orderForm.orderType !== 'market' && (!orderForm.price || orderForm.price <= 0)) {
    errors.price = 'Price must be greater than 0'
    isValid = false
  }

  if (orderForm.orderType === 'stop_limit' && (!orderForm.limitPrice || orderForm.limitPrice <= 0)) {
    errors.limitPrice = 'Limit price must be greater than 0'
    isValid = false
  }

  return isValid
}

const handlePlaceOrder = async () => {
  if (!validateForm()) return

  isSubmitting.value = true

  try {
    const tradeData = {
      symbol: orderForm.symbol,
      side: orderSide.value,
      order_type: orderForm.orderType,
      quantity: orderForm.quantity!,
      price: orderForm.orderType !== 'market' ? orderForm.price : undefined,
      stop_price: orderForm.orderType === 'stop_limit' ? orderForm.limitPrice : undefined,
      time_in_force: orderForm.timeInForce
    }

    // Try trading engine first, fallback to crypto trade
    try {
      await api.trading.executeTrade(tradeData)
    } catch (tradingError) {
      console.log('Trading engine not available, trying crypto trade endpoint:', tradingError)
      await api.trades.executeCryptoTrade(tradeData)
    }

    showNotification({
      type: 'success',
      title: 'Order Placed',
      message: `${orderSide.value.toUpperCase()} order for ${orderForm.quantity} ${orderForm.symbol} has been placed successfully.`
    })

    // Reset form
    orderForm.symbol = ''
    orderForm.quantity = null
    orderForm.price = null
    orderForm.limitPrice = null
    selectedSymbol.value = null
    symbolResults.value = []

  } catch (error: any) {
    console.error('Error placing order:', error)
    showNotification({
      type: 'error',
      title: 'Order Failed',
      message: error.response?.data?.detail || 'Failed to place order. Please try again.'
    })
  } finally {
    isSubmitting.value = false
  }
}

// Load market data
const loadMarketData = async () => {
  try {
    // Load order book
    try {
      const orderBookResponse = await api.trading.getOrderBook(selectedSymbol.value?.symbol)
      orderBook.value = orderBookResponse.data
    } catch (error) {
      console.log('Order book not available:', error)
    }
    
    // Load price feed
    try {
      const priceFeedResponse = await api.trading.getPriceFeed(selectedSymbol.value?.symbol)
      priceFeed.value = priceFeedResponse.data
    } catch (error) {
      console.log('Price feed not available:', error)
    }
    
    // Load recent trades
    try {
      const tradesResponse = await api.trades.getTrades({ 
        symbol: selectedSymbol.value?.symbol,
        limit: 10,
        ordering: '-created_at'
      })
      recentTrades.value = tradesResponse.data.results || tradesResponse.data
    } catch (error) {
      console.log('Recent trades not available:', error)
    }
    
    // Load positions/crypto wallets
    try {
      const walletsResponse = await api.wallets.getCryptoWallets()
      positions.value = (walletsResponse.data.results || walletsResponse.data).map((wallet: any) => ({
        symbol: wallet.currency?.symbol || wallet.currency,
        quantity: parseFloat(wallet.balance || '0')
      }))
    } catch (error) {
      console.log('Positions not available:', error)
    }
    
  } catch (error) {
    console.error('Error loading market data:', error)
  }
}

// Auto-refresh market data
let refreshInterval: NodeJS.Timeout | null = null

onMounted(async () => {
  // Load initial data
  await loadMarketData()
  
  // Set up auto-refresh every 30 seconds for market data
  refreshInterval = setInterval(() => {
    if (selectedSymbol.value) {
      loadMarketData()
    }
  }, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})

// Watch for symbol changes to load symbol data
watch(() => orderForm.symbol, (newSymbol) => {
  if (newSymbol && symbolResults.value.length > 0) {
    const found = symbolResults.value.find(s => s.symbol === newSymbol)
    if (found) {
      selectedSymbol.value = { ...found, open: 152.50, high: 155.20, low: 151.80, volume: 2450000 }
    }
  }
})
</script>