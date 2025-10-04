<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Trading Control Panel</h1>
        <p class="text-sm text-gray-600">Manage trade outcomes and confirm payments</p>
      </div>
      <div class="flex space-x-3">
        <button @click="refreshData" :disabled="loading" class="btn-secondary">
          <span v-if="loading">Refreshing...</span>
          <span v-else>🔄 Refresh</span>
        </button>
        <button @click="showOutcomeModal = true" class="btn-primary">
          ⚡ Set Trade Outcome
        </button>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">⏱️</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Active Trades</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.activeTrades }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-warning-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">💰</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Pending Payments</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.pendingPayments }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-success-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">📈</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Controlled Outcomes</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.controlledOutcomes }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-danger-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm">📊</span>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Success Rate</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.successRate }}%</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Pending Payments -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900 flex items-center">
            💰 Pending Payments
            <span class="ml-2 badge-warning">{{ pendingPayments.length }}</span>
          </h3>
        </div>
        <div class="card-body p-0">
          <div class="max-h-96 overflow-y-auto">
            <div v-if="pendingPayments.length === 0" class="text-center py-8 text-gray-500">
              No pending payments
            </div>
            <div v-else class="divide-y divide-gray-200">
              <div v-for="payment in pendingPayments" :key="payment.id" 
                   class="p-4 hover:bg-gray-50 transition-colors">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="flex items-center space-x-2">
                      <span class="font-medium text-gray-900">{{ payment.username }}</span>
                      <span :class="payment.type === 'withdrawal' ? 'badge-danger' : 'badge-success'">
                        {{ payment.type }}
                      </span>
                    </div>
                    <p class="text-sm text-gray-600 mt-1">
                      Amount: <span class="font-medium">${{ formatCurrency(payment.amount) }}</span>
                    </p>
                    <p class="text-xs text-gray-400 mt-1">
                      {{ formatTimeAgo(payment.createdAt) }}
                    </p>
                  </div>
                  <div class="flex space-x-2">
                    <button @click="confirmPayment(payment.id, 'approve')" 
                            class="text-success-600 hover:text-success-800 text-sm font-medium">
                      ✅ Approve
                    </button>
                    <button @click="confirmPayment(payment.id, 'reject')" 
                            class="text-danger-600 hover:text-danger-800 text-sm font-medium">
                      ❌ Reject
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Trade Outcomes -->
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900 flex items-center">
            ⚡ Active Trade Outcomes
            <span class="ml-2 badge-primary">{{ activeOutcomes.length }}</span>
          </h3>
        </div>
        <div class="card-body p-0">
          <div class="max-h-96 overflow-y-auto">
            <div v-if="activeOutcomes.length === 0" class="text-center py-8 text-gray-500">
              No active outcomes set
            </div>
            <div v-else class="divide-y divide-gray-200">
              <div v-for="outcome in activeOutcomes" :key="outcome.id" 
                   class="p-4 hover:bg-gray-50 transition-colors">
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="flex items-center space-x-2">
                      <span class="font-medium text-gray-900">{{ outcome.pair }}</span>
                      <span :class="outcome.outcome === 'profit' ? 'badge-success' : 'badge-danger'">
                        {{ outcome.outcome === 'profit' ? '+' : '-' }}{{ outcome.percentage }}%
                      </span>
                    </div>
                    <p class="text-sm text-gray-600 mt-1">
                      Duration: <span class="font-medium">{{ formatDuration(outcome.duration, outcome.durationUnit) }}</span>
                    </p>
                    <p class="text-xs text-gray-400 mt-1">
                      Expires: {{ formatTimeRemaining(outcome.expiresAt) }}
                    </p>
                  </div>
                  <div class="flex space-x-2">
                    <button @click="editOutcome(outcome)" 
                            class="text-primary-600 hover:text-primary-800 text-sm font-medium">
                      ✏️ Edit
                    </button>
                    <button @click="cancelOutcome(outcome.id)" 
                            class="text-danger-600 hover:text-danger-800 text-sm font-medium">
                      🗑️ Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Trade Results -->
    <div class="card">
      <div class="card-header">
        <h3 class="text-lg font-medium text-gray-900">📊 Recent Trade Results</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="table">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-header">Time</th>
              <th class="table-header">Trader</th>
              <th class="table-header">Pair</th>
              <th class="table-header">Amount</th>
              <th class="table-header">Controlled Outcome</th>
              <th class="table-header">Actual Market</th>
              <th class="table-header">Result</th>
              <th class="table-header">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="trade in recentTrades" :key="trade.id" class="hover:bg-gray-50">
              <td class="table-cell">{{ formatTime(trade.timestamp) }}</td>
              <td class="table-cell">{{ trade.username }}</td>
              <td class="table-cell font-medium">{{ trade.pair }}</td>
              <td class="table-cell">${{ formatCurrency(trade.amount) }}</td>
              <td class="table-cell">
                <span :class="trade.controlledOutcome > 0 ? 'text-success-600' : 'text-danger-600'">
                  {{ trade.controlledOutcome > 0 ? '+' : '' }}{{ trade.controlledOutcome }}%
                </span>
              </td>
              <td class="table-cell">
                <span :class="trade.marketOutcome > 0 ? 'text-success-600' : 'text-danger-600'">
                  {{ trade.marketOutcome > 0 ? '+' : '' }}{{ trade.marketOutcome }}%
                </span>
              </td>
              <td class="table-cell">
                <span :class="trade.result === 'profit' ? 'text-success-600' : 'text-danger-600'">
                  {{ trade.result === 'profit' ? '+' : '-' }}${{ formatCurrency(Math.abs(trade.pnl)) }}
                </span>
              </td>
              <td class="table-cell">
                <span :class="trade.status === 'completed' ? 'badge-success' : trade.status === 'pending' ? 'badge-warning' : 'badge-danger'">
                  {{ trade.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Set Trade Outcome Modal -->
    <div v-if="showOutcomeModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 border max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingOutcome ? 'Edit Trade Outcome' : 'Set New Trade Outcome' }}
          </h3>
          
          <form @submit.prevent="saveOutcome" class="space-y-4">
            <!-- Trading Pair -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Trading Pair</label>
                <select v-model="outcomeForm.pair" class="input-field" required>
                  <option value="">Select Pair</option>
                  <option v-for="pair in availablePairs" :key="pair" :value="pair">
                    {{ pair }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Outcome Type</label>
                <select v-model="outcomeForm.outcome" class="input-field" required>
                  <option value="profit">Profit 📈</option>
                  <option value="loss">Loss 📉</option>
                </select>
              </div>
            </div>

            <!-- Percentage and Duration -->
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Percentage</label>
                <input v-model.number="outcomeForm.percentage" type="number" min="1" max="1000" 
                       class="input-field" placeholder="100" required>
                <p class="text-xs text-gray-500 mt-1">1% - 1000%</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Duration</label>
                <input v-model.number="outcomeForm.duration" type="number" min="1" 
                       class="input-field" placeholder="40" required>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Time Unit</label>
                <select v-model="outcomeForm.durationUnit" class="input-field" required>
                  <option value="seconds">Seconds</option>
                  <option value="minutes">Minutes</option>
                  <option value="hours">Hours</option>
                  <option value="days">Days</option>
                  <option value="months">Months</option>
                </select>
              </div>
            </div>

            <!-- Target Users -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Apply To</label>
              <select v-model="outcomeForm.target" class="input-field" required>
                <option value="all">All Users</option>
                <option value="new">New Users Only</option>
                <option value="specific">Specific User</option>
                <option value="vip">VIP Users</option>
              </select>
            </div>

            <!-- Specific User (if selected) -->
            <div v-if="outcomeForm.target === 'specific'">
              <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input v-model="outcomeForm.username" type="text" class="input-field" 
                     placeholder="Enter username" required>
            </div>

            <!-- Priority -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Priority Level</label>
              <select v-model="outcomeForm.priority" class="input-field">
                <option value="low">Low - Apply if no other rules</option>
                <option value="medium">Medium - Standard priority</option>
                <option value="high">High - Override other rules</option>
              </select>
            </div>

            <!-- Preview -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Preview</h4>
              <p class="text-sm text-gray-600">
                In the next <strong>{{ outcomeForm.duration }} {{ outcomeForm.durationUnit }}</strong>, 
                trades on <strong>{{ outcomeForm.pair || 'selected pair' }}</strong> will have a 
                <strong :class="outcomeForm.outcome === 'profit' ? 'text-success-600' : 'text-danger-600'">
                  {{ outcomeForm.percentage }}% {{ outcomeForm.outcome }}
                </strong>
                for <strong>{{ getTargetDescription(outcomeForm.target) }}</strong>.
              </p>
            </div>
            
            <div class="flex space-x-2">
              <button type="button" @click="cancelOutcomeEdit" class="btn-secondary flex-1">
                Cancel
              </button>
              <button type="submit" :disabled="saving" class="btn-primary flex-1">
                <span v-if="saving">Setting...</span>
                <span v-else>{{ editingOutcome ? 'Update' : 'Set Outcome' }}</span>
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
import { formatDistanceToNow } from 'date-fns'

// State
const loading = ref(false)
const saving = ref(false)
const showOutcomeModal = ref(false)
const editingOutcome = ref<any>(null)

// Sample data
const stats = ref({
  activeTrades: 127,
  pendingPayments: 8,
  controlledOutcomes: 3,
  successRate: 94.2
})

const pendingPayments = ref([
  {
    id: 1,
    username: 'john_trader',
    type: 'withdrawal',
    amount: 2500.00,
    createdAt: new Date(Date.now() - 300000)
  },
  {
    id: 2,
    username: 'crypto_emma',
    type: 'deposit',
    amount: 1000.00,
    createdAt: new Date(Date.now() - 600000)
  },
  {
    id: 3,
    username: 'btc_mike',
    type: 'withdrawal',
    amount: 5000.00,
    createdAt: new Date(Date.now() - 900000)
  }
])

const activeOutcomes = ref([
  {
    id: 1,
    pair: 'BTC/USD',
    outcome: 'profit',
    percentage: 85,
    duration: 2,
    durationUnit: 'minutes',
    expiresAt: new Date(Date.now() + 120000)
  },
  {
    id: 2,
    pair: 'ETH/USD',
    outcome: 'loss',
    percentage: 40,
    duration: 45,
    durationUnit: 'seconds',
    expiresAt: new Date(Date.now() + 45000)
  },
  {
    id: 3,
    pair: 'ADA/USD',
    outcome: 'profit',
    percentage: 120,
    duration: 1,
    durationUnit: 'hours',
    expiresAt: new Date(Date.now() + 3600000)
  }
])

const recentTrades = ref([
  {
    id: 1,
    timestamp: new Date(Date.now() - 300000),
    username: 'alice_trader',
    pair: 'BTC/USD',
    amount: 500.00,
    controlledOutcome: 85,
    marketOutcome: 45.2,
    result: 'profit',
    pnl: 425.00,
    status: 'completed'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 600000),
    username: 'bob_crypto',
    pair: 'ETH/USD',
    amount: 300.00,
    controlledOutcome: -40,
    marketOutcome: 12.3,
    result: 'loss',
    pnl: -120.00,
    status: 'completed'
  }
])

const availablePairs = [
  'BTC/USD', 'ETH/USD', 'ADA/USD', 'DOT/USD', 'SOL/USD',
  'BNB/USD', 'XRP/USD', 'LUNA/USD', 'AVAX/USD', 'MATIC/USD'
]

// Form
const outcomeForm = reactive({
  pair: '',
  outcome: 'profit',
  percentage: 100,
  duration: 40,
  durationUnit: 'seconds',
  target: 'all',
  username: '',
  priority: 'medium'
})

// Methods
const formatCurrency = (amount: number): string => {
  return amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString()
}

const formatTimeAgo = (date: Date): string => {
  return formatDistanceToNow(date, { addSuffix: true })
}

const formatTimeRemaining = (date: Date): string => {
  return formatDistanceToNow(date)
}

const formatDuration = (duration: number, unit: string): string => {
  return `${duration} ${unit}`
}

const getTargetDescription = (target: string): string => {
  const descriptions = {
    all: 'all users',
    new: 'new users only',
    specific: 'specific user',
    vip: 'VIP users'
  }
  return descriptions[target as keyof typeof descriptions] || target
}

const confirmPayment = async (paymentId: number, action: 'approve' | 'reject') => {
  try {
    // TODO: API call to confirm payment
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Remove from pending list
    const index = pendingPayments.value.findIndex(p => p.id === paymentId)
    if (index > -1) {
      pendingPayments.value.splice(index, 1)
      stats.value.pendingPayments--
    }
    
    console.log(`Payment ${paymentId} ${action}d`)
  } catch (error) {
    console.error('Error confirming payment:', error)
  }
}

const saveOutcome = async () => {
  saving.value = true
  try {
    // TODO: API call to save outcome
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (editingOutcome.value) {
      // Update existing outcome
      Object.assign(editingOutcome.value, outcomeForm)
    } else {
      // Add new outcome
      const newOutcome = {
        id: Date.now(),
        ...outcomeForm,
        expiresAt: new Date(Date.now() + getDurationInMs(outcomeForm.duration, outcomeForm.durationUnit))
      }
      activeOutcomes.value.push(newOutcome)
      stats.value.controlledOutcomes++
    }
    
    cancelOutcomeEdit()
  } finally {
    saving.value = false
  }
}

const editOutcome = (outcome: any) => {
  editingOutcome.value = outcome
  Object.assign(outcomeForm, outcome)
  showOutcomeModal.value = true
}

const cancelOutcome = async (outcomeId: number) => {
  if (confirm('Are you sure you want to cancel this outcome?')) {
    const index = activeOutcomes.value.findIndex(o => o.id === outcomeId)
    if (index > -1) {
      activeOutcomes.value.splice(index, 1)
      stats.value.controlledOutcomes--
    }
  }
}

const cancelOutcomeEdit = () => {
  editingOutcome.value = null
  showOutcomeModal.value = false
  Object.assign(outcomeForm, {
    pair: '',
    outcome: 'profit',
    percentage: 100,
    duration: 40,
    durationUnit: 'seconds',
    target: 'all',
    username: '',
    priority: 'medium'
  })
}

const getDurationInMs = (duration: number, unit: string): number => {
  const multipliers = {
    seconds: 1000,
    minutes: 60 * 1000,
    hours: 60 * 60 * 1000,
    days: 24 * 60 * 60 * 1000,
    months: 30 * 24 * 60 * 60 * 1000
  }
  return duration * (multipliers[unit as keyof typeof multipliers] || 1000)
}

const refreshData = async () => {
  loading.value = true
  try {
    // TODO: Load fresh data from API
    await new Promise(resolve => setTimeout(resolve, 1000))
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  // Auto-refresh data every 30 seconds
  setInterval(() => {
    if (!loading.value) {
      refreshData()
    }
  }, 30000)
})
</script>