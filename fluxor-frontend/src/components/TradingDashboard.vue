<template>
  <div class="trading-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h1>Trading Dashboard</h1>
      <div class="header-actions">
        <button @click="refreshData" class="btn btn-primary" :disabled="loading">
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
          Refresh
        </button>
      </div>
    </div>

    <!-- Portfolio Summary -->
    <div class="portfolio-summary">
      <div class="summary-card">
        <h3>Portfolio Value</h3>
        <div class="value">{{ formatCurrency(portfolioSummary.total_value) }}</div>
        <div class="change" :class="portfolioSummary.total_pnl >= 0 ? 'positive' : 'negative'">
          {{ formatCurrency(portfolioSummary.total_pnl) }} ({{ portfolioSummary.total_pnl_percentage.toFixed(2) }}%)
        </div>
      </div>

      <div class="summary-card">
        <h3>Total Assets</h3>
        <div class="value">{{ portfolioSummary.total_assets }}</div>
        <div class="subtitle">Different cryptocurrencies</div>
      </div>

      <div class="summary-card">
        <h3>Net Deposits</h3>
        <div class="value">{{ formatCurrency(portfolioSummary.net_deposits) }}</div>
        <div class="subtitle">Total invested</div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="dashboard-grid">
      <!-- Market Data -->
      <div class="market-data-section">
        <h3>Market Data</h3>
        <div class="price-cards">
          <div
            v-for="symbol in watchedSymbols"
            :key="symbol"
            class="price-card"
          >
            <div class="symbol">{{ symbol }}</div>
            <div class="price">{{ formatPrice(marketData[symbol]?.price) }}</div>
            <div
              class="change"
              :class="marketData[symbol]?.change_percent_24h >= 0 ? 'positive' : 'negative'"
            >
              {{ marketData[symbol]?.change_percent_24h?.toFixed(2) }}%
            </div>
          </div>
        </div>
      </div>

      <!-- Trading Panel -->
      <div class="trading-panel">
        <h3>Quick Trade</h3>
        <form @submit.prevent="executeTrade" class="trade-form">
          <div class="form-group">
            <label>Symbol</label>
            <select v-model="tradeForm.symbol" required>
              <option value="">Select Symbol</option>
              <option value="BTC/USDT">BTC/USDT</option>
              <option value="ETH/USDT">ETH/USDT</option>
              <option value="BNB/USDT">BNB/USDT</option>
            </select>
          </div>

          <div class="form-group">
            <label>Side</label>
            <div class="side-buttons">
              <button
                type="button"
                :class="{ active: tradeForm.side === 'buy' }"
                @click="tradeForm.side = 'buy'"
              >
                Buy
              </button>
              <button
                type="button"
                :class="{ active: tradeForm.side === 'sell' }"
                @click="tradeForm.side = 'sell'"
              >
                Sell
              </button>
            </div>
          </div>

          <div class="form-group">
            <label>Amount</label>
            <input
              type="number"
              v-model="tradeForm.amount"
              step="0.00000001"
              required
            >
          </div>

          <div class="form-group">
            <label>Price (Optional - Market Order if empty)</label>
            <input
              type="number"
              v-model="tradeForm.price"
              step="0.01"
              placeholder="Market Price"
            >
          </div>

          <button type="submit" class="btn btn-primary" :disabled="trading">
            {{ trading ? 'Executing...' : 'Execute Trade' }}
          </button>
        </form>
      </div>

      <!-- Portfolio Holdings -->
      <div class="portfolio-holdings">
        <h3>Portfolio Holdings</h3>
        <div class="holdings-table">
          <div class="table-header">
            <div>Asset</div>
            <div>Quantity</div>
            <div>Value</div>
            <div>P&L</div>
          </div>
          <div
            v-for="holding in portfolioBalances"
            :key="holding.asset"
            class="table-row"
          >
            <div class="asset">{{ holding.asset }}</div>
            <div>{{ formatNumber(holding.quantity) }}</div>
            <div>{{ formatCurrency(holding.current_value) }}</div>
            <div
              class="pnl"
              :class="holding.unrealized_pnl >= 0 ? 'positive' : 'negative'"
            >
              {{ formatCurrency(holding.unrealized_pnl) }}
              <small>({{ holding.unrealized_pnl_percentage.toFixed(2) }}%)</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Orders -->
      <div class="recent-orders">
        <h3>Recent Orders</h3>
        <div class="orders-list">
          <div
            v-for="order in recentOrders"
            :key="order.id"
            class="order-item"
          >
            <div class="order-info">
              <div class="symbol">{{ order.symbol }}</div>
              <div class="side" :class="order.side">{{ order.side.toUpperCase() }}</div>
              <div class="quantity">{{ formatNumber(order.quantity) }}</div>
              <div class="price">{{ formatPrice(order.price || order.average_fill_price) }}</div>
            </div>
            <div class="order-status" :class="order.status">
              {{ order.status.toUpperCase() }}
            </div>
          </div>
        </div>
      </div>

      <!-- Price Chart -->
      <div class="price-chart">
        <h3>Price Chart - {{ selectedChartSymbol }}</h3>
        <div class="chart-container" ref="chartContainer">
          <!-- Chart will be rendered here -->
        </div>
        <div class="chart-controls">
          <button
            v-for="timeframe in timeframes"
            :key="timeframe"
            :class="{ active: selectedTimeframe === timeframe }"
            @click="selectTimeframe(timeframe)"
          >
            {{ timeframe }}
          </button>
        </div>
      </div>
    </div>

    <!-- Notifications -->
    <div v-if="notifications.length > 0" class="notifications-panel">
      <h4>Notifications</h4>
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
        :class="notification.notification_type"
      >
        <div class="notification-content">
          <strong>{{ notification.title }}</strong>
          <p>{{ notification.message }}</p>
        </div>
        <button @click="markNotificationAsRead(notification.id)" class="btn-close">
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI, marketAPI, tradingAPI, portfolioAPI, notificationAPI } from '@/services/api'

