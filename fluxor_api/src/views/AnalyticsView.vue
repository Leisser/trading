<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Analytics & Performance</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/dashboard" class="btn-secondary text-sm">Back to Dashboard</router-link>
            <button @click="authStore.logout" class="btn-secondary text-sm">Logout</button>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Performance Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div class="card">
          <h3 class="text-sm font-medium text-gray-500">Total P&L</h3>
          <p class="text-2xl font-bold" :class="totalPnL >= 0 ? 'text-green-600' : 'text-red-600'">
            {{ totalPnL >= 0 ? '+' : '' }}${{ formatNumber(totalPnL) }}
          </p>
          <p class="text-sm text-gray-500">{{ totalPnLPercent >= 0 ? '+' : '' }}{{ totalPnLPercent.toFixed(2) }}%</p>
        </div>
        
        <div class="card">
          <h3 class="text-sm font-medium text-gray-500">Win Rate</h3>
          <p class="text-2xl font-bold text-primary-600">{{ winRate.toFixed(1) }}%</p>
          <p class="text-sm text-gray-500">{{ winningTrades }} of {{ totalTrades }} trades</p>
        </div>
        
        <div class="card">
          <h3 class="text-sm font-medium text-gray-500">Average Trade</h3>
          <p class="text-2xl font-bold" :class="avgTrade >= 0 ? 'text-green-600' : 'text-red-600'">
            {{ avgTrade >= 0 ? '+' : '' }}${{ formatNumber(avgTrade) }}
          </p>
          <p class="text-sm text-gray-500">Per trade</p>
        </div>
        
        <div class="card">
          <h3 class="text-sm font-medium text-gray-500">Portfolio Value</h3>
          <p class="text-2xl font-bold text-gray-900">${{ formatNumber(portfolioValue) }}</p>
          <p class="text-sm text-gray-500">Current balance</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- P&L Chart -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">P&L Over Time</h3>
          <line-chart v-if="pnlChartData" :chart-data="pnlChartData" :chart-options="pnlChartOptions" />
          <div v-else class="text-center py-8 text-gray-500">Loading chart...</div>
        </div>

        <!-- Trade Distribution -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Trade Distribution</h3>
          <doughnut-chart v-if="distributionChartData" :chart-data="distributionChartData" :chart-options="distributionChartOptions" />
          <div v-else class="text-center py-8 text-gray-500">Loading chart...</div>
        </div>
      </div>

      <!-- Detailed Analytics -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Monthly Performance -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Monthly Performance</h3>
          <div class="space-y-3">
            <div v-for="month in monthlyPerformance" :key="month.month" class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-700">{{ month.month }}</span>
              <div class="text-right">
                <p class="text-sm font-medium" :class="month.pnl >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ month.pnl >= 0 ? '+' : '' }}${{ formatNumber(month.pnl) }}
                </p>
                <p class="text-xs text-gray-500">{{ month.trades }} trades</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Risk Metrics -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Risk Metrics</h3>
          <div class="space-y-4">
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Sharpe Ratio</span>
              <span class="text-sm font-medium">{{ sharpeRatio.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Max Drawdown</span>
              <span class="text-sm font-medium text-red-600">{{ maxDrawdown.toFixed(2) }}%</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Volatility</span>
              <span class="text-sm font-medium">{{ volatility.toFixed(2) }}%</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Best Trade</span>
              <span class="text-sm font-medium text-green-600">+${{ formatNumber(bestTrade) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-600">Worst Trade</span>
              <span class="text-sm font-medium text-red-600">-${{ formatNumber(worstTrade) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Trade Analysis -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Trade Analysis</h3>
          <div class="flex space-x-2">
            <select v-model="timeFilter" class="input-field text-sm">
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
              <option value="365">Last year</option>
            </select>
          </div>
        </div>
        
        <div v-if="filteredTrades.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P&L</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ROI</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="trade in filteredTrades" :key="trade.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(trade.timestamp) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="trade.trade_type === 'buy' ? 'text-green-600' : 'text-red-600'" class="font-medium">
                    {{ trade.trade_type.toUpperCase() }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ trade.btc_amount }} BTC
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${{ trade.usd_price }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm" :class="trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ trade.pnl >= 0 ? '+' : '' }}${{ formatNumber(trade.pnl || 0) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm" :class="trade.roi >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ trade.roi >= 0 ? '+' : '' }}{{ (trade.roi || 0).toFixed(2) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="text-center py-8">
          <p class="text-gray-500">No trades found for the selected period</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from 'chart.js'
import { useAuthStore } from '@/stores/auth'
import { useTradingStore } from '@/stores/trading'
import axios from 'axios'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, ArcElement)

const authStore = useAuthStore()
const tradingStore = useTradingStore()

const timeFilter = ref(30)
const trades = ref<any[]>([])

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
  return trades.value.filter(trade => (trade.pnl || 0) > 0).length
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

const filteredTrades = computed(() => {
  const daysAgo = new Date()
  daysAgo.setDate(daysAgo.getDate() - timeFilter.value)
  return trades.value.filter(trade => new Date(trade.timestamp) >= daysAgo)
})

const monthlyPerformance = computed(() => {
  const months: { [key: string]: { pnl: number; trades: number } } = {}
  
  trades.value.forEach(trade => {
    const date = new Date(trade.timestamp)
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    
    if (!months[monthKey]) {
      months[monthKey] = { pnl: 0, trades: 0 }
    }
    
    months[monthKey].pnl += trade.pnl || 0
    months[monthKey].trades += 1
  })
  
  return Object.entries(months)
    .map(([month, data]) => ({ month, ...data }))
    .sort((a, b) => b.month.localeCompare(a.month))
    .slice(0, 6)
})

// Risk metrics
const sharpeRatio = computed(() => {
  if (trades.value.length < 2) return 0
  const returns = trades.value.map(trade => (trade.pnl || 0) / 10000) // Assuming $10k per trade
  const avgReturn = returns.reduce((sum, ret) => sum + ret, 0) / returns.length
  const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - avgReturn, 2), 0) / returns.length
  const stdDev = Math.sqrt(variance)
  return stdDev > 0 ? avgReturn / stdDev : 0
})

const maxDrawdown = computed(() => {
  let peak = 0
  let maxDrawdown = 0
  let runningTotal = 0
  
  trades.value.forEach(trade => {
    runningTotal += trade.pnl || 0
    if (runningTotal > peak) {
      peak = runningTotal
    }
    const drawdown = ((peak - runningTotal) / peak) * 100
    if (drawdown > maxDrawdown) {
      maxDrawdown = drawdown
    }
  })
  
  return maxDrawdown
})

const volatility = computed(() => {
  if (trades.value.length < 2) return 0
  const returns = trades.value.map(trade => (trade.pnl || 0) / 10000)
  const avgReturn = returns.reduce((sum, ret) => sum + ret, 0) / returns.length
  const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - avgReturn, 2), 0) / returns.length
  return Math.sqrt(variance) * 100
})

const bestTrade = computed(() => {
  return Math.max(...trades.value.map(trade => trade.pnl || 0), 0)
})

const worstTrade = computed(() => {
  return Math.abs(Math.min(...trades.value.map(trade => trade.pnl || 0), 0))
})

// Chart data
const pnlChartData = computed(() => {
  if (trades.value.length === 0) return null
  
  const sortedTrades = [...trades.value].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
  let runningPnL = 0
  const data = sortedTrades.map(trade => {
    runningPnL += trade.pnl || 0
    return runningPnL
  })
  
  const labels = sortedTrades.map(trade => new Date(trade.timestamp).toLocaleDateString())
  
  return {
    labels,
    datasets: [{
      label: 'Cumulative P&L',
      data,
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.3,
    }]
  }
})

const pnlChartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: {
      beginAtZero: true,
      title: { display: true, text: 'P&L ($)' }
    }
  }
}

