<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Crypto Investments</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button @click="showCreateModal = true" class="btn-primary">
              New Investment
            </button>
            <router-link to="/dashboard" class="btn-secondary">Dashboard</router-link>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Portfolio Overview -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
        <div class="card">
          <div class="text-center">
            <p class="text-sm text-gray-600">Total Portfolio Value</p>
            <p class="text-2xl font-bold text-green-600">{{ formatBTC(totalPortfolioValue) }} BTC</p>
          </div>
        </div>
        <div class="card">
          <div class="text-center">
            <p class="text-sm text-gray-600">Total P&L</p>
            <p class="text-2xl font-bold" :class="totalPnl >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ formatBTC(totalPnl) }} BTC
            </p>
          </div>
        </div>
        <div class="card">
          <div class="text-center">
            <p class="text-sm text-gray-600">Total Return</p>
            <p class="text-2xl font-bold" :class="totalReturnPercent >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ formatPercent(totalReturnPercent) }}%
            </p>
          </div>
        </div>
        <div class="card">
          <div class="text-center">
            <p class="text-sm text-gray-600">Active Investments</p>
            <p class="text-2xl font-bold text-blue-600">{{ activeInvestmentsCount }}</p>
          </div>
        </div>
      </div>

      <!-- Investments Table -->
      <div class="card mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-medium text-gray-900">Your Investments</h2>
          <button @click="refreshInvestments" class="btn-secondary text-sm">
            Refresh
          </button>
        </div>

        <div v-if="loading" class="text-center py-8">
          <p class="text-gray-500">Loading investments...</p>
        </div>

        <div v-else-if="investments.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Investment</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invested</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Value</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">P&L</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Return</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="investment in investments" :key="investment.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ investment.name }}</div>
                    <div class="text-sm text-gray-500">{{ investment.investment_target_name }}</div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                    {{ investment.investment_type }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatBTC(investment.total_invested_btc) }} BTC
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatBTC(investment.current_value_btc) }} BTC
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm" :class="investment.is_profitable ? 'text-green-600' : 'text-red-600'">
                  {{ formatBTC(investment.unrealized_pnl_btc) }} BTC
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm" :class="investment.is_profitable ? 'text-green-600' : 'text-red-600'">
                  {{ formatPercent(investment.total_return_percent) }}%
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                        :class="getStatusClass(investment.status)">
                    {{ investment.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex space-x-2">
                    <button @click="viewInvestment(investment)" class="text-indigo-600 hover:text-indigo-900">View</button>
                    <button @click="addFunds(investment)" class="text-green-600 hover:text-green-900">Add Funds</button>
                    <button @click="withdrawFunds(investment)" class="text-red-600 hover:text-red-900">Withdraw</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-8">
          <p class="text-gray-500">No investments found</p>
          <button @click="showCreateModal = true" class="btn-primary mt-4">
            Create Your First Investment
          </button>
        </div>
      </div>

      <!-- Available Crypto Indices -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-medium text-gray-900">Available Crypto Indices</h2>
          <button @click="refreshIndices" class="btn-secondary text-sm">
            Refresh
          </button>
        </div>

        <div v-if="indices.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="index in indices" :key="index.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-medium text-gray-900">{{ index.name }}</h3>
              <span class="text-sm text-gray-500">{{ index.symbol }}</span>
            </div>
            <p class="text-sm text-gray-600 mb-2">{{ index.description }}</p>
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm text-gray-500">{{ index.total_components }} assets</span>
              <span class="text-sm font-medium" :class="index.price_change_24h >= 0 ? 'text-green-600' : 'text-red-600'">
                {{ formatPercent(index.price_change_24h) }}%
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Min: {{ formatBTC(index.minimum_investment) }} BTC</span>
              <button @click="investInIndex(index)" class="btn-primary text-sm">
                Invest
              </button>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <p class="text-gray-500">No indices available</p>
        </div>
      </div>
    </div>

    <!-- Create Investment Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Create New Investment</h3>
          
          <form @submit.prevent="createInvestment" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Investment Name</label>
              <input
                v-model="createForm.name"
                type="text"
                class="input-field"
                placeholder="My Bitcoin Investment"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Investment Type</label>
              <select v-model="createForm.investment_type" class="input-field" required>
                <option value="index">Crypto Index</option>
                <option value="single_crypto">Single Cryptocurrency</option>
                <option value="dca">Dollar Cost Averaging</option>
                <option value="hodl">Long-term Hold</option>
              </select>
            </div>

            <div v-if="createForm.investment_type === 'index'">
              <label class="block text-sm font-medium text-gray-700">Select Index</label>
              <select v-model="createForm.crypto_index_id" class="input-field" required>
                <option value="">Choose an index...</option>
                <option v-for="index in indices" :key="index.id" :value="index.id">
                  {{ index.name }} ({{ index.symbol }})
                </option>
              </select>
            </div>

            <div v-if="createForm.investment_type === 'single_crypto'">
              <label class="block text-sm font-medium text-gray-700">Select Cryptocurrency</label>
              <select v-model="createForm.cryptocurrency_id" class="input-field" required>
                <option value="">Choose a cryptocurrency...</option>
                <option v-for="crypto in availableCryptos" :key="crypto.id" :value="crypto.id">
                  {{ crypto.name }} ({{ crypto.symbol }})
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Initial Investment (BTC)</label>
              <input
                v-model.number="createForm.initial_investment_btc"
                type="number"
                step="0.00000001"
                min="0.001"
                class="input-field"
                placeholder="0.01"
                required
              />
            </div>

            <div v-if="createForm.investment_type === 'dca'">
              <label class="block text-sm font-medium text-gray-700">DCA Amount (BTC)</label>
              <input
                v-model.number="createForm.dca_amount_btc"
                type="number"
                step="0.00000001"
                min="0.001"
                class="input-field"
                placeholder="0.001"
              />
            </div>

            <div v-if="createForm.investment_type === 'dca'">
              <label class="block text-sm font-medium text-gray-700">DCA Frequency</label>
              <select v-model="createForm.dca_frequency" class="input-field">
                <option value="">Select frequency...</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>

            <div class="flex items-center">
              <input
                v-model="createForm.auto_compound"
                type="checkbox"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label class="ml-2 block text-sm text-gray-900">Auto-compound gains</label>
            </div>
            
            <div class="flex space-x-2">
              <button type="button" @click="showCreateModal = false" class="btn-secondary flex-1">
                Cancel
              </button>
              <button type="submit" :disabled="creating" class="btn-primary flex-1">
                <span v-if="creating">Creating...</span>
                <span v-else>Create Investment</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Transaction Modal -->
    <div v-if="showTransactionModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ transactionType === 'deposit' ? 'Add Funds' : 'Withdraw Funds' }}
          </h3>
          
          <form @submit.prevent="executeTransaction" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Amount (BTC)</label>
              <input
                v-model.number="transactionForm.amount_btc"
                type="number"
                step="0.00000001"
                min="0.00000001"
                class="input-field"
                placeholder="0.001"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Notes (Optional)</label>
              <textarea
                v-model="transactionForm.notes"
                class="input-field"
                rows="3"
                placeholder="Transaction notes..."
              ></textarea>
            </div>
            
            <div class="flex space-x-2">
              <button type="button" @click="showTransactionModal = false" class="btn-secondary flex-1">
                Cancel
              </button>
              <button type="submit" :disabled="processingTransaction" class="btn-primary flex-1">
                <span v-if="processingTransaction">Processing...</span>
                <span v-else>{{ transactionType === 'deposit' ? 'Add Funds' : 'Withdraw' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { api } from '@/src/services/api'

const toast = useToast()

// Reactive state
const investments = ref([])
const indices = ref([])
const availableCryptos = ref([])
const loading = ref(false)
const creating = ref(false)
const processingTransaction = ref(false)
const showCreateModal = ref(false)
const showTransactionModal = ref(false)
const transactionType = ref('deposit')
const selectedInvestment = ref(null)

// Forms
const createForm = reactive({
  name: '',
  investment_type: 'index',
  crypto_index_id: null,
  cryptocurrency_id: null,
  initial_investment_btc: 0.01,
  auto_compound: false,
  dca_amount_btc: null,
  dca_frequency: ''
})

const transactionForm = reactive({
  amount_btc: 0,
  notes: ''
})

// Computed properties
const totalPortfolioValue = computed(() => {
  return investments.value.reduce((sum, inv) => sum + parseFloat(inv.current_value_btc || 0), 0)
})

const totalPnl = computed(() => {
  return investments.value.reduce((sum, inv) => sum + parseFloat(inv.unrealized_pnl_btc || 0), 0)
})

const totalReturnPercent = computed(() => {
  const totalInvested = investments.value.reduce((sum, inv) => sum + parseFloat(inv.total_invested_btc || 0), 0)
  return totalInvested > 0 ? (totalPnl.value / totalInvested) * 100 : 0
})

const activeInvestmentsCount = computed(() => {
  return investments.value.filter(inv => inv.status === 'active').length
})

// Methods
const formatBTC = (value) => {
  return parseFloat(value || 0).toFixed(8)
}

const formatPercent = (value) => {
  return parseFloat(value || 0).toFixed(2)
}

const getStatusClass = (status) => {
  switch (status) {
    case 'active':
      return 'bg-green-100 text-green-800'
    case 'paused':
      return 'bg-yellow-100 text-yellow-800'
    case 'closed':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const refreshInvestments = async () => {
  loading.value = true
  try {
    const response = await api.get('/trades/investments/')
    investments.value = response.data
  } catch (error) {
    toast.showToast('Failed to load investments', 'error')
    console.error('Error loading investments:', error)
  } finally {
    loading.value = false
  }
}

const refreshIndices = async () => {
  try {
    const response = await api.get('/trades/crypto-indices/')
    indices.value = response.data
  } catch (error) {
    toast.showToast('Failed to load indices', 'error')
    console.error('Error loading indices:', error)
  }
}

const loadAvailableCryptos = async () => {
  try {
    const response = await api.trades.getCryptocurrencies()
    availableCryptos.value = response.data
  } catch (error) {
    console.error('Error loading cryptocurrencies:', error)
  }
}

const createInvestment = async () => {
  creating.value = true
  try {
    const response = await api.post('/trades/investments/', createForm)
    toast.showToast('Investment created successfully!', 'success')
    showCreateModal.value = false
    resetCreateForm()
    await refreshInvestments()
  } catch (error) {
    toast.showToast('Failed to create investment', 'error')
    console.error('Error creating investment:', error)
  } finally {
    creating.value = false
  }
}

const resetCreateForm = () => {
  Object.assign(createForm, {
    name: '',
    investment_type: 'index',
    crypto_index_id: null,
    cryptocurrency_id: null,
    initial_investment_btc: 0.01,
    auto_compound: false,
    dca_amount_btc: null,
    dca_frequency: ''
  })
}

const investInIndex = (index) => {
  createForm.investment_type = 'index'
  createForm.crypto_index_id = index.id
  createForm.name = `${index.name} Investment`
  createForm.initial_investment_btc = parseFloat(index.minimum_investment)
  showCreateModal.value = true
}

const viewInvestment = (investment) => {
  // Navigate to investment detail view or show modal
  window.location.href = `/investments/${investment.id}`
}

const addFunds = (investment) => {
  selectedInvestment.value = investment
  transactionType.value = 'deposit'
  transactionForm.amount_btc = 0.001
  transactionForm.notes = ''
  showTransactionModal.value = true
}

const withdrawFunds = (investment) => {
  selectedInvestment.value = investment
  transactionType.value = 'withdraw'
  transactionForm.amount_btc = 0.001
  transactionForm.notes = ''
  showTransactionModal.value = true
}

const executeTransaction = async () => {
  if (!selectedInvestment.value) return
  
  processingTransaction.value = true
  try {
    const endpoint = transactionType.value === 'deposit' 
      ? `/trades/investments/${selectedInvestment.value.id}/add-funds/`
      : `/trades/investments/${selectedInvestment.value.id}/withdraw/`
    
    const data = {
      transaction_type: transactionType.value,
      amount_btc: transactionForm.amount_btc,
      notes: transactionForm.notes
    }
    
    const response = await api.post(endpoint, data)
    toast.showToast(response.data.message, 'success')
    showTransactionModal.value = false
    await refreshInvestments()
  } catch (error) {
    toast.showToast(`Failed to ${transactionType.value} funds`, 'error')
    console.error(`Error ${transactionType.value}ing funds:`, error)
  } finally {
    processingTransaction.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    refreshInvestments(),
    refreshIndices(),
    loadAvailableCryptos()
  ])
})
</script>