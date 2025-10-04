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
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div 
          v-for="crypto in marketData" 
          :key="crypto.symbol"
          class="bg-white/10 backdrop-blur-md rounded-lg p-6 border border-white/20"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                {{ crypto.symbol.charAt(0) }}
              </div>
              <span class="ml-2 text-white font-semibold">{{ crypto.symbol }}</span>
            </div>
            <span :class="crypto.change >= 0 ? 'text-green-400' : 'text-red-400'" class="text-sm">
              {{ crypto.change >= 0 ? '+' : '' }}{{ crypto.change.toFixed(2) }}%
            </span>
          </div>
          <div class="text-2xl font-bold text-white">${{ crypto.price.toLocaleString() }}</div>
          <div class="text-sm text-purple-300">24h Volume: ${{ crypto.volume.toLocaleString() }}</div>
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

// Mock market data - in production this would come from the API
const marketData = ref([
  { symbol: 'BTC', price: 43250.50, change: 2.34, volume: 2847293847 },
  { symbol: 'ETH', price: 2650.75, change: -1.23, volume: 1829475632 },
  { symbol: 'BNB', price: 315.20, change: 0.87, volume: 847392847 },
  { symbol: 'ADA', price: 0.52, change: 3.45, volume: 392847392 }
])

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
