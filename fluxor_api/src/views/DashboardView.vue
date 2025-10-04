<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Fluxor Trading</h1>
            <router-link v-if="authStore.isAdmin" to="/admin" class="ml-6 btn-secondary text-sm">Admin Panel</router-link>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-700">Welcome, {{ authStore.user?.full_name }}</span>
            <router-link to="/investments" class="btn-secondary text-sm">Investments</router-link>
            <router-link to="/profile" class="btn-secondary text-sm">Profile</router-link>
            <router-link to="/analytics" class="btn-secondary text-sm">Analytics</router-link>
            <router-link v-if="authStore.isAdmin" to="/cryptocurrencies" class="btn-primary text-sm">💰 Cryptos</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin" class="btn-secondary text-sm">Admin</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin-dashboard" class="btn-primary text-sm">Control Panel</router-link>
            <button @click="authStore.logout" class="btn-secondary text-sm">Logout</button>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Price Chart -->
      <PriceChart class="mb-6" />
      <!-- Price Feed Section -->
      <div class="card mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-medium text-gray-900">Bitcoin Price</h2>
          <div class="flex space-x-4">
            <button @click="tradingStore.fetchCurrentPrice" class="btn-secondary text-sm">
              Refresh
            </button>
            <button @click="togglePriceFeed" class="btn-primary text-sm">
              {{ priceFeedActive ? 'Stop' : 'Start' }} Live Feed
            </button>
          </div>
        </div>
        
        <div v-if="tradingStore.currentPrice" class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="text-center">
            <p class="text-sm text-gray-600">Binance Price</p>
            <p class="text-2xl font-bold text-green-600">${{ formatPrice(tradingStore.currentPrice.binance) }}</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-gray-600">CoinGecko Price</p>
            <p class="text-2xl font-bold text-blue-600">${{ formatPrice(tradingStore.currentPrice.coingecko) }}</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-gray-600">Trading Signal</p>
            <p class="text-lg font-semibold" :class="signalColor">{{ tradingStore.tradeSignal?.signal || 'N/A' }}</p>
          </div>
        </div>
        
        <div v-else class="text-center py-8">
          <p class="text-gray-500">Loading price data...</p>
        </div>
      </div>

      <!-- Trading Interface -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Trade Form -->
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Execute Trade</h3>
          
          <form @submit.prevent="executeTrade" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Trade Type</label>
              <select v-model="tradeForm.trade_type" class="input-field">
                <option value="buy">Buy</option>
                <option value="sell">Sell</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Amount (USD)</label>
              <input
                v-model.number="tradeForm.amount"
                type="number"
                step="0.01"
                min="0"
                class="input-field"
                placeholder="Enter amount in USD"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Leverage</label>
              <input
                v-model.number="tradeForm.leverage"
                type="number"
                step="0.1"
                min="1"
                max="10"
                class="input-field"
                placeholder="1-10x"
              />
            </div>
            
            <button
              type="submit"
              :disabled="tradingStore.loading"
              class="btn-primary w-full"
            >
              <span v-if="tradingStore.loading">Executing...</span>
              <span v-else>Execute Trade</span>
            </button>
          </form>
          
          <div v-if="tradingStore.error" class="mt-4 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded">
            {{ tradingStore.error }}
          </div>
        </div>

        <!-- Wallet Information -->
        <div class="card">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">Wallet</h3>
            <button @click="refreshWallet" class="btn-secondary text-sm">
              Refresh
            </button>
          </div>
          
          <div v-if="tradingStore.wallet" class="space-y-4">
            <div>
              <p class="text-sm text-gray-600">Address</p>
              <p class="text-sm font-mono text-gray-900 break-all">{{ tradingStore.wallet.address }}</p>
            </div>
            
            <div>
              <p class="text-sm text-gray-600">Balance</p>
              <p class="text-2xl font-bold text-green-600">{{ tradingStore.wallet.balance }} BTC</p>
            </div>
            
            <div class="flex space-x-2">
              <button @click="checkDeposits" class="btn-secondary text-sm flex-1">
                Check Deposits
              </button>
              <button @click="showWithdrawalModal = true" class="btn-primary text-sm flex-1">
                Withdraw
              </button>
            </div>
          </div>
          
          <div v-else class="text-center py-8">
            <p class="text-gray-500">Loading wallet...</p>
          </div>
        </div>
      </div>

      <!-- Trade History -->
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Trade History</h3>
          <button @click="tradingStore.fetchTrades" class="btn-secondary text-sm">
            Refresh
          </button>
        </div>
        
        <div v-if="tradingStore.trades.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="trade in tradingStore.trades" :key="trade.id">
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
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {{ trade.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(trade.timestamp) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="text-center py-8">
          <p class="text-gray-500">No trades found</p>
        </div>
      </div>
    </div>

    <!-- Withdrawal Modal -->
    <div v-if="showWithdrawalModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Withdraw Bitcoin</h3>
          
          <form @submit.prevent="handleWithdrawal" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Amount (BTC)</label>
              <input
                v-model="withdrawalForm.amount"
                type="number"
                step="0.00000001"
                min="0"
                class="input-field"
                placeholder="0.001"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">To Address</label>
              <input
                v-model="withdrawalForm.to_address"
                type="text"
                class="input-field"
                placeholder="bc1q..."
              />
            </div>
            
            <div class="flex space-x-2">
              <button type="button" @click="showWithdrawalModal = false" class="btn-secondary flex-1">
                Cancel
              </button>
              <button type="submit" class="btn-primary flex-1">
                Withdraw
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTradingStore } from '@/stores/trading'
import PriceChart from '@/components/PriceChart.vue'
import { useToast } from '@/composables/useToast'

const authStore = useAuthStore()
const tradingStore = useTradingStore()
const toast = useToast()

const priceFeedActive = ref(false)
const showWithdrawalModal = ref(false)

const tradeForm = reactive({
  trade_type: 'buy' as 'buy' | 'sell',
  amount: 0,
  leverage: 1
})

const withdrawalForm = reactive({
  amount: '',
  to_address: ''
})

const signalColor = computed(() => {
  const signal = tradingStore.tradeSignal?.signal
  if (signal === 'buy') return 'text-green-600'
  if (signal === 'sell') return 'text-red-600'
  return 'text-gray-600'
})

const formatPrice = (price: number) => {
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const togglePriceFeed = () => {
  if (priceFeedActive.value) {
    tradingStore.disconnectPriceFeed()
    priceFeedActive.value = false
  } else {
    tradingStore.connectPriceFeed()
    priceFeedActive.value = true
  }
}

const executeTrade = async () => {
  const result = await tradingStore.executeTrade(tradeForm)
  if (result.success) {
    toast.showToast('Trade executed successfully!', 'success')
    // Reset form
    tradeForm.amount = 0
    tradeForm.leverage = 1
  } else if (result.error) {
    toast.showToast(result.error, 'error')
  }
}

const refreshWallet = async () => {
  await tradingStore.fetchWallet()
}

const handleWithdrawal = async () => {
  const result = await tradingStore.requestWithdrawal(withdrawalForm)
  if (result.success) {
    toast.showToast('Withdrawal request submitted!', 'success')
    showWithdrawalModal.value = false
    withdrawalForm.amount = ''
    withdrawalForm.to_address = ''
  } else if (result.error) {
    toast.showToast(result.error, 'error')
  }
}

const checkDeposits = async () => {
  const result = await tradingStore.checkDeposits()
  if (result.success) {
    toast.showToast('Deposit check complete!', 'success')
  } else if (result.error) {
    toast.showToast(result.error, 'error')
  }
}

onMounted(async () => {
  await tradingStore.fetchCurrentPrice()
  await tradingStore.fetchTradeSignal()
  await tradingStore.fetchTrades()
  await tradingStore.fetchWallet()
  toast.showToast('Welcome to Fluxor Trading!', 'success', 2000)
})

onUnmounted(() => {
  tradingStore.disconnectPriceFeed()
})
</script> 