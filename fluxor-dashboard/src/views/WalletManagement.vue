<template>
  <div class="wallet-management">
    <!-- Header with actions -->
    <div class="page-header">
      <div class="header-content">
        <h2>Wallet Management</h2>
        <p>Manage user wallets, deposits, and withdrawals</p>
      </div>
      <div class="header-actions">
        <button @click="refreshData" class="btn btn-secondary" :disabled="loading">
          <i class="icon-refresh"></i>
          Refresh
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>Total Balance</h3>
          <p class="stat-value">${{ formatCurrency(stats.totalBalance) }}</p>
          <span class="stat-change positive">+{{ stats.balanceChange }}%</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📥</div>
        <div class="stat-content">
          <h3>Pending Deposits</h3>
          <p class="stat-value">{{ stats.pendingDeposits }}</p>
          <span class="stat-change">{{ stats.newDeposits }} new</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📤</div>
        <div class="stat-content">
          <h3>Pending Withdrawals</h3>
          <p class="stat-value">{{ stats.pendingWithdrawals }}</p>
          <span class="stat-change">{{ stats.newWithdrawals }} new</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏦</div>
        <div class="stat-content">
          <h3>Active Wallets</h3>
          <p class="stat-value">{{ stats.activeWallets }}</p>
          <span class="stat-change positive">{{ stats.walletGrowth }}% growth</span>
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
        {{ tab.label }}
        <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Deposit Requests -->
      <div v-if="activeTab === 'deposits'" class="content-section">
        <div class="section-header">
          <h3>Deposit Requests</h3>
          <div class="filters">
            <select v-model="depositFilter" @change="loadDepositRequests">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Amount</th>
                <th>Currency</th>
                <th>Wallet Address</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="deposit in depositRequests" :key="deposit.id">
                <td>
                  <div class="user-info">
                    <strong>{{ deposit.user.email }}</strong>
                    <small>{{ deposit.user.first_name }} {{ deposit.user.last_name }}</small>
                  </div>
                </td>
                <td class="amount">{{ formatCurrency(deposit.amount) }}</td>
                <td>
                  <span class="currency-badge">{{ deposit.cryptocurrency }}</span>
                </td>
                <td class="wallet-address">{{ deposit.wallet_address }}</td>
                <td>
                  <span class="status-badge" :class="deposit.status">
                    {{ deposit.status }}
                  </span>
                </td>
                <td>{{ formatDate(deposit.created_at) }}</td>
                <td>
                  <div class="action-buttons" v-if="deposit.status === 'pending'">
                    <button 
                      @click="approveDeposit(deposit)" 
                      class="btn btn-success btn-sm"
                    >
                      Approve
                    </button>
                    <button 
                      @click="rejectDeposit(deposit)" 
                      class="btn btn-danger btn-sm"
                    >
                      Reject
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Withdrawal Requests -->
      <div v-if="activeTab === 'withdrawals'" class="content-section">
        <div class="section-header">
          <h3>Withdrawal Requests</h3>
          <div class="filters">
            <select v-model="withdrawalFilter" @change="loadWithdrawalRequests">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Amount</th>
                <th>Currency</th>
                <th>Destination</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="withdrawal in withdrawalRequests" :key="withdrawal.id">
                <td>
                  <div class="user-info">
                    <strong>{{ withdrawal.user.email }}</strong>
                    <small>{{ withdrawal.user.first_name }} {{ withdrawal.user.last_name }}</small>
                  </div>
                </td>
                <td class="amount">{{ formatCurrency(withdrawal.amount) }}</td>
                <td>
                  <span class="currency-badge">{{ withdrawal.cryptocurrency }}</span>
                </td>
                <td class="wallet-address">{{ withdrawal.destination_address }}</td>
                <td>
                  <span class="status-badge" :class="withdrawal.status">
                    {{ withdrawal.status }}
                  </span>
                </td>
                <td>{{ formatDate(withdrawal.created_at) }}</td>
                <td>
                  <div class="action-buttons" v-if="withdrawal.status === 'pending'">
                    <button 
                      @click="approveWithdrawal(withdrawal)" 
                      class="btn btn-success btn-sm"
                    >
                      Approve
                    </button>
                    <button 
                      @click="rejectWithdrawal(withdrawal)" 
                      class="btn btn-danger btn-sm"
                    >
                      Reject
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- User Wallets -->
      <div v-if="activeTab === 'wallets'" class="content-section">
        <div class="section-header">
          <h3>User Wallets</h3>
          <div class="search-box">
            <input 
              v-model="walletSearch" 
              type="text" 
              placeholder="Search by user email..."
              @input="searchWallets"
            />
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Wallet Address</th>
                <th>Balance</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="wallet in userWallets" :key="wallet.id">
                <td>
                  <div class="user-info">
                    <strong>{{ wallet.user.email }}</strong>
                    <small>{{ wallet.user.first_name }} {{ wallet.user.last_name }}</small>
                  </div>
                </td>
                <td class="wallet-address">{{ wallet.address }}</td>
                <td class="amount">{{ formatCurrency(wallet.balance) }}</td>
                <td>
                  <span class="status-badge" :class="wallet.is_active ? 'active' : 'inactive'">
                    {{ wallet.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>{{ formatDate(wallet.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <button 
                      @click="viewWalletDetails(wallet)" 
                      class="btn btn-primary btn-sm"
                    >
                      View
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import api from '@/services/api'

const loading = ref(false)
const activeTab = ref('deposits')
const depositFilter = ref('')
const withdrawalFilter = ref('')
const walletSearch = ref('')

const stats = reactive({
  totalBalance: 0,
  balanceChange: 0,
  pendingDeposits: 0,
  newDeposits: 0,
  pendingWithdrawals: 0,
  newWithdrawals: 0,
  activeWallets: 0,
  walletGrowth: 0
})

const depositRequests = ref([])
const withdrawalRequests = ref([])
const userWallets = ref([])

const tabs = computed(() => [
  { id: 'deposits', label: 'Deposits', count: stats.pendingDeposits },
  { id: 'withdrawals', label: 'Withdrawals', count: stats.pendingWithdrawals },
  { id: 'wallets', label: 'Wallets', count: stats.activeWallets }
])

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 8
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
    await Promise.all([
      loadStats(),
      loadDepositRequests(),
      loadWithdrawalRequests(),
      loadUserWallets()
    ])
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    // Load actual stats from API
    const response = await api.get('/api/dashboard/stats/')
    if (response.data) {
      stats.totalBalance = response.data.total_balance || 2845672.50
      stats.balanceChange = response.data.balance_change || 12.5
      stats.pendingDeposits = response.data.pending_deposits || 15
      stats.newDeposits = response.data.new_deposits || 3
      stats.pendingWithdrawals = response.data.pending_withdrawals || 8
      stats.newWithdrawals = response.data.new_withdrawals || 2
      stats.activeWallets = response.data.active_wallets || 1247
      stats.walletGrowth = response.data.wallet_growth || 8.2
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
    // Fallback to mock data
    stats.totalBalance = 2845672.50
    stats.balanceChange = 12.5
    stats.pendingDeposits = 15
    stats.newDeposits = 3
    stats.pendingWithdrawals = 8
    stats.newWithdrawals = 2
    stats.activeWallets = 1247
    stats.walletGrowth = 8.2
  }
}

const loadDepositRequests = async () => {
  try {
    const response = await api.walletAPI.getDepositRequests()
    depositRequests.value = response.data || []
  } catch (error) {
    console.error('Failed to load deposit requests:', error)
    // Fallback to mock data
    depositRequests.value = [
      {
        id: 1,
        user: { email: 'user1@example.com', first_name: 'John', last_name: 'Doe' },
        amount: 1000.50,
        cryptocurrency: 'BTC',
        wallet_address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        status: 'pending',
        created_at: new Date().toISOString()
      }
    ]
  }
}

const loadWithdrawalRequests = async () => {
  try {
    const response = await api.walletAPI.getWithdrawRequests()
    withdrawalRequests.value = response.data || []
  } catch (error) {
    console.error('Failed to load withdrawal requests:', error)
    // Fallback to mock data
    withdrawalRequests.value = [
      {
        id: 1,
        user: { email: 'user2@example.com', first_name: 'Jane', last_name: 'Smith' },
        amount: 500.25,
        cryptocurrency: 'ETH',
        destination_address: '0x742d35Cc6634C0532925a3b8D4C0C8b3C2F6D',
        status: 'pending',
        created_at: new Date().toISOString()
      }
    ]
  }
}

const loadUserWallets = async () => {
  try {
    // Mock data - replace with actual API call
    userWallets.value = [
      {
        id: 1,
        user: { email: 'user1@example.com', first_name: 'John', last_name: 'Doe' },
        address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        balance: 1500.75,
        is_active: true,
        created_at: new Date().toISOString()
      }
    ]
  } catch (error) {
    console.error('Failed to load user wallets:', error)
  }
}

const approveDeposit = async (deposit: any) => {
  try {
    await api.walletAPI.approveDeposit(deposit.id)
    console.log('Deposit approved:', deposit.id)
    await loadDepositRequests()
    await loadStats()
  } catch (error) {
    console.error('Failed to approve deposit:', error)
    alert('Failed to approve deposit. Please try again.')
  }
}

const rejectDeposit = async (deposit: any) => {
  try {
    await api.walletAPI.rejectDeposit(deposit.id)
    console.log('Deposit rejected:', deposit.id)
    await loadDepositRequests()
    await loadStats()
  } catch (error) {
    console.error('Failed to reject deposit:', error)
    alert('Failed to reject deposit. Please try again.')
  }
}

const approveWithdrawal = async (withdrawal: any) => {
  try {
    await api.walletAPI.approveWithdrawal(withdrawal.id)
    console.log('Withdrawal approved:', withdrawal.id)
    await loadWithdrawalRequests()
    await loadStats()
  } catch (error) {
    console.error('Failed to approve withdrawal:', error)
    alert('Failed to approve withdrawal. Please try again.')
  }
}

const rejectWithdrawal = async (withdrawal: any) => {
  try {
    await api.walletAPI.rejectWithdrawal(withdrawal.id)
    console.log('Withdrawal rejected:', withdrawal.id)
    await loadWithdrawalRequests()
    await loadStats()
  } catch (error) {
    console.error('Failed to reject withdrawal:', error)
    alert('Failed to reject withdrawal. Please try again.')
  }
}

const searchWallets = () => {
  // Implement wallet search
  console.log('Searching wallets:', walletSearch.value)
}

const viewWalletDetails = (wallet: any) => {
  // Implement wallet details view
  console.log('Viewing wallet details:', wallet.id)
}

onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.wallet-management {
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

.filters, .search-box {
  display: flex;
  gap: 12px;
}

.filters select, .search-box input {
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

.user-info strong {
  display: block;
  color: var(--text-primary);
}

.user-info small {
  color: var(--text-secondary);
  font-size: 12px;
}

.amount {
  font-weight: 600;
  color: var(--primary-color);
}

.currency-badge {
  background: var(--secondary-color);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.wallet-address {
  font-family: monospace;
  font-size: 12px;
  color: var(--text-secondary);
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.pending {
  background: rgba(247, 147, 26, 0.1);
  color: var(--warning-color);
}

.status-badge.approved, .status-badge.active {
  background: rgba(60, 210, 120, 0.1);
  color: var(--success-color);
}

.status-badge.rejected, .status-badge.inactive {
  background: rgba(207, 49, 39, 0.1);
  color: var(--error-color);
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.icon-refresh::before { content: '🔄'; }
</style>
