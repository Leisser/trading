<template>
  <div class="trading-control">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h2>Trading Control</h2>
        <p>Manage trading pairs, monitor orders, and control trading activities</p>
      </div>
      <div class="header-actions">
        <button @click="refreshData" class="btn btn-secondary" :disabled="loading">
          <i class="icon-refresh"></i>
          Refresh
        </button>
        <button @click="emergencyStop" class="btn btn-danger">
          <i class="icon-stop"></i>
          Emergency Stop
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <h3>Active Trading Pairs</h3>
          <p class="stat-value">{{ stats.activePairs }}</p>
          <span class="stat-change">{{ stats.totalPairs }} total</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>Open Orders</h3>
          <p class="stat-value">{{ stats.openOrders }}</p>
          <span class="stat-change positive">{{ stats.ordersToday }} today</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>24h Volume</h3>
          <p class="stat-value">${{ formatCurrency(stats.volume24h) }}</p>
          <span class="stat-change positive">{{ stats.volumeChange }}% change</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-content">
          <h3>Trading Status</h3>
          <p class="stat-value">{{ stats.tradingEnabled ? 'Active' : 'Disabled' }}</p>
          <span :class="stats.tradingEnabled ? 'stat-change positive' : 'stat-change negative'">
            {{ stats.tradingEnabled ? 'All systems operational' : 'Trading suspended' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        class="tab-button"
        :class="{ active: activeTab === tab.id }"
      >
        <i :class="tab.icon"></i>
        {{ tab.label }}
        <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Trading Pairs Management -->
      <div v-if="activeTab === 'pairs'" class="content-section">
        <div class="section-header">
          <h3>Trading Pairs</h3>
          <div class="header-actions">
            <button @click="addTradingPair" class="btn btn-primary">
              <i class="icon-plus"></i>
              Add Pair
            </button>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Pair</th>
                <th>Current Price</th>
                <th>24h Change</th>
                <th>24h Volume</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pair in tradingPairs" :key="pair.id">
                <td>
                  <div class="pair-info">
                    <strong>{{ pair.symbol }}</strong>
                    <small>{{ pair.base_currency }}/{{ pair.quote_currency }}</small>
                  </div>
                </td>
                <td class="price">${{ formatCurrency(pair.current_price) }}</td>
                <td>
                  <span :class="pair.price_change_24h >= 0 ? 'positive' : 'negative'">
                    {{ pair.price_change_24h >= 0 ? '+' : '' }}{{ pair.price_change_24h.toFixed(2) }}%
                  </span>
                </td>
                <td>${{ formatCurrency(pair.volume_24h) }}</td>
                <td>
                  <span class="status-badge" :class="pair.is_active ? 'active' : 'inactive'">
                    {{ pair.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button 
                      @click="togglePairStatus(pair)" 
                      class="btn btn-sm"
                      :class="pair.is_active ? 'btn-warning' : 'btn-success'"
                    >
                      {{ pair.is_active ? 'Disable' : 'Enable' }}
                    </button>
                    <button @click="editPair(pair)" class="btn btn-secondary btn-sm">
                      Edit
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Active Orders -->
      <div v-if="activeTab === 'orders'" class="content-section">
        <div class="section-header">
          <h3>Active Orders</h3>
          <div class="filters">
            <select v-model="orderFilter" @change="filterOrders">
              <option value="">All Orders</option>
              <option value="buy">Buy Orders</option>
              <option value="sell">Sell Orders</option>
              <option value="limit">Limit Orders</option>
              <option value="market">Market Orders</option>
            </select>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Pair</th>
                <th>Type</th>
                <th>Side</th>
                <th>Amount</th>
                <th>Price</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in filteredOrders" :key="order.id">
                <td>
                  <div class="user-info">
                    <strong>{{ order.user.email }}</strong>
                    <small>ID: {{ order.user.id }}</small>
                  </div>
                </td>
                <td>{{ order.trading_pair }}</td>
                <td>
                  <span class="type-badge" :class="order.order_type">
                    {{ order.order_type }}
                  </span>
                </td>
                <td>
                  <span :class="order.side === 'buy' ? 'positive' : 'negative'">
                    {{ order.side.toUpperCase() }}
                  </span>
                </td>
                <td>{{ order.amount }}</td>
                <td>${{ formatCurrency(order.price) }}</td>
                <td>
                  <span class="status-badge" :class="order.status">
                    {{ order.status }}
                  </span>
                </td>
                <td>{{ formatDate(order.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <button 
                      v-if="order.status === 'open'"
                      @click="cancelOrder(order)" 
                      class="btn btn-danger btn-sm"
                    >
                      Cancel
                    </button>
                    <button @click="viewOrderDetails(order)" class="btn btn-secondary btn-sm">
                      View
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Trading Settings -->
      <div v-if="activeTab === 'settings'" class="content-section">
        <div class="section-header">
          <h3>Trading Settings</h3>
        </div>
        
        <div class="settings-grid">
          <div class="setting-card">
            <h4>Global Trading Control</h4>
            <div class="setting-item">
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="settings.tradingEnabled"
                  @change="updateTradingSetting('trading_enabled', settings.tradingEnabled)"
                />
                <span class="toggle-slider"></span>
              </label>
              <div class="setting-info">
                <strong>Enable Trading</strong>
                <p>Allow users to place new orders</p>
              </div>
            </div>
            
            <div class="setting-item">
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="settings.maintenanceMode"
                  @change="updateTradingSetting('maintenance_mode', settings.maintenanceMode)"
                />
                <span class="toggle-slider"></span>
              </label>
              <div class="setting-info">
                <strong>Maintenance Mode</strong>
                <p>Suspend all trading activities</p>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <h4>Order Limits</h4>
            <div class="setting-item">
              <input 
                type="number" 
                v-model="settings.maxOrderSize"
                @change="updateTradingSetting('max_order_size', settings.maxOrderSize)"
                class="setting-input"
              />
              <div class="setting-info">
                <strong>Maximum Order Size (USD)</strong>
                <p>Maximum value per single order</p>
              </div>
            </div>
            
            <div class="setting-item">
              <input 
                type="number" 
                v-model="settings.minOrderSize"
                @change="updateTradingSetting('min_order_size', settings.minOrderSize)"
                class="setting-input"
              />
              <div class="setting-info">
                <strong>Minimum Order Size (USD)</strong>
                <p>Minimum value per single order</p>
              </div>
            </div>
          </div>

          <div class="setting-card">
            <h4>Trading Fees</h4>
            <div class="setting-item">
              <input 
                type="number" 
                step="0.001"
                v-model="settings.makerFee"
                @change="updateTradingSetting('maker_fee', settings.makerFee)"
                class="setting-input"
              />
              <div class="setting-info">
                <strong>Maker Fee (%)</strong>
                <p>Fee for limit orders that add liquidity</p>
              </div>
            </div>
            
            <div class="setting-item">
              <input 
                type="number" 
                step="0.001"
                v-model="settings.takerFee"
                @change="updateTradingSetting('taker_fee', settings.takerFee)"
                class="setting-input"
              />
              <div class="setting-info">
                <strong>Taker Fee (%)</strong>
                <p>Fee for market orders that remove liquidity</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/services/api'

const loading = ref(false)
const activeTab = ref('pairs')
const orderFilter = ref('')

const stats = reactive({
  activePairs: 12,
  totalPairs: 15,
  openOrders: 247,
  ordersToday: 89,
  volume24h: 2450000,
  volumeChange: 15.7,
  tradingEnabled: true
})

const settings = reactive({
  tradingEnabled: true,
  maintenanceMode: false,
  maxOrderSize: 100000,
  minOrderSize: 10,
  makerFee: 0.1,
  takerFee: 0.15
})

const tabs = computed(() => [
  { id: 'pairs', label: 'Trading Pairs', icon: 'icon-chart', count: stats.activePairs },
  { id: 'orders', label: 'Active Orders', icon: 'icon-list', count: stats.openOrders },
  { id: 'settings', label: 'Settings', icon: 'icon-settings' }
])

const tradingPairs = ref([
  {
    id: 'BTC-USD',
    symbol: 'BTC/USD',
    base_currency: 'BTC',
    quote_currency: 'USD',
    current_price: 43250.50,
    price_change_24h: 2.45,
    volume_24h: 1250000,
    is_active: true
  },
  {
    id: 'ETH-USD',
    symbol: 'ETH/USD',
    base_currency: 'ETH',
    quote_currency: 'USD',
    current_price: 2650.75,
    price_change_24h: -1.23,
    volume_24h: 850000,
    is_active: true
  }
])

const orders = ref([
  {
    id: 1,
    user: { id: 1, email: 'user1@example.com' },
    trading_pair: 'BTC/USD',
    order_type: 'limit',
    side: 'buy',
    amount: 0.5,
    price: 43000,
    status: 'open',
    created_at: new Date().toISOString()
  }
])

const filteredOrders = computed(() => {
  if (!orderFilter.value) return orders.value
  return orders.value.filter(order => {
    if (orderFilter.value === 'buy' || orderFilter.value === 'sell') {
      return order.side === orderFilter.value
    }
    if (orderFilter.value === 'limit' || orderFilter.value === 'market') {
      return order.order_type === orderFilter.value
    }
    return true
  })
})

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const refreshData = async () => {
  loading.value = true
  try {
    // Load trading data from API
    console.log('Refreshing trading data...')
  } finally {
    loading.value = false
  }
}

const emergencyStop = async () => {
  if (confirm('Are you sure you want to stop all trading activities? This will cancel all open orders.')) {
    try {
      console.log('Emergency stop activated')
      settings.tradingEnabled = false
      settings.maintenanceMode = true
    } catch (error) {
      console.error('Failed to activate emergency stop:', error)
    }
  }
}

const togglePairStatus = async (pair: any) => {
  try {
    pair.is_active = !pair.is_active
    console.log(`${pair.is_active ? 'Enabled' : 'Disabled'} trading pair:`, pair.symbol)
  } catch (error) {
    console.error('Failed to toggle pair status:', error)
  }
}

const addTradingPair = () => {
  console.log('Add new trading pair')
}

const editPair = (pair: any) => {
  console.log('Edit trading pair:', pair.symbol)
}

const cancelOrder = async (order: any) => {
  if (confirm('Are you sure you want to cancel this order?')) {
    try {
      order.status = 'cancelled'
      console.log('Order cancelled:', order.id)
    } catch (error) {
      console.error('Failed to cancel order:', error)
    }
  }
}

const viewOrderDetails = (order: any) => {
  console.log('View order details:', order.id)
}

const filterOrders = () => {
  console.log('Filtering orders by:', orderFilter.value)
}

const updateTradingSetting = async (key: string, value: any) => {
  try {
    console.log(`Updated ${key}:`, value)
    // API call to update setting
  } catch (error) {
    console.error('Failed to update setting:', error)
  }
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.trading-control {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.header-content h2 {
  color: var(--text-primary);
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.header-content p {
  color: var(--text-secondary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: var(--primary-color);
  color: var(--text-dark);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-success {
  background: var(--success-color);
  color: white;
}

.btn-warning {
  background: var(--warning-color);
  color: white;
}

.btn-danger {
  background: var(--error-color);
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: 12px;
}

.stat-content h3 {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.stat-change {
  font-size: 12px;
  color: var(--text-muted);
}

.stat-change.positive {
  color: var(--success-color);
}

.stat-change.negative {
  color: var(--error-color);
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 24px;
}

.tab-button {
  background: none;
  border: none;
  padding: 16px 24px;
  color: var(--text-secondary);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-button:hover {
  color: var(--text-primary);
}

.tab-button.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.tab-count {
  background: var(--primary-color);
  color: var(--text-dark);
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.content-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.section-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.filters select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-weight: 500;
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.data-table td {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
}

.pair-info strong {
  display: block;
  color: var(--text-primary);
}

.pair-info small {
  color: var(--text-secondary);
  font-size: 12px;
}

.user-info strong {
  display: block;
  color: var(--text-primary);
}

.user-info small {
  color: var(--text-secondary);
  font-size: 12px;
}

.price {
  font-weight: 600;
  color: var(--primary-color);
}

.positive {
  color: var(--success-color);
}

.negative {
  color: var(--error-color);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.active, .status-badge.open {
  background: rgba(60, 210, 120, 0.1);
  color: var(--success-color);
}

.status-badge.inactive, .status-badge.cancelled {
  background: rgba(207, 49, 39, 0.1);
  color: var(--error-color);
}

.type-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.type-badge.limit {
  background: var(--secondary-color);
  color: white;
}

.type-badge.market {
  background: var(--warning-color);
  color: white;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  padding: 24px;
}

.setting-card {
  background: var(--bg-tertiary);
  border-radius: 8px;
  padding: 20px;
}

.setting-card h4 {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.setting-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.setting-info strong {
  display: block;
  color: var(--text-primary);
  font-size: 14px;
  margin-bottom: 4px;
}

.setting-info p {
  color: var(--text-secondary);
  font-size: 12px;
  margin: 0;
}

.setting-input {
  width: 120px;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--border-color);
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

/* Icons */
.icon-refresh::before { content: '🔄'; }
.icon-stop::before { content: '⏹️'; }
.icon-plus::before { content: '➕'; }
.icon-chart::before { content: '📈'; }
.icon-list::before { content: '📋'; }
.icon-settings::before { content: '⚙️'; }
</style>
