<template>
  <div class="analytics_view">
    <!-- Header -->
    <div class="analytics_header">
      <div class="header_content">
        <h1 class="page_title">Analytics & Performance</h1>
        <p class="page_subtitle">Comprehensive trading insights and performance metrics</p>
      </div>
      <div class="header_actions">
        <router-link to="/dashboard" class="nav_btn">
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
          Back to Dashboard
        </router-link>
        <button @click="refreshData" class="refresh_btn">
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
              clip-rule="evenodd"
            ></path>
          </svg>
          Refresh Data
        </button>
      </div>
    </div>

    <!-- Performance Overview Cards -->
    <div class="performance_overview">
      <div class="overview_header">
        <h2 class="section_title">Performance Overview</h2>
        <div class="time_filter">
          <select v-model="selectedTimeframe" class="timeframe_select">
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
            <option value="1y">Last Year</option>
            <option value="all">All Time</option>
          </select>
        </div>
      </div>

      <div class="metrics_grid">
        <div class="metric_card" :class="getMetricClass('pnl')">
          <div class="metric_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="metric_content">
            <h3 class="metric_title">Total P&L</h3>
            <p class="metric_value" :class="totalPnL >= 0 ? 'positive' : 'negative'">
              {{ totalPnL >= 0 ? '+' : '' }}${{ formatNumber(totalPnL) }}
            </p>
            <p class="metric_change" :class="totalPnLPercent >= 0 ? 'positive' : 'negative'">
              {{ totalPnLPercent >= 0 ? '+' : '' }}{{ totalPnLPercent.toFixed(2) }}%
            </p>
          </div>
        </div>

        <div class="metric_card">
          <div class="metric_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="metric_content">
            <h3 class="metric_title">Win Rate</h3>
            <p class="metric_value">{{ winRate.toFixed(1) }}%</p>
            <p class="metric_subtitle">{{ winningTrades }} of {{ totalTrades }} trades</p>
          </div>
        </div>

        <div class="metric_card">
          <div class="metric_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"
              ></path>
            </svg>
          </div>
          <div class="metric_content">
            <h3 class="metric_title">Average Trade</h3>
            <p class="metric_value" :class="avgTrade >= 0 ? 'positive' : 'negative'">
              {{ avgTrade >= 0 ? '+' : '' }}${{ formatNumber(avgTrade) }}
            </p>
            <p class="metric_subtitle">Per trade</p>
          </div>
        </div>

        <div class="metric_card">
          <div class="metric_icon">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="metric_content">
            <h3 class="metric_title">Portfolio Value</h3>
            <p class="metric_value">${{ formatNumber(portfolioValue) }}</p>
            <p class="metric_subtitle">Current balance</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts_section">
      <div class="charts_grid">
        <!-- P&L Chart -->
        <div class="chart_card">
          <div class="chart_header">
            <h3 class="chart_title">P&L Over Time</h3>
            <div class="chart_controls">
              <button @click="exportChart('pnl')" class="export_btn">
                <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Export
              </button>
            </div>
          </div>
          <div class="chart_container">
            <apexchart
              v-if="pnlChartData"
              type="line"
              height="300"
              :options="pnlChartOptions"
              :series="pnlChartData"
            />
            <div v-else class="loading_state">
              <div class="loading_spinner"></div>
              <p>Loading chart data...</p>
            </div>
          </div>
        </div>

        <!-- Trade Distribution -->
        <div class="chart_card">
          <div class="chart_header">
            <h3 class="chart_title">Trade Distribution</h3>
            <div class="chart_controls">
              <button @click="exportChart('distribution')" class="export_btn">
                <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Export
              </button>
            </div>
          </div>
          <div class="chart_container">
            <apexchart
              v-if="distributionChartData"
              type="donut"
              height="300"
              :options="distributionChartOptions"
              :series="distributionChartData"
            />
            <div v-else class="loading_state">
              <div class="loading_spinner"></div>
              <p>Loading chart data...</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Analytics -->
    <div class="detailed_analytics">
      <div class="analytics_grid">
        <!-- Monthly Performance -->
        <div class="analytics_card">
          <div class="card_header">
            <h3 class="card_title">Monthly Performance</h3>
            <div class="card_actions">
              <button @click="exportMonthlyData" class="action_btn">
                <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Export
              </button>
            </div>
          </div>
          <div class="performance_list">
            <div v-for="month in monthlyPerformance" :key="month.month" class="performance_item">
              <div class="item_header">
                <span class="month_name">{{ month.month }}</span>
                <span class="trade_count">{{ month.trades }} trades</span>
              </div>
              <div class="item_metrics">
                <div class="metric">
                  <span class="metric_label">P&L:</span>
                  <span class="metric_value" :class="month.pnl >= 0 ? 'positive' : 'negative'">
                    {{ month.pnl >= 0 ? '+' : '' }}${{ formatNumber(month.pnl) }}
                  </span>
                </div>
                <div class="metric">
                  <span class="metric_label">Win Rate:</span>
                  <span class="metric_value">{{ month.winRate.toFixed(1) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Performing Assets -->
        <div class="analytics_card">
          <div class="card_header">
            <h3 class="card_title">Top Performing Assets</h3>
            <div class="card_actions">
              <button @click="exportAssetData" class="action_btn">
                <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
                Export
              </button>
            </div>
          </div>
          <div class="assets_list">
            <div v-for="(asset, index) in topAssets" :key="asset.symbol" class="asset_item">
              <div class="asset_rank">{{ index + 1 }}</div>
              <div class="asset_info">
                <div class="asset_icon" :class="asset.symbol.toLowerCase()">
                  {{ asset.symbol.charAt(0) }}
                </div>
                <div class="asset_details">
                  <span class="asset_name">{{ asset.name }}</span>
                  <span class="asset_symbol">{{ asset.symbol }}</span>
                </div>
              </div>
              <div class="asset_performance">
                <span class="performance_value" :class="asset.pnl >= 0 ? 'positive' : 'negative'">
                  {{ asset.pnl >= 0 ? '+' : '' }}${{ formatNumber(asset.pnl) }}
                </span>
                <span
                  class="performance_percent"
                  :class="asset.percentChange >= 0 ? 'positive' : 'negative'"
                >
                  {{ asset.percentChange >= 0 ? '+' : '' }}{{ asset.percentChange.toFixed(2) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Trades Table -->
    <div class="recent_trades">
      <div class="trades_header">
        <h2 class="section_title">Recent Trades</h2>
        <router-link to="/live-trade" class="view_all_btn">
          View All Trades
          <svg class="btn_icon" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </router-link>
      </div>

      <div class="trades_table">
        <div class="table_header">
          <div class="header_cell">Date</div>
          <div class="header_cell">Asset</div>
          <div class="header_cell">Type</div>
          <div class="header_cell">Amount</div>
          <div class="header_cell">Price</div>
          <div class="header_cell">P&L</div>
          <div class="header_cell">Status</div>
        </div>

        <div class="table_body">
          <div v-for="trade in recentTrades" :key="trade.id" class="table_row">
            <div class="table_cell">{{ formatDate(trade.date) }}</div>
            <div class="table_cell">
              <div class="asset_display">
                <div class="asset_icon small" :class="trade.asset.toLowerCase()">
                  {{ trade.asset.charAt(0) }}
                </div>
                <span>{{ trade.asset }}</span>
              </div>
            </div>
            <div class="table_cell">
              <span class="trade_type" :class="trade.type.toLowerCase()">
                {{ trade.type }}
              </span>
            </div>
            <div class="table_cell">{{ formatNumber(trade.amount) }}</div>
            <div class="table_cell">${{ formatNumber(trade.price) }}</div>
            <div class="table_cell" :class="trade.pnl >= 0 ? 'positive' : 'negative'">
              {{ trade.pnl >= 0 ? '+' : '' }}${{ formatNumber(trade.pnl) }}
            </div>
            <div class="table_cell">
              <span class="status_badge" :class="trade.status.toLowerCase()">
                {{ trade.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import axios from 'axios'

const authStore = useAuthStore()
const { showToast } = useToast()

// Reactive data
const selectedTimeframe = ref('30d')
const trades = ref<Trade[]>([])
const topAssets = ref<TopAsset[]>([])
const recentTrades = ref<RecentTrade[]>([])

// Define interfaces
interface Trade {
  id: number
  trade_type: 'buy' | 'sell'
  btc_amount: string
  usd_price: string
  timestamp: string
  status: string
  pnl?: number
  roi?: number
}

interface TopAsset {
  symbol: string
  name: string
  pnl: number
  percentChange: number
}

interface RecentTrade {
  id: number
  date: string
  asset: string
  type: string
  amount: number
  price: number
  pnl: number
  status: string
}

// Mock data for demonstration
const mockTopAssets: TopAsset[] = [
  { symbol: 'BTC', name: 'Bitcoin', pnl: 2500, percentChange: 15.5 },
  { symbol: 'ETH', name: 'Ethereum', pnl: 1800, percentChange: 12.3 },
  { symbol: 'SOL', name: 'Solana', pnl: 1200, percentChange: 8.7 },
  { symbol: 'ADA', name: 'Cardano', pnl: -300, percentChange: -2.1 },
  { symbol: 'DOT', name: 'Polkadot', pnl: 800, percentChange: 5.4 },
  { symbol: 'LINK', name: 'Chainlink', pnl: 600, percentChange: 4.2 },
]

const mockRecentTrades: RecentTrade[] = [
  {
    id: 1,
    date: '2024-01-15',
    asset: 'BTC',
    type: 'Buy',
    amount: 0.5,
    price: 45000,
    pnl: 2500,
    status: 'Completed',
  },
  {
    id: 2,
    date: '2024-01-14',
    asset: 'ETH',
    type: 'Sell',
    amount: 2.0,
    price: 3200,
    pnl: -150,
    status: 'Completed',
  },
  {
    id: 3,
    date: '2024-01-13',
    asset: 'SOL',
    type: 'Buy',
    amount: 10,
    price: 95,
    pnl: 500,
    status: 'Completed',
  },
  {
    id: 4,
    date: '2024-01-12',
    asset: 'ADA',
    type: 'Buy',
    amount: 1000,
    price: 0.45,
    pnl: -200,
    status: 'Pending',
  },
  {
    id: 5,
    date: '2024-01-11',
    asset: 'DOT',
    type: 'Sell',
    amount: 50,
    price: 7.2,
    pnl: 300,
    status: 'Completed',
  },
]

// Computed properties for analytics
const totalPnL = computed(() => {
  return trades.value.reduce((sum, trade) => sum + (trade.pnl || 0), 0)
})

const totalPnLPercent = computed(() => {
  const initialInvestment = 10000 // Assuming $10k initial investment
  return (totalPnL.value / initialInvestment) * 100
})

const totalTrades = computed(() => trades.value.length)

const winningTrades = computed(() => {
  return trades.value.filter((trade) => (trade.pnl || 0) > 0).length
})

const winRate = computed(() => {
  return totalTrades.value > 0 ? (winningTrades.value / totalTrades.value) * 100 : 0
})

const avgTrade = computed(() => {
  return totalTrades.value > 0 ? totalPnL.value / totalTrades.value : 0
})

const portfolioValue = computed(() => {
  return 10000 + totalPnL.value // Initial investment + P&L
})

const monthlyPerformance = computed(() => {
  const months: { [key: string]: { pnl: number; trades: number; winRate: number } } = {}

  trades.value.forEach((trade) => {
    const date = new Date(trade.timestamp)
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`

    if (!months[monthKey]) {
      months[monthKey] = { pnl: 0, trades: 0, winRate: 0 }
    }

    months[monthKey].pnl += trade.pnl || 0
    months[monthKey].trades += 1
  })

  // Calculate win rate for each month
  Object.keys(months).forEach((monthKey) => {
    const monthTrades = trades.value.filter((trade) => {
      const date = new Date(trade.timestamp)
      const tradeMonthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
      return tradeMonthKey === monthKey
    })
    const winningMonthTrades = monthTrades.filter((trade) => (trade.pnl || 0) > 0).length
    months[monthKey].winRate =
      monthTrades.length > 0 ? (winningMonthTrades / monthTrades.length) * 100 : 0
  })

  return Object.entries(months)
    .map(([month, data]) => ({ month, ...data }))
    .sort((a, b) => b.month.localeCompare(a.month))
    .slice(0, 6)
})

// Chart data for ApexCharts
const pnlChartData = computed(() => {
  if (trades.value.length === 0) return []

  const sortedTrades = [...trades.value].sort(
    (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
  )
  let runningPnL = 0
  const data = sortedTrades.map((trade) => {
    runningPnL += trade.pnl || 0
    return runningPnL
  })

  return [
    {
      name: 'P&L',
      data: data,
    },
  ]
})

const pnlChartOptions = computed(() => ({
  chart: {
    type: 'line',
    background: 'transparent',
    toolbar: {
      show: false,
    },
  },
  theme: {
    mode: 'dark',
  },
  stroke: {
    curve: 'smooth',
    width: 3,
  },
  colors: ['#10b981'],
  grid: {
    borderColor: 'rgba(255, 255, 255, 0.1)',
    strokeDashArray: 5,
  },
  xaxis: {
    categories:
      trades.value.length > 0
        ? [...trades.value]
            .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
            .map((trade) => new Date(trade.timestamp).toLocaleDateString())
        : [],
    labels: {
      style: {
        colors: 'rgba(255, 255, 255, 0.7)',
      },
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: 'rgba(255, 255, 255, 0.7)',
      },
      formatter: (value: number) => `$${value.toLocaleString()}`,
    },
  },
  tooltip: {
    theme: 'dark',
    y: {
      formatter: (value: number) => `$${value.toLocaleString()}`,
    },
  },
}))

const distributionChartData = computed(() => {
  const buyTrades = trades.value.filter((trade) => trade.trade_type === 'buy').length
  const sellTrades = trades.value.filter((trade) => trade.trade_type === 'sell').length
  return [buyTrades, sellTrades]
})

const distributionChartOptions = computed(() => ({
  chart: {
    type: 'donut',
    background: 'transparent',
  },
  theme: {
    mode: 'dark',
  },
  colors: ['#10b981', '#ef4444'],
  labels: ['Buy', 'Sell'],
  legend: {
    position: 'bottom',
    labels: {
      colors: 'rgba(255, 255, 255, 0.7)',
    },
  },
  tooltip: {
    theme: 'dark',
  },
}))

// Methods
const refreshData = async () => {
  try {
    showToast('Refreshing data...', 'info')
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))
    showToast('Data refreshed successfully!', 'success')
  } catch (error) {
    showToast('Failed to refresh data', 'error')
  }
}

const getMetricClass = (metric: string) => {
  if (metric === 'pnl') {
    return totalPnL.value >= 0 ? 'positive' : 'negative'
  }
  return ''
}

const exportChart = (chartType: string) => {
  showToast(`Exporting ${chartType} chart...`, 'info')
  // Implement chart export functionality
}

const exportMonthlyData = () => {
  showToast('Exporting monthly data...', 'info')
  // Implement monthly data export
}

const exportAssetData = () => {
  showToast('Exporting asset data...', 'info')
  // Implement asset data export
}

const formatNumber = (num: number) => {
  return Math.abs(num).toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  })
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

// Lifecycle
onMounted(async () => {
  try {
    // Load mock data
    topAssets.value = mockTopAssets
    recentTrades.value = mockRecentTrades

    // Simulate loading trades from API
    const response = await axios.get('/api/trades')
    trades.value = response.data
  } catch (error) {
    // Use mock data if API fails
    trades.value = [
      {
        id: 1,
        trade_type: 'buy',
        btc_amount: '0.5',
        usd_price: '45000',
        timestamp: '2024-01-15T10:30:00Z',
        status: 'completed',
        pnl: 2500,
      },
      {
        id: 2,
        trade_type: 'sell',
        btc_amount: '0.2',
        usd_price: '46000',
        timestamp: '2024-01-14T15:45:00Z',
        status: 'completed',
        pnl: -150,
      },
    ]
  }
})

// Watch for timeframe changes
watch(selectedTimeframe, (newTimeframe) => {
  // Implement timeframe filtering logic
  console.log('Timeframe changed to:', newTimeframe)
})
</script>

<style scoped>
.analytics_view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.analytics_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.header_content {
  flex: 1;
}

.page_title {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin: 0 0 0.5rem 0;
}

.page_subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  margin: 0;
}

.header_actions {
  display: flex;
  gap: 1rem;
}

.nav_btn,
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
  text-decoration: none;
}

.nav_btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.refresh_btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.nav_btn:hover,
.refresh_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.performance_overview {
  margin-bottom: 2rem;
}

.overview_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section_title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.time_filter {
  display: flex;
  gap: 0.5rem;
}

.timeframe_select {
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
}

.metrics_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.metric_card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.metric_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.metric_icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.metric_content {
  flex: 1;
}

.metric_title {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric_value {
  font-size: 1.75rem;
  font-weight: 800;
  color: white;
  margin: 0 0 0.25rem 0;
}

.metric_value.positive {
  color: #10b981;
}

.metric_value.negative {
  color: #ef4444;
}

.metric_change,
.metric_subtitle {
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0;
}

.metric_change.positive {
  color: #10b981;
}

.metric_change.negative {
  color: #ef4444;
}

.metric_subtitle {
  color: rgba(255, 255, 255, 0.7);
}

.charts_section {
  margin-bottom: 2rem;
}

.charts_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 1.5rem;
}

.chart_card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 1.5rem;
}

.chart_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.chart_controls {
  display: flex;
  gap: 0.5rem;
}

.export_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export_btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.chart_container {
  position: relative;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.loading_state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.7);
}

.loading_spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.detailed_analytics {
  margin-bottom: 2rem;
}

.analytics_grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.analytics_card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 1.5rem;
}

.card_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card_title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.card_actions {
  display: flex;
  gap: 0.5rem;
}

.action_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action_btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.performance_list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.performance_item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.3s ease;
}

.performance_item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.item_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.month_name {
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.trade_count {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.item_metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric_label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.metric_value {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
}

.metric_value.positive {
  color: #10b981;
}

.metric_value.negative {
  color: #ef4444;
}

.assets_list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.asset_item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.3s ease;
}

.asset_item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.asset_rank {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.asset_info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.asset_icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  color: white;
  flex-shrink: 0;
}

.asset_icon.btc {
  background: linear-gradient(135deg, #f7931a 0%, #ff9500 100%);
}

.asset_icon.eth {
  background: linear-gradient(135deg, #627eea 0%, #4f6cdb 100%);
}

.asset_icon.sol {
  background: linear-gradient(135deg, #9945ff 0%, #14f195 100%);
}

.asset_icon.ada {
  background: linear-gradient(135deg, #0033ad 0%, #3399ff 100%);
}

.asset_icon.dot {
  background: linear-gradient(135deg, #e6007a 0%, #ff6b9d 100%);
}

.asset_icon.link {
  background: linear-gradient(135deg, #2a5ada 0%, #5a7bff 100%);
}

.asset_details {
  display: flex;
  flex-direction: column;
}

.asset_name {
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.asset_symbol {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.asset_performance {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.performance_value {
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.performance_value.positive {
  color: #10b981;
}

.performance_value.negative {
  color: #ef4444;
}

.performance_percent {
  font-size: 0.875rem;
  font-weight: 600;
}

.performance_percent.positive {
  color: #10b981;
}

.performance_percent.negative {
  color: #ef4444;
}

.recent_trades {
  margin-bottom: 2rem;
}

.trades_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.view_all_btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.view_all_btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

.trades_table {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  overflow: hidden;
}

.table_header {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header_cell {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.table_body {
  max-height: 400px;
  overflow-y: auto;
}

.table_row {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.table_row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.table_row:last-child {
  border-bottom: none;
}

.table_cell {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: white;
}

.asset_display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.asset_icon.small {
  width: 1.5rem;
  height: 1.5rem;
  font-size: 0.75rem;
}

.trade_type {
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.trade_type.buy {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.trade_type.sell {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status_badge {
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status_badge.completed {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status_badge.pending {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.status_badge.failed {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.btn_icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Dark mode adjustments */
[data-theme='dark'] .analytics_view {
  background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

[data-theme='dark'] .analytics_header,
[data-theme='dark'] .metric_card,
[data-theme='dark'] .chart_card,
[data-theme='dark'] .analytics_card,
[data-theme='dark'] .trades_table {
  background: rgba(31, 41, 55, 0.8);
  border-color: rgba(55, 65, 81, 0.5);
}

/* Responsive design */
@media (max-width: 768px) {
  .analytics_view {
    padding: 1rem;
  }

  .analytics_header {
    flex-direction: column;
    gap: 1rem;
  }

  .header_actions {
    width: 100%;
    justify-content: space-between;
  }

  .metrics_grid {
    grid-template-columns: 1fr;
  }

  .charts_grid {
    grid-template-columns: 1fr;
  }

  .analytics_grid {
    grid-template-columns: 1fr;
  }

  .table_header,
  .table_row {
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .header_cell:nth-child(n + 4),
  .table_cell:nth-child(n + 4) {
    display: none;
  }
}
</style>