export default {
  name: 'TradingDashboard',
  data() {
    return {
      loading: false,
      trading: false,

      // Portfolio data
      portfolioSummary: {
        total_value: 0,
        total_pnl: 0,
        total_pnl_percentage: 0,
        total_assets: 0,
        net_deposits: 0
      },
      portfolioBalances: [],

      // Market data
      marketData: {},
      watchedSymbols: ['BTC/USDT', 'ETH/USDT', 'BNB/USDT'],

      // Trading form
      tradeForm: {
        symbol: '',
        side: 'buy',
        amount: '',
        price: ''
      },

      // Orders
      recentOrders: [],

      // Chart
      selectedChartSymbol: 'BTC/USDT',
      selectedTimeframe: '1h',
      timeframes: ['1m', '5m', '15m', '1h', '4h', '1d'],

      // Notifications
      notifications: [],

      // Refresh intervals
      refreshInterval: null,
      marketDataInterval: null
    }
  },

  async mounted() {
    await this.loadInitialData()
    this.setupRefreshIntervals()
  },

  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
    if (this.marketDataInterval) {
      clearInterval(this.marketDataInterval)
    }
  },

  methods: {
    async loadInitialData() {
      this.loading = true
      try {
        await Promise.all([
          this.loadPortfolioSummary(),
          this.loadPortfolioBalances(),
          this.loadRecentOrders(),
          this.loadNotifications(),
          this.loadMarketData()
        ])
      } catch (error) {
        console.error('Error loading initial data:', error)
        this.$toast.error('Failed to load dashboard data')
      } finally {
        this.loading = false
      }
    },

    async loadPortfolioSummary() {
      try {
        const data = await portfolioAPI.getSummary()
        this.portfolioSummary = data
      } catch (error) {
        console.error('Error loading portfolio summary:', error)
      }
    },

    async loadPortfolioBalances() {
      try {
        const data = await portfolioAPI.getBalances()
        this.portfolioBalances = data.balances || []
      } catch (error) {
        console.error('Error loading portfolio balances:', error)
      }
    },

    async loadRecentOrders() {
      try {
        const data = await tradingAPI.getOrderHistory(1, 10)
        this.recentOrders = data.orders || []
      } catch (error) {
        console.error('Error loading recent orders:', error)
      }
    },

    async loadNotifications() {
      try {
        const data = await notificationAPI.getNotifications()
        this.notifications = data.results || []
      } catch (error) {
        console.error('Error loading notifications:', error)
      }
    },

    async loadMarketData() {
      try {
        const promises = this.watchedSymbols.map(symbol =>
          marketAPI.getPrice(symbol).then(data => ({ symbol, data }))
        )
        const results = await Promise.all(promises)

        results.forEach(({ symbol, data }) => {
          this.marketData[symbol] = data
        })
      } catch (error) {
        console.error('Error loading market data:', error)
      }
    },

    async executeTrade() {
      this.trading = true
      try {
        const tradeData = {
          symbol: this.tradeForm.symbol,
          side: this.tradeForm.side,
          amount: parseFloat(this.tradeForm.amount)
        }

        if (this.tradeForm.price) {
          tradeData.price = parseFloat(this.tradeForm.price)
        }

        await tradingAPI.executeTrade(tradeData)
        this.$toast.success('Trade executed successfully')

        // Reset form
        this.tradeForm = {
          symbol: '',
          side: 'buy',
          amount: '',
          price: ''
        }

        // Refresh data
        await this.refreshData()
      } catch (error) {
        console.error('Error executing trade:', error)
        this.$toast.error('Failed to execute trade')
      } finally {
        this.trading = false
      }
    },

    async refreshData() {
      await this.loadInitialData()
    },

    async markNotificationAsRead(notificationId) {
      try {
        await notificationAPI.markAsRead(notificationId)
        this.notifications = this.notifications.filter(n => n.id !== notificationId)
      } catch (error) {
        console.error('Error marking notification as read:', error)
      }
    },

    setupRefreshIntervals() {
      // Refresh portfolio data every 30 seconds
      this.refreshInterval = setInterval(() => {
        this.loadPortfolioSummary()
        this.loadPortfolioBalances()
      }, 30000)

      // Refresh market data every 5 seconds
      this.marketDataInterval = setInterval(() => {
        this.loadMarketData()
      }, 5000)
    },

    selectTimeframe(timeframe) {
      this.selectedTimeframe = timeframe
      // Load chart data for new timeframe
      this.loadChartData()
    },

    async loadChartData() {
      // Implementation for loading chart data
      console.log(`Loading chart data for ${this.selectedChartSymbol} - ${this.selectedTimeframe}`)
    },

    formatCurrency(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value || 0)
    },

    formatPrice(value) {
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 8
      }).format(value || 0)
    },

    formatNumber(value) {
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 8
      }).format(value || 0)
    }
  }
}
</script>

