<template>
  <div class="live_trade_view">
    <!-- Header -->
    <div class="live_trade_header">
      <div class="header_content">
        <h1 class="page_title">Live Trade Dashboard</h1>
        <div class="live_status">
          <div class="status_indicator" :class="{ active: isLive }"></div>
          <span class="status_text">{{ isLive ? 'LIVE' : 'OFFLINE' }}</span>
        </div>
      </div>
      <div class="header_actions">
        <button @click="toggleLive" class="live_toggle_btn" :class="{ active: isLive }">
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
              clip-rule="evenodd"
            ></path>
          </svg>
          {{ isLive ? 'Stop Live' : 'Start Live' }}
        </button>
        <button @click="refreshData" class="refresh_btn">
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
              clip-rule="evenodd"
            ></path>
          </svg>
          Refresh
        </button>
      </div>
    </div>

    <!-- Spot Buy Selection -->
    <div class="spot_buy_selector">
      <div class="selector_header">
        <h2 class="section_title">Your Spot Buys</h2>
        <span class="spot_count">{{ userSpotBuys.length }} active positions</span>
      </div>
      <div class="spot_buy_grid">
        <div
          v-for="spotBuy in userSpotBuys"
          :key="spotBuy.id"
          class="spot_buy_card"
          :class="{ active: selectedSpotBuy?.id === spotBuy.id }"
          @click="selectSpotBuy(spotBuy)"
        >
          <div class="spot_buy_header">
            <div class="crypto_info">
              <div class="crypto_icon" :class="spotBuy.crypto.toLowerCase()">
                {{ spotBuy.crypto.charAt(0) }}
              </div>
              <div class="crypto_details">
                <h3 class="crypto_name">{{ spotBuy.crypto }}/USD</h3>
                <p class="entry_price">Entry: ${{ formatPrice(spotBuy.entryPrice) }}</p>
              </div>
            </div>
            <div class="performance" :class="getPerformanceClass(spotBuy)">
              <span class="performance_value">{{ getPerformanceValue(spotBuy) }}</span>
              <span class="performance_percent">{{ getPerformancePercent(spotBuy) }}</span>
            </div>
          </div>
          <div class="spot_buy_details">
            <div class="detail_item">
              <span class="detail_label">Amount:</span>
              <span class="detail_value">{{ formatCrypto(spotBuy.amount, spotBuy.crypto) }}</span>
            </div>
            <div class="detail_item">
              <span class="detail_label">Value:</span>
              <span class="detail_value">${{ formatPrice(spotBuy.currentValue) }}</span>
            </div>
            <div class="detail_item">
              <span class="detail_label">P&L:</span>
              <span class="detail_value" :class="getPerformanceClass(spotBuy)">
                ${{ formatPrice(spotBuy.pnl) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Chart Section -->
    <div v-if="selectedSpotBuy" class="live_chart_section">
      <div class="chart_header">
        <div class="chart_info">
          <h2 class="chart_title">{{ selectedSpotBuy.crypto }}/USD - Live Performance</h2>
          <div class="current_price" :class="getPriceChangeClass(selectedSpotBuy)">
            <span class="price_value">${{ formatPrice(selectedSpotBuy.currentPrice) }}</span>
            <span class="price_change">{{ getPriceChange(selectedSpotBuy) }}</span>
          </div>
        </div>
        <div class="chart_controls">
          <select v-model="timeframe" class="timeframe_select">
            <option value="1m">1m</option>
            <option value="5m">5m</option>
            <option value="15m">15m</option>
            <option value="1h">1h</option>
            <option value="4h">4h</option>
            <option value="1d">1d</option>
          </select>
          <button @click="toggleFullscreen" class="fullscreen_btn">
            <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 11-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293-2.293a1 1 0 111.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15 13.586V12a1 1 0 011-1z"
              ></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Real-time Candlestick Chart -->
      <div class="chart_container">
        <apexchart
          ref="candlestickChart"
          :options="chartOptions"
          :series="chartSeries"
          height="400"
          type="candlestick"
        />
      </div>

      <!-- Live Updates Animation -->
      <div v-if="isLive && newDataPoint" class="live_update_indicator">
        <div class="update_animation"></div>
        <span class="update_text"
          >Live data updated at {{ formatTime(newDataPoint.timestamp) }}</span
        >
      </div>
    </div>

    <!-- No Selection State -->
    <div v-else class="no_selection_state">
      <div class="empty_state">
        <div class="empty_icon">
          <svg fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </div>
        <h3 class="empty_title">Select a Spot Buy</h3>
        <p class="empty_description">
          Choose one of your spot buy positions above to view live performance and real-time
          candlestick charts.
        </p>
      </div>
    </div>

    <!-- Trade Actions -->
    <div v-if="selectedSpotBuy" class="trade_actions">
      <button @click="modifyPosition" class="action_btn modify_btn">
        <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"
          ></path>
        </svg>
        Modify Position
      </button>
      <button @click="closePosition" class="action_btn close_btn">
        <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          ></path>
        </svg>
        Close Position
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTradingStore } from '@/stores/trading'
import { useToast } from '@/composables/useToast'

// Stores
const authStore = useAuthStore()
const tradingStore = useTradingStore()
const { showToast } = useToast()

// Reactive state
const isLive = ref(false)
const selectedSpotBuy = ref<any>(null)
const timeframe = ref('5m')
const newDataPoint = ref<any>(null)
const candlestickChart = ref<any>(null)

// Mock user spot buys data
const userSpotBuys = ref([
  {
    id: 1,
    crypto: 'BTC',
    amount: 0.5,
    entryPrice: 45000,
    currentPrice: 46500,
    currentValue: 23250,
    pnl: 750,
    entryDate: new Date('2024-01-15T10:30:00Z'),
    performance: 1.67,
  },
  {
    id: 2,
    crypto: 'ETH',
    amount: 5.0,
    entryPrice: 3200,
    currentPrice: 3150,
    currentValue: 15750,
    pnl: -250,
    entryDate: new Date('2024-01-16T14:20:00Z'),
    performance: -1.56,
  },
  {
    id: 3,
    crypto: 'SOL',
    amount: 50.0,
    entryPrice: 95,
    currentPrice: 102,
    currentValue: 5100,
    pnl: 350,
    entryDate: new Date('2024-01-17T09:15:00Z'),
    performance: 7.37,
  },
])

// Chart data
const chartSeries = ref([
  {
    name: 'BTC/USD',
    data: [],
  },
])

// Computed chart options
const chartOptions = computed(() => ({
  chart: {
    type: 'candlestick',
    height: 400,
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150,
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350,
      },
    },
    background: 'transparent',
    foreColor: '#6b7280',
    toolbar: {
      show: false,
    },
  },
  title: {
    text: `${selectedSpotBuy.value?.crypto || 'BTC'}/USD Live Chart`,
    align: 'left',
    style: {
      fontSize: '16px',
      fontWeight: 'bold',
    },
  },
  xaxis: {
    type: 'datetime',
    labels: {
      style: {
        colors: '#6b7280',
      },
    },
  },
  yaxis: {
    tooltip: {
      enabled: true,
    },
    labels: {
      style: {
        colors: '#6b7280',
      },
    },
  },
  plotOptions: {
    candlestick: {
      colors: {
        upward: '#10b981',
        downward: '#ef4444',
      },
    },
  },
  theme: {
    mode: 'dark',
  },
}))

