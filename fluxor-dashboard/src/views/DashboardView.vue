<template>
  <div class="min-h-screen bg-gradient-to-br from-black via-purple-900 to-black text-white">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 w-full z-50 backdrop-blur-2xl bg-black/30 shadow-2xl border-b border-white/10">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <!-- Logo -->
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-2xl">
              <span class="text-white font-bold text-xl">F</span>
            </div>
            <div>
              <h1 class="text-3xl font-black bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                Fluxor
              </h1>
              <span class="text-sm text-gray-400 font-medium tracking-wider">DASHBOARD</span>
            </div>
          </div>

          <!-- Navigation Links -->
          <div class="hidden lg:flex items-center space-x-8">
            <router-link to="/" class="relative group text-cyan-400 font-medium">
              <span class="relative z-10">Dashboard</span>
              <div class="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-lg opacity-100"></div>
            </router-link>
            <router-link to="/trading" class="relative group text-gray-300 hover:text-white transition-all duration-300 font-medium">
              <span class="relative z-10">Trade</span>
              <div class="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>
            <router-link to="/analytics" class="relative group text-gray-300 hover:text-white transition-all duration-300 font-medium">
              <span class="relative z-10">Analytics</span>
              <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>
            <router-link to="/settings" class="relative group text-gray-300 hover:text-white transition-all duration-300 font-medium">
              <span class="relative z-10">Settings</span>
              <div class="absolute inset-0 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>
          </div>

          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <div class="text-right">
              <div class="text-sm text-gray-400">Welcome back</div>
              <div class="text-white font-semibold">{{ user?.full_name || user?.email || 'User' }}</div>
            </div>
            <button @click="handleLogout" class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-xl transition-all duration-300">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="pt-20">
      <!-- Hero Section -->
      <section class="py-16">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-12">
            <h1 class="text-5xl font-black bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-6">
              TRADING DASHBOARD
            </h1>
            <p class="text-xl text-gray-400 max-w-3xl mx-auto">
              Monitor your portfolio, execute trades, and track market performance in real-time
            </p>
          </div>

          <!-- Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            <div class="bg-gradient-to-br from-cyan-500/10 via-blue-500/10 to-purple-500/10 backdrop-blur-2xl rounded-3xl p-6 border border-cyan-500/20 shadow-2xl">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-bold text-cyan-400">Portfolio Value</h3>
                <div class="w-10 h-10 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                  </svg>
                </div>
              </div>
              <p class="text-3xl font-black text-white mb-2">$0.00</p>
              <p class="text-green-400 font-semibold flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12"></path>
                </svg>
                +0.00% (24h)
              </p>
            </div>

            <div class="bg-gradient-to-br from-purple-500/10 via-pink-500/10 to-red-500/10 backdrop-blur-2xl rounded-3xl p-6 border border-purple-500/20 shadow-2xl">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-bold text-purple-400">Total P&L</h3>
                <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                  </svg>
                </div>
              </div>
              <p class="text-3xl font-black text-white mb-2">$0.00</p>
              <p class="text-gray-400 text-sm">No trades yet</p>
            </div>

            <div class="bg-gradient-to-br from-emerald-500/10 via-teal-500/10 to-cyan-500/10 backdrop-blur-2xl rounded-3xl p-6 border border-emerald-500/20 shadow-2xl">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-bold text-emerald-400">Active Positions</h3>
                <div class="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
              </div>
              <p class="text-3xl font-black text-white mb-2">0</p>
              <p class="text-gray-400 text-sm">No open positions</p>
            </div>

            <div class="bg-gradient-to-br from-orange-500/10 via-red-500/10 to-pink-500/10 backdrop-blur-2xl rounded-3xl p-6 border border-orange-500/20 shadow-2xl">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-bold text-orange-400">Win Rate</h3>
                <div class="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
              </div>
              <p class="text-3xl font-black text-white mb-2">0%</p>
              <p class="text-gray-400 text-sm">No trades completed</p>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Quick Trade -->
            <div class="bg-gradient-to-br from-slate-900/50 via-purple-900/20 to-slate-900/50 backdrop-blur-2xl rounded-3xl p-8 border border-white/10 shadow-2xl">
              <h3 class="text-2xl font-bold text-white mb-6">Quick Trade</h3>
              <div class="space-y-4">
                <div class="flex gap-4">
                  <button class="flex-1 py-3 bg-green-500/20 hover:bg-green-500/30 text-green-400 rounded-xl font-semibold transition-all duration-300">
                    Buy
                  </button>
                  <button class="flex-1 py-3 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-xl font-semibold transition-all duration-300">
                    Sell
                  </button>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm text-gray-400 mb-2">Amount</label>
                    <input type="number" placeholder="0.00" class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
                  </div>
                  <div>
                    <label class="block text-sm text-gray-400 mb-2">Asset</label>
                    <select class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-cyan-500">
                      <option>BTC</option>
                      <option>ETH</option>
                      <option>BNB</option>
                    </select>
                  </div>
                </div>
                <button class="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-xl font-semibold transition-all duration-300">
                  Execute Trade
                </button>
              </div>
            </div>

            <!-- Market Overview -->
            <div class="bg-gradient-to-br from-slate-900/50 via-purple-900/20 to-slate-900/50 backdrop-blur-2xl rounded-3xl p-8 border border-white/10 shadow-2xl">
              <h3 class="text-2xl font-bold text-white mb-6">Market Overview</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between py-3 border-b border-white/10">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-gradient-to-r from-orange-500 to-yellow-500 rounded-lg flex items-center justify-center">
                      <span class="text-white font-bold text-sm">₿</span>
                    </div>
                    <div>
                      <div class="font-semibold text-white">Bitcoin</div>
                      <div class="text-sm text-gray-400">BTC</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="font-bold text-white">$67,234.56</div>
                    <div class="text-green-400 text-sm">+2.34%</div>
                  </div>
                </div>

                <div class="flex items-center justify-between py-3 border-b border-white/10">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                      <span class="text-white font-bold text-sm">Ξ</span>
                    </div>
                    <div>
                      <div class="font-semibold text-white">Ethereum</div>
                      <div class="text-sm text-gray-400">ETH</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="font-bold text-white">$3,456.78</div>
                    <div class="text-green-400 text-sm">+1.87%</div>
                  </div>
                </div>

                <div class="flex items-center justify-between py-3">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center">
                      <span class="text-white font-bold text-sm">B</span>
                    </div>
                    <div>
                      <div class="font-semibold text-white">Binance Coin</div>
                      <div class="text-sm text-gray-400">BNB</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="font-bold text-white">$456.23</div>
                    <div class="text-red-400 text-sm">-0.45%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="mt-12">
            <div class="bg-gradient-to-br from-slate-900/50 via-purple-900/20 to-slate-900/50 backdrop-blur-2xl rounded-3xl p-8 border border-white/10 shadow-2xl">
              <h3 class="text-2xl font-bold text-white mb-6">Recent Activity</h3>
              <div class="text-center py-12">
                <div class="w-16 h-16 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg class="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                </div>
                <div class="text-gray-400 mb-2">No recent activity</div>
                <div class="text-sm text-gray-500">Start trading to see your activity here</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
