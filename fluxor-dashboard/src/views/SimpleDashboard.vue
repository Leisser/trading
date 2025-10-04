<template>
  <div class="dashboard-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h2>Failed to Load Dashboard</h2>
      <p>{{ error }}</p>
      <button @click="fetchDashboardData" class="retry-btn">🔄 Retry</button>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Header -->
      <div class="dashboard-header">
        <h1 class="dashboard-title">🚀 Fluxor Trading Dashboard</h1>
        <p class="dashboard-subtitle">Professional cryptocurrency trading platform</p>
      </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3 class="stat-title">Total Portfolio</h3>
          <p class="stat-value">{{ formatCurrency(stats.totalPortfolioValue) }}</p>
          <span class="stat-change" :class="stats.portfolioChange >= 0 ? 'positive' : 'negative'">
            {{ formatPercentage(stats.portfolioChange) }}
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <h3 class="stat-title">Active Trades</h3>
          <p class="stat-value">{{ stats.activeTrades.toLocaleString() }}</p>
          <span class="stat-change positive">+{{ stats.newTradesToday }} today</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3 class="stat-title">Active Users</h3>
          <p class="stat-value">{{ stats.activeUsers.toLocaleString() }}</p>
          <span class="stat-change" :class="stats.userGrowth >= 0 ? 'positive' : 'negative'">
            {{ formatPercentage(stats.userGrowth) }}
          </span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-content">
          <h3 class="stat-title">System Health</h3>
          <p class="stat-value">{{ stats.systemHealth.toFixed(1) }}%</p>
          <span class="stat-change" :class="stats.systemHealth >= 95 ? 'positive' : 'negative'">
            {{ stats.systemHealth >= 95 ? 'Excellent' : 'Needs Attention' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Top Cryptocurrencies -->
      <div class="content-card">
        <h2 class="card-title">🔥 Top Cryptocurrencies</h2>
        <div class="crypto-list">
          <div v-for="crypto in topCryptocurrencies" :key="crypto.symbol" class="crypto-item">
            <div class="crypto-info">
              <span class="crypto-symbol">{{ crypto.symbol }}</span>
              <span class="crypto-name">{{ crypto.name }}</span>
            </div>
            <div class="crypto-price">
              <span class="price">${{ crypto.price }}</span>
              <span class="change" :class="crypto.change >= 0 ? 'positive' : 'negative'">
                {{ formatPercentage(crypto.change) }}
              </span>
            </div>
          </div>
          <div v-if="topCryptocurrencies.length === 0" class="no-data">
            <p>No cryptocurrency data available</p>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="content-card">
        <h2 class="card-title">📊 Recent Trading Activity</h2>
        <div class="activity-list">
          <div v-for="trade in recentTrades" :key="trade.id" class="activity-item">
            <div class="activity-icon" :class="trade.type === 'buy' ? 'buy' : 'sell'">
              {{ trade.type === 'buy' ? '📈' : '📉' }}
            </div>
            <div class="activity-details">
              <span class="activity-pair">{{ trade.pair }}</span>
              <span class="activity-amount">${{ trade.amount }}</span>
            </div>
            <span class="activity-time">{{ formatTimeAgo(trade.timestamp) }}</span>
          </div>
          <div v-if="recentTrades.length === 0" class="no-data">
            <p>No recent trades available</p>
          </div>
        </div>
      </div>

      <!-- System Alerts -->
      <div class="content-card">
        <h2 class="card-title">🚨 System Alerts</h2>
        <div class="alerts-list">
          <div class="alert-item medium">
            <div class="alert-icon">⚠️</div>
            <div class="alert-content">
              <span class="alert-title">High Trading Volume</span>
              <span class="alert-message">Bitcoin trading volume increased by 45%</span>
            </div>
            <span class="alert-time">30 min ago</span>
          </div>
          <div class="alert-item low">
            <div class="alert-icon">ℹ️</div>
            <div class="alert-content">
              <span class="alert-title">System Update</span>
              <span class="alert-message">New trading algorithms deployed</span>
            </div>
            <span class="alert-time">1 hour ago</span>
          </div>
          <div class="alert-item high">
            <div class="alert-icon">🔥</div>
            <div class="alert-content">
              <span class="alert-title">Market Alert</span>
              <span class="alert-message">Ethereum price surge detected</span>
            </div>
            <span class="alert-time">2 hours ago</span>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="content-card">
        <h2 class="card-title">⚡ Quick Actions</h2>
        <div class="actions-grid">
          <button class="action-btn primary">
            <span class="action-icon">📊</span>
            <span class="action-text">View Analytics</span>
          </button>
          <button class="action-btn secondary">
            <span class="action-icon">👥</span>
            <span class="action-text">Manage Users</span>
          </button>
          <button class="action-btn success">
            <span class="action-icon">💰</span>
            <span class="action-text">Trading Control</span>
          </button>
          <button class="action-btn warning">
            <span class="action-icon">📈</span>
            <span class="action-text">Generate Reports</span>
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dashboardAPI } from '@/services/api'

// Reactive data
const loading = ref(true)
const error = ref('')
const stats = ref({
  totalPortfolioValue: 0,
  portfolioChange: 0,
  activeTrades: 0,
  newTradesToday: 0,
  activeUsers: 0,
  userGrowth: 0,
  systemHealth: 0
})

const topCryptocurrencies = ref([])
const recentTrades = ref([])
const systemAlerts = ref([])

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    loading.value = true
    error.value = ''

    // Fetch all data in parallel
    const [
      statsData,
      marketData,
      tradesData,
      userStats
    ] = await Promise.allSettled([
      dashboardAPI.getStats(),
      dashboardAPI.getMarketData(),
      dashboardAPI.getRecentTrades(5),
      dashboardAPI.getUserStats()
    ])

    // Process stats data
    if (statsData.status === 'fulfilled') {
      stats.value = {
        totalPortfolioValue: statsData.value.total_portfolio_value || 0,
        portfolioChange: statsData.value.portfolio_change || 0,
        activeTrades: statsData.value.active_trades || 0,
        newTradesToday: statsData.value.new_trades_today || 0,
        activeUsers: statsData.value.active_users || 0,
        userGrowth: statsData.value.user_growth || 0,
        systemHealth: statsData.value.system_health || 0
      }
    }

    // Process market data
    if (marketData.status === 'fulfilled') {
      topCryptocurrencies.value = marketData.value.slice(0, 5).map((crypto: any) => ({
        symbol: crypto.symbol,
        name: crypto.name,
        price: crypto.price,
        change: crypto.change_24h
      }))
    }

    // Process trades data
    if (tradesData.status === 'fulfilled') {
      recentTrades.value = tradesData.value.map((trade: any) => ({
        id: trade.id,
        pair: trade.pair,
        amount: trade.amount,
        type: trade.trade_type,
        timestamp: new Date(trade.created_at)
      }))
    }

    // Process user stats
    if (userStats.status === 'fulfilled') {
      stats.value.activeUsers = userStats.value.total_users || 0
      stats.value.userGrowth = userStats.value.growth_rate || 0
    }

  } catch (err: any) {
    console.error('Dashboard data fetch error:', err)
    error.value = err.response?.data?.detail || 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

// Format currency
const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Format percentage
const formatPercentage = (value: number) => {
  return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`
}

// Format time ago
const formatTimeAgo = (date: Date) => {
  const now = new Date()
  const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60))

  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes} min ago`

  const diffInHours = Math.floor(diffInMinutes / 60)
  if (diffInHours < 24) return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`

  const diffInDays = Math.floor(diffInHours / 24)
  return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`
}

// Load data on mount
onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 0;
  margin: -1.5rem; /* Override parent padding */
  background: #f8fafc;
  min-height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
  z-index: 10;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 2rem 2rem 0 2rem;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  font-size: 1.125rem;
  color: #64748b;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 0 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 8px;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.stat-change {
  font-size: 0.875rem;
  font-weight: 500;
}