// Methods
const toggleLive = () => {
  isLive.value = !isLive.value
  if (isLive.value) {
    startLiveData()
    showToast('Live trading started', 'success')
  } else {
    stopLiveData()
    showToast('Live trading stopped', 'info')
  }
}

const startLiveData = () => {
  // Simulate real-time data updates every 2 seconds
  const interval = setInterval(() => {
    if (!isLive.value) {
      clearInterval(interval)
      return
    }

    updateChartData()
  }, 2000)
}

const stopLiveData = () => {
  // Stop live data updates
}

const updateChartData = () => {
  if (!selectedSpotBuy.value) return

  const now = new Date()
  const basePrice = selectedSpotBuy.value.currentPrice
  const volatility = 0.02 // 2% volatility

  // Generate realistic candlestick data
  const open = basePrice * (1 + (Math.random() - 0.5) * volatility)
  const high = open * (1 + Math.random() * volatility)
  const low = open * (1 - Math.random() * volatility)
  const close = low + Math.random() * (high - low)

  const newCandle = {
    x: now.getTime(),
    y: [open, high, low, close],
  }

  // Add new candle to chart
  chartSeries.value[0].data.push(newCandle)

  // Keep only last 100 candles
  if (chartSeries.value[0].data.length > 100) {
    chartSeries.value[0].data.shift()
  }

  // Update selected spot buy current price
  selectedSpotBuy.value.currentPrice = close
  selectedSpotBuy.value.currentValue = selectedSpotBuy.value.amount * close
  selectedSpotBuy.value.pnl =
    selectedSpotBuy.value.currentValue -
    selectedSpotBuy.value.amount * selectedSpotBuy.value.entryPrice

  // Show live update animation
  newDataPoint.value = {
    timestamp: now,
    price: close,
  }

  // Clear animation after 3 seconds
  setTimeout(() => {
    newDataPoint.value = null
  }, 3000)
}