const distributionChartData = computed(() => {
  const buyTrades = trades.value.filter(trade => trade.trade_type === 'buy').length
  const sellTrades = trades.value.filter(trade => trade.trade_type === 'sell').length
  
  return {
    labels: ['Buy', 'Sell'],
    datasets: [{
      data: [buyTrades, sellTrades],
      backgroundColor: ['#10b981', '#ef4444'],
      borderWidth: 0,
    }]
  }
})

const distributionChartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
  }
}

const formatNumber = (num: number) => {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const fetchTrades = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/trades/')
    trades.value = response.data.results || response.data
    
    // Add mock P&L and ROI data for demonstration
    trades.value = trades.value.map(trade => ({
      ...trade,
      pnl: (Math.random() - 0.5) * 1000, // Mock P&L
      roi: (Math.random() - 0.5) * 20 // Mock ROI
    }))
  } catch (error) {
    console.error('Failed to fetch trades:', error)
    trades.value = []
  }
}

onMounted(() => {
  fetchTrades()
})

watch(timeFilter, () => {
  // Refresh data when filter changes
})
</script>

<script lang="ts">
import { defineComponent } from 'vue'
import { Line, Doughnut } from 'vue-chartjs'

export default defineComponent({
  name: 'AnalyticsView',
  components: { 
    LineChart: Line,
    DoughnutChart: Doughnut
  },
})
</script> 