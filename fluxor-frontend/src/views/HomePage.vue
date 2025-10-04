<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
    <!-- Navigation -->
    <nav class="bg-black/20 backdrop-blur-md border-b border-white/10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-white">Fluxor</h1>
            <span class="ml-2 text-sm text-purple-300">Trading Platform</span>
          </div>
          <div class="flex items-center space-x-4">
            <router-link 
              to="/login" 
              class="text-white hover:text-purple-300 transition-colors"
            >
              Sign In
            </router-link>
            <router-link 
              to="/register" 
              class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center">
        <h1 class="text-5xl font-bold text-white mb-6">
          Advanced Cryptocurrency Trading
        </h1>
        <p class="text-xl text-purple-200 mb-8 max-w-3xl mx-auto">
          Trade cryptocurrencies with professional-grade tools, real-time market data, and advanced trading features.
        </p>
        <div class="flex justify-center space-x-4">
          <router-link 
            to="/register" 
            class="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
          >
            Start Trading
          </router-link>
          <button 
            @click="scrollToFeatures" 
            class="border border-purple-400 text-purple-300 hover:bg-purple-400 hover:text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
          >
            Learn More
          </button>
        </div>
      </div>
    </div>

    <!-- Market Data Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <h2 class="text-3xl font-bold text-white text-center mb-12">Live Market Data</h2>
      
      <!-- Top 4 Cryptocurrencies Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div 
          v-for="crypto in marketData.slice(0, 4)" 
          :key="crypto.symbol"
          class="bg-white/10 backdrop-blur-md rounded-lg p-6 border border-white/20"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                {{ crypto.rank }}
              </div>
              <div class="ml-2">
                <span class="text-white font-semibold">{{ crypto.symbol }}</span>
                <div class="text-xs text-purple-300">{{ crypto.name }}</div>
              </div>
            </div>
            <span :class="crypto.change_24h >= 0 ? 'text-green-400' : 'text-red-400'" class="text-sm">
              {{ crypto.change_24h >= 0 ? '+' : '' }}{{ crypto.change_24h.toFixed(1) }}%
            </span>
          </div>
          <div class="text-2xl font-bold text-white">${{ formatPrice(crypto.price) }}</div>
          <div class="text-sm text-purple-300 mt-2">
            <div>24h Vol: ${{ formatVolume(crypto.volume_24h) }}</div>
            <div>Market Cap: ${{ formatVolume(crypto.market_cap) }}</div>
          </div>
        </div>
      </div>

      <!-- Complete Market Data Table -->
      <div class="bg-white/5 backdrop-blur-md rounded-lg border border-white/20 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-white/10">
              <tr class="text-purple-300">
                <th class="px-4 py-3 text-left font-semibold">#</th>
                <th class="px-4 py-3 text-left font-semibold">Coin</th>
                <th class="px-4 py-3 text-right font-semibold">Price</th>
                <th class="px-4 py-3 text-right font-semibold">1h</th>
                <th class="px-4 py-3 text-right font-semibold">24h</th>
                <th class="px-4 py-3 text-right font-semibold">7d</th>
                <th class="px-4 py-3 text-right font-semibold">30d</th>
                <th class="px-4 py-3 text-right font-semibold">24h Volume</th>
                <th class="px-4 py-3 text-right font-semibold">Circulating Supply</th>
                <th class="px-4 py-3 text-right font-semibold">Total Supply</th>
                <th class="px-4 py-3 text-right font-semibold">Market Cap</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/10">
              <tr 
                v-for="crypto in marketData" 
                :key="crypto.symbol"
                class="hover:bg-white/5 transition-colors"
              >
                <td class="px-4 py-3 text-purple-300">{{ crypto.rank }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center">
                    <div class="w-6 h-6 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-xs mr-2">
                      {{ crypto.symbol.charAt(0) }}
                    </div>
                    <div>
                      <div class="text-white font-semibold">{{ crypto.symbol }}</div>
                      <div class="text-purple-300 text-xs">{{ crypto.name }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-4 py-3 text-white font-semibold text-right">${{ formatPrice(crypto.price) }}</td>
                <td class="px-4 py-3 text-right">
                  <span :class="crypto.change_1h >= 0 ? 'text-green-400' : 'text-red-400'">
                    {{ crypto.change_1h >= 0 ? '+' : '' }}{{ crypto.change_1h.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-4 py-3 text-right">
                  <span :class="crypto.change_24h >= 0 ? 'text-green-400' : 'text-red-400'">
                    {{ crypto.change_24h >= 0 ? '+' : '' }}{{ crypto.change_24h.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-4 py-3 text-right">
                  <span :class="crypto.change_7d >= 0 ? 'text-green-400' : 'text-red-400'">
                    {{ crypto.change_7d >= 0 ? '+' : '' }}{{ crypto.change_7d.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-4 py-3 text-right">
                  <span :class="crypto.change_30d >= 0 ? 'text-green-400' : 'text-red-400'">
                    {{ crypto.change_30d >= 0 ? '+' : '' }}{{ crypto.change_30d.toFixed(1) }}%
                  </span>
                </td>
                <td class="px-4 py-3 text-purple-300 text-right">${{ formatVolume(crypto.volume_24h) }}</td>
                <td class="px-4 py-3 text-purple-300 text-right">{{ formatSupply(crypto.circulating_supply) }}</td>
                <td class="px-4 py-3 text-purple-300 text-right">{{ formatSupply(crypto.total_supply) }}</td>
                <td class="px-4 py-3 text-white font-semibold text-right">${{ formatVolume(crypto.market_cap) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <h2 class="text-3xl font-bold text-white text-center mb-12">Trading Features</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20">
          <div class="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Real-time Trading</h3>
          <p class="text-purple-200">Execute trades instantly with real-time market data and lightning-fast order processing.</p>
        </div>

        <div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20">
          <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Advanced Analytics</h3>
          <p class="text-purple-200">Professional charting tools, technical indicators, and market analysis to make informed decisions.</p>
        </div>

        <div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20">
          <div class="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Secure & Compliant</h3>
          <p class="text-purple-200">Bank-grade security with regulatory compliance and insurance protection for your assets.</p>
        </div>

        <div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20">
          <div class="w-12 h-12 bg-yellow-600 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Portfolio Management</h3>
          <p class="text-purple-200">Track your investments, analyze performance, and manage your crypto portfolio efficiently.</p>
        </div>

        <div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20">
          <div class="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4.828 7l2.586 2.586a2 2 0 002.828 0L12.828 7H4.828zm0 10l2.586-2.586a2 2 0 012.828 0L12.828 17H4.828z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Risk Management</h3>
          <p class="text-purple-200">Advanced risk controls, stop-loss orders, and position sizing to protect your capital.</p>
        </div>

        <div class="bg-white/10 backdrop-blur-md rounded-lg p-8 border border-white/20">
          <div class="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">High Performance</h3>
          <p class="text-purple-200">Low latency execution, high-frequency trading support, and institutional-grade infrastructure.</p>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">Ready to Start Trading?</h2>
        <p class="text-xl text-purple-100 mb-8">Join thousands of traders using Fluxor for their cryptocurrency investments.</p>
        <router-link 
          to="/register" 
          class="bg-white text-purple-600 hover:bg-purple-50 px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
        >
          Create Free Account
        </router-link>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-black/40 backdrop-blur-md border-t border-white/10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-lg font-semibold text-white mb-4">Fluxor</h3>
            <p class="text-purple-300">Professional cryptocurrency trading platform with advanced features and security.</p>
          </div>
          <div>
            <h4 class="text-white font-semibold mb-4">Trading</h4>
            <ul class="space-y-2 text-purple-300">
              <li><a href="#" class="hover:text-white transition-colors">Spot Trading</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Futures</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Options</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Margin Trading</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-semibold mb-4">Support</h4>
            <ul class="space-y-2 text-purple-300">
              <li><a href="#" class="hover:text-white transition-colors">Help Center</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Contact Us</a></li>
              <li><a href="#" class="hover:text-white transition-colors">API Documentation</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Status</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-semibold mb-4">Legal</h4>
            <ul class="space-y-2 text-purple-300">
              <li><a href="#" class="hover:text-white transition-colors">Terms of Service</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Risk Disclosure</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Compliance</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-white/10 mt-8 pt-8 text-center text-purple-300">
          <p>&copy; 2024 Fluxor. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Real cryptocurrency market data
const marketData = ref([
  { 
    rank: 1, 
    symbol: 'BTC', 
    name: 'Bitcoin', 
    price: 122104, 
    change_1h: 0.1, 
    change_24h: 0.5, 
    change_7d: 11.5, 
    change_30d: 11.0, 
    volume_24h: 36459039042, 
    circulating_supply: 19928203, 
    total_supply: 19930000, 
    market_cap: 2433318759440 
  },
  { 
    rank: 2, 
    symbol: 'ETH', 
    name: 'Ethereum', 
    price: 4486.01, 
    change_1h: 0.4, 
    change_24h: 1.3, 
    change_7d: 12.0, 
    change_30d: 4.9, 
    volume_24h: 21603209113, 
    circulating_supply: 120702395, 
    total_supply: 120700000, 
    market_cap: 541077386471 
  },
  { 
    rank: 3, 
    symbol: 'XRP', 
    name: 'XRP', 
    price: 2.95, 
    change_1h: 0.3, 
    change_24h: 2.8, 
    change_7d: 5.8, 
    change_30d: 5.9, 
    volume_24h: 3997658883, 
    circulating_supply: 59871700035, 
    total_supply: 99990000000, 
    market_cap: 176729111579 
  },
  { 
    rank: 4, 
    symbol: 'USDT', 
    name: 'Tether', 
    price: 1.00, 
    change_1h: 0.0, 
    change_24h: 0.0, 
    change_7d: 0.0, 
    change_30d: 0.0, 
    volume_24h: 72647530609, 
    circulating_supply: 176241404874, 
    total_supply: 176240000000, 
    market_cap: 176302387916 
  },
  { 
    rank: 5, 
    symbol: 'BNB', 
    name: 'BNB', 
    price: 1148.90, 
    change_1h: 0.4, 
    change_24h: 1.8, 
    change_7d: 18.6, 
    change_30d: 36.3, 
    volume_24h: 2966782382, 
    circulating_supply: 139184915, 
    total_supply: 139180000, 
    market_cap: 160129362550 
  },
  { 
    rank: 6, 
    symbol: 'SOL', 
    name: 'Solana', 
    price: 227.85, 
    change_1h: 0.4, 
    change_24h: 2.4, 
    change_7d: 13.0, 
    change_30d: 12.1, 
    volume_24h: 4858307248, 
    circulating_supply: 545359468, 
    total_supply: 611160000, 
    market_cap: 124277857925 
  },
  { 
    rank: 7, 
    symbol: 'USDC', 
    name: 'USDC', 
    price: 1.00, 
    change_1h: 0.0, 
    change_24h: 0.0, 
    change_7d: 0.0, 
    change_30d: 0.0, 
    volume_24h: 10227412498, 
    circulating_supply: 75366144659, 
    total_supply: 75370000000, 
    market_cap: 75384493126 
  },
  { 
    rank: 8, 
    symbol: 'STETH', 
    name: 'Lido Staked Ether', 
    price: 4481.47, 
    change_1h: 0.3, 
    change_24h: 1.2, 
    change_7d: 12.3, 
    change_30d: 4.9, 
    volume_24h: 14825050, 
    circulating_supply: 8524860, 
    total_supply: 8520000, 
    market_cap: 38199942698 
  },
  { 
    rank: 9, 
    symbol: 'DOGE', 
    name: 'Dogecoin', 
    price: 0.2501, 
    change_1h: 0.4, 
    change_24h: 3.9, 
    change_7d: 9.1, 
    change_30d: 18.6, 
    volume_24h: 2033001875, 
    circulating_supply: 151186236384, 
    total_supply: 151210000000, 
    market_cap: 37829049657 
  },
  { 
    rank: 10, 
    symbol: 'TRX', 
    name: 'TRON', 
    price: 0.3401, 
    change_1h: 0.0, 
    change_24h: 0.7, 
    change_7d: 0.7, 
    change_30d: 1.5, 
    volume_24h: 463902500, 
    circulating_supply: 94667155456, 
    total_supply: 94670000000, 
    market_cap: 32187004998 
  }
])

// Formatting functions
const formatPrice = (price: number): string => {
  if (price >= 1000) {
    return price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  } else if (price >= 1) {
    return price.toFixed(2)
  } else {
    return price.toFixed(4)
  }
}

const formatVolume = (volume: number): string => {
  if (volume >= 1e12) {
    return (volume / 1e12).toFixed(1) + 'T'
  } else if (volume >= 1e9) {
    return (volume / 1e9).toFixed(1) + 'B'
  } else if (volume >= 1e6) {
    return (volume / 1e6).toFixed(1) + 'M'
  } else if (volume >= 1e3) {
    return (volume / 1e3).toFixed(1) + 'K'
  } else {
    return volume.toFixed(0)
  }
}

const formatSupply = (supply: number): string => {
  if (supply >= 1e12) {
    return (supply / 1e12).toFixed(1) + 'T'
  } else if (supply >= 1e9) {
    return (supply / 1e9).toFixed(1) + 'B'
  } else if (supply >= 1e6) {
    return (supply / 1e6).toFixed(1) + 'M'
  } else if (supply >= 1e3) {
    return (supply / 1e3).toFixed(1) + 'K'
  } else {
    return supply.toFixed(0)
  }
}

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  // In production, fetch real market data from the API
  console.log('HomePage mounted - ready to fetch market data')
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