const selectSpotBuy = (spotBuy: any) => {
  selectedSpotBuy.value = spotBuy
  initializeChartData()
}

const initializeChartData = () => {
  if (!selectedSpotBuy.value) return

  // Generate historical candlestick data
  const data = []
  const basePrice = selectedSpotBuy.value.entryPrice
  const now = new Date()

  for (let i = 100; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 5 * 60 * 1000) // 5-minute intervals
    const volatility = 0.015
    const trend = Math.sin(i * 0.1) * 0.01 // Slight trend

    const open = basePrice * (1 + trend + (Math.random() - 0.5) * volatility)
    const high = open * (1 + Math.random() * volatility)
    const low = open * (1 - Math.random() * volatility)
    const close = low + Math.random() * (high - low)

    data.push({
      x: time.getTime(),
      y: [open, high, low, close],
    })
  }

  chartSeries.value[0].data = data
  chartSeries.value[0].name = `${selectedSpotBuy.value.crypto}/USD`
}

const refreshData = () => {
  if (selectedSpotBuy.value) {
    initializeChartData()
  }
  showToast('Data refreshed', 'success')
}

const toggleFullscreen = () => {
  // Implement fullscreen functionality
  showToast('Fullscreen mode toggled', 'info')
}

const modifyPosition = () => {
  // Implement position modification
  showToast('Position modification coming soon', 'info')
}

const closePosition = () => {
  if (selectedSpotBuy.value) {
    const profit = selectedSpotBuy.value.pnl
    const message =
      profit >= 0
        ? `Position closed with profit of $${formatPrice(profit)}`
        : `Position closed with loss of $${formatPrice(Math.abs(profit))}`
    showToast(message, profit >= 0 ? 'success' : 'warning')

    // Remove from user spot buys
    const index = userSpotBuys.value.findIndex((sb) => sb.id === selectedSpotBuy.value.id)
    if (index > -1) {
      userSpotBuys.value.splice(index, 1)
    }
    selectedSpotBuy.value = null
  }
}

