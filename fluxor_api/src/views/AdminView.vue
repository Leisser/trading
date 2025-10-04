<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
        <h1 class="text-xl font-semibold text-gray-900">Admin Dashboard</h1>
        <div class="flex items-center space-x-4">
          <router-link to="/cryptocurrencies" class="btn-primary text-sm">
            💰 Manage Cryptocurrencies
          </router-link>
          <router-link to="/admin-dashboard" class="btn-secondary text-sm">
            Advanced Admin
          </router-link>
          <router-link to="/dashboard" class="btn-secondary text-sm">Back to Trading</router-link>
        </div>
      </div>
    </header>
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Users -->
        <div class="card">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Users</h2>
          <div v-if="users.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">KYC</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="user in users" :key="user.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.full_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.role }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span :class="user.kyc_verified ? 'text-green-600' : 'text-red-600'">
                      {{ user.kyc_verified ? 'Verified' : 'Unverified' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-8 text-gray-500">No users found</div>
        </div>
        <!-- Trades -->
        <div class="card">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Trades</h2>
          <div v-if="trades.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="trade in trades" :key="trade.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ trade.user_email || 'N/A' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ trade.trade_type }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ trade.btc_amount }} BTC</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${{ trade.usd_price }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      {{ trade.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(trade.timestamp) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center py-8 text-gray-500">No trades found</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const users = ref<any[]>([])
const trades = ref<any[]>([])

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/accounts/users/')
    users.value = response.data.results || response.data
  } catch (err) {
    users.value = []
  }
}

const fetchTrades = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/trades/')
    trades.value = response.data.results || response.data
  } catch (err) {
    trades.value = []
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  if (!authStore.isAdmin) {
    router.push('/dashboard')
  }
  fetchUsers()
  fetchTrades()
})
</script> 