.stat-change.positive {
  color: #059669;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  padding: 0 2rem 2rem 2rem;
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

.crypto-list {
  space-y: 0.75rem;
}

.crypto-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.crypto-item:last-child {
  border-bottom: none;
}

.crypto-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.crypto-symbol {
  font-weight: 600;
  color: #1e293b;
}

.crypto-name {
  font-size: 0.875rem;
  color: #64748b;
}

.crypto-price {
  text-align: right;
}

.price {
  font-weight: 600;
  color: #1e293b;
  display: block;
}

.change {
  font-size: 0.875rem;
  font-weight: 500;
}

.change.positive {
  color: #059669;
}

.change.negative {
  color: #dc2626;
}

.activity-list {
  space-y: 0.75rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}

.activity-icon.buy {
  background: #dcfce7;
  color: #059669;
}

.activity-icon.sell {
  background: #fef2f2;
  color: #dc2626;
}

.activity-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.activity-pair {
  font-weight: 600;
  color: #1e293b;
}

.activity-amount {
  font-size: 0.875rem;
  color: #64748b;
}

.activity-time {
  font-size: 0.875rem;
  color: #94a3b8;
}

.alerts-list {
  space-y: 0.75rem;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 0.75rem;
}

.alert-item.high {
  background: #fef2f2;
  border-left: 4px solid #dc2626;
}

.alert-item.medium {
  background: #fffbeb;
  border-left: 4px solid #f59e0b;
}

.alert-item.low {
  background: #f0f9ff;
  border-left: 4px solid #3b82f6;
}

.alert-icon {
  font-size: 1.25rem;
}

.alert-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.alert-title {
  font-weight: 600;
  color: #1e293b;
}

.alert-message {
  font-size: 0.875rem;
  color: #64748b;
}

.alert-time {
  font-size: 0.875rem;
  color: #94a3b8;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.action-btn.primary {
  background: #dbeafe;
  color: #1e40af;
}

.action-btn.secondary {
  background: #f1f5f9;
  color: #475569;
}

.action-btn.success {
  background: #dcfce7;
  color: #166534;
}

.action-btn.warning {
  background: #fef3c7;
  color: #92400e;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 1.5rem;
}

.action-text {
  font-size: 0.875rem;
}

/* Loading and Error States */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  padding: 2rem;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-container h2 {
  color: #dc2626;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.retry-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #2563eb;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

.stat-change.negative {
  color: #dc2626;
}
</style>