// Utility functions
const formatPrice = (price: number) => {
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatCrypto = (amount: number, crypto: string) => {
  return `${amount.toFixed(4)} ${crypto}`
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('en-US', { hour12: false })
}

const getPerformanceClass = (spotBuy: any) => {
  return spotBuy.pnl >= 0 ? 'positive' : 'negative'
}

const getPerformanceValue = (spotBuy: any) => {
  return `$${formatPrice(Math.abs(spotBuy.pnl))}`
}

const getPerformancePercent = (spotBuy: any) => {
  const percent = ((spotBuy.currentPrice - spotBuy.entryPrice) / spotBuy.entryPrice) * 100
  return `${percent >= 0 ? '+' : ''}${percent.toFixed(2)}%`
}

const getPriceChangeClass = (spotBuy: any) => {
  return spotBuy.pnl >= 0 ? 'positive' : 'negative'
}

const getPriceChange = (spotBuy: any) => {
  const change = spotBuy.currentPrice - spotBuy.entryPrice
  const percent = (change / spotBuy.entryPrice) * 100
  return `${change >= 0 ? '+' : ''}$${formatPrice(change)} (${percent >= 0 ? '+' : ''}${percent.toFixed(2)}%)`
}

// Lifecycle
onMounted(() => {
  // Initialize with first spot buy if available
  if (userSpotBuys.value.length > 0) {
    selectSpotBuy(userSpotBuys.value[0])
  }
})

onUnmounted(() => {
  stopLiveData()
})

// Watch for timeframe changes
watch(timeframe, () => {
  if (selectedSpotBuy.value) {
    initializeChartData()
  }
})
</script>

<style scoped>
.live_trade_view {
  padding: 2rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.live_trade_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.header_content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page_title {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.live_status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status_indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ef4444;
  transition: all 0.3s ease;
}

.status_indicator.active {
  background: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status_text {
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.header_actions {
  display: flex;
  gap: 1rem;
}

.live_toggle_btn,
.refresh_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.live_toggle_btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.live_toggle_btn.active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.refresh_btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.live_toggle_btn:hover,
.refresh_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.spot_buy_selector {
  margin-bottom: 2rem;
}

.selector_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.spot_count {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
}

.spot_buy_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.spot_buy_card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.spot_buy_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.spot_buy_card.active {
  border-color: #3b82f6;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.spot_buy_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.crypto_info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.crypto_icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  color: white;
}

.crypto_icon.btc {
  background: linear-gradient(135deg, #f7931a 0%, #ff9500 100%);
}

.crypto_icon.eth {
  background: linear-gradient(135deg, #627eea 0%, #4f6cdb 100%);
}

.crypto_icon.sol {
  background: linear-gradient(135deg, #9945ff 0%, #14f195 100%);
}

.crypto_name {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.25rem 0;
}

.entry_price {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  margin: 0;
}

.performance {
  text-align: right;
}

.performance_value {
  display: block;
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
}

.performance_percent {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
}

.performance.positive .performance_percent {
  color: #10b981;
}

.performance.negative .performance_percent {
  color: #ef4444;
}

.spot_buy_details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.detail_item {
  text-align: center;
}

.detail_label {
  display: block;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.detail_value {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.detail_value.positive {
  color: #10b981;
}

.detail_value.negative {
  color: #ef4444;
}

.live_chart_section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.chart_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart_info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chart_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.current_price {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price_value {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
}

.price_change {
  font-size: 0.875rem;
  font-weight: 600;
}

.price_change.positive {
  color: #10b981;
}

.price_change.negative {
  color: #ef4444;
}

.chart_controls {
  display: flex;
  gap: 0.5rem;
}

.timeframe_select {
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.875rem;
}

.fullscreen_btn {
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.fullscreen_btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.chart_container {
  position: relative;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.live_update_indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(16, 185, 129, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 0.5rem;
}

.update_animation {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0.3;
  }
}

.update_text {
  color: #10b981;
  font-size: 0.875rem;
  font-weight: 600;
}

.no_selection_state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty_state {
  text-align: center;
  padding: 3rem;
}

.empty_icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
}

.empty_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
}

.empty_description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin: 0;
}

.trade_actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 2rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
}

.action_btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 2.5rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 180px;
  justify-content: center;
}

.modify_btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.close_btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.action_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.btn_icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Dark mode adjustments */
[data-theme='dark'] .live_trade_view {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

[data-theme='dark'] .live_trade_header,
[data-theme='dark'] .spot_buy_card,
[data-theme='dark'] .live_chart_section {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(55, 65, 81, 0.5);
}
</style>