<style scoped>
.trading-dashboard {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  margin: 0;
  color: #333;
}

.portfolio-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.summary-card h3 {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.summary-card .value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.summary-card .change {
  font-size: 14px;
  font-weight: 500;
}

.summary-card .change.positive {
  color: #10b981;
}

.summary-card .change.negative {
  color: #ef4444;
}

.summary-card .subtitle {
  font-size: 12px;
  color: #666;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.market-data-section,
.trading-panel,
.portfolio-holdings,
.recent-orders,
.price-chart {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.price-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.price-card {
  padding: 15px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  text-align: center;
}

.price-card .symbol {
  font-weight: bold;
  margin-bottom: 5px;
}

.price-card .price {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.side-buttons {
  display: flex;
  gap: 10px;
}

.side-buttons button {
  flex: 1;
  padding: 10px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.side-buttons button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.trade-form .form-group {
  margin-bottom: 15px;
}

.trade-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.trade-form input,
.trade-form select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.holdings-table {
  margin-top: 15px;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
}

.table-header {
  font-weight: bold;
  color: #666;
  border-bottom: 2px solid #e5e7eb;
}

.pnl.positive {
  color: #10b981;
}

.pnl.negative {
  color: #ef4444;
}

.orders-list {
  margin-top: 15px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
}

.order-info {
  display: flex;
  gap: 15px;
}

.order-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.order-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.order-status.filled {
  background: #d1fae5;
  color: #065f46;
}

.order-status.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.chart-container {
  height: 300px;
  margin: 15px 0;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
}

.chart-controls {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.chart-controls button {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.chart-controls button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.notifications-panel {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  z-index: 1000;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
}

.notification-item:last-child {
  border-bottom: none;
}

.btn-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #666;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}
</style>